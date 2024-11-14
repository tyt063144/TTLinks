from typing import List

from ttlinks.common.tools.network import NetTools
from ttlinks.ipservice.ip_type_classifiers import IPType
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_builder import IPv4HeaderBuilderDirector, IPv4HeaderBuilder, IPv4Header
from ttlinks.protocol_stack.transport_layer.TCP.tcp_builder import TCPHeader, TCPHeaderBuilder, TCPBuilderDirector
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionUnit, TCPOptionBuilderDirector, TCPOption2HeaderBuilder, \
    TCPOption3HeaderBuilder, TCPOption4HeaderBuilder
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags

# ----------------------SSH TCP Header----------------------
class SSHTCPBuilderDirector(TCPBuilderDirector):
    def construct(
            self,
            source_ip: str = None,
            destination_ip: str = None,
            source_port: int = None,
            destination_port: int = None,
            sequence_number: int = None,
            acknowledgment_number: int = None,
            reserved: int = None,
            flags: List[TCPFlags] = None,
            option_units: List[TCPOptionUnit] = None,
            window_size: int = None,
            urgent_pointer: int = 0,
            payload: bytes = b'',
    ):
        tcp_header = TCPHeader()
        tcp_builder = TCPHeaderBuilder(tcp_header)
        tcp_builder.set_source_ip(source_ip) if source_ip else tcp_builder.set_source_ip(NetTools.get_outgoing_interface_ip())
        tcp_builder.set_destination_ip(destination_ip) if destination_ip else tcp_builder.set_destination_ip('0.0.0.0')
        tcp_builder.set_source_port(source_port) if source_port else tcp_builder.set_source_port()
        tcp_builder.set_destination_port(destination_port) if destination_port else tcp_builder.set_destination_port(22)
        tcp_builder.set_sequence_number(sequence_number) if sequence_number else tcp_builder.set_sequence_number()
        tcp_builder.set_acknowledgment_number(acknowledgment_number) if acknowledgment_number else tcp_builder.set_acknowledgment_number()
        tcp_builder.set_reserved(reserved) if reserved else tcp_builder.set_reserved()
        tcp_builder.set_flags(flags) if flags else tcp_builder.set_flags([])
        tcp_builder.set_options(option_units) if option_units else tcp_builder.set_options([])
        tcp_builder.set_window_size(window_size) if window_size else tcp_builder.set_window_size(8)
        tcp_builder.set_urgent_pointer(urgent_pointer) if urgent_pointer else tcp_builder.set_urgent_pointer()
        tcp_builder.set_payload(payload) if payload else tcp_builder.set_payload(b'')

        result = tcp_builder.build()
        return result.unit

class SSH:
    def __init__(
            self,
            ip_version: IPType = IPType.IPv4,
            ihl: int = 5,
            dscp: int = 0,
            ecn: int = 0,
            total_length: int = None,
            identification: int = 0,
            ipv4_flags: IPv4Flags = IPv4Flags.NO_FLAGS,
            fragment_offset: int = 0,
            ttl: int = 64,
            protocol: IPPayloadProtocolTypes = IPPayloadProtocolTypes.TCP,
            checksum: int = None,
            source_address: str = NetTools.get_outgoing_interface_ip(),
            destination_address: str = '0.0.0.0',
            ipv4_options: bytes = b'',
            source_port: int = NetTools.get_unused_port(),
            destination_port: int = 22,
            sequence_number: int = NetTools.get_tcp_sequence_number(),
            acknowledgment_number: int = 0,
            reserved: int = 0,
            tcp_flags: List[TCPFlags] = None,
            tcp_option_units: List[TCPOptionUnit] = None,
            window_size: int = 64240,
            urgent_pointer: int = 0,
            payload: bytes = b'',
    ):
        if ip_version == IPType.IPv4:
            self.ip_header_director = IPv4HeaderBuilderDirector(IPv4HeaderBuilder(IPv4Header()))
        self.tcp_header_director = SSHTCPBuilderDirector(TCPHeaderBuilder(TCPHeader()))
        self._ip_version = ip_version.value
        self._ihl = ihl
        self._dscp = dscp
        self._ecn = ecn
        self._total_length = total_length
        self._identification = identification
        self._ipv4_flags = ipv4_flags
        self._fragment_offset = fragment_offset
        self._ttl = ttl
        self._protocol = protocol
        self._checksum = checksum
        self._source_address = source_address
        self._destination_address = destination_address
        self._ipv4_options = ipv4_options
        self._source_port = source_port
        self._destination_port = destination_port
        self._sequence_number = sequence_number
        self._acknowledgment_number = acknowledgment_number
        self._reserved = reserved
        self._tcp_flags = tcp_flags
        self._tcp_option_units = tcp_option_units
        self._window_size = window_size
        self._urgent_pointer = urgent_pointer
        self._payload = payload

    def construct(self) -> bytes:
        self._construct_tcp()
        self._construct_ip()
        return self.ip_unit_.as_bytes + self.tcp_unit_.as_bytes

    def _construct_tcp(self):
        self.tcp_unit_ = self.tcp_header_director.construct(
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
        self.ip_unit_ = self.ip_header_director.construct(
            version=self._ip_version,
            ihl=self._ihl if not self._ipv4_options else self._ihl+len(self._ipv4_options),
            dscp=self._dscp,
            ecn=self._ecn,
            total_length=self._total_length if self._total_length else 20+len(self.tcp_unit_.as_bytes),
            identification=self._identification,
            flags=self._ipv4_flags,
            fragment_offset=self._fragment_offset,
            ttl=self._ttl,
            protocol=self._protocol,
            checksum=self._checksum,
            source_address=self._source_address,
            destination_address=self._destination_address,
            options=self._ipv4_options,
        )

