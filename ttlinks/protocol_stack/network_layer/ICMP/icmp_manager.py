import asyncio
import traceback
from inspect import trace
from typing import Union, List, Generator

from ttlinks.ipservice.ip_address import IPv4Addr
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig, IPv4WildCardConfig
from ttlinks.protocol_stack.base_classes.protocol_socket import SocketBuilderDirector, ICMPSocketBuilder
from ttlinks.protocol_stack.network_layer.ICMP.icmp_builder import ICMPEchoRequestHeader, ICMPEchoRequestHeaderBuilder, ICMPHeaderBuilderDirector
from ttlinks.protocol_stack.network_layer.ICMP.icmp_receivers import ICMPReceiver
from ttlinks.protocol_stack.network_layer.ICMP.icmp_senders import ICMPEchoRequestSender
from ttlinks.protocol_stack.network_layer.ICMP.icmp_utils import ICMPResponseDescription, ICMPTypes


class ICMPPingResponse:
    """
    A class representing the response of an ICMP ping request.

    This class provides various properties to access details about the ICMP ping response,
    such as the destination address, round-trip time (RTT), packet size, and whether the
    response was successful (i.e., whether an ICMP Echo Reply was received). It also provides
    a verbose textual representation of the ping result, indicating whether it succeeded or failed.

    Methods:
    - destination: Returns the destination IP address of the response.
    - ttl: Returns the Time-To-Live (TTL) value from the IPv4 unit if available.
    - packet_size: Returns the size of the ICMP packet in bytes.
    - icmp_unit: Returns the ICMP payload unit from the IPv4 packet.
    - icmp_type: Returns the ICMP message type (e.g., Echo Reply).
    - icmp_code: Returns the ICMP code.
    - is_success: Indicates whether the response was an ICMP Echo Reply.
    - verbose: Returns a textual description of the ping response (for user-friendly output).

    Parameters:
    - destination (str): The destination IP address or hostname.
    - rtt (float): The round-trip time (RTT) of the ping in milliseconds.
    - ipv4_unit (IPv4Unit): The IPv4 protocol unit containing the ICMP payload (optional).
    """
    def __init__(self, destination, rtt, ipv4_unit=None):
        """
        Initializes the ICMPPingResponse with the destination, round-trip time,
        and optionally, an IPv4 unit containing the ICMP response.

        Parameters:
        - destination (str): The destination IP address or hostname of the ping.
        - rtt (float): The round-trip time of the ping.
        - ipv4_unit (IPv4Unit, optional): The IPv4 unit containing the ICMP response.
        """
        self._destination = destination
        self._rtt = rtt
        self._ipv4_unit = ipv4_unit

    @property
    def destination(self):
        """
        Returns the destination address.

        If the IPv4 unit is available, returns the source address of the received response;
        otherwise, returns the original destination.

        Returns:
        str: The destination IP address.
        """
        return self._ipv4_unit.source_address if self._ipv4_unit else self._destination

    @property
    def ttl(self):
        """
        Returns the Time-To-Live (TTL) value from the IPv4 unit.

        Returns:
        int: The TTL value if available, otherwise None.
        """
        return self._ipv4_unit.ttl if self._ipv4_unit else None

    @property
    def packet_size(self):
        """
        Returns the size of the ICMP packet from the IPv4 unit.

        Returns:
        int: The total length of the packet if available, otherwise None.
        """
        return self._ipv4_unit.total_length if self._ipv4_unit else None

    @property
    def icmp_unit(self):
        """
        Returns the ICMP payload unit from the IPv4 unit.

        Returns:
        ICMPUnit: The ICMP payload if available, otherwise None.
        """
        return self._ipv4_unit.payload if self._ipv4_unit else None

    @property
    def icmp_type(self):
        """
        Returns the ICMP message type (e.g., Echo Reply) as an `ICMPTypes` enum.

        Returns:
        ICMPTypes: The ICMP message type if available, otherwise None.
        """
        return ICMPTypes(self._ipv4_unit.payload.icmp_type) if self._ipv4_unit else None

    @property
    def icmp_code(self):
        """
        Returns the ICMP message code.

        Returns:
        int: The ICMP code if available, otherwise None.
        """
        return self._ipv4_unit.payload.icmp_code if self._ipv4_unit else None

    @property
    def is_success(self):
        """
        Returns whether the ICMP response was successful (i.e., an ICMP Echo Reply).

        Returns:
        bool: True if the response is an ICMP Echo Reply, otherwise False.
        """
        return self.icmp_type == ICMPTypes.ECHO_REPLY if self._ipv4_unit else False

    @property
    def verbose(self):
        """
        Returns a verbose string describing the result of the ping.

        If the response was successful, it provides details such as the number of bytes,
        TTL, and a description of the ICMP message. If the ping failed, it reports that
        the request timed out.

        Returns:
        str: A verbose description of the ping response.
        """
        if self._ipv4_unit is None:
            return f"(Failed) Request to {self.destination} timed out"
        return (f"{'(Successful)' if self.icmp_type == ICMPTypes.ECHO_REPLY else '(Failed)'} "
                f"Reply from {self.destination}: bytes={self.packet_size} TTL={self.ttl}: "
                f"{ICMPResponseDescription.get_description(self.icmp_type, self.icmp_code)}")

