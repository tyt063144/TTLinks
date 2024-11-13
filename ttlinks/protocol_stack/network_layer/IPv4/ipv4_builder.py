import socket
import struct
from abc import ABC, abstractmethod
from ttlinks.common.algorithm.checksum import ChecksumCalculator, InternetChecksum
from ttlinks.common.tools.network import NetTools
from ttlinks.protocol_stack.base_classes.header_builder import Header, HeaderBuilder
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.network_layer.IPv4 import ipv4_units


# -------------------IPv4 Header-------------------
class IPv4Header(Header):
    """
    A class for constructing and representing an IPv4 header.

    This class constructs the IPv4 header based on the provided fields, such as
    version, IHL, DSCP, ECN, total length, identification, flags, fragment offset,
    TTL, protocol, checksum, source IP, and destination IP. It computes the
    Internet checksum based on the header fields, returning the fully constructed
    header in bytes format.

    Methods:
    - _construct: Constructs the IPv4 header and calculates the checksum.
    - unit: Returns the corresponding protocol unit for the IPv4 header.

    Parameters:
    None (inherits from Header)
    """
    def _construct(self) -> dict:
        """
        Constructs the IPv4 header and calculates the checksum.

        This method takes the fields provided in the `_fields` dictionary and constructs
        the IPv4 header. It computes the checksum for the header and returns the fields
        in bytes format, ready to be transmitted.

        Returns:
        dict: A dictionary containing the IPv4 header fields in bytes format.
        """
        version_and_ihl = struct.pack('!B', (self._fields['version'] << 4) + self._fields['ihl'])
        tos = struct.pack('!B', (self._fields['dscp'] << 2) + self._fields['ecn'])
        total_length = struct.pack('!H', self._fields['total_length'])
        identification = struct.pack('!H', self._fields['identification'])
        flags_fragment_offset = struct.pack('!H', (self._fields['flags'] << 13) + self._fields['fragment_offset'])
        ttl = struct.pack('!B', self._fields['ttl'])
        protocol = struct.pack('!B', self._fields['protocol'])
        raw_checksum = self._fields.get('header_checksum')
        source_address = struct.pack('!4s', socket.inet_aton(self._fields['source_address']))
        destination_address = struct.pack('!4s', socket.inet_aton(self._fields['destination_address']))
        header_checksum = self._calculate_checksum(
            version_and_ihl, tos, total_length, identification, flags_fragment_offset,
            ttl, protocol, raw_checksum, source_address, destination_address
        )
        return {
            'version_and_ihl': version_and_ihl,
            'tos': tos,
            'total_length': total_length,
            'identification': identification,
            'flags_and_fragment_offset': flags_fragment_offset,
            'ttl': ttl,
            'protocol': protocol,
            'header_checksum': header_checksum,
            'source_address': source_address,
            'destination_address': destination_address,
            'options': self._fields.get('options', b''),
            'payload': self._fields.get('payload', b'')
        }

    @staticmethod
    def _calculate_checksum(
            version_and_ihl, tos, total_length, identification, flags_fragment_offset,
            ttl, protocol, raw_checksum, source_address, destination_address) -> bytes:
        if raw_checksum is not None:
            return struct.pack('!H', raw_checksum)
        else:
            raw_bytes_before_checksum = (
                    version_and_ihl
                    + tos
                    + total_length
                    + identification
                    + flags_fragment_offset
                    + ttl
                    + protocol
                    + struct.pack('!H', 0)
                    + source_address
                    + destination_address
            )
            checksum_int = ChecksumCalculator(InternetChecksum()).calculate(raw_bytes_before_checksum)
            return struct.pack('!H', checksum_int)

    @property
    def unit(self) -> ProtocolUnit:
        """
        Returns the IPv4 unit for the constructed header.
        """
        return ipv4_units.IPv4Unit(**self._construct())

