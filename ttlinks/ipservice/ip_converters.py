import ipaddress
import re
from abc import abstractmethod
from typing import Any, List, Union

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class IPConverterHandler(SimpleCoRHandler):
    """
    Abstract base class for handling IP conversion requests in a chain-of-responsibility pattern.
    It provides a mechanism to pass requests down a chain of handlers and defines the structure for converting IP components to octets.

    Parameters:
    request (Any): The incoming request to be handled, which could represent an IP address or similar data.

    Returns:
    The result of the next handler in the chain if it exists, otherwise returns None.
    """

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Handles the request. If the current handler cannot process the request,
        it passes the request to the next handler in the chain (if any).

        Parameters:
        request (Any): The incoming request to be handled.

        Returns:
        The processed result from the next handler, if available; otherwise, returns None.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _to_octets(self, request: Any) -> List[Octet]:
        """
        Abstract method that should be implemented to convert the incoming request (IP address or components)
        into a list of octets.

        Parameters:
        request (Any): The IP-related data to convert into octet format.

        Returns:
        A list of octets representing the converted form of the request.
        """
        pass


class OctetIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete implementation of the IPConverterHandler for handling IPv4 addresses.
    It checks if the incoming request is a list of 4 octets (as expected for IPv4) and converts them using the _to_octets method.

    Parameters:
    request (Any): The incoming request, expected to be a list of 4 octets for IPv4.

    Returns:
    A list of octets if the request is valid; otherwise passes the request to the next handler in the chain.
    """

    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Handles the request by checking if it's a valid list of 4 octets for an IPv4 address.
        If valid, it converts the request to a list of octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a list of 4 octets for an IPv4 address.

        Returns:
        A list of octets if the request is valid; otherwise, the result from the next handler.
        """
        if isinstance(request, list) and len(request) == 4 and all(isinstance(octet, Octet) for octet in request):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: List[Octet]) -> List[Octet]:
        """
        Converts the provided list of octets (IPv4) into its desired octet format.
        In this case, the method assumes the request is already in the correct format and returns it unchanged.

        Parameters:
        request (List[Octet]): The list of 4 octets representing the IPv4 address.

        Returns:
        The same list of octets, assuming it is already in the correct format.
        """
        return request


class BinaryDigitsIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes binary digit representations of IPv4 addresses.
    It expects the request to be a list of 32 integers representing the binary digits of an IPv4 address.

    Parameters:
    request (Any): The incoming request, expected to be a list of 32 integers (0s and 1s) representing binary digits of an IPv4 address.

    Returns:
    A list of Octet objects created from the binary digits if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a list of 32 integers representing the binary digits of an IPv4 address.
        If valid, it converts the binary digits to octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a list of 32 integers.

        Returns:
        A list of octets created from the binary digits if the request is valid; otherwise, the result from the next handler.
        """
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 32:
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: list[int]) -> List[Octet]:
        """
        Converts a list of 32 binary digits (integers) into a list of 4 octets by grouping every 8 bits.
        Each group of 8 bits is treated as a binary string and converted into an octet via the OctetFlyWeightFactory.

        Parameters:
        request (list[int]): A list of 32 integers representing binary digits (0 or 1) of an IPv4 address.

        Returns:
        A list of Octet objects created from the binary digits.
        """
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            OctetFlyWeightFactory.get_octet(binary_string)
            for binary_string in binary_string_list
        ]


class CIDRIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes CIDR notation of IPv4 addresses.
    It expects the request to be a CIDR string in the format '/X', where X is a number representing the subnet mask length.

    Parameters:
    request (Any): The incoming request, expected to be a string in CIDR format (e.g., '/24').

    Returns:
    A list of Octet objects representing the subnet mask if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid CIDR string (e.g., '/24').
        If valid, it converts the CIDR notation into octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a CIDR string in the form '/X'.

        Returns:
        A list of octets representing the subnet mask if the request is valid; otherwise, the result from the next handler.
        """
        if isinstance(request, str) and re.search(r'^/(\d+)$', request):
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: str) -> List[Octet]:
        """
        Converts a CIDR string (e.g., '/24') into a subnet mask represented by octets.
        It generates a binary string with the specified number of '1's followed by '0's to make up 32 bits,
        and then divides it into octets using the OctetFlyWeightFactory.

        Parameters:
        request (str): A string in CIDR format (e.g., '/24'), representing the subnet mask.

        Returns:
        A list of Octet objects representing the subnet mask.
        """
        mask_match = re.search(r'^/(\d+)$', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
        address = [
            OctetFlyWeightFactory.get_octet(binary_string[index: index + 8])
            for index in range(0, len(binary_string), 8)
        ]
        return address


class DotIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv4 addresses in dotted decimal notation (e.g., '192.168.0.1').
    It expects the request to be a string representing an IPv4 address in the standard format with four decimal octets.

    Parameters:
    request (Any): The incoming request, expected to be a string in dotted decimal format (e.g., '192.168.0.1').

    Returns:
    A list of Octet objects if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid IPv4 address in dotted decimal notation.
        If valid, it converts the address to a list of octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a string representing an IPv4 address in dotted decimal notation.

        Returns:
        A list of octets representing the binary form of the address if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, str) and re.search(r'^\d+\.\d+\.\d+.\d+$', request):
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: str) -> List[Octet]:
        """
        Converts an IPv4 address in dotted decimal notation into a list of octets.
        Each octet in the address is converted from its decimal form into binary, and then the binary is converted to an Octet object.

        Parameters:
        request (str): A string representing the IPv4 address in dotted decimal format (e.g., '192.168.0.1').

        Returns:
        A list of Octet objects representing the binary form of the IPv4 address.
        """
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.decimal_to_binary(octet_decimal))
            for octet_decimal in map(int, request.split('.'))
        ]

