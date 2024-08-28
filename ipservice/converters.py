import ipaddress
import re
from abc import abstractmethod
from typing import Any, List

from ttlinks.common.base_utils import CoRHandler, BinaryClass, BinaryFlyWeightFactory


class NumeralConverter:
    @staticmethod
    def binary_to_decimal(binary: str) -> int:
        """
        Convert a binary string to its decimal integer representation.
        :param binary: (str). The binary string to convert.
        :return: (int). The decimal representation of the binary string.
        """
        if type(binary) is not str:
            raise TypeError("Binary is not a string.")
        return int(binary, 2)

    @staticmethod
    def decimal_to_binary(decimal: int, r_just: int = 8) -> str:
        """
        Convert a decimal integer to its binary string representation,
        right-justified and padded with zeros to at least `r_just` characters.
        :param decimal: (int). The decimal integer to convert.
        :param r_just: (int). The minimum width of the resulting binary string;
                             defaults to 8 for byte alignment.
        :return: (str). The binary string representation of the decimal.
        """
        if type(decimal) is not int:
            raise TypeError("decimal is not a int.")
        if type(r_just) is not int:
            raise TypeError("r_just is not a int.")
        return bin(decimal)[2:].rjust(r_just, '0')

    @staticmethod
    def binary_to_hexadecimal(binary: str) -> str:
        """
        Convert a binary string to its hexadecimal string representation.
        :param binary: (str). The binary string to convert.
        :return: (str). The uppercase hexadecimal representation of the binary string.
        """
        if type(binary) is not str:
            raise TypeError("binary is not a string.")
        # Convert binary to an integer
        decimal_value = int(binary, 2)
        # Convert the integer to a hexadecimal string, remove the '0x' prefix
        hexadecimal_string = hex(decimal_value)[2:]
        return hexadecimal_string.upper()  # Return the hexadecimal in uppercase

    @staticmethod
    def hexadecimal_to_binary(hexadecimal: str, r_just: int = 8) -> str:
        """
        Convert a hexadecimal string to its binary string representation,
        right-justified and padded with zeros to at least `r_just` characters.
        :param hexadecimal: (str). The hexadecimal string to convert.
        :param r_just: (int). The minimum width of the resulting binary string;
                             defaults to 8 for byte alignment.
        :return: (str). The binary string representation of the hexadecimal.
        """
        if type(hexadecimal) is not str:
            raise TypeError("hexadecimal is not a string.")
        if type(r_just) is not int:
            raise TypeError("r_just is not a int.")
        # Convert hexadecimal to an integer
        decimal_value = int(hexadecimal, 16)
        # Convert the integer to a binary string, remove the '0b' prefix
        binary_string = bin(decimal_value)[2:].rjust(r_just, '0')
        return binary_string


class IPConverterHandler(CoRHandler):
    """
    Abstract base class for IP conversion handlers implementing the Chain of Responsibility pattern.
    It provides a framework for setting the next handler in the chain and abstract methods to process requests.
    """
    _next_handler = None

    def set_next(self, h: CoRHandler) -> CoRHandler:
        """
        Set the next handler in the chain.

        Args:
        h (CoRHandler): An instance of CoRHandler to be the next in the chain.

        Returns:
        CoRHandler: The next handler instance for method chaining.

        Raises:
        TypeError: If the provided handler is not an instance of CoRHandler.
        """
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, request: Any):
        """
        Process the request and pass it to the next handler if it cannot be handled.

        Args:
        request (Any): The request to process.

        Returns:
        Any: The result from processing the request or from the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert the IP address in the request to a list of binary representations.

        Args:
        request (Any): The IP address or part thereof to convert.

        Returns:
        List[BinaryClass]: A list of BinaryClass instances representing the binary format.
        """
        pass


class DotDecimalIPv4ConverterHandler(IPConverterHandler):
    """
    Handler to convert dot-decimal IP addresses to binary classes.
    """

    def handle(self, request: Any):
        """
        Process dot-decimal IP address strings, converting them to binary class lists.

        Args:
        request (Any): The dot-decimal IP address to convert.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, str) and re.search(r'\d+\.\d+\.\d+.\d+', request):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert a dot-decimal IP address into binary classes using a factory for weight sharing.

        Args:
        request (Any): The dot-decimal IP address to convert.

        Returns:
        List[BinaryClass]: Binary representations of each octet.
        """
        return [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.decimal_to_binary(octet))
            for octet in map(int, request.split('.'))
        ]