# -------------------IPv4 Header Builder-------------------
class IPv4HeaderBuilderInterface(HeaderBuilder, ABC):
    """
    Interface for building an IPv4 header. This abstract base class defines methods that must be implemented
    to construct an IPv4 header, covering fields such as version, header length, type of service,
    and other key properties.

    Parameters:
    - Each method takes a specific parameter related to IPv4 header fields and sets its value in the implementation.

    Methods:
    - set_version(version: int): Sets the IP version. For IPv4, this value is typically 4.
    - set_ihl(ihl: int): Sets the Internet Header Length (IHL), which defines the length of the IP header in 32-bit words.
    - set_dscp(dscp: int): Sets the Differentiated Services Code Point (DSCP) for Quality of Service (QoS) control.
    - set_ecn(ecn: int): Sets the Explicit Congestion Notification (ECN) bits for congestion control.
    - set_total_length(total_length: int): Sets the total length of the IP packet (header + payload).
    - set_identification(identification: int): Sets the identification field, typically used for reassembling fragmented packets.
    - set_flags(flags: IPv4Flags): Sets the IPv4 flags (e.g., Don't Fragment, More Fragments).
    - set_fragment_offset(fragment_offset: int): Sets the fragment offset for fragmented packets.
    - set_ttl(ttl: int): Sets the Time To Live (TTL) field, indicating the packet's lifespan in network hops.
    - set_protocol(protocol: IPPayloadProtocolTypes): Sets the protocol type for the payload (e.g., TCP, UDP).
    - set_checksum(checksum: int): Sets the checksum for the header to ensure data integrity.
    - set_source_address(source_address: str): Sets the source IP address.
    - set_destination_address(destination_address: str): Sets the destination IP address.
    - set_options(options: bytes): Sets optional fields and extensions, if any.
    - set_payload(payload: bytes): Sets the payload data to be carried in the IP packet.

    Returns:
    - None. This is an interface meant to be implemented by a concrete IPv4 header builder class.
    """
    @abstractmethod
    def set_version(self, version: int):
        pass
    @abstractmethod
    def set_ihl(self, ihl: int):
        pass
    @abstractmethod
    def set_dscp(self, dscp: int):
        pass
    @abstractmethod
    def set_ecn(self, ecn: int):
        pass
    @abstractmethod
    def set_total_length(self, total_length: int):
        pass
    @abstractmethod
    def set_identification(self, identification: int):
        pass
    @abstractmethod
    def set_flags(self, flags: IPv4Flags):
        pass
    @abstractmethod
    def set_fragment_offset(self, fragment_offset: int):
        pass
    @abstractmethod
    def set_ttl(self, ttl: int):
        pass
    @abstractmethod
    def set_protocol(self, protocol: IPPayloadProtocolTypes):
        pass
    @abstractmethod
    def set_checksum(self, checksum: int):
        pass
    @abstractmethod
    def set_source_address(self, source_address: str):
        pass
    @abstractmethod
    def set_destination_address(self, destination_address: str):
        pass
    @abstractmethod
    def set_options(self, options: bytes):
        pass
    @abstractmethod
    def set_payload(self, payload: bytes):
        pass

class IPv4HeaderBuilder(IPv4HeaderBuilderInterface):
    def set_version(self, version: int = 4):
        if version != 4:
            raise ValueError('IPv4 version must be 4')
        self._header.add_field('version', version)

    def set_ihl(self, ihl: int = 5):
        if ihl < 5 or ihl > 15:
            raise ValueError('IPv4 IHL must be between 5 and 15')
        self._header.add_field('ihl', ihl)

    def set_dscp(self, dscp: int = 0):
        if dscp < 0 or dscp > 63:
            raise ValueError('IPv4 DSCP must be between 0 and 63')
        self._header.add_field('dscp', dscp)

    def set_ecn(self, ecn: int = 0):
        if ecn < 0 or ecn > 3:
            raise ValueError('IPv4 ECN must be between 0 and 3')
        self._header.add_field('ecn', ecn)

    def set_total_length(self, total_length: int):
        self._header.add_field('total_length', total_length)

    def set_identification(self, identification: int):
        self._header.add_field('identification', identification)

    def set_flags(self, flags: IPv4Flags):
        self._header.add_field('flags', flags.value)

    def set_fragment_offset(self, fragment_offset: int):
        self._header.add_field('fragment_offset', fragment_offset)

    def set_ttl(self, ttl: int):
        self._header.add_field('ttl', ttl)

    def set_protocol(self, protocol: IPPayloadProtocolTypes):
        self._header.add_field('protocol', protocol.value)

    def set_checksum(self, checksum: int = None):
        self._header.add_field('header_checksum', checksum)

    def set_source_address(self, source_address: str):
        self._header.add_field('source_address', source_address)

    def set_destination_address(self, destination_address: str):
        self._header.add_field('destination_address', destination_address)

    def set_options(self, options: bytes=b''):
        self._header.add_field('options', options)

    def set_payload(self, payload: ProtocolUnit = None):
        if payload is not None:
            self._header.add_field('payload', payload.as_bytes)
        else:
            self._header.add_field('payload', b'')

