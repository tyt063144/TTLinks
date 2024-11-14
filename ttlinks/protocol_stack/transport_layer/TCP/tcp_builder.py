from __future__ import annotations
import socket
import struct
from abc import ABC, abstractmethod
from typing import List

from ttlinks.common.algorithm.checksum import ChecksumCalculator, InternetChecksum
from ttlinks.common.tools.network import NetTools
from ttlinks.protocol_stack.base_classes.header_builder import Header, HeaderBuilder
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.transport_layer.TCP import tcp_units
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionUnit, TCPOptionHeader, TCPOption1HeaderBuilder
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


# -------------------TCP Header-------------------
class TCPHeader(Header):
    """
    Represents the TCP header and provides methods for constructing and structuring fields,
    including options padding, flags combination, and checksum calculation.

    Methods:
    - _struct_options(options: List[TCPOptionHeader]) -> bytes: Structures the options field, padding to 32-bit boundaries.
    - _struct_data_offset_reserved_flags(data_offset: int, reserved: int, flags: List[TCPFlags]) -> bytes: Combines data offset, reserved bits, and flags.
    - _calculate_checksum(...) -> bytes: Calculates the TCP checksum using a pseudo-header and the TCP segment fields.
    - _construct() -> dict: Constructs the full TCP header fields into byte format.

    Attributes:
    - unit (ProtocolUnit): Returns an instance of TCPUnit containing the structured header fields.
    """
    @staticmethod
    def _struct_options(options: List[TCPOptionHeader]) -> bytes:
        """
        Structures the options field by padding each option to a 32-bit boundary using No-Operation (NOP) options as needed.

        Parameters:
        - options (List[TCPOptionHeader]): List of TCP option headers to structure.

        Returns:
        - bytes: Structured options field in bytes with necessary padding.
        """
        padded_options = []
        for option in options:
            option_length = option.get_field('length')
            next_multiple_of_4 = (option_length + 3) // 4 * 4
            padding_length = next_multiple_of_4 - option_length
            if padding_length > 0:
                nop_builder = TCPOption1HeaderBuilder(TCPOptionHeader())
                for _ in range(padding_length):
                    nop_builder.set_kind(1)
                    nop_builder.set_length()
                    nop_builder.set_value()
                    padded_options.append(nop_builder.build())
            padded_options.append(option)
        return b''.join([option.unit.as_bytes for option in padded_options])

    @staticmethod
    def _struct_data_offset_reserved_flags(data_offset: int, reserved: int, flags: List[TCPFlags]) -> bytes:
        """
        Combines data offset, reserved bits, and flags into a 16-bit field.

        Parameters:
        - data_offset (int): Length of the header in 32-bit words.
        - reserved (int): Reserved bits, typically 0.
        - flags (List[TCPFlags]): List of TCP flags to set.

        Returns:
        - bytes: 16-bit combined field in bytes.
        """
        # Ensure data_offset only uses the upper 4 bits
        data_offset &= 0xF
        # Ensure reserved only uses 3 bits
        reserved &= 0x7
        # Combine flags using bitwise OR
        flag_sum = 0
        for flag in flags:
            flag_sum |= flag.value
        # Combine into 16-bit integer representation
        combined = (data_offset << 12) | (reserved << 9) | flag_sum
        # Pack into bytes (big-endian format)
        return struct.pack('!H', combined)

    @staticmethod
    def _calculate_checksum(
            source_ip: bytes, destination_ip: bytes,
            source_port: bytes, destination_port: bytes, sequence_number: bytes, acknowledgment_number: bytes,
            offset_reserved_flags: bytes, window_size: bytes, checksum: bytes, urgent_pointer: bytes, options: bytes,
            payload: bytes
    ) -> bytes:
        tcp_length = (int.from_bytes(offset_reserved_flags, 'big') >> 12) * 4 + len(payload)
        """
        Calculates the checksum of the TCP segment using a pseudo-header, the segment fields, and the payload.

        Parameters:
        - source_ip (bytes): Source IP address in bytes.
        - destination_ip (bytes): Destination IP address in bytes.
        - All other TCP segment fields as described in the TCP header.

        Returns:
        - bytes: The checksum field in bytes.
        """
        pseudo_header = (
            socket.inet_aton(source_ip)
            + socket.inet_aton(destination_ip)
            + b'\x00'
            + b'\x06'
            + struct.pack('!H', tcp_length)
        )
        raw_bytes_before_checksum = (
                source_port
                + destination_port
                + sequence_number
                + acknowledgment_number
                + offset_reserved_flags
                + window_size
                + checksum
                + urgent_pointer
                + options
        )
        checksum_int = ChecksumCalculator(InternetChecksum()).calculate(pseudo_header+raw_bytes_before_checksum+payload)
        return struct.pack('!H', checksum_int)

    def _construct(self) -> dict:
        """
        Constructs the TCP header by converting and combining each field into byte format, calculates checksum, and returns the complete header dictionary.

        Returns:
        - dict: Dictionary of TCP header fields in byte format.
        """
        source_ip = self._fields['source_ip']
        destination_ip = self._fields['destination_ip']
        source_port = struct.pack('!H', self._fields['source_port'])
        destination_port = struct.pack('!H', self._fields['destination_port'])
        sequence_number = struct.pack('!I', self._fields['sequence_number'])
        acknowledgment_number = struct.pack('!I', self._fields['acknowledgment_number'])
        options = self._struct_options(self._fields['options'])
        data_offset = (20 + len(options)) // 4
        reserved = self._fields['reserved']
        flags = self._fields['flags']
        offset_reserved_flags = self._struct_data_offset_reserved_flags(data_offset, reserved, flags)
        window_size = struct.pack('!H', self._fields['window_size'])
        urgent_pointer = struct.pack('!H', self._fields['urgent_pointer'])
        checksum = struct.pack('!H', 0)
        # Calculate checksum
        checksum = self._calculate_checksum(
            source_ip, destination_ip,
            source_port, destination_port, sequence_number, acknowledgment_number,
            offset_reserved_flags, window_size, checksum, urgent_pointer, options, self._fields['payload'])
        payload = self._fields['payload']

        return {
            'source_port': source_port,
            'destination_port': destination_port,
            'sequence_number': sequence_number,
            'acknowledgment_number': acknowledgment_number,
            'offset_reserved_flags': offset_reserved_flags,
            'window_size': window_size,
            'checksum': checksum,
            'urgent_pointer': urgent_pointer,
            'options': options,
            'payload': payload
        }

    @property
    def unit(self) -> ProtocolUnit:
        """
        Returns a fully constructed TCP unit with all header fields.

        Returns:
        - ProtocolUnit: An instance of TCPUnit containing the structured TCP header fields.
        """
        return tcp_units.TCPUnit(**self._construct())


