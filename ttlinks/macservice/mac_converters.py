import re
from abc import abstractmethod
from typing import Any, List, Union

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class MACConverterHandler(SimpleCoRHandler):
    """
    An abstract base class for handling MAC address conversion requests in
    a chain of responsibility pattern. Each subclass implements specific
    logic to convert MAC address representations into bytes.

    This class follows the Chain of Responsibility design pattern, allowing
    different handlers to process various MAC address formats. If a handler
    cannot process a request, it passes it to the next handler in the chain.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes the MAC address conversion request and passes it
            along the chain if not handled.
        
        _to_bytes(request: Any) -> bytes:
            An abstract method to define how the subclass converts the
            request to a byte representation.
    """

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the MAC address conversion request. If this handler cannot
        process the request, it passes it to the next handler in the chain.

        Args:
            request (Any): The MAC address in various formats (binary list,
                          dashed hex, colon hex, or dot hex).
            *args, **kwargs: Additional arguments.

        Returns:
            bytes: The converted MAC address in byte format if handled.
            Otherwise, the request is passed to the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _to_bytes(self, request: Any) -> bytes:
        """
        Abstract method that converts a MAC address into bytes.

        Args:
            request (Any): The MAC address to be converted.

        Returns:
            bytes: The MAC address in byte format.
        """
        pass


class BinaryDigitsMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses represented as a list of 48 binary digits.

    This handler checks if the request is a list of exactly 48 elements
    containing only `0s` and `1s`. If valid, it converts the binary
    representation into a 6-byte sequence.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes binary digit MAC addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a binary list into a 6-byte representation.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and len(request) == 48 and set(request) == {0, 1}:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a list of binary digits into a 6-byte representation.

        Args:
            request (list): A list of 48 binary digits (0s and 1s).

        Returns:
            bytes: The corresponding MAC address in byte format.
        """
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 6)


class DashedHexMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses in dashed hexadecimal format (e.g., "AA-BB-CC-DD-EE-FF").

    This handler validates whether the request is a MAC address in dashed
    hexadecimal notation. If valid, it converts it to a 6-byte sequence.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes dashed hexadecimal MAC addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a dashed hex string into a 6-byte representation.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('-', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a dashed hexadecimal MAC address into a 6-byte sequence.

        Args:
            request (str): A MAC address in "AA-BB-CC-DD-EE-FF" format.

        Returns:
            bytes: The corresponding MAC address in byte format.
        """
        raw_mac = request.replace('-', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class ColonHexMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses in colon-separated hexadecimal format (e.g., "AA:BB:CC:DD:EE:FF").

    This handler validates whether the request is a MAC address in colon-separated
    hexadecimal notation. If valid, it converts it to a 6-byte sequence.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes colon-separated hexadecimal MAC addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a colon-separated hex string into a 6-byte representation.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace(':', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a colon-separated hexadecimal MAC address into a 6-byte sequence.

        Args:
            request (str): A MAC address in "AA:BB:CC:DD:EE:FF" format.

        Returns:
            bytes: The corresponding MAC address in byte format.
        """
        raw_mac = request.replace(':', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class DotHexMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses in dot-separated hexadecimal format (e.g., "AABB.CCDD.EEFF").

    This handler validates whether the request is a MAC address in dot-separated
    hexadecimal notation. If valid, it converts it to a 6-byte sequence.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes dot-separated hexadecimal MAC addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a dot-separated hex string into a 6-byte representation.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('.', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a dot-separated hexadecimal MAC address into a 6-byte sequence.

        Args:
            request (str): A MAC address in "AABB.CCDD.EEFF" format.

        Returns:
            bytes: The corresponding MAC address in byte format.
        """
        raw_mac = request.replace('.', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class DecimalMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses represented as decimal integers.

    This handler checks if the request is an integer within the valid
    48-bit MAC address range (greater than 0 and within 48 bits).
    If valid, it converts the integer into a 6-byte MAC address.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes decimal MAC addresses and converts them to bytes.

        _to_bytes(request: int) -> bytes:
            Converts a decimal integer into a 6-byte representation.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, int) and request.bit_length() <= 48 and request > 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: int) -> bytes:
        """
        Converts a decimal MAC address to a 6-byte sequence.

        Args:
            request (int): A MAC address represented as an integer.

        Returns:
            bytes: The corresponding MAC address in byte format.
        """
        return NumeralConverter.decimal_to_bytes(request, 6)


class BytesMAC48ConverterHandler(MACConverterHandler):
    """
    Handles MAC addresses represented as raw byte sequences.

    This handler checks if the request is a **6-byte sequence** where
    each byte falls within the valid range (0-255). If valid, it returns
    the bytes as-is.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes MAC addresses given as bytes.

        _to_bytes(request: bytes) -> bytes:
            Returns the input bytes unchanged.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 6 and max(request) <= 255 and min(request) >= 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        """
        Returns the raw byte sequence as the MAC address.

        Args:
            request (bytes): A 6-byte MAC address.

        Returns:
            bytes: The original byte sequence.
        """
        return request


class BinaryDigitsOUI24ConverterHandler(MACConverterHandler):
    """
    Handles OUI addresses (first 24 bits of a MAC address) represented as binary digits.

    This handler checks if the request is a **24-bit binary list** containing
    only `0s` and `1s`. If valid, it converts it into a **3-byte OUI sequence**
    and pads it with three `\x00` bytes to form a 6-byte MAC address.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes binary digit OUI addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a binary list into a 3-byte OUI sequence padded to 6 bytes.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and len(request) == 24 and set(request) == {0, 1}:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a 24-bit binary OUI into a 6-byte MAC address.

        Args:
            request (list): A list of 24 binary digits (0s and 1s).

        Returns:
            bytes: The 3-byte OUI sequence padded with three `\x00` bytes.
        """
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 3) + b'\x00' * 3


class DashedHexOUI24ConverterHandler(MACConverterHandler):
    """
    Handles OUI addresses (first 24 bits of a MAC address) in **dashed hexadecimal format**
    (e.g., `"AA-BB-CC"`).

    This handler validates whether the request is a **6-character hexadecimal** string
    (ignoring dashes). If valid, it converts it into a **3-byte OUI sequence** and
    appends three `\x00` bytes.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes dashed hexadecimal OUI addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a dashed hex string into a 3-byte OUI sequence padded to 6 bytes.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('-', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a dashed hexadecimal OUI into a 6-byte MAC address.

        Args:
            request (str): An OUI in "AA-BB-CC" format.

        Returns:
            bytes: The 3-byte OUI sequence padded with three `\x00` bytes.
        """
        raw_mac = request.replace('-', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3


class ColonHexOUI24ConverterHandler(MACConverterHandler):
    """
    Handles OUI addresses (first 24 bits of a MAC address) in **colon-separated hexadecimal format**
    (e.g., `"AA:BB:CC"`).

    This handler validates whether the request is a **6-character hexadecimal** string
    (ignoring colons). If valid, it converts it into a **3-byte OUI sequence** and
    appends three `\x00` bytes.

    Methods:
        handle(request: Any, *args, **kwargs):
            Processes colon-separated hexadecimal OUI addresses and converts them to bytes.

        _to_bytes(request: Any) -> bytes:
            Converts a colon-separated hex string into a 3-byte OUI sequence padded to 6 bytes.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace(':', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        """
        Converts a colon-separated hexadecimal OUI into a 6-byte MAC address.

        Args:
            request (str): An OUI in "AA:BB:CC" format.

        Returns:
            bytes: The 3-byte OUI sequence padded with three `\x00` bytes.
        """
        raw_mac = request.replace(':', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3


class DotHexOUI24ConverterHandler(MACConverterHandler):
    """
    Handles OUI addresses (first 24 bits of a MAC address) in dot-separated hexadecimal format (e.g., "AABB.CCDD").
    It validates whether the request is a 6-character hexadecimal string (ignoring dots).
    If valid, it converts it into a 3-byte OUI sequence and appends three \x00 bytes.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('.', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace('.', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3


class BytesMAC24ConverterHandler(MACConverterHandler):
    """
    Handles OUI addresses in raw byte format (3-byte sequence).
    It checks if the request is a 3-byte sequence where each byte falls within the valid range (0-255).
    If valid, it pads it to 6 bytes.
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 3 and max(request) <= 255 and min(request) >= 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        return request + b'\x00' * 3


class OctetEUI64ConverterHandler(MACConverterHandler):
    """
    Handles EUI-64 conversion by transforming a 6-byte MAC address into an 8-byte EUI-64 identifier.
    It splits the MAC address into two 3-byte sections, inserts the FFFE in between, and returns the 8-byte result.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 6:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        left_binary_digits = request[0:3]
        right_binary_digits = request[3:]
        return b''.join([left_binary_digits, b'\xFF\xFE', right_binary_digits])


class MACConverter:
    """
    A static utility class for converting MAC addresses and OUI prefixes into bytes using the Chain of Responsibility pattern.
    """
    @staticmethod
    def convert_mac(mac: Any, converters: List[MACConverterHandler] = None) -> bytes:
        """
        Converts a MAC address into a 6-byte sequence, processing different formats such as binary, hexadecimal (dashed, colon, dot), decimal, and raw bytes.
        """
        if converters is None:
            converters = [
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                DecimalMAC48ConverterHandler(),
                BytesMAC48ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_oui(mac: Any, converters: List[MACConverterHandler] = None) -> bytes:
        """
        Converts an OUI (Organizationally Unique Identifier) into a 6-byte sequence, supporting multiple formats and ensuring consistency.
        """
        if converters is None:
            converters = [
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                DecimalMAC48ConverterHandler(),
                BytesMAC48ConverterHandler(),
                BinaryDigitsOUI24ConverterHandler(),
                DashedHexOUI24ConverterHandler(),
                ColonHexOUI24ConverterHandler(),
                DotHexOUI24ConverterHandler(),
                BytesMAC24ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_to_eui64(mac: Any) -> Union[bytes, None]:
        """
        Converts a MAC-48 address into an EUI-64 identifier, adding the FFFE insertion in the middle.
        """
        mac_address = MACConverter.convert_mac(mac)
        if mac_address is not None:
            converter_handler = OctetEUI64ConverterHandler()
            return converter_handler.handle(mac_address)
        return None