# -------------------IPv4 Header Builder Director-------------------

class IPv4HeaderBuilderDirector:
    """
        Director class for constructing an IPv4 header using a builder interface. This class orchestrates
        the construction of an IPv4 header by setting default and user-specified values for each field.

        Parameters:
        - builder (IPv4HeaderBuilderInterface): An instance of a class that implements the IPv4HeaderBuilderInterface.

        Methods:
        - construct(...): Constructs an IPv4 header by sequentially setting various fields via the builder interface.

        Parameters for construct method:
        - version (int, default=4): The IP version. Typically 4 for IPv4.
        - ihl (int, default=5): Internet Header Length in 32-bit words.
        - dscp (int, default=0): Differentiated Services Code Point for QoS.
        - ecn (int, default=0): Explicit Congestion Notification for congestion control.
        - total_length (int, default=40): Total length of the IP packet.
        - identification (int, default=0): Identification field for fragmented packets.
        - flags (IPv4Flags, default=IPv4Flags.NO_FLAGS): IPv4 flags, like Don't Fragment.
        - fragment_offset (int, default=0): Offset for fragmenting packets.
        - ttl (int, default=64): Time To Live, defining packet lifespan.
        - protocol (IPPayloadProtocolTypes, default=IPPayloadProtocolTypes.TCP): Protocol of the payload (e.g., TCP).
        - checksum (int, optional): Header checksum for integrity verification.
        - source_address (str, default=NetTools.get_outgoing_interface_ip()): Source IP address.
        - destination_address (str, default='0.0.0.0'): Destination IP address.
        - options (bytes, default=b''): Optional IPv4 header fields/extensions.

        Returns:
        - IPv4Header: A constructed IPv4 header object with all fields set.
    """
    def __init__(self, builder: IPv4HeaderBuilderInterface):
        self._builder = builder

    def construct(
            self,
            version: int = 4,
            ihl: int = 5,
            dscp: int = 0,
            ecn: int = 0,
            total_length: int = 40,
            identification: int = 0,
            flags: IPv4Flags = IPv4Flags.NO_FLAGS,
            fragment_offset: int = 0,
            ttl: int = 64,
            protocol: IPPayloadProtocolTypes = IPPayloadProtocolTypes.TCP,
            checksum: int = None,
            source_address: str = NetTools.get_outgoing_interface_ip(),
            destination_address: str = '0.0.0.0',
            options: bytes = b'',
    ):
        ipv4_builder = IPv4HeaderBuilder(IPv4Header())
        ipv4_builder.set_version(version)
        ipv4_builder.set_ihl(ihl)
        ipv4_builder.set_dscp(dscp)
        ipv4_builder.set_ecn(ecn)
        ipv4_builder.set_total_length(total_length)
        ipv4_builder.set_identification(identification)
        ipv4_builder.set_flags(flags)
        ipv4_builder.set_fragment_offset(fragment_offset)
        ipv4_builder.set_ttl(ttl)
        ipv4_builder.set_protocol(protocol)
        ipv4_builder.set_checksum(checksum)
        ipv4_builder.set_source_address(source_address)
        ipv4_builder.set_destination_address(destination_address)
        ipv4_builder.set_options(options)
        ipv4_builder.set_payload(None)

        return ipv4_builder.build().unit