# -------------------TCP Header Builder-------------------
class TCPHeaderBuilderInterface(HeaderBuilder, ABC):
    """
    Abstract builder interface for constructing a TCP header using the Builder pattern.
    Each method allows setting specific fields of the TCP header, enabling flexibility and customization.

    Methods:
    - set_source_ip(source_ip: str): Abstract method to set the source IP address.
    - set_destination_ip(destination_ip: str): Abstract method to set the destination IP address.
    - set_source_port(source_port: int): Abstract method to set the source port.
    - set_destination_port(destination_port: int): Abstract method to set the destination port.
    - set_sequence_number(sequence_number: int): Abstract method to set the sequence number.
    - set_acknowledgment_number(acknowledgment_number: int): Abstract method to set the acknowledgment number.
    - set_data_offset(data_offset: int): Abstract method to set the data offset (header length).
    - set_reserved(reserved: int): Abstract method to set reserved bits.
    - set_flags(flags: List[TCPFlags]): Abstract method to set TCP flags.
    - set_window_size(window_size: int): Abstract method to set the window size.
    - set_checksum(checksum: int): Abstract method to set the checksum.
    - set_urgent_pointer(urgent_pointer: int): Abstract method to set the urgent pointer.
    - set_options(options: List[TCPOptionUnit]): Abstract method to set TCP options.
    - set_payload(payload: bytes): Abstract method to set the payload data.
    """
    @abstractmethod
    def set_source_ip(self, source_ip: str):
        pass

    @abstractmethod
    def set_destination_ip(self, destination_ip: str):
        pass

    @abstractmethod
    def set_source_port(self, source_port: int):
        pass

    @abstractmethod
    def set_destination_port(self, destination_port: int):
        pass

    @abstractmethod
    def set_sequence_number(self, sequence_number: int):
        pass

    @abstractmethod
    def set_acknowledgment_number(self, acknowledgment_number: int):
        pass

    @abstractmethod
    def set_data_offset(self, data_offset: int):
        pass

    @abstractmethod
    def set_reserved(self, reserved: int):
        pass

    @abstractmethod
    def set_flags(self, flags: List[TCPFlags]):
        pass

    @abstractmethod
    def set_window_size(self, window_size: int):
        pass

    @abstractmethod
    def set_checksum(self, checksum: int):
        pass

    @abstractmethod
    def set_urgent_pointer(self, urgent_pointer: int):
        pass

    @abstractmethod
    def set_options(self, options: List[TCPOptionUnit]):
        pass

    @abstractmethod
    def set_payload(self, payload: bytes):
        pass

