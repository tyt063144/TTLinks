from __future__ import annotations

from typing import List

from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionUnit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_parsers import TCPOptionParser
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


class TCPUnit(ProtocolUnit):
    """
    Represents a TCP protocol unit, encapsulating key components of a TCP packet, including ports, sequence and acknowledgment
    numbers, flags, window size, checksum, and optional data fields. Provides methods to access each attribute in byte or
    integer format, as well as utilities for interpreting flag and option settings.

    Attributes:
    - source_port (bytes): Source port number in bytes.
    - destination_port (bytes): Destination port number in bytes.
    - sequence_number (bytes): Sequence number of the TCP segment.
    - acknowledgment_number (bytes): Acknowledgment number of the TCP segment.
    - offset_reserved_flags (bytes): Data offset, reserved bits, and flags combined in a single byte sequence.
    - window_size (bytes): The window size for flow control.
    - checksum (bytes): Error-checking field for the header.
    - urgent_pointer (bytes): Points to urgent data within the segment.
    - options (bytes): TCP options, if any.
    - payload (bytes): Payload data to be transmitted in the segment.

    Properties:
    - as_bytes: Returns the raw byte representation of the TCP segment.
    - attributes: Returns a dictionary of core TCP segment fields and their byte values.
    - summary: Returns a dictionary summary with key attributes in a human-readable format.
    - source_port, destination_port, sequence_number, acknowledgment_number, data_offset, reserved, flags, window_size,
      checksum, urgent_pointer, options, payload: Provides detailed access to each attribute with the appropriate type.

    Methods:
    - data_offset: Extracts the data offset (header length) from offset_reserved_flags.
    - reserved: Extracts reserved bits from offset_reserved_flags.
    - flags: Interprets the flags set in the TCP header and returns them as a list of `TCPFlags`.
    """
    def __init__(
            self,
            source_port: bytes,
            destination_port: bytes,
            sequence_number: bytes,
            acknowledgment_number: bytes,
            offset_reserved_flags: bytes,
            window_size: bytes,
            checksum: bytes,
            urgent_pointer: bytes,
            options: bytes,
            payload: bytes
    ):
        self._source_port = source_port
        self._destination_port = destination_port
        self._sequence_number = sequence_number
        self._acknowledgment_number = acknowledgment_number
        self._offset_reserved_flags = offset_reserved_flags
        self._window_size = window_size
        self._checksum = checksum
        self._urgent_pointer = urgent_pointer
        self._options = options
        self._payload = payload

    @property
    def as_bytes(self):
        """
        Returns the raw byte representation of the TCP segment by concatenating all segment parts.

        Returns:
        - bytes: Complete TCP segment as bytes.
        """
        return (
            self._source_port
            + self._destination_port
            + self._sequence_number
            + self._acknowledgment_number
            + self._offset_reserved_flags
            + self._window_size
            + self._checksum
            + self._urgent_pointer
            + self._options
        )

    @property
    def attributes(self):
        """
        Returns a dictionary of core TCP segment fields in their raw byte form.

        Returns:
        - dict: Dictionary mapping field names to their byte values.
        """
        return {
            "source_port": self._source_port,
            "destination_port": self._destination_port,
            "sequence_number": self._sequence_number,
            "acknowledgment_number": self._acknowledgment_number,
            "offset_reserved_flags": self._offset_reserved_flags,
            "window_size": self._window_size,
            "checksum": self._checksum,
            "urgent_pointer": self._urgent_pointer,
            "options": self._options,
        }

    @property
    def summary(self) -> dict:
        """
        Provides a summary dictionary with core TCP segment fields in human-readable format.

        Returns:
        - dict: Dictionary with descriptive keys and processed values for key TCP attributes.
        """
        return {
            "source_port": self.source_port,
            "destination_port": self.destination_port,
            "sequence_number": self.sequence_number,
            "acknowledgment_number": self.acknowledgment_number,
            "data_offset": self.data_offset,
            "reserved": self.reserved,
            "flags": self.flags,
            "window_size": self.window_size,
            "checksum": self.checksum,
            "urgent_pointer": self.urgent_pointer,
            "options": self.options,
            "payload": self.payload
        }

    @property
    def source_port(self) -> int:
        """
        Retrieves the source port number.

        Returns:
        - int: Source port number as an integer.
        """
        return int.from_bytes(self._source_port, byteorder="big")

    @property
    def destination_port(self) -> int:
        """
        Retrieves the destination port number.

        Returns:
        - int: Destination port number as an integer.
        """
        return int.from_bytes(self._destination_port, byteorder="big")

    @property
    def sequence_number(self) -> int:
        """
        Retrieves the TCP sequence number.

        Returns:
        - int: Sequence number as an integer.
        """
        return int.from_bytes(self._sequence_number, byteorder="big")

    @property
    def acknowledgment_number(self) -> int:
        """
        Retrieves the acknowledgment number.

        Returns:
        - int: Acknowledgment number as an integer.
        """
        return int.from_bytes(self._acknowledgment_number, byteorder="big")

    @property
    def data_offset(self) -> int:
        """
        Extracts the data offset, indicating the header length in 32-bit words.

        Returns:
        - int: Data offset value.
        """
        data_offset = int.from_bytes(self._offset_reserved_flags, byteorder="big") >> 12
        return data_offset

    @property
    def reserved(self) -> int:
        """
        Extracts the reserved bits from the offset_reserved_flags field.

        Returns:
        - int: Reserved bits as an integer.
        """
        reserved = (int.from_bytes(self._offset_reserved_flags, byteorder="big") & 0x0E00) >> 9
        return reserved

    @property
    def flags(self) -> List[TCPFlags]:
        """
        Extracts and interprets TCP flags from the offset_reserved_flags field.

        Returns:
        - List[TCPFlags]: List of active TCP flags.
        """
        flags = []
        offset_reserved_flags = int.from_bytes(self._offset_reserved_flags, byteorder="big") & 0x01FF
        for tcp_flag in TCPFlags:
            if offset_reserved_flags & tcp_flag.value:
                flags.append(tcp_flag)
        return flags

    @property
    def window_size(self) -> int:
        """
        Retrieves the window size for flow control.

        Returns:
        - int: Window size as an integer.
        """
        return int.from_bytes(self._window_size, byteorder="big")

    @property
    def checksum(self) -> hex:
        """
        Retrieves the checksum for error-checking purposes.

        Returns:
        - hex: Checksum as a hexadecimal string.
        """
        return hex(int.from_bytes(self._checksum, byteorder="big"))

    @property
    def urgent_pointer(self) -> int:
        """
        Retrieves the urgent pointer, if any.

        Returns:
        - int: Urgent pointer as an integer.
        """
        return int.from_bytes(self._urgent_pointer, byteorder="big")

    @property
    def options(self) -> List[TCPOptionUnit]:
        """
        Parses TCP options using TCPOptionParser.

        Returns:
        - List[TCPOptionUnit]: List of parsed TCP options.
        """
        tcp_option_parser = TCPOptionParser()
        return tcp_option_parser.parse(self._options)

    @property
    def payload(self) -> bytes:
        """
        Retrieves the payload data of the TCP segment.

        Returns:
        - bytes: Payload data.
        """
        return self._payload


