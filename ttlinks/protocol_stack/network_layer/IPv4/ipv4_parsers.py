from __future__ import annotations
from abc import ABC

from ttlinks.common.design_template.cor import TrackedCoRHandler


class IPv4ParserHandler(TrackedCoRHandler, ABC):
    """
    Abstract base class for all IPv4 field parser handlers.
    Inherits from TrackedCoRHandler, which presumably manages the Chain of Responsibility (CoR)
    and provides tracking through the `_tracker` attribute.
    """
    pass

class IPv4VersionAndIHLFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Version and Internet Header Length (IHL) field from an IPv4 packet.
    The first byte of the packet contains both the version (first 4 bits) and IHL (last 4 bits).
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['version_and_ihl'] = packet[0:1]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)


class IPv4TOSFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Type of Service (TOS) field from an IPv4 packet.
    The second byte (index 1) contains the TOS, which includes DSCP and ECN fields.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['tos'] = packet[1:2]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4TotalLengthFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Total Length field from an IPv4 packet.
    The total length is a 2-byte field located at bytes 2 and 3.
    It represents the entire length of the IPv4 packet (header + payload).
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['total_length'] = packet[2:4]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4IdentificationFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Identification field from an IPv4 packet.
    The identification is a 2-byte field located at bytes 4 and 5.
    It is used to identify fragments of an original packet.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['identification'] = packet[4:6]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4FlagsAndFragmentOffsetFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Flags and Fragment Offset field from an IPv4 packet.
    This is a 2-byte field located at bytes 6 and 7. The first 3 bits are the flags,
    and the remaining 13 bits are the fragment offset.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['flags_and_fragment_offset'] = packet[6:8]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4TTLFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Time to Live (TTL) field from an IPv4 packet.
    The TTL field is a 1-byte field located at byte 8. It determines the maximum
    number of hops the packet can take before being discarded.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['ttl'] = packet[8:9]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4ProtocolFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Protocol field from an IPv4 packet.
    The Protocol field is a 1-byte field located at byte 9. It indicates the protocol
    of the encapsulated payload (e.g., ICMP, TCP, UDP).
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['protocol'] = packet[9:10]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4HeaderChecksumFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Header Checksum field from an IPv4 packet.
    The Header Checksum is a 2-byte field located at bytes 10 and 11. It is used to
    verify the integrity of the IPv4 header.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['header_checksum'] = packet[10:12]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4SourceAddressFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Source Address field from an IPv4 packet.
    The Source Address is a 4-byte field located at bytes 12 to 15. It contains
    the IPv4 address of the packet's sender.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['source_address'] = packet[12:16]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4DestinationAddressFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Destination Address field from an IPv4 packet.
    The Destination Address is a 4-byte field located at bytes 16 to 19. It contains
    the IPv4 address of the packet's intended recipient.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['destination_address'] = packet[16:20]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4OptionsFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Options field from an IPv4 packet.
    The Options field is variable-length and starts after the fixed 20-byte header.
    The length of the options field is determined by the Internet Header Length (IHL),
    which specifies the total header length in 4-byte words. If IHL > 5, options are present.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            ihl = self._tracker.get('ihl', 5) * 4
            self._tracker['options'] = packet[20:ihl]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4PayloadFieldParserHandler(IPv4ParserHandler):
    """
    Handler for parsing the Payload (data) field from an IPv4 packet.
    The payload begins immediately after the IPv4 header and options. The header length
    is determined by the Internet Header Length (IHL) field, and the payload starts from that offset.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            ihl = self._tracker.get('ihl', 5) * 4
            self._tracker['payload'] = packet[ihl:]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class IPv4PacketParser:
    """
    Singleton parser class for parsing an IPv4 packet field by field using the Chain of Responsibility (CoR) pattern.
    The class ensures that only one instance of the parser exists at a time.
    """
    __instance: IPv4PacketParser = None

    def __new__(cls):
        """
        Implements the Singleton pattern. Ensures that only one instance of IPv4PacketParser is created.
        If an instance doesn't exist, a new one is created. If it exists, the existing instance is returned.
        """
        if cls.__instance is None:
            cls.__instance = super(IPv4PacketParser, cls).__new__(cls)
        return cls.__instance

    def _reset_parser(self):
        """
        Resets the parser chain by initializing all the field parser handlers in sequence.
        Each handler is responsible for parsing a specific field from the IPv4 packet.
        The handlers are linked together using the set_next() method to form a chain of responsibility.
        """
        self._packet_parser = IPv4VersionAndIHLFieldParserHandler()
        (
            self._packet_parser
            .set_next(IPv4TOSFieldParserHandler())
            .set_next(IPv4TotalLengthFieldParserHandler())
            .set_next(IPv4IdentificationFieldParserHandler())
            .set_next(IPv4FlagsAndFragmentOffsetFieldParserHandler())
            .set_next(IPv4TTLFieldParserHandler())
            .set_next(IPv4ProtocolFieldParserHandler())
            .set_next(IPv4HeaderChecksumFieldParserHandler())
            .set_next(IPv4SourceAddressFieldParserHandler())
            .set_next(IPv4DestinationAddressFieldParserHandler())
            .set_next(IPv4OptionsFieldParserHandler())
            .set_next(IPv4PayloadFieldParserHandler())
        )

    def parse(self, frame: bytes):
        """
        Parses the given IPv4 packet (frame) by passing it through the chain of handlers.

        Args:
            frame (bytes): The raw IPv4 packet data in bytes.

        Returns:
            dict: A dictionary of parsed IPv4 fields stored in the handler's tracker.
        """
        self._reset_parser()
        self._packet_parser.handle(frame)
        return self._packet_parser.get_tracker()
