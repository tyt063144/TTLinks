from typing import Union, Any

from ttlinks.common.design_template.cor import ProtocolUnitSelectorCoRHandler
from ttlinks.ipservice.ip_address import IPv4Addr
from ttlinks.ipservice.ip_converters import IPConverter
from ttlinks.ipservice.ip_type_classifiers import IPType
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.dscp_utils import DSCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_payload_unit_factory import IPv4PayloadUnitFactory


class IPv4PacketUnit(ProtocolUnit):
    """
    This class represents an IPv4 packet and provides methods to access and manipulate
    the various fields in the packet header. It also allows you to convert the packet
    into its byte representation and provides a summary of the packet's attributes.
    """
    def __init__(self, version_and_ihl: bytes, tos: bytes, total_length: bytes, identification: bytes,
                 flags_and_fragment_offset: bytes, ttl: bytes, protocol: bytes, header_checksum: bytes, source_address: bytes,
                 destination_address: bytes, options: bytes, payload: bytes):
        """
        Initialize the IPv4PacketUnit with all the necessary header fields and payload.

        Args:
            version_and_ihl (bytes): First byte containing both the IP version and header length (IHL).
            tos (bytes): Type of Service (ToS), which includes DSCP and ECN fields.
            total_length (bytes): The total length of the packet (header + payload).
            identification (bytes): Unique identifier for fragmenting the packet.
            flags_and_fragment_offset (bytes): Flags (3 bits) and fragment offset (13 bits).
            ttl (bytes): Time to Live value, determines how long the packet should stay in the network.
            protocol (bytes): The protocol of the encapsulated payload (e.g., ICMP, TCP, UDP).
            header_checksum (bytes): The checksum for the header to ensure its integrity.
            source_address (bytes): The IPv4 source address (32-bit address).
            destination_address (bytes): The IPv4 destination address (32-bit address).
            options (bytes): Additional options in the IPv4 header, if any.
            payload (bytes): The data payload (upper-layer data like TCP, UDP, ICMP).
        """
        self._version_and_ihl = version_and_ihl
        self._tos = tos
        self._total_length = total_length
        self._identification = identification
        self._flags_and_fragment_offset = flags_and_fragment_offset
        self._ttl = ttl
        self._protocol = protocol
        self._header_checksum = header_checksum
        self._source_address = source_address
        self._destination_address = destination_address
        self._options = options
        self._payload = payload

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the entire packet in its byte form by concatenating all the IPv4 header fields and the payload.

        Returns:
            bytes: A byte representation of the complete IPv4 packet (header + options + payload).
        """
        return (
            self._version_and_ihl
            + self._tos
            + self._total_length
            + self._identification
            + self._flags_and_fragment_offset
            + self._ttl
            + self._protocol
            + self._header_checksum
            + self._source_address
            + self._destination_address
            + self._options
            + self._payload
        )

    @property
    def attributes(self) -> dict:
        """
        Returns all the IPv4 packet fields in a dictionary format for easier access and debugging.

        Returns:
            dict: A dictionary of all the packet attributes in their raw byte form.
        """
        return {
            'version_and_ihl': self._version_and_ihl,
            'tos': self._tos,
            'total_length': self._total_length,
            'identification': self._identification,
            'flags_and_fragment_offset': self._flags_and_fragment_offset,
            'ttl': self._ttl,
            'protocol': self._protocol,
            'header_checksum': self._header_checksum,
            'source_address': self._source_address,
            'destination_address': self._destination_address,
            'options': self._options,
            'payload': self._payload
        }

    @property
    def summary(self) -> dict:
        """
        Provides a human-readable summary of the IPv4 packet attributes with decoded values like version,
        DSCP, flags, source/destination addresses, and more.

        Returns:
            dict: A dictionary containing the decoded and human-readable packet attributes.
        """
        return {
            'version': self.version,
            'ihl': self.ihl,
            'header_length': self.header_length,
            'dscp': self.dscp,
            'ecn': self.ecn,
            'total_length': self.total_length,
            'identification': self.identification,
            'flags': self.flags,
            'fragment_offset': self.fragment_offset,
            'ttl': self.ttl,
            'protocol': self.protocol,
            'header_checksum': self.header_checksum,
            'source_address': self.source_address,
            'destination_address': self.destination_address,
            'options': self.options,
            'payload': self.payload
        }

    @property
    def version(self) -> IPType:
        """
        Extracts the IP version from the first 4 bits of the 'version_and_ihl' field.

        Returns:
            IPType: The IP version (typically 4 for IPv4).
        """
        return IPType(int.from_bytes(self._version_and_ihl, byteorder='big') >> 4)

    @property
    def header_length(self) -> int:
        """
        Extracts the header length (IHL) from the 'version_and_ihl' field. The header length is
        """
        return (int.from_bytes(self._version_and_ihl, byteorder='big') & 0xF) * 4

    @property
    def ihl(self) -> int:
        """
        Extracts the header length (IHL) from the 'version_and_ihl' field. The header length is
        """
        return (int.from_bytes(self._version_and_ihl, byteorder='big') & 0xF)

    @property
    def dscp(self) -> DSCP:
        """
        Extracts the Differentiated Services Code Point (DSCP) value from the Type of Service (ToS) byte.

        Returns:
            DSCP: The DSCP value, indicating the packet's priority or Quality of Service (QoS) settings.
        """
        return DSCP.get_name_or_value(int.from_bytes(self._tos, byteorder='big') >> 2)

    @property
    def ecn(self) -> int:
        """
        Extracts the Explicit Congestion Notification (ECN) value from the last 2 bits of the ToS byte.

        Returns:
            int: The ECN value, used for signaling network congestion.
        """
        return int.from_bytes(self._tos, byteorder='big') & 0x3

    @property
    def total_length(self) -> int:
        """
        Extracts the total length of the IPv4 packet, including the header and the payload.

        Returns:
            int: The total length of the packet in bytes.
        """
        return int.from_bytes(self._total_length, byteorder='big')

    @property
    def identification(self) -> int:
        """
        Extracts the identification value used for fragmenting the packet. Each fragmented packet
        will have the same identification number to allow reassembly.

        Returns:
            int: The identification field used for fragmenting.
        """
        return int.from_bytes(self._identification, byteorder='big')

    @property
    def flags(self) -> IPv4Flags:
        """
        Extracts the 3-bit flags field from the 'flags_and_fragment_offset' value. The flags include:
        - Reserved (must be 0)
        - DF (Don't Fragment)
        - MF (More Fragments)

        Returns:
            IPv4Flags: Enum representing the flags.
        """
        return IPv4Flags(int.from_bytes(self._flags_and_fragment_offset, byteorder='big') >> 13)

    @property
    def fragment_offset(self) -> int:
        """
        Extracts the fragment offset value from the 'flags_and_fragment_offset' field, which is used to
        indicate the position of the fragment in the original packet.

        Returns:
            int: The fragment offset in bytes.
        """
        return int.from_bytes(self._flags_and_fragment_offset, byteorder='big') & 0x1FFF

    @property
    def ttl(self) -> int:
        """
        Extracts the Time to Live (TTL) value from the IPv4 header. The TTL value is decremented by each router
        the packet passes through and is used to prevent packets from circulating indefinitely.

        Returns:
            int: The TTL value.
        """
        return int.from_bytes(self._ttl, byteorder='big')

    @property
    def protocol(self) -> IPPayloadProtocolTypes:
        """
        Extracts the protocol field from the IPv4 header, which indicates the protocol of the payload (e.g., TCP, UDP, ICMP).

        Returns:
            IPPayloadProtocolTypes: The protocol type encapsulated in the packet (e.g., ICMP, TCP, UDP).
        """
        return IPPayloadProtocolTypes(int.from_bytes(self._protocol, byteorder='big'))

    @property
    def header_checksum(self) -> hex:
        """
        Extracts the header checksum value, which is used to ensure the integrity of the IPv4 header.

        Returns:
            str: The header checksum value in hexadecimal format.
        """
        return hex(int.from_bytes(self._header_checksum, byteorder='big'))

    @property
    def source_address(self) -> IPv4Addr:
        """
        Converts the raw bytes of the source address into a human-readable IPv4 address.

        Returns:
            IPv4Addr: The source IPv4 address.
        """
        return IPv4Addr(IPConverter.convert_to_ipv4_octets(int.from_bytes(self._source_address, byteorder='big')))

    @property
    def destination_address(self) -> IPv4Addr:
        """
        Converts the raw bytes of the destination address into a human-readable IPv4 address.

        Returns:
            IPv4Addr: The destination IPv4 address.
        """
        return IPv4Addr(IPConverter.convert_to_ipv4_octets(int.from_bytes(self._destination_address, byteorder='big')))

    @property
    def options(self) -> bytes:
        """
        Returns the options field, if any. The options field is optional and is only present if the IHL is greater than 5.

        Returns:
            bytes: The options field as raw bytes, or empty if no options are present.
        """
        return self._options

    @property
    def payload(self) -> Any:
        """
        Attempts to parse the payload of the packet, based on the protocol specified. If it is recognized,
        it returns the appropriate Protocol Unit; otherwise, it returns the raw payload bytes.

        Returns:
            Any: The parsed payload if the protocol is recognized, or the raw payload otherwise.
        """
        ipv4_payload = IPv4PayloadUnitFactory.create_unit(self._payload, self.protocol)
        if ipv4_payload:
            return ipv4_payload
        return self._payload

class IPv4UnitSelectorHandler(ProtocolUnitSelectorCoRHandler):
    """
    Handler for selecting and creating an IPv4PacketUnit based on the parsed packet data.

    This class checks if the packet contains the necessary fields for an IPv4 packet.
    If it does, it creates an IPv4PacketUnit. Otherwise, it passes the packet to the next
    handler in the chain.
    """
    def _parse(self, packet: bytes):
        """
        Parses the given packet using the _parser object if the parsed data is not already available.

        Args:
            packet (bytes): The raw byte data of the IPv4 packet.
        """
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet by checking if it contains the necessary fields for an IPv4 packet.
        If all the fields are present, it creates an IPv4PacketUnit. Otherwise, it passes
        the packet to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be processed.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            IPv4PacketUnit: If the packet contains all necessary IPv4 fields.
            Otherwise, the packet is passed to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if isinstance(self._parsed_data, dict) and [
            'version_and_ihl', 'tos', 'total_length', 'identification',
            'flags_and_fragment_offset', 'ttl', 'protocol', 'header_checksum',
            'source_address', 'destination_address', 'options', 'payload'
        ] == list(self._parsed_data.keys()):
            return IPv4PacketUnit(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class IPv4UnitFactory:
    """
    Factory for creating IPv4PacketUnit instances.

    This factory uses an IPv4UnitSelectorHandler to process the packet and return an IPv4PacketUnit.
    If IPv6 packets are implemented, a separate factory will be needed for handling them.
    """
    @staticmethod
    def create_unit(packet: bytes):
        """
        Creates an IPv4PacketUnit by passing the packet to the IPv4UnitSelectorHandler.

        Args:
            packet (bytes): The raw packet data to be processed.

        Returns:
            IPv4PacketUnit: The processed IPv4 packet as an IPv4PacketUnit instance.
        """
        ipv4_unit_selector = IPv4UnitSelectorHandler(IPv4PacketParser())
        return ipv4_unit_selector.handle(packet)