import ipaddress
import re
from abc import abstractmethod
from typing import Any, List

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class IPConverterHandler(SimpleCoRHandler):
    """
    An abstract base class for IP conversion handlers using the Chain of Responsibility (CoR) pattern.
    This class defines a structure for handling IP conversion requests and delegating them to the next handler if unprocessed.

    Methods:
        - handle: Processes the request or passes it to the next handler in the chain.
        - _to_bytes: Converts the input request to its byte representation.
    """
    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Processes the IP conversion request. If the current handler cannot process the request,
        it delegates to the next handler in the chain.

        Parameters:
        request (Any): The input request to handle.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The result of the conversion or the result from the next handler in the chain.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _to_bytes(self, request: Any) -> bytes:
        """
        Abstract method to convert the input request to a byte representation.

        Parameters:
        request (Any): The input IP address to convert.

        Returns:
        bytes: The byte representation of the IP address. It's in big-endian order.

        Raises:
        Implemented in subclasses: Subclasses must provide specific logic for converting an IP address to bytes.
        """
        pass

class BytesIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from bytes.
    This class specifically processes requests where the input is a 4-byte representation of an IPv4 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 4:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        bytes_list = [
            NumeralConverter.decimal_to_bytes(octet, 1)
            for octet in request
        ]
        return b''.join(bytes_list)

class BinaryDigitsIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from binary digits.
    This class specifically processes requests where the input is a list of 32 binary digits representing an IPv4 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 32:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: list[int]) -> bytes:
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 4)

class BinaryStringIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from binary string.
    This class specifically processes requests where the input is a string of 32 binary digits representing an IPv4 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.search(r'^[01]{32}$', request):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        return NumeralConverter.binary_to_bytes(request, 4)

class CIDRIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from CIDR notation.
    This class specifically processes requests where the input is a string in CIDR notation (e.g., "/24").
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.search(r'^/(3[0-2]|[12]?[0-9])$', request):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        mask_match = re.search(r'^/(\d+)$', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
        return NumeralConverter.binary_to_bytes(binary_string, 4)

class DotIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from dot-decimal notation.
    This class specifically processes requests where the input is a string in dot-decimal notation (e.g., "192.168.1.1").
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.search(
            r'^(0*(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))\.'
            r'(0*(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))\.'
            r'(0*(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))\.'
            r'(0*(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))$',
            request):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        bytes_list = [
            NumeralConverter.decimal_to_bytes(int(octet), 1)
            for octet in request.split('.')
        ]
        return b''.join(bytes_list)

class DecimalIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv4 address conversions from decimal.
    This class processes requests where the input is an integer representing an IPv4 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, int) and request.bit_length() <= 32:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: int) -> bytes:
        bytes_list = [
            NumeralConverter.decimal_to_bytes((request >> (24 - 8 * i)) & 0xFF, 1)
            for i in range(4)
        ]
        return b''.join(bytes_list)


class BytesIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from bytes.
    This class specifically processes requests where the input is a 16-byte representation of an IPv6 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 16:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        bytes_list = [
            NumeralConverter.decimal_to_bytes(octet, 1)
            for octet in request
        ]
        return b''.join(bytes_list)

class BinaryDigitsIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from binary digits.
    This class specifically processes requests where the input is a list of 128 binary digits representing an IPv6 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 128:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 16)

class BinaryStringIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from binary string.
    This class specifically processes requests where the input is a string of 128 binary digits representing an IPv6 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.search(r'^[01]{128}$', request):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        return NumeralConverter.binary_to_bytes(request, 16)

class CIDRIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from CIDR notation.
    This class specifically processes requests where the input is a string in CIDR notation (e.g., "/64").
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.search(r'^/(12[0-8]|1[01][0-9]|[1-9]?[0-9])$', request):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        mask_match = re.search(r'^/(\d+)$', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
        return NumeralConverter.binary_to_bytes(binary_string, 16)

class ColonIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from colon-hexadecimal notation.
    This class specifically processes requests where the input is a string in colon-hexadecimal notation (e.g., "2001:db8::1").
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str):
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: str) -> bytes:
        ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
        octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
        return b''.join([NumeralConverter.hexadecimal_to_bytes(octet, 1) for octet in octets])

class DecimalIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of IPConverterHandler to handle IPv6 address conversions from decimal.
    This class processes requests where the input is an integer representing an IPv6 address.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, int) and request.bit_length() <= 128:
            try:
                return self._to_bytes(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: int) -> bytes:
        bytes_list = [
            NumeralConverter.decimal_to_bytes((request >> (120 - 8 * i)) & 0xFF, 1)
            for i in range(16)
        ]
        return b''.join(bytes_list)


class IPConverter:
    """
    A utility class to handle the conversion of IP addresses to their byte representations.
    This class uses a chain of responsibility pattern, leveraging multiple handlers to process requests.

    Methods:
        - convert_to_ipv4_bytes: Converts IPv4 address representations to bytes.
        - convert_to_ipv6_bytes: Converts IPv6 address representations to bytes.
    """
    @staticmethod
    def convert_to_ipv4_bytes(request_format: Any, converters: List[IPConverterHandler] = None) -> bytes:
        """
        Converts various IPv4 address formats into their byte representation.
        Utilizes a chain of responsibility pattern with predefined handlers to process different formats.

        Parameters:
        request_format (Any): The IPv4 address to convert. Supported formats include bytes, binary digits,
                              CIDR notation, dotted-decimal, and decimal representations.
        converters (List[IPConverterHandler], optional): A custom list of IPv4 conversion handlers.
                                                         Defaults to a standard set of handlers.

        Returns:
        bytes: The byte representation of the IPv4 address.

        Example:
        For input '192.168.1.1', the output is b'\xc0\xa8\x01\x01'.
        For input 3232235777, the output is also b'\xc0\xa8\x01\x01'.
        For input '11000000101010000000000100000001', the output is b'\xc0\xa8\x01\x01'.
        For input '/24', the output is b'\xff\xff\xff\x00'.
        For input b'\xc0\xa8\x01\x01', the output is b'\xc0\xa8\x01\x01'.

        Raises:
        Any exceptions raised by the handlers during conversion.
        """
        if converters is None:
            converters = [
                BytesIPv4ConverterHandler(),
                BinaryDigitsIPv4ConverterHandler(),
                BinaryStringIPv4ConverterHandler(),
                CIDRIPv4ConverterHandler(),
                DotIPv4ConverterHandler(),
                DecimalIPv4ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(request_format)

    @staticmethod
    def convert_to_ipv6_bytes(request_format: Any, converters: List[IPConverterHandler] = None) -> bytes:
        """
        Converts various IPv6 address formats into their byte representation.
        Utilizes a chain of responsibility pattern with predefined handlers to process different formats.

        Parameters:
        request_format (Any): The IPv6 address to convert. Supported formats include bytes, binary digits,
                              CIDR notation, colon-hexadecimal, and decimal representations.
        converters (List[IPConverterHandler], optional): A custom list of IPv6 conversion handlers.
                                                         Defaults to a standard set of handlers.

        Returns:
        bytes: The byte representation of the IPv6 address.

        Example:
        For input '2001:db8::1', the output is b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'.
        For input 42540766452641154071740215577757643572, the output is the same byte sequence.
        Other supported formats include binary digits, CIDR notation, and decimal representations are also supported like `convert_to_ipv4_bytes`.

        Raises:
        Any exceptions raised by the handlers during conversion.
        """
        if converters is None:
            converters = [
                BytesIPv6ConverterHandler(),
                BinaryDigitsIPv6ConverterHandler(),
                BinaryStringIPv6ConverterHandler(),
                CIDRIPv6ConverterHandler(),
                ColonIPv6ConverterHandler(),
                DecimalIPv6ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(request_format)