class TCPHeaderBuilder(TCPHeaderBuilderInterface):

    def set_source_ip(self, source_ip: str):
        """
        Sets the source IP address.

        Parameters:
        - source_ip (str): The source IP address.
        """
        self._header.add_field('source_ip', source_ip)

    def set_destination_ip(self, destination_ip: str):
        """
        Sets the destination IP address.

        Parameters:
        - destination_ip (str): The destination IP address.
        """
        self._header.add_field('destination_ip', destination_ip)

    def set_source_port(self, source_port: int = None):
        """
        Sets the source port. If None, assigns an unused port.

        Parameters:
        - source_port (int): The source port number.
        """
        if source_port is None:
            source_port = NetTools.get_unused_port()
        self._header.add_field('source_port', source_port)

    def set_destination_port(self, destination_port: int):
        """
        Sets the destination port.

        Parameters:
        - destination_port (int): The destination port number.
        """
        self._header.add_field('destination_port', destination_port)

    def set_sequence_number(self, sequence_number: int = None):
        """
        Sets the sequence number. If None, assigns a random sequence number.

        Parameters:
        - sequence_number (int): The sequence number.
        """
        if sequence_number is None:
            sequence_number = NetTools.get_tcp_sequence_number()
        self._header.add_field('sequence_number', sequence_number)

    def set_acknowledgment_number(self, acknowledgment_number: int = 0):
        """
        Sets the acknowledgment number. Defaults to 0.

        Parameters:
        - acknowledgment_number (int): The acknowledgment number.
        """
        self._header.add_field('acknowledgment_number', acknowledgment_number)

    def set_data_offset(self, data_offset: int = 5):
        """
        Sets the data offset, indicating the header length. Defaults to 5.

        Parameters:
        - data_offset (int): The data offset.
        """
        self._header.add_field('data_offset', data_offset)

    def set_reserved(self, reserved: int = 0):
        """
        Sets reserved bits in the TCP header. Defaults to 0.

        Parameters:
        - reserved (int): The reserved bits.
        """
        self._header.add_field('reserved', reserved)

    def set_flags(self, flags:List[TCPFlags]=None):
        """
        Sets the TCP flags. Defaults to the ACK flag if None.

        Parameters:
        - flags (List[TCPFlags]): List of TCP flags.
        """
        if flags is None:
            flags = [TCPFlags.ACK]
        self._header.add_field('flags', flags)

    def set_window_size(self, window_size: int=None):
        """
        Sets the window size for flow control. Defaults to 64240 if None.

        Parameters:
        - window_size (int): The window size.
        """
        if window_size is None:
            window_size = 64240
        self._header.add_field('window_size', window_size)

    def set_checksum(self, checksum: int = None):
        """
        Sets the checksum. Defaults to None (calculated later).

        Parameters:
        - checksum (int): The checksum.
        """
        self._header.add_field('checksum', checksum)

    def set_urgent_pointer(self, urgent_pointer: int = 0):
        """
        Sets the urgent pointer, which points to urgent data in the TCP segment. Defaults to 0.

        Parameters:
        - urgent_pointer (int): The urgent pointer.
        """
        self._header.add_field('urgent_pointer', urgent_pointer)

    def set_options(self, options: List[TCPOptionUnit] = None):
        """
        Sets the TCP options. Defaults to an empty list if None.

        Parameters:
        - options (List[TCPOptionUnit]): List of TCP options.
        """
        if options is None:
            options = []
        self._header.add_field('options', options)

    def set_payload(self, payload: bytes = b''):
        """
        Sets the payload data for the TCP segment. Defaults to an empty byte string.

        Parameters:
        - payload (bytes): The payload data.
        """
        self._header.add_field('payload', payload)