class DecimalIPv4ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv4 addresses in decimal notation (e.g., 3232235520).
    It expects the request to be an integer representing an IPv4 address in its 32-bit decimal form.

    This handler is responsible for:
    - Validating the incoming request to ensure it is a valid integer representing a 32-bit IPv4 address.
    - If valid, it converts the integer into four octets, each representing one part of the IPv4 address.
    - The integer is bitwise shifted and masked to extract each octet, which is then converted to its binary representation and
      encapsulated in an Octet object using the OctetFlyWeightFactory.
    - If the request is invalid, it passes the request to the next handler in the chain.

    Parameters:
    request (Any): The incoming request, expected to be an integer representing a 32-bit IPv4 address.

    Returns:
    A list of Octet objects if the request is valid; otherwise, the request is passed to the next handler.
    """
    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid integer representing a 32-bit IPv4 address.
        If valid, it converts the address to a list of octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be an integer representing a 32-bit IPv4 address.

        Returns:
        A list of octets representing the binary form of the IPv4 address if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, int) and request.bit_length() <= 32:
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: int) -> List[Octet]:
        """
        Converts an integer representing a 32-bit IPv4 address into a list of octets.
        The integer is split into four octets by bitwise shifting and masking operations.
        Each octet is then converted from its decimal form into binary and encapsulated in an Octet object.

        Parameters:
        request (int): An integer representing a 32-bit IPv4 address.

        Returns:
        A list of Octet objects representing the binary form of the IPv4 address.
        """
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.decimal_to_binary((request >> (24 - 8 * i)) & 0xFF))
            for i in range(4)
        ]


class OctetIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv6 addresses represented as a list of 16 octets.
    It expects the request to be a list of 16 octets, which is the standard size for IPv6 addresses.

    Parameters:
    request (Any): The incoming request, expected to be a list of 16 octets representing an IPv6 address.

    Returns:
    The list of octets if the request is valid; otherwise, the request is passed to the next handler in the chain.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid list of 16 octets for an IPv6 address.
        If valid, it returns the request directly (assuming it's already in the correct format).
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a list of 16 octets representing an IPv6 address.

        Returns:
        The list of octets if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, list) and len(request) == 16 and all(isinstance(octet, Octet) for octet in request):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        """
        Returns the provided list of 16 octets, assuming the request is already in the correct format.
        For IPv6 addresses, the request is expected to already be a list of octets.

        Parameters:
        request (Any): A list of 16 octets representing an IPv6 address.

        Returns:
        The same list of octets that was passed in.
        """
        return request


class BinaryDigitsIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv6 addresses represented as a list of 128 binary digits.
    It expects the request to be a list of 128 integers (0s and 1s) representing binary digits of an IPv6 address.

    Parameters:
    request (Any): The incoming request, expected to be a list of 128 integers representing the binary form of an IPv6 address.

    Returns:
    A list of Octet objects created from the binary digits if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid list of 128 integers representing the binary digits of an IPv6 address.
        If valid, it converts the binary digits to octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a list of 128 binary digits (0s and 1s).

        Returns:
        A list of octets created from the binary digits if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 128:
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        """
        Converts a list of 128 binary digits (0s and 1s) into a list of octets by grouping every 8 bits.
        Each group of 8 bits is treated as a binary string and converted into an octet via the OctetFlyWeightFactory.

        Parameters:
        request (Any): A list of 128 integers representing binary digits of an IPv6 address.

        Returns:
        A list of Octet objects created from the binary digits.
        """
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            OctetFlyWeightFactory.get_octet(binary_string)
            for binary_string in binary_string_list
        ]


class CIDRIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes CIDR notation for IPv6 addresses.
    It expects the request to be a CIDR string in the format '/X', where X is a number representing the subnet mask length.

    Parameters:
    request (Any): The incoming request, expected to be a string in CIDR format (e.g., '/64').

    Returns:
    A list of Octet objects representing the subnet mask if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid CIDR string (e.g., '/64').
        If valid, it converts the CIDR notation into octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a CIDR string (e.g., '/64').

        Returns:
        A list of octets representing the subnet mask if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, str) and re.search(r'^/(\d+)$', request):
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: str) -> List[Octet]:
        """
        Converts a CIDR string (e.g., '/64') into a subnet mask represented by octets.
        It generates a binary string with the specified number of '1's followed by '0's to make up 128 bits,
        and then divides it into octets using the OctetFlyWeightFactory.

        Parameters:
        request (str): A string in CIDR format (e.g., '/64'), representing the subnet mask.

        Returns:
        A list of Octet objects representing the subnet mask.
        """
        mask_match = re.search(r'^/(\d+)$', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
        address = [
            OctetFlyWeightFactory.get_octet(binary_string[index: index + 8])
            for index in range(0, len(binary_string), 8)
        ]
        return address


class ColonIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv6 addresses in colon-hexadecimal notation (e.g., '2001:0db8:85a3:0000:0000:8a2e:0370:7334').
    It expects the request to be a string representing an IPv6 address in standard colon notation.
    If the conversion fails, the request is passed to the next handler in the chain.

    Parameters:
    request (Any): The incoming request, expected to be a string in colon-hexadecimal format representing an IPv6 address.

    Returns:
    A list of Octet objects if the request is valid; otherwise, the request is passed to the next handler.
    """

    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a string representing an IPv6 address.
        If valid, it converts the IPv6 address to octets using the _to_octets method.
        If the conversion fails, it passes the request to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be a string representing an IPv6 address in colon-hexadecimal notation.

        Returns:
        A list of octets representing the IPv6 address if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, str):
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: str) -> List[Octet]:
        """
        Converts an IPv6 address in colon-hexadecimal notation into a list of octets.
        It uses the ipaddress library to expand the shorthand form of the IPv6 address (if any) and removes colons.
        The hexadecimal octets are then converted into binary, and Octet objects are created using the OctetFlyWeightFactory.

        Parameters:
        request (str): A string representing an IPv6 address in colon-hexadecimal notation.

        Returns:
        A list of Octet objects representing the binary form of the IPv6 address.
        """
        ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
        octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
        address = [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(octet))
            for octet in octets
        ]
        return address

