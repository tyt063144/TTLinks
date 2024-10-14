import asyncio
import time
from typing import List

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.protocol_stack.base_classes.packet_receiver import PacketReceiver
from ttlinks.protocol_stack.base_classes.protocol_socket import Socket
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.ethernet_layer.ethernet_payload_unit_factory import EthernetPayloadUnitFactory
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import EthernetPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.ICMP.icmp_utils import ICMPTypes
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_packet_units import IPv4PacketUnit


# ----------------- ICMP Echo Request Receiver Monitor Handlers -----------------
class ICMPSenderReceiveMonitorHandler(SimpleCoRHandler):
    """
    Base class for monitoring ICMP responses using the Chain of Responsibility pattern.

    This handler passes the received IPv4 packet to the next handler in the chain if the current handler
    doesn't process it. It serves as the base class for more specific ICMP response handlers.
    """
    def handle(self, replied_ipv4_unit, *args, **kwargs):
        if self._next_handler:
            return self._next_handler.handle(replied_ipv4_unit, *args, **kwargs)
        return self._next_handler

class ICMPSenderEchoReplyMonitorHandler(ICMPSenderReceiveMonitorHandler):
    """
    Handler for monitoring ICMP Echo Reply messages.

    This handler checks if the received IPv4 packet contains an ICMP Echo Reply that matches the original
    ICMP Echo Request, based on the protocol, message type, sequence number, identifier, and IP destination.
    If it matches, it returns True. Otherwise, it passes the packet to the next handler.
    """
    def handle(self, replied_ipv4_unit: IPv4PacketUnit, *args, **kwargs):
        if (
                isinstance(replied_ipv4_unit, IPv4PacketUnit)
                and replied_ipv4_unit.protocol == IPPayloadProtocolTypes.ICMP
                and replied_ipv4_unit.payload.message_type == ICMPTypes.ECHO_REPLY
                and kwargs.get('original_icmp_unit').sequence_number == replied_ipv4_unit.payload.sequence_number
                and kwargs.get('original_icmp_unit').identifier == replied_ipv4_unit.payload.identifier
                and kwargs.get('ip_destination') == str(replied_ipv4_unit.source_address)
        ):
            return True
        else:
            return super().handle(replied_ipv4_unit, *args, **kwargs)

class ICMPSenderDestinationUnreachableMonitorHandler(ICMPSenderReceiveMonitorHandler):
    """
    Handler for monitoring ICMP Destination Unreachable messages.

    This handler checks if the received IPv4 packet contains an ICMP Destination Unreachable message
    that references the original ICMP Echo Request, based on the protocol, message type, payload content,
    and destination address. If it matches, it returns True. Otherwise, it passes the packet to the next handler.
    """
    def handle(self, replied_ipv4_unit: IPv4PacketUnit, *args, **kwargs):
        if (
                isinstance(replied_ipv4_unit, IPv4PacketUnit)
                and replied_ipv4_unit.protocol == IPPayloadProtocolTypes.ICMP
                and replied_ipv4_unit.payload.message_type == ICMPTypes.DESTINATION_UNREACHABLE
                and kwargs.get('original_icmp_unit').as_bytes == replied_ipv4_unit.payload.payload.payload.as_bytes
                and kwargs.get('ip_destination') == str(replied_ipv4_unit.payload.payload.destination_address)
        ):
            return True
        else:
            return super().handle(replied_ipv4_unit, *args, **kwargs)

class ICMPSenderRedirectMonitorHandler(ICMPSenderReceiveMonitorHandler):
    """
    Handler for monitoring ICMP Redirect messages.

    This handler checks if the received IPv4 packet contains an ICMP Redirect message that references
    the original ICMP request. It compares the protocol, message type, payload, and destination address.
    If it matches, it returns True. Otherwise, it passes the packet to the next handler.
    """
    def handle(self, replied_ipv4_unit: IPv4PacketUnit, *args, **kwargs):
        if (
                isinstance(replied_ipv4_unit, IPv4PacketUnit)
                and replied_ipv4_unit.protocol == IPPayloadProtocolTypes.ICMP
                and replied_ipv4_unit.payload.message_type == ICMPTypes.REDIRECT
                and kwargs.get('original_icmp_unit').as_bytes == replied_ipv4_unit.payload.payload.payload.as_bytes
                and kwargs.get('ip_destination') == str(replied_ipv4_unit.payload.payload.destination_address)
        ):
            return True
        else:
            return super().handle(replied_ipv4_unit, *args, **kwargs)

class ICMPSenderTTLExceededMonitorHandler(ICMPSenderReceiveMonitorHandler):
    """
    Handler for monitoring ICMP Time Exceeded messages.

    This handler checks if the received IPv4 packet contains an ICMP Time Exceeded message that references
    the original ICMP request. It compares the protocol, message type, payload, and destination address.
    If it matches, it returns True. Otherwise, it passes the packet to the next handler.
    """
    def handle(self, replied_ipv4_unit: IPv4PacketUnit, *args, **kwargs):
        if (
                isinstance(replied_ipv4_unit, IPv4PacketUnit)
                and replied_ipv4_unit.protocol == IPPayloadProtocolTypes.ICMP
                and replied_ipv4_unit.payload.message_type == ICMPTypes.TIME_EXCEEDED
                and kwargs.get('original_icmp_unit').as_bytes == replied_ipv4_unit.payload.payload.payload.as_bytes
                and kwargs.get('ip_destination') == str(replied_ipv4_unit.payload.payload.destination_address)
        ):
            return True
        else:
            return super().handle(replied_ipv4_unit, *args, **kwargs)

