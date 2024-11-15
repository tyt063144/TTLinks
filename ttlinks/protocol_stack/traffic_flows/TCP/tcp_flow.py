import asyncio
import socket

from ttlinks.common.tools.systems import FirewallTools
from ttlinks.protocol_stack.base_classes.protocol_socket import SocketBuilderDirector, TCPRawSocketBuilder, Socket
from ttlinks.protocol_stack.ip_packets.tcp import TCP, IPv4TCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.traffic_flows.TCP.tcp_receivers import TCPReceiver
from ttlinks.protocol_stack.traffic_flows.TCP.tcp_senders import TCPSender
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOption2Unit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_units import TCPUnit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


# class TCP

class IPv4TCPFlowController:

    def __init__(self, initial_packet: TCP = None, timeout=5, semaphore=255):
        self._semaphore_value = semaphore
        self._initial_packet = None
        self._initialize_packet(initial_packet)
        self._tcp_receiver = TCPReceiver()
        self._tcp_sender = TCPSender()
        self._socket_unit = SocketBuilderDirector(TCPRawSocketBuilder()).build_socket()
        self.received_packets = []
        self._timeout = timeout
        self._next_ipv4_id = None
        self._next_seq_number = None
        self._next_ack_number = None
        self._negotiated_mss = None
        self._listener_task = None  # Task to hold the listener
        self._is_handshake_completed = False
        self._is_flow_reset = False

    @property
    def is_handshake_completed(self):
        return self._is_handshake_completed

    def _check_handshake_completion(self, remote_tcp_unit: TCPUnit):
        if TCPFlags.ACK in remote_tcp_unit.flags and TCPFlags.SYN in remote_tcp_unit.flags:
            self._is_handshake_completed = True

    async def _handling_reset(self, remote_tcp_unit: TCPUnit):
        if TCPFlags.RST in remote_tcp_unit.flags:
            self._is_flow_reset = True
            await self.close()
            print(f'port {self._initial_packet.tcp_unit.source_port} is RESET by the remote host')

    def _initialize_packet(self, initial_packet: TCP):
        if initial_packet is None:
            self._initial_packet = IPv4TCP(
                ipv4_flags=IPv4Flags.DONT_FRAGMENT,
                ttl=128,
                destination_address='0.0.0.0',
                tcp_flags=[TCPFlags.SYN],
            )
        else:
            self._initial_packet = initial_packet

    def _extract_mss_option(self, remote_tcp_unit: TCPUnit):
        for option in remote_tcp_unit.options:
            if type(option) == TCPOption2Unit:
                self._negotiated_mss = option.value
                break

    def _increment_ip_identification(self):
        self._next_ipv4_id = self._initial_packet.ip_unit.identification + 1

    def _update_sequence_number(self, payload_len=0):
        self._next_seq_number = self._next_seq_number + payload_len

    def _update_acknowledgment_number(self, tcp_unit: TCPUnit):
        self._next_ack_number = self._next_ack_number + len(tcp_unit.payload)

    async def _start_packet_listener(self):
        self._listener_task = asyncio.create_task(self._tcp_receiver.listen(
            self._socket_unit, initial_packet=self._initial_packet, return_packets=self.received_packets
        ))

    async def _wait_for_handshake_response(self):
        # Wait for response packets within the timeout period
        while True:
            if self.received_packets:
                packet = self.received_packets.pop(0)
                self._extract_mss_option(packet[1])
                self._next_ack_number = packet[1].sequence_number + 1
                self._increment_ip_identification()

                # Construct and send the second handshake packet
                second_packet = IPv4TCP(
                    ipv4_flags=self._initial_packet.ip_unit.flags,
                    ttl=self._initial_packet.ip_unit.ttl,
                    identification=self._next_ipv4_id,
                    source_address=str(self._initial_packet.ip_unit.source_address),
                    destination_address=str(self._initial_packet.ip_unit.destination_address),
                    source_port=self._initial_packet.tcp_unit.source_port,
                    destination_port=self._initial_packet.tcp_unit.destination_port,
                    sequence_number=self._next_seq_number,
                    acknowledgment_number=self._next_ack_number,
                    tcp_flags=[TCPFlags.ACK],
                    tcp_option_units=[],
                )
                await self._tcp_sender.send(self._socket_unit, str(second_packet.ip_unit.destination_address), second_packet.unit)
                self._increment_ip_identification()
                self._check_handshake_completion(packet[1])
                await self._handling_reset(packet[1])
                break
            await asyncio.sleep(0.1)

    async def handshake(self):
        await self._start_packet_listener()
        # # Apply per-port RST filter asynchronously
        # await FirewallTools.unfilter_tcp_rst_by_sport(self._initial_packet.tcp_unit.source_port)
        # await FirewallTools.filter_tcp_rst_by_sport(self._initial_packet.tcp_unit.source_port)

        self._next_seq_number = self._initial_packet.tcp_unit.sequence_number + 1
        self._next_ack_number = 0

        await self._tcp_sender.send(self._socket_unit, str(self._initial_packet.ip_unit.destination_address), self._initial_packet.unit, initial=True)

        try:
            await asyncio.wait_for(self._wait_for_handshake_response(), timeout=self._timeout)
        except asyncio.TimeoutError:
            print('Handshake timeout, no packets received within timeout period.')
            # await self.close()


    async def application_data(self, data: bytes=b''):
        await self._start_packet_listener()
        end_time = asyncio.get_event_loop().time() + self._timeout

        while True:
            current_time = asyncio.get_event_loop().time()
            if current_time >= end_time:
                print("Application flow timeout, no packets received within timeout period.")
                break

            if self.received_packets:
                packet = self.received_packets.pop(0)
                self._update_acknowledgment_number(packet[1])
                end_time = current_time + self._timeout
            await asyncio.sleep(0.1)

        if data:
            data_packet = IPv4TCP(
                ipv4_flags=self._initial_packet.ip_unit.flags,
                ttl=self._initial_packet.ip_unit.ttl,
                identification=self._next_ipv4_id,
                source_address=str(self._initial_packet.ip_unit.source_address),
                destination_address=str(self._initial_packet.ip_unit.destination_address),
                source_port=self._initial_packet.tcp_unit.source_port,
                destination_port=self._initial_packet.tcp_unit.destination_port,
                sequence_number=self._next_seq_number,
                acknowledgment_number=self._next_ack_number,
                tcp_flags=[TCPFlags.ACK],
                tcp_option_units=[],
                payload=data,
            )
            await self._tcp_sender.send(self._socket_unit, str(data_packet.ip_unit.destination_address), data_packet.unit)
            self._increment_ip_identification()
            self._update_sequence_number(len(data))

    async def close(self, close_socket=False):
        fin_packet = IPv4TCP(
            ipv4_flags=self._initial_packet.ip_unit.flags,
            ttl=self._initial_packet.ip_unit.ttl,
            identification=self._next_ipv4_id,
            source_address=str(self._initial_packet.ip_unit.source_address),
            destination_address=str(self._initial_packet.ip_unit.destination_address),
            source_port=self._initial_packet.tcp_unit.source_port,
            destination_port=self._initial_packet.tcp_unit.destination_port,
            sequence_number=self._next_seq_number,
            acknowledgment_number=self._next_ack_number,
            tcp_flags=[TCPFlags.FIN, TCPFlags.ACK],
            tcp_option_units=[],
        )
        await self._tcp_sender.send(self._socket_unit, str(self._initial_packet.ip_unit.destination_address), fin_packet.unit)
        self._socket_unit.get_socket.close() if close_socket else None
        # await FirewallTools.unfilter_tcp_rst_by_sport(self._initial_packet.tcp_unit.source_port)

        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass