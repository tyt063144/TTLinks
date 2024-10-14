from __future__ import annotations
import random
import struct
from abc import ABC, abstractmethod

from ttlinks.common.algorithm.checksum import ChecksumCalculator, InternetChecksum
from ttlinks.protocol_stack.base_classes.header_builder import HeaderBuilder, Header
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.network_layer.ICMP import icmp_units


# -------------------ICMP Header-------------------
class ICMPEchoRequestHeader(Header):
    """
    A class for constructing and representing an ICMP Echo Request header.

    This class constructs the ICMP Echo Request header based on the provided fields, such as
    ICMP type, code, checksum, identifier, sequence number, and payload. It computes the
    Internet checksum based on the header fields and the payload, returning the fully
    constructed header in bytes format.

    Methods:
    - _construct: Constructs the ICMP header and calculates the checksum.
    - unit: Returns the corresponding protocol unit for the ICMP Echo and Reply.

    Parameters:
    None (inherits from Header)
    """
    def _construct(self) -> dict:
        """
        Constructs the ICMP Echo Request header and calculates the checksum.

        This method takes the fields provided in the `_fields` dictionary and constructs
        the ICMP Echo Request header. It computes the checksum for the header and returns
        the fields in bytes format, ready to be transmitted.

        Returns:
        dict: A dictionary containing the ICMP header fields in bytes format.
        """
        icmp_type_bytes = struct.pack('!B', self._fields['icmp_type'])
        icmp_code_bytes = struct.pack('!B', self._fields['icmp_code'])
        checksum_bytes = struct.pack('!H', self._fields['checksum'])
        identifier_bytes = struct.pack('!H', self._fields['identifier'])
        sequence_number_bytes = struct.pack('!H', self._fields['sequence_number'])
        payload = self._fields['payload']
        raw_bytes_before_checksum = icmp_type_bytes + icmp_code_bytes + checksum_bytes + identifier_bytes + sequence_number_bytes
        calculated_checksum = ChecksumCalculator(InternetChecksum()).calculate(raw_bytes_before_checksum)
        calculated_checksum = struct.pack('!H', calculated_checksum)
        return {
            'icmp_type': icmp_type_bytes,
            'icmp_code': icmp_code_bytes,
            'checksum': calculated_checksum,
            'identifier': identifier_bytes,
            'sequence_number': sequence_number_bytes,
            'payload': payload
        }

    @property
    def unit(self) -> ProtocolUnit:
        """
        Returns the ICMP Echo and Reply unit for the constructed header.

        This property constructs the ICMP Echo Request header using `_construct` and
        returns an instance of `ICMPEchoAndReplyUnits` with the constructed header.

        Returns:
        ProtocolUnit: An instance of `ICMPEchoAndReplyUnits` containing the constructed header.
        """
        return icmp_units.ICMPEchoAndReplyUnits(**self._construct())


# -------------------ICMP Header Builder-------------------
class ICMPHeaderBuilder(HeaderBuilder, ABC):

    @abstractmethod
    def set_type(self, type: int):
        pass

    @abstractmethod
    def set_code(self, code: int):
        pass

    @abstractmethod
    def set_checksum(self, checksum: int):
        pass

    @abstractmethod
    def set_payload(self, payload: bytes):
        pass

class ICMPEchoRequestHeaderBuilder(ICMPHeaderBuilder):
    def set_type(self, type: int = 8):
        if type != 8:
            raise ValueError('ICMP Echo Request type must be 8')
        self._header.add_field('icmp_type', type)

    def set_code(self, code: int = 0):
        if code != 0:
            raise ValueError('ICMP Echo Request code must be 0')
        self._header.add_field('icmp_code', code)

    def set_checksum(self, checksum: int = 0):
        self._header.add_field('checksum', checksum)

    def set_identifier(self, identifier: int = None):
        if identifier is None:
            identifier = random.getrandbits(16)
        self._header.add_field('identifier', identifier)

    def set_sequence_number(self, sequence_number: int = None):
        if sequence_number is None:
            sequence_number = random.getrandbits(16)
        self._header.add_field('sequence_number', sequence_number)

    def set_payload(self, payload: bytes = b''):
        self._header.add_field('payload', payload)


# -------------------ICMP Header Builder Director-------------------
class ICMPHeaderBuilderDirector:
    """
    This director is used to build ICMP packets. If you want to customize the packet, you can call the builders methods directly.
    """
    def __init__(self, builder):
        self.builder = builder

    def build_echo_request(self):
        self.builder.set_type()
        self.builder.set_code()
        self.builder.set_checksum()
        self.builder.set_identifier()
        self.builder.set_sequence_number()
        self.builder.set_payload()
        return self.builder.build()