class DecimalIPv6ConverterHandler(IPConverterHandler):
    """
    A concrete handler that processes IPv6 addresses in decimal notation.
    It expects the request to be an integer representing an IPv6 address in its 128-bit decimal form.

    This handler is responsible for:
    - Validating the incoming request to ensure it is a valid integer representing a 128-bit IPv6 address.
    - If valid, it converts the integer into 16 octets, each representing one part of the IPv6 address.
    - The integer is bitwise shifted and masked to extract each octet, which is then converted to its binary representation and
      encapsulated in an Octet object using the OctetFlyWeightFactory.
    - If the request is invalid, it passes the request to the next handler in the chain.

    Parameters:
    request (Any): The incoming request, expected to be an integer representing a 128-bit IPv6 address.

    Returns:
    A list of Octet objects if the request is valid; otherwise, the request is passed to the next handler.
    """
    def handle(self, request: Any, *args, **kwargs):
        """
        Handles the request by checking if it's a valid integer representing a 128-bit IPv6 address.
        If valid, it converts the address to a list of octets using the _to_octets method.
        Otherwise, the request is passed to the next handler in the chain.

        Parameters:
        request (Any): The incoming request, expected to be an integer representing a 128-bit IPv6 address.

        Returns:
        A list of octets representing the binary form of the IPv6 address if valid; otherwise, the result from the next handler.
        """
        if isinstance(request, int) and request.bit_length() <= 128:
            try:
                return self._to_octets(request)
            except (ValueError, TypeError):
                return super().handle(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: int) -> List[Octet]:
        """
        Converts an integer representing a 128-bit IPv6 address into a list of octets.
        The integer is split into 16 octets by bitwise shifting and masking operations.
        Each octet is then converted from its decimal form into binary and encapsulated in an Octet object.

        Parameters:
        request (int): An integer representing a 128-bit IPv6 address.

        Returns:
        A list of Octet objects representing the binary form of the IPv6 address.
        """
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.decimal_to_binary((request >> (120 - 8 * i)) & 0xFF))
            for i in range(16)
        ]