class ICMPSenderParameterProblemMonitorHandler(ICMPSenderReceiveMonitorHandler):
    """
    Handler for monitoring ICMP Parameter Problem messages.

    This handler checks if the received IPv4 packet contains an ICMP Parameter Problem message that references
    the original ICMP request. It compares the protocol, message type, payload, and destination address.
    If it matches, it returns True. Otherwise, it passes the packet to the next handler.
    """
    def handle(self, replied_ipv4_unit: IPv4PacketUnit, *args, **kwargs):
        if (
                isinstance(replied_ipv4_unit, IPv4PacketUnit)
                and replied_ipv4_unit.protocol == IPPayloadProtocolTypes.ICMP
                and replied_ipv4_unit.payload.message_type == ICMPTypes.PARAMETER_PROBLEM
                and kwargs.get('original_icmp_unit').as_bytes == replied_ipv4_unit.payload.payload.payload.as_bytes
                and kwargs.get('ip_destination') == str(replied_ipv4_unit.payload.payload.destination_address)
        ):
            return True
        else:
            return super().handle(replied_ipv4_unit, *args, **kwargs)


class ICMPReceiveMonitor:
    """
    Utility class for monitoring ICMP responses and checking if they match the original ICMP request.

    This class uses the Chain of Responsibility pattern to pass an IPv4 packet through a chain of handlers
    that check for different ICMP response types (e.g., Echo Reply, Destination Unreachable, etc.).
    """
    @staticmethod
    def monitor(
            ipv4_unit: IPv4PacketUnit,
            original_icmp_unit: ProtocolUnit,
            ip_destination:str,
            monitors: List[ICMPSenderReceiveMonitorHandler] = None
    ) -> bool:
        """
        Monitors the received ICMP response by passing it through a chain of handlers.

        Parameters:
        - ipv4_unit (IPv4PacketUnit): The received IPv4 packet containing the ICMP response.
        - original_icmp_unit (ProtocolUnit): The original ICMP request that was sent.
        - ip_destination (str): The destination IP address used in the original request.
        - monitors (List[ICMPSenderReceiveMonitorHandler], optional): A list of handlers for different ICMP response types.
          If None is provided, a default list of handlers is used.

        Returns:
        - bool: True if one of the handlers successfully processes the ICMP response, False otherwise.
        """
        if monitors is None:
            monitors = [
                ICMPSenderEchoReplyMonitorHandler(),
                ICMPSenderDestinationUnreachableMonitorHandler(),
                ICMPSenderRedirectMonitorHandler(),
                ICMPSenderTTLExceededMonitorHandler(),
                ICMPSenderParameterProblemMonitorHandler()
            ]
        monitor_handler = monitors[0]
        for next_handler in monitors[1:]:
            monitor_handler.set_next(next_handler)
            monitor_handler = next_handler
        return monitors[0].handle(ipv4_unit, original_icmp_unit=original_icmp_unit, ip_destination=ip_destination)


# ----------------- ICMP Echo Request Receiver -----------------
class ICMPReceiver(PacketReceiver):
    """
    Asynchronous ICMP receiver that listens for ICMP replies using a socket.

    This class listens for incoming ICMP responses and checks if they match the original ICMP request.
    It processes the received packet and uses the ICMPReceiveMonitor to check if the response is valid.
    """
    async def listen(self, socket_unit: Socket, destination:str, *args, **kwargs):
        """
        Listens for ICMP replies on the provided socket and checks if they match the original ICMP request.

        Parameters:
        - socket_unit (Socket): The socket object used for receiving the ICMP replies.
        - destination (str): The destination IP address used in the original request.
        - *args, **kwargs: Additional arguments, including:
          - 'timeout' (float): The timeout for waiting for replies.
          - 'icmp_unit' (ProtocolUnit): The original ICMP request.
          - 'time_record' (dict): A record of the start and end times for the request/response.

        Returns:
        - IPv4PacketUnit: The matching ICMP response if found, or None if the operation times out.
        """
        start_time = time.perf_counter()
        sock = socket_unit.get_socket
        remaining_timeout = kwargs['timeout']
        loop = asyncio.get_running_loop()
        while True:
            try:
                future = loop.sock_recv(sock, 65535)
                # Wait for the reply with a timeout
                reply = await asyncio.wait_for(future, remaining_timeout)
                receiving_time = time.perf_counter()

                elapsed_time = receiving_time - start_time
                remaining_timeout = kwargs['timeout'] - elapsed_time

                ethernet_payload_factory = EthernetPayloadUnitFactory
                replied_ipv4_unit = ethernet_payload_factory.create_unit(reply, EthernetPayloadProtocolTypes.IPv4)
                reply_matched = ICMPReceiveMonitor.monitor(replied_ipv4_unit, original_icmp_unit=kwargs['icmp_unit'], ip_destination=destination)
                if reply_matched:
                    kwargs['time_record']['end_time'] = receiving_time
                    return replied_ipv4_unit
                if remaining_timeout <= 0:
                    kwargs['time_record']['end_time'] = receiving_time
                    raise asyncio.TimeoutError
            except asyncio.TimeoutError:
                kwargs['time_record']['end_time'] = time.perf_counter()
                return