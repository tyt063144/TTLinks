import socket
from abc import ABC
from typing import List

from ttlinks.common.tools.network import NetTools
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_builder import IPv4HeaderBuilderDirector, IPv4HeaderBuilder, IPv4Header
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_units import IPv4Unit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_builder import TCPHeaderBuilder, TCPHeader, TCPBuilderDirector
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionUnit, TCPOptionBuilderDirector, TCPOption2HeaderBuilder, \
    TCPOption3HeaderBuilder, TCPOption4HeaderBuilder
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


class TCP(ABC):
    pass

class IPv4TCP(TCP):
    def __init__(
            self,
            ihl: int = 5,
            dscp: int = 0,
            ecn: int = 0,
            total_length: int = None,
            identification: int = NetTools.get_ipv4_id(),
            ipv4_flags: IPv4Flags = IPv4Flags.NO_FLAGS,
            fragment_offset: int = 0,
            ttl: int = 64,
            ipv4_checksum: int = None,
            source_address: str = NetTools.get_outgoing_interface_ip(),
            destination_address: str = '0.0.0.0',
            ipv4_options: bytes = b'',
            source_port: int = NetTools.get_unused_port(),
            destination_port: int = 80,
            sequence_number: int = NetTools.get_tcp_sequence_number(),
            acknowledgment_number: int = 0,
            reserved: int = 0,
            tcp_flags: List[TCPFlags] = None,
            tcp_option_units: List[TCPOptionUnit] = None,
            window_size: int = 64240,
            urgent_pointer: int = 0,
            payload: bytes = b'',
    ):
        self._ip_header_director = IPv4HeaderBuilderDirector(IPv4HeaderBuilder(IPv4Header()))
        self._tcp_header_director = TCPBuilderDirector(TCPHeaderBuilder(TCPHeader()))
        self._ip_version = 4
        self._ihl = ihl
        self._dscp = dscp
        self._ecn = ecn
        self._total_length = total_length
        self._identification = identification
        self._ipv4_flags = ipv4_flags
        self._fragment_offset = fragment_offset
        self._ttl = ttl
        self._protocol = IPPayloadProtocolTypes.TCP
        self._ipv4_checksum = ipv4_checksum
        self._source_address = source_address
        self._destination_address = destination_address
        self._ipv4_options = ipv4_options
        self._source_port = source_port
        self._destination_port = destination_port
        self._sequence_number = sequence_number
        self._acknowledgment_number = acknowledgment_number
        self._reserved = reserved
        self._tcp_flags = tcp_flags
        self._tcp_option_units = tcp_option_units if tcp_option_units is not None else self.default_tcp_option_units
        self._window_size = window_size
        self._urgent_pointer = urgent_pointer
        self._payload = payload
        self._construct()

    @property
    def default_tcp_option_units(self):
        tcp_option_director = TCPOptionBuilderDirector(TCPOption2HeaderBuilder)
        tcp_option2_units = tcp_option_director.build(kind=2)
        tcp_option_director.set_builder(TCPOption3HeaderBuilder)
        tcp_option3_units = tcp_option_director.build(kind=3, length=3, value=8)
        tcp_option_director.set_builder(TCPOption4HeaderBuilder)
        tcp_option4_units = tcp_option_director.build(kind=4, length=2)
        return [tcp_option2_units, tcp_option3_units, tcp_option4_units]

    def _construct(self):
        self._construct_tcp()
        self._construct_ip()
        self._packet = self._ip_unit.as_bytes + self._tcp_unit.as_bytes

    @property
    def packet(self):
        return self._packet

    @property
    def unit(self):
        ipv4_parser = IPv4PacketParser()
        return IPv4Unit(**ipv4_parser.parse(self._packet))

    @property
    def tcp_unit(self):
        return self._tcp_unit

    @property
    def ip_unit(self):
        return self._ip_unit

    def _construct_tcp(self):
        self._tcp_unit = self._tcp_header_director.construct(
            source_ip=self._source_address,
            destination_ip=self._destination_address,
            source_port=self._source_port,
            destination_port=self._destination_port,
            sequence_number=self._sequence_number,
            acknowledgment_number=self._acknowledgment_number,
            reserved=self._reserved,
            flags=self._tcp_flags,
            option_units=self._tcp_option_units,
            window_size=self._window_size,
            urgent_pointer=self._urgent_pointer,
            payload=self._payload
        )

    def _construct_ip(self):
        self._ip_unit = self._ip_header_director.construct(
            version=self._ip_version,
            ihl=self._ihl if not self._ipv4_options else self._ihl+len(self._ipv4_options),
            dscp=self._dscp,
            ecn=self._ecn,
            total_length=self._total_length if self._total_length else 20+len(self._tcp_unit.as_bytes),
            identification=self._identification,
            flags=self._ipv4_flags,
            fragment_offset=self._fragment_offset,
            ttl=self._ttl,
            protocol=self._protocol,
            checksum=self._ipv4_checksum,
            source_address=self._source_address,
            destination_address=self._destination_address,
            options=self._ipv4_options,
        )


if __name__ == '__main__':
    tcp = IPv4TCP(
        ipv4_flags=IPv4Flags.DONT_FRAGMENT,
        ttl=32,
        destination_address='192.168.1.30',
        source_port=54156,
        destination_port=22,
        sequence_number=1370412840,
        tcp_flags=[TCPFlags.SYN],
    )
    tcp_packet = tcp.packet
    print(tcp_packet)
    print(tcp.ip_unit.attributes)
    print(tcp.tcp_unit.attributes)


    def send_raw_packet(packet):
        try:
            # Create a raw socket (requires administrative/root privileges)
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

            # Set the socket option to include the IP header
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            # Extract destination IP from the packet (for demonstration)
            dest_ip = '192.168.1.30'  # This should match the destination in your packet's header

            # Send the packet
            s.sendto(packet, (dest_ip, 0))
            print("Packet sent successfully.")
        except PermissionError:
            print("Permission denied. You need to run this script as root/administrator.")
        except Exception as e:
            print(f"An error occurred: {e}")


    # Send the packet
    send_raw_packet(tcp_packet)