class IPConverter:
    """
    A utility class that provides static methods to convert different IP address formats into octets.
    It uses a chain-of-responsibility pattern, where multiple converter handlers are applied in sequence
    to process and convert IP addresses of various formats (IPv4 or IPv6) into a list of octets.

    Methods:
    - convert_to_ipv4_octet: Converts an IPv4 address from various formats into octets.
    - convert_to_ipv6_octet: Converts an IPv6 address from various formats into octets.
    - convert_to_ip: Converts either an IPv4 or IPv6 address from various formats into octets.
    """
    @staticmethod
    def convert_to_ipv4_octets(request_format: Any, converters: List[IPConverterHandler] = None) -> List[Octet]:
        """
        Converts an IPv4 address from various formats (e.g., dotted decimal, binary digits, CIDR) into a list of octets.
        It applies a series of converter handlers in sequence until one successfully converts the input.

        Parameters:
        request_format (Any): The input representing an IPv4 address, which can be in different formats (dotted decimal, binary, CIDR).
        converters (List[IPConverterHandler], optional): A list of IPConverterHandler instances for handling different IPv4 formats.
                                                         If not provided, a default list of handlers will be used.

        Returns:
        List[Octet]: A list of Octet objects representing the IPv4 address, after conversion from the input format.
        """
        if converters is None:
            converters = [
                OctetIPv4ConverterHandler(),
                BinaryDigitsIPv4ConverterHandler(),
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
    def convert_to_ipv6_octets(request_format: Any, converters: List[IPConverterHandler] = None) -> List[Octet]:
        """
        Converts an IPv6 address from various formats (e.g., colon-hexadecimal, binary digits, CIDR) into a list of octets.
        It applies a series of converter handlers in sequence until one successfully converts the input.

        Parameters:
        request_format (Any): The input representing an IPv6 address, which can be in different formats (colon-hexadecimal, binary, CIDR).
        converters (List[IPConverterHandler], optional): A list of IPConverterHandler instances for handling different IPv6 formats.
                                                         If not provided, a default list of handlers will be used.

        Returns:
        List[Octet]: A list of Octet objects representing the IPv6 address, after conversion from the input format.
        """
        if converters is None:
            converters = [
                OctetIPv6ConverterHandler(),
                BinaryDigitsIPv6ConverterHandler(),
                CIDRIPv6ConverterHandler(),
                ColonIPv6ConverterHandler(),
                DecimalIPv6ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(request_format)

    @staticmethod
    def convert_to_ip_octets(request_format: Any, converters: List[IPConverterHandler] = None) -> List[Octet]:
        """
        Converts either an IPv4 or IPv6 address from various formats into a list of octets.
        It applies a series of converter handlers in sequence until one successfully converts the input, regardless of whether it is IPv4 or IPv6.

        Parameters:
        request_format (Any): The input representing an IP address, which can be in different formats (dotted decimal, binary, CIDR, colon-hexadecimal).
        converters (List[IPConverterHandler], optional): A list of IPConverterHandler instances for handling different IP formats (both IPv4 and IPv6).
                                                         If not provided, a default list of handlers for both IPv4 and IPv6 will be used.

        Returns:
        List[Octet]: A list of Octet objects representing the IP address (either IPv4 or IPv6), after conversion from the input format.
        """
        if converters is None:
            converters = [
                OctetIPv4ConverterHandler(),
                BinaryDigitsIPv4ConverterHandler(),
                DotIPv4ConverterHandler(),
                DecimalIPv4ConverterHandler(),
                OctetIPv6ConverterHandler(),
                BinaryDigitsIPv6ConverterHandler(),
                ColonIPv6ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(request_format)