class PingStatistics:
    """
    A Singleton class for calculating and storing statistics related to ICMP ping responses.

    This class keeps track of ICMP ping responses and provides a method for calculating statistics
    such as the total number of packets sent, packets received, packet loss percentage, and whether
    any of the ping responses were successful.

    Methods:
    - calculate_statistics: Takes a list of ICMP ping responses and returns a dictionary with statistics.

    Attributes:
    __instance (PingStatistics): The singleton instance of the class.
    _responses (list): A list of ICMPPingResponse objects for tracking responses.
    """
    __instance = None

    def __new__(cls):
        """
        Ensures that only one instance of PingStatistics exists (Singleton pattern).

        If no instance exists, it creates one and initializes the `_responses` list to store
        ICMP ping responses. Subsequent instantiations return the existing instance.

        Returns:
        PingStatistics: The singleton instance of the class.
        """
        if cls.__instance is None:
            cls.__instance = super(PingStatistics, cls).__new__(cls)
            cls.__instance._responses = []
        return cls.__instance

    @staticmethod
    def calculate_statistics(responses: List[ICMPPingResponse]):
        """
        Calculates ping statistics based on a list of ICMPPingResponse objects.

        This method computes:
        - The total number of packets sent.
        - The total number of successful packets received.
        - The percentage of packet loss.
        - Whether any successful ping responses were received.

        Parameters:
        responses (List[ICMPPingResponse]): A list of ICMPPingResponse objects.

        Returns:
        dict: A dictionary containing ping statistics:
            - total_packets_sent (int): The total number of packets sent.
            - total_packets_received (int): The number of successful ping responses.
            - packet_loss (float): The percentage of packet loss.
            - is_success (bool): Whether any successful ping responses were received.
        """
        result = {
            'total_packets_sent': len(responses),
            'total_packets_received': len([response for response in responses if response.is_success]),
            'packet_loss': len([response for response in responses if not response.is_success]) / len(responses) * 100,
            'is_success': any([response.is_success for response in responses]),
        }
        return result


class ICMPPingManager:
    """
    A manager class for handling ICMP ping requests asynchronously.

    This class manages the sending of ICMP echo requests and the receiving of ICMP echo replies,
    allowing pings to be sent to one or multiple destinations. It calculates statistics about
    the ping responses and supports synchronous and asynchronous operation.

    Attributes:
    - _socket_director: Director for building ICMP sockets.
    - _icmp_header_build_director: Director for constructing ICMP echo request headers.
    - _sender: Responsible for sending ICMP echo requests.
    - _receiver: Responsible for receiving ICMP echo replies.
    - _semaphore: Limits the number of concurrent pings.

    Methods:
    - async_ping: Asynchronously sends pings to a single destination.
    - async_ping_multiple: Asynchronously sends pings to multiple destinations concurrently.
    - ping: Sends pings to a single destination synchronously.
    - ping_multiple: Sends pings to multiple destinations synchronously.
    """
    def __init__(self, semaphore=255):
        """
        Initializes the ICMPPingManager with default components.

        Parameters:
        - semaphore (int): The maximum number of concurrent ping requests. Defaults to 255.
        """
        self._socket_director = SocketBuilderDirector(ICMPSocketBuilder())
        self._icmp_header_build_director = ICMPHeaderBuilderDirector(ICMPEchoRequestHeaderBuilder(ICMPEchoRequestHeader()))
        self._sender = ICMPEchoRequestSender()
        self._receiver = ICMPReceiver()
        self._semaphore = asyncio.Semaphore(semaphore)

    @staticmethod
    def _validate(timeout, interval, count):
        """
        Validates the ping configuration to ensure valid values for timeout, interval, and count.

        Raises a ValueError if any of the conditions are violated:
        - Timeout must be ≥ 0.
        - Interval must be ≥ 0.
        - Count must be ≥ 1.
        - Timeout must be greater than or equal to the interval.

        Parameters:
        - timeout (int): The maximum time to wait for a reply.
        - interval (int): The interval between successive ping requests.
        - count (int): The number of ping requests to send.
        """
        if timeout < 0:
            raise ValueError("Timeout must be greater than or equal to 0")
        if interval < 0:
            raise ValueError("Interval must be greater than or equal to 0")
        if count < 1:
            raise ValueError("Count must be greater than or equal to 1")
        if timeout < interval:
            raise ValueError("Timeout must be greater than or equal to interval")

    async def async_ping(self, destination: str, timeout: int = 2, interval=1, count: int = 5, verbose=True):
        """
        Asynchronously sends ICMP echo requests to a single destination.

        Parameters:
        - destination (str): The destination to ping.
        - timeout (int): The time to wait for a reply before timing out. Defaults to 2 seconds.
        - interval (int): The interval between successive ping requests. Defaults to 1 second.
        - count (int): The number of ping requests to send. Defaults to 5.
        - verbose (bool): Whether to print verbose output. Defaults to True.

        Returns:
        - dict: A dictionary of ping statistics.
        """
        self._validate(timeout, interval, count)
        responses = []
        socket_unit = self._socket_director.build_icmp_socket()
        async with self._semaphore:
            for _ in range(count):
                icmp_echo_request_header = self._icmp_header_build_director.build_echo_request()
                icmp_unit = icmp_echo_request_header.unit
                time_record = {'start_time': 0, 'end_time': 0}
                await self._sender.send(socket_unit, destination, icmp_unit, time_record=time_record)
                received_ipv4_unit = await self._receiver.listen(socket_unit, destination, icmp_unit=icmp_unit, timeout=timeout, time_record=time_record)
                responses.append(ICMPPingResponse(destination, time_record['end_time'] - time_record['start_time'], received_ipv4_unit))
                print(responses[-1].verbose) if verbose else None
                await asyncio.sleep(interval)
        return PingStatistics.calculate_statistics(responses)

    async def async_ping_multiple(self, destinations: Union[List[str], Generator[IPv4Addr, None, None]],
                                  timeout: int = 2, interval=1, count: int = 2, verbose=True):
        """
        Asynchronously sends ICMP echo requests to multiple destinations concurrently.

        Parameters:
        - destinations (Union[List[str], Generator[str, None, None]]): A list or generator of destinations to ping.
        - timeout (int): The time to wait for a reply before timing out. Defaults to 2 seconds.
        - interval (int): The interval between successive ping requests. Defaults to 1 second.
        - count (int): The number of ping requests to send. Defaults to 2.
        - verbose (bool): Whether to print verbose output. Defaults to True.

        Returns:
        - dict: A dictionary mapping each destination to its corresponding ping statistics.
        """
        self._validate(timeout, interval, count)
        tasks = {
            destination: asyncio.create_task(
                self.async_ping(str(destination), timeout, interval, count, verbose)
            )
            for destination in destinations
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return {str(destination): result for destination, result in zip(tasks.keys(), results)}

    def ping(self, destination: str, timeout: int = 2):
        """
        Sends ICMP echo requests to a single destination synchronously.

        Parameters:
        - destination (str): The destination to ping.
        - timeout (int): The time to wait for a reply before timing out. Defaults to 2 seconds.

        Returns:
        - dict: A dictionary of ping statistics.
        """
        return asyncio.run(self.async_ping(destination, timeout))

    def ping_multiple(self, destinations: Union[List[str], Generator[IPv4Addr, None, None]],
                      timeout: int = 2, interval=1, count: int = 2, verbose=True):
        """
        Sends ICMP echo requests to multiple destinations synchronously.

        Parameters:
        - destinations (Union[List[str], Generator[str, None, None]]): A list or generator of destinations to ping.
        - timeout (int): The time to wait for a reply before timing out. Defaults to 2 seconds.
        - interval (int): The interval between successive ping requests. Defaults to 1 second.
        - count (int): The number of ping requests to send. Defaults to 2.
        - verbose (bool): Whether to print verbose output. Defaults to True.

        Returns:
        - dict: A dictionary mapping each destination to its corresponding ping statistics.
        """
        return asyncio.run(self.async_ping_multiple(destinations, timeout, interval, count, verbose))