# -------------------TCP builder director-------------------
class TCPBuilderDirector:
    """
    Director class for constructing a TCP header using a specified builder. This class organizes
    the construction of a TCP header with commonly required fields and values.

    Methods:
    - construct(...): Orchestrates the TCP header construction process by setting fields in the builder.

    Attributes:
    - builder (TCPHeaderBuilderInterface): The builder instance used for constructing the TCP header.
    """
    def __init__(self, builder):
        """
        Initializes the director with a builder for constructing the TCP header.

        Parameters:
        - builder (TCPHeaderBuilderInterface): The builder instance to use for TCP header construction.
        """
        self.builder = builder

    def construct(
            self,
            source_ip: str,
            destination_ip: str,
            source_port: int,
            destination_port: int,
            sequence_number: int,
            acknowledgment_number: int,
            reserved: int,
            flags: List[TCPFlags],
            option_units: List[TCPOptionUnit],
            window_size: int,
            urgent_pointer: int = 0,
            payload: bytes = b'',
    ):
        """
        Constructs the TCP header by setting fields with the builder and returning the completed header unit.

        Parameters:
        - source_ip (str): The source IP address.
        - destination_ip (str): The destination IP address.
        - source_port (int): The source port number.
        - destination_port (int): The destination port number.
        - sequence_number (int): The TCP sequence number.
        - acknowledgment_number (int): The TCP acknowledgment number.
        - reserved (int): Reserved bits in the TCP header.
        - flags (List[TCPFlags]): List of TCP flags to set.
        - option_units (List[TCPOptionUnit]): List of TCP options.
        - window_size (int): The TCP window size.
        - urgent_pointer (int): The urgent pointer; defaults to 0.
        - payload (bytes): The TCP segment payload; defaults to an empty byte string.

        Returns:
        - ProtocolUnit: The constructed TCP header as a TCPUnit instance.
        """
        tcp_header = TCPHeader()
        tcp_builder = TCPHeaderBuilder(tcp_header)
        tcp_builder.set_source_ip(source_ip)
        tcp_builder.set_destination_ip(destination_ip)
        tcp_builder.set_source_port(source_port)
        tcp_builder.set_destination_port(destination_port)
        tcp_builder.set_sequence_number(sequence_number)
        tcp_builder.set_acknowledgment_number(acknowledgment_number)
        tcp_builder.set_reserved(reserved)
        tcp_builder.set_flags(flags)
        tcp_builder.set_options(option_units)
        tcp_builder.set_window_size(window_size)
        tcp_builder.set_urgent_pointer(urgent_pointer)
        tcp_builder.set_payload(payload)

        result = tcp_builder.build()
        return result.unit
