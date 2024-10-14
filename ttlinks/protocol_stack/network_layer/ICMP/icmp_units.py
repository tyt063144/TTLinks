from abc import ABC, abstractmethod

from ttlinks.common.design_template.cor import ProtocolUnitSelectorCoRHandler
from ttlinks.ipservice.ip_address import IPv4Addr
from ttlinks.ipservice.ip_converters import IPConverter
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.ethernet_layer import ethernet_payload_unit_factory
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import EthernetPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.ICMP.icmp_parsers import ICMPParser
from ttlinks.protocol_stack.network_layer.ICMP.icmp_utils import ICMPTypes


class ICMPUnits(ProtocolUnit, ABC):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, payload: bytes):
        self._icmp_type = icmp_type
        self._icmp_code = icmp_code
        self._checksum = checksum
        self._payload = payload

    @property
    def as_bytes(self) -> bytes:
        """Convert all attributes to bytes and return the complete byte representation."""
        bytes_result = b''
        for attr in self.attributes.values():
            bytes_result += attr
        return bytes_result

    @property
    @abstractmethod
    def attributes(self) -> dict:
        """Returns a dictionary of ICMP attributes as bytes. Can be overridden by subclasses."""
        return {
            'icmp_type': self._icmp_type,
            'icmp_code': self._icmp_code,
            'checksum': self._checksum,
            'payload': self._payload
        }

    @property
    @abstractmethod
    def summary(self) -> dict:
        """Summarize the main details of the ICMP message."""
        return {
            'message_type': self.message_type,
            'icmp_type': self.icmp_type,
            'icmp_code': self.icmp_code,
            'checksum': self.checksum,
            'payload': self.payload
        }

    @property
    def message_type(self) -> ICMPTypes:
        """Returns the ICMP message type as an `ICMPTypes` enum."""
        return ICMPTypes(int.from_bytes(self._icmp_type))

    @property
    def icmp_type(self) -> int:
        """Returns the ICMP type as an integer."""
        return int.from_bytes(self._icmp_type, 'big')

    @property
    def icmp_code(self) -> int:
        """Returns the ICMP code as an integer."""
        return int.from_bytes(self._icmp_code, 'big')

    @property
    def checksum(self) -> hex:
        """Returns the checksum as a hexadecimal string."""
        return hex(int.from_bytes(self._checksum, 'big'))

    @property
    @abstractmethod
    def payload(self) -> bytes:
        """Returns the ICMP payload."""
        return self._payload

class ICMPEchoAndReplyUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, identifier: bytes, sequence_number: bytes, payload: bytes):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._identifier = identifier
        self._sequence_number = sequence_number

    @property
    def attributes(self) -> dict:
        """Merge base class attributes with identifier and sequence number."""
        return super().attributes | {
            'identifier': self._identifier,
            'sequence_number': self._sequence_number
        }

    @property
    def summary(self) -> dict:
        """Merge base class summary with identifier and sequence number."""
        return super().summary | {
            'identifier': self.identifier,
            'sequence_number': self.sequence_number
        }

    @property
    def identifier(self) -> int:
        """Return the identifier as an integer."""
        return int.from_bytes(self._identifier, 'big')

    @property
    def sequence_number(self) -> int:
        """Return the sequence number as an integer."""
        return int.from_bytes(self._sequence_number, 'big')

    @property
    def payload(self) -> bytes:
        return self._payload

class ICMPDestinationUnreachableUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, unused: bytes, payload: bytes):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._unused = unused

    @property
    def attributes(self) -> dict:
        return super().attributes | {
            'unused': self._unused
        }

    @property
    def summary(self) -> dict:
        return super().summary | {
            'unused': self.unused
        }

    @property
    def unused(self) -> bytes:
        return self._unused

    @property
    def payload(self) -> bytes:
        parsed_payload = ethernet_payload_unit_factory.EthernetPayloadUnitFactory.create_unit(self._payload, EthernetPayloadProtocolTypes.IPv4)
        if parsed_payload:
            return parsed_payload
        return self._payload

class ICMPRedirectUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, gateway_address: bytes, payload: bytes):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._gateway_address = gateway_address

    @property
    def attributes(self) -> dict:
        return super().attributes | {
            'gateway_address': self._gateway_address
        }

    @property
    def summary(self) -> dict:
        return super().summary | {
            'gateway_address': self.gateway_address
        }

    @property
    def gateway_address(self) -> IPv4Addr:
        return IPv4Addr(IPConverter.convert_to_ipv4_octets(int.from_bytes(self._gateway_address, byteorder='big')))

    @property
    def payload(self) -> bytes:
        parsed_payload = ethernet_payload_unit_factory.EthernetPayloadUnitFactory.create_unit(self._payload, EthernetPayloadProtocolTypes.IPv4)
        if parsed_payload:
            return parsed_payload
        return self._payload

class ICMPTimeExceededUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, unused: bytes, payload: bytes):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._unused = unused

    @property
    def attributes(self) -> dict:
        return super().attributes | {
            'unused': self._unused
        }

    @property
    def summary(self) -> dict:
        return super().summary | {
            'unused': self.unused
        }

    @property
    def unused(self) -> bytes:
        return self._unused

    @property
    def payload(self) -> bytes:
        parsed_payload = ethernet_payload_unit_factory.EthernetPayloadUnitFactory.create_unit(self._payload, EthernetPayloadProtocolTypes.IPv4)
        if parsed_payload:
            return parsed_payload
        return self._payload

class ICMPParameterProblemUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, pointer: bytes, payload: bytes):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._pointer = pointer

    @property
    def attributes(self) -> dict:
        return super().attributes | {
            'pointer': self._pointer
        }

    @property
    def summary(self) -> dict:
        return super().summary | {
            'pointer': self.pointer
        }

    @property
    def pointer(self) -> bytes:
        return self._pointer

    @property
    def payload(self) -> bytes:
        parsed_payload = ethernet_payload_unit_factory.EthernetPayloadUnitFactory.create_unit(self._payload, EthernetPayloadProtocolTypes.IPv4)
        if parsed_payload:
            return parsed_payload
        return self._payload

class ICMPTimestampAndReplyUnits(ICMPUnits):
    def __init__(self, icmp_type: bytes, icmp_code: bytes, checksum: bytes, identifier: bytes,
                 sequence_number: bytes, originate_timestamp: bytes, receive_timestamp: bytes, transmit_timestamp: bytes, payload: bytes=b''):
        super().__init__(icmp_type, icmp_code, checksum, payload)
        self._identifier = identifier
        self._sequence_number = sequence_number
        self._originate_timestamp = originate_timestamp
        self._receive_timestamp = receive_timestamp
        self._transmit_timestamp = transmit_timestamp

    @property
    def attributes(self) -> dict:
        return super().attributes | {
            'identifier': self._identifier,
            'sequence_number': self._sequence_number,
            'originate_timestamp': self._originate_timestamp,
            'receive_timestamp': self._receive_timestamp,
            'transmit_timestamp': self._transmit_timestamp
        }

    @property
    def summary(self) -> dict:
        return super().summary | {
            'identifier': self.identifier,
            'sequence_number': self.sequence_number,
            'originate_timestamp': self.originate_timestamp,
            'receive_timestamp': self.receive_timestamp,
            'transmit_timestamp': self.transmit_timestamp
        }

    @property
    def identifier(self) -> int:
        return int.from_bytes(self._identifier, 'big')

    @property
    def sequence_number(self) -> int:
        return int.from_bytes(self._sequence_number, 'big')

    @property
    def originate_timestamp(self) -> bytes:
        return self._originate_timestamp

    @property
    def receive_timestamp(self) -> bytes:
        return self._receive_timestamp

    @property
    def transmit_timestamp(self) -> bytes:
        return self._transmit_timestamp

    @property
    def payload(self) -> bytes:
        return self._payload

# ------------------------------Unit Factory--------------------------------

class ICMPUnitSelectorHandler(ProtocolUnitSelectorCoRHandler):
    """
    Base handler for selecting and processing ICMP units.
    This class is part of a Chain of Responsibility pattern where multiple handlers
    process an incoming packet. If this handler cannot process the packet, it passes
    the packet to the next handler in the chain.
    """
    def handle(self, packet, *args, **kwargs):
        """
        Attempts to handle the packet or passes it to the next handler if it cannot.

        Args:
            packet (bytes): The raw packet data that needs to be parsed.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            Processed ICMP unit (if this handler processes the packet), or passes the
            packet to the next handler in the chain.
        """
        if self._next_handler:
            self._next_handler.set_parsed_data(self._parsed_data)
            return self._next_handler.handle(packet, *args, **kwargs)
        return self._next_handler

class ICMPEchoAndReplyUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Echo Request and Echo Reply messages.
    This handler checks if the parsed ICMP packet corresponds to an Echo Request (type 8)
    or Echo Reply (type 0). If so, it processes the packet by constructing an
    `ICMPEchoAndReplyUnits` object. Otherwise, it passes the packet to the next handler.
    """
    def _parse(self, packet: bytes):
        """
        Parses the ICMP packet and stores the result in _parsed_data.
        The packet should contain the raw bytes of the ICMP message, and the parser
        converts this into a structured data format (likely a dictionary).

        Args:
            packet (bytes): The raw packet data that needs to be parsed.
        """
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Echo Request (type 8) or Echo Reply (type 0).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPEchoAndReplyUnits: If the packet matches the Echo Request or Reply type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                in [ICMPTypes.ECHO.value, ICMPTypes.ECHO_REPLY.value]
        ):
            return ICMPEchoAndReplyUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPDestinationUnreachableUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Destination Unreachable messages (type 3).
    This handler checks if the parsed ICMP packet corresponds to a Destination Unreachable message.
    If so, it processes the packet by constructing an `ICMPDestinationUnreachableUnits` object.
    Otherwise, it passes the packet to the next handler.
    """
    def _parse(self, packet: bytes):
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Destination Unreachable message (type 3).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPDestinationUnreachableUnits: If the packet matches the Destination Unreachable type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                == ICMPTypes.DESTINATION_UNREACHABLE.value
        ):
            return ICMPDestinationUnreachableUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPRedirectUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Redirect messages (type 5).
    This handler checks if the parsed ICMP packet corresponds to an ICMP Redirect message.
    If so, it processes the packet by constructing an `ICMPRedirectUnits` object.
    Otherwise, it passes the packet to the next handler in the chain.
    """
    def _parse(self, packet: bytes):
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Redirect message (type 5).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPRedirectUnits: If the packet matches the Redirect message type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                == ICMPTypes.REDIRECT.value
        ):
            return ICMPRedirectUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPTimeExceededUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Time Exceeded messages (type 11).
    This handler checks if the parsed ICMP packet corresponds to an ICMP Time Exceeded message.
    If so, it processes the packet by constructing an `ICMPTimeExceededUnits` object.
    Otherwise, it passes the packet to the next handler in the chain.
    """
    def _parse(self, packet: bytes):
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Time Exceeded message (type 11).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPTimeExceededUnits: If the packet matches the Time Exceeded message type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                == ICMPTypes.TIME_EXCEEDED.value
        ):
            return ICMPTimeExceededUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPParameterProblemUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Parameter Problem messages (type 12).
    This handler checks if the parsed ICMP packet corresponds to a Parameter Problem message.
    If so, it processes the packet by constructing an `ICMPParameterProblemUnits` object.
    Otherwise, it passes the packet to the next handler in the chain.
    """
    def _parse(self, packet: bytes):
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Parameter Problem message (type 12).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPParameterProblemUnits: If the packet matches the Parameter Problem message type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                == ICMPTypes.PARAMETER_PROBLEM.value
        ):
            return ICMPParameterProblemUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPTimestampAndReplyUnitSelectorHandler(ICMPUnitSelectorHandler):
    """
    Handler for ICMP Timestamp Request and Timestamp Reply messages (types 13 and 14).
    This handler checks if the parsed ICMP packet corresponds to a Timestamp Request (type 13)
    or Timestamp Reply (type 14). If so, it processes the packet by constructing an
    `ICMPTimestampAndReplyUnits` object. Otherwise, it passes the packet to the next handler.
    """
    def _parse(self, packet: bytes):
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(packet)
    def handle(self, packet: bytes, *args, **kwargs):
        """
        Handles the packet if it is an ICMP Timestamp Request (type 13) or Timestamp Reply (type 14).
        If the packet is of another type, it passes it to the next handler in the chain.

        Args:
            packet (bytes): The raw packet data to be handled.
            *args: Additional arguments that may be passed to handlers.
            **kwargs: Additional keyword arguments that may be passed to handlers.

        Returns:
            ICMPTimestampAndReplyUnits: If the packet matches the Timestamp Request or Reply message type.
            Otherwise, passes the packet to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(packet)
        if (
                isinstance(self._parsed_data, dict)
                and int.from_bytes(self._parsed_data.get('icmp_type'), 'big')
                in [ICMPTypes.TIMESTAMP.value, ICMPTypes.TIMESTAMP_REPLY.value]
        ):
            return ICMPTimestampAndReplyUnits(**self._parsed_data)
        else:
            return super().handle(packet, *args, **kwargs)

class ICMPUnitFactory:
    """
    ICMPUnitFactory creates a chain of responsibility to handle different ICMP message types.
    It uses different handlers for each type of ICMP message, such as Echo Request/Reply,
    Destination Unreachable, Time Exceeded, Redirect, Parameter Problem, and Timestamp.
    """
    @staticmethod
    def create_unit(packet: bytes) -> ProtocolUnit:
        """
        Creates and returns the appropriate ICMP unit based on the packet data.

        Args:
            packet (bytes): The raw bytes of the ICMP packet.

        Returns:
            ProtocolUnit: The appropriate ICMP unit (e.g., Echo Request/Reply, Destination Unreachable, etc.).
                          If no handler can process the packet, returns None or raises an exception.
        """
        icmp_unit_selector = ICMPEchoAndReplyUnitSelectorHandler(ICMPParser())
        (
            icmp_unit_selector
            .set_next(ICMPDestinationUnreachableUnitSelectorHandler())
            .set_next(ICMPTimeExceededUnitSelectorHandler())
            .set_next(ICMPRedirectUnitSelectorHandler())
            .set_next(ICMPParameterProblemUnitSelectorHandler())
            .set_next(ICMPTimestampAndReplyUnitSelectorHandler())
        )
        return icmp_unit_selector.handle(packet)