class CIDRIPv4ConverterHandler(IPConverterHandler):
    """
    Handler to convert CIDR notation IP addresses to binary classes.
    """

    def handle(self, request: Any):
        """
        Process CIDR notation IP address strings, converting them to binary class lists.

        Args:
        request (Any): The CIDR IP address to convert.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, str):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert a CIDR notation IP address into binary classes.

        Args:
        request (Any): The CIDR IP address to convert.

        Returns:
        List[BinaryClass]: Binary representations of the network mask.
        """
        mask_match = re.search(r'/(\d+)', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
        address = [
            BinaryFlyWeightFactory.get_binary_class(binary_string[index: index + 8])
            for index in range(0, len(binary_string), 8)
        ]
        return address


class BinaryIPv4ConverterHandler(IPConverterHandler):
    """
    Handler to directly process lists of binary class instances.
    """

    def handle(self, request: Any):
        """
        Process requests that are already lists of BinaryClass instances.

        Args:
        request (Any): The list of BinaryClass instances.

        Returns:
        Any: The input list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, list):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Directly return the list of binary classes.

        Args:
        request (Any): The list of BinaryClass instances.

        Returns:
        List[BinaryClass]: The input list.
        """
        return request


class BinaryDigitsIPv4ConverterHandler(IPConverterHandler):
    """
    Handler to convert a list of integer digits (0 or 1) representing an IPv4 address into binary classes.
    """

    def handle(self, request: Any):
        """
        Process lists representing IPv4 addresses where each integer represents a binary digit.

        Args:
        request (Any): The list of binary digits representing an IPv4 address.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, list) and all(isinstance(item, int) for item in request):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert the binary digit list into binary classes by grouping them into octets.

        Args:
        request (Any): The list of binary digits.

        Returns:
        List[BinaryClass]: Binary representations grouped into octets.
        """
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            BinaryFlyWeightFactory.get_binary_class(binary_string)
            for binary_string in binary_string_list
        ]


class ColonHexIPv6ConverterHandler(IPConverterHandler):
    """
    Handler to convert IPv6 addresses in colon-separated hexadecimal notation to binary classes.
    """

    def handle(self, request: Any):
        """
        Process IPv6 address strings in colon-separated hexadecimal format, converting them to binary classes.

        Args:
        request (Any): The IPv6 address string in hexadecimal format.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, str):
            try:
                return self.to_binary_class(request)
            except ValueError:
                return super().handle(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert a colon-separated hexadecimal IPv6 address into binary classes.

        Args:
        request (Any): The IPv6 address to convert.

        Returns:
        List[BinaryClass]: Binary representations of each hexadecimal segment.
        """
        ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
        octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
        address = [
            BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(octet))
            for octet in octets
        ]
        return address


class BinaryIPv6ConverterHandler(IPConverterHandler):
    """
    Handler to directly process lists of binary class instances representing an IPv6 address.
    """

    def handle(self, request: Any):
        """
        Process requests that are already lists of BinaryClass instances for IPv6 addresses.

        Args:
        request (Any): The list of BinaryClass instances.

        Returns:
        Any: The input list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, list):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Directly return the list of binary classes for IPv6 addresses.

        Args:
        request (Any): The list of BinaryClass instances.

        Returns:
        List[BinaryClass]: The input list.
        """
        return request


class CIDRIPv6ConverterHandler(IPConverterHandler):
    """
    Handler to convert CIDR notation IPv6 addresses to binary classes.
    """

    def handle(self, request: Any):
        """
        Process CIDR notation IPv6 address strings, converting them to binary class lists.

        Args:
        request (Any): The CIDR IPv6 address to convert.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, str):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert a CIDR notation IPv6 address into binary classes.

        Args:
        request (Any): The CIDR IPv6 address to convert.

        Returns:
        List[BinaryClass]: Binary representations of the network mask.
        """
        mask_match = re.search(r'/(\d+)', request)
        binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
        address = [
            BinaryFlyWeightFactory.get_binary_class(binary_string[index: index + 8])
            for index in range(0, len(binary_string), 8)
        ]
        return address


class BinaryDigitsIPv6ConverterHandler(IPConverterHandler):
    """
    Handler to convert a list of integer digits (0 or 1) representing an IPv6 address into binary classes.
    """

    def handle(self, request: Any):
        """
        Process lists representing IPv6 addresses where each integer represents a binary digit.

        Args:
        request (Any): The list of binary digits representing an IPv6 address.

        Returns:
        Any: A list of BinaryClass instances or forward the request to the next handler.
        """
        if isinstance(request, list) and all(isinstance(item, int) for item in request):
            return self.to_binary_class(request)
        else:
            return super().handle(request)

    def to_binary_class(self, request: Any) -> List[BinaryClass]:
        """
        Convert the binary digit list into binary classes by grouping them into octets.

        Args:
        request (Any): The list of binary digits.

        Returns:
        List[BinaryClass]: Binary representations grouped into octets.
        """
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            BinaryFlyWeightFactory.get_binary_class(binary_string)
            for binary_string in binary_string_list
        ]
