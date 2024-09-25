from __future__ import annotations

import ipaddress
import re
from abc import abstractmethod
from enum import Enum
from typing import Any, List, Union, Dict

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.design_template.cor import BidirectionalCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class IPType(Enum):
    """Enumeration for different IP types with methods for validation and retrieval."""
    IPv4 = 4
    IPv6 = 16

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """Check if the provided value is a valid member of the enumeration."""
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """Retrieve a dictionary mapping of the enumeration members and their values."""
        return cls._value2member_map_


class IPTypeClassifierHandler(BidirectionalCoRHandler):
    """
    Abstract handler class for classifying IP types in a chain of responsibility.
    Inherits from the BidirectionalCoRHandler and defines a method for handling IP requests.
    This class is part of the Chain of Responsibility pattern and allows for passing the request to the next handler if needed.
    """

    @abstractmethod
    def handle(self, request: List[Octet]):
        """
        Handles the request to classify IP types. If the current handler cannot process the request,
        it passes the request to the next handler in the chain, if one exists.

        Parameters:
        request (List[Octet]): A list of octets representing an IP address.

        Returns:
        Any: The result of the next handler in the chain if the current handler cannot handle the request.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler


class IPv4IPTypeClassifierHandler(IPTypeClassifierHandler):
    """
    Abstract handler class for classifying IPv4 IP types. Inherits from IPTypeClassifierHandler.
    This class contains the core logic to validate whether a request is an IPv4 address but leaves specific handling
    to its subclasses.
    """

    @abstractmethod
    def handle(self, request: Any):
        """
        Handles the request by validating it and, if necessary, passing it to the next handler.
        This method must be implemented by concrete subclasses.

        Parameters:
        request (Any): The request to handle, can be any type but typically expected to be an IP in some form.

        Returns:
        Any: The result of the next handler or the classified IP type.
        """
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the provided request consists of exactly 4 octets, corresponding to an IPv4 address.

        Parameters:
        request (List[Octet]): A list of octets representing an IP address.

        Returns:
        bool: True if the request is a valid IPv4 address (4 octets), otherwise False.
        """
        octet_count = len(request)
        if octet_count != 4:
            return False
        return True


class OctetIPv4IPTypeClassifierHandler(IPv4IPTypeClassifierHandler):
    """
    Concrete handler class that classifies an IP as IPv4 based on the number of octets.
    If the request consists of 4 octets, it classifies the IP as IPv4. Otherwise, it passes the request to the next handler.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as an IPv4 IP type if it consists of 4 octets.
        If the request cannot be classified, it passes it to the next handler in the chain.

        Parameters:
        request (Any): The request to handle, typically a list of octets representing an IP address.

        Returns:
        IPType: IPType.IPv4 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, list) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the request is a valid IPv4 address by checking that it consists of 4 octets.
        This method extends the validation logic from the superclass.

        Parameters:
        request (List[Octet]): A list of octets representing an IP address.

        Returns:
        bool: True if the request is valid, False otherwise.
        """
        return super()._validate(request)


class DotIPv4IPTypeClassifierHandler(IPv4IPTypeClassifierHandler):
    """
    Concrete handler class that classifies an IP as IPv4 based on its dotted-decimal string format.
    If the request is a valid dotted-decimal IPv4 string, it classifies the IP as IPv4.
    Otherwise, it passes the request to the next handler in the chain.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as an IPv4 IP type if it is a valid dotted-decimal string.
        If the request cannot be classified, it passes it to the next handler in the chain.

        Parameters:
        request (Any): The request to handle, typically a string in the format "x.x.x.x", where x is a decimal number.

        Returns:
        IPType: IPType.IPv4 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: str) -> bool:
        """
        Validates whether the provided request is a valid dotted-decimal IPv4 address.

        The validation involves:
        1. Splitting the string by periods ('.') to get individual octet values.
        2. Converting each octet to a binary representation using the NumeralConverter class.
        3. Ensuring the address consists of exactly 4 octets, which is validated by the parent class.

        Parameters:
        request (str): A string representing an IP address in dotted-decimal format.

        Returns:
        bool: True if the request is a valid IPv4 address, otherwise False.
        """
        try:
            address = [
                OctetFlyWeightFactory.get_octet(NumeralConverter.decimal_to_binary(octet_decimal))
                for octet_decimal in map(int, request.split('.'))
            ]
            return super()._validate(address)
        except (ValueError, TypeError):
            return False


class IPv4NetmaskClassifierHandler(IPTypeClassifierHandler):
    """
    Abstract handler class for classifying IPv4 netmasks. It provides core validation logic for netmask patterns,
    specifically checking if the binary representation of the netmask contains only contiguous 1s followed by 0s.
    Subclasses implement specific handling logic.
    """

    @abstractmethod
    def handle(self, request: Any):
        """
        Handles the request by passing it to the next handler if necessary. Must be implemented by subclasses.

        Parameters:
        request (Any): The request to handle, which could be in various formats (list of octets, string, etc.).

        Returns:
        Any: The result from the next handler if the current handler cannot process the request.
        """
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the provided request is a valid IPv4 netmask.

        The netmask is considered valid if:
        1. It contains exactly 4 octets.
        2. The binary representation consists of contiguous 1s followed by 0s (e.g., 255.255.255.0).

        Parameters:
        request (List[Octet]): A list of octets representing the netmask.

        Returns:
        bool: True if the request is a valid IPv4 netmask, False otherwise.
        """
        octet_count = len(request)
        if octet_count != 4:
            return False
        binary_digits = []
        for octet in request:
            binary_digits.extend(octet.binary_digits)
        if re.search('^1*0*$', ''.join(map(str, binary_digits))) is None:
            return False
        return True


class OctetIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    Concrete handler class that classifies a netmask represented as a list of octets. If the request is valid,
    it classifies the netmask as IPv4; otherwise, it passes the request to the next handler.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as IPv4 if it is a valid list of octets representing a netmask.

        Parameters:
        request (Any): A list of octets representing a netmask.

        Returns:
        IPType: IPType.IPv4 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, list) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the request is a valid IPv4 netmask based on the octet list.
        It uses the validation logic from the superclass.

        Parameters:
        request (List[Octet]): A list of octets representing the netmask.

        Returns:
        bool: True if the netmask is valid, False otherwise.
        """
        return super()._validate(request)


class DotIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    Concrete handler class that classifies a netmask represented as a dotted-decimal string.
    If the request is valid, it classifies the netmask as IPv4; otherwise, it passes the request to the next handler.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as IPv4 if it is a valid dotted-decimal string representing a netmask.

        Parameters:
        request (Any): A string in dotted-decimal format representing a netmask (e.g., "255.255.255.0").

        Returns:
        IPType: IPType.IPv4 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: str) -> bool:
        """
        Validates whether the request is a valid dotted-decimal IPv4 netmask.

        The validation involves:
        1. Splitting the string by periods ('.') to get individual octet values.
        2. Converting each octet to its binary representation using the NumeralConverter class.
        3. Ensuring the address is a valid IPv4 netmask.

        Parameters:
        request (str): A string representing a netmask in dotted-decimal format.

        Returns:
        bool: True if the request is a valid IPv4 netmask, otherwise False.
        """
        try:
            address = [
                OctetFlyWeightFactory.get_octet(NumeralConverter.decimal_to_binary(octet_decimal))
                for octet_decimal in map(int, request.split('.'))
            ]
            return super()._validate(address)
        except (ValueError, TypeError):
            return False


class CIDRIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    Concrete handler class that classifies a netmask represented in CIDR notation (e.g., "/24").
    If the request is valid, it classifies the netmask as IPv4; otherwise, it passes the request to the next handler.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as IPv4 if it is a valid CIDR string representing a netmask.

        Parameters:
        request (Any): A string in CIDR format representing a netmask (e.g., "/24").

        Returns:
        IPType: IPType.IPv4 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: str) -> bool:
        """
        Validates whether the request is a valid IPv4 netmask in CIDR notation.

        The validation involves:
        1. Extracting the number of bits from the CIDR notation (e.g., "/24").
        2. Creating a binary string with the corresponding number of 1s followed by 0s.
        3. Ensuring the resulting binary representation is valid for an IPv4 netmask.

        Parameters:
        request (str): A string representing a netmask in CIDR format.

        Returns:
        bool: True if the request is a valid IPv4 netmask, otherwise False.
        """
        try:
            mask_match = re.search(r'^/(\d+)$', request)
            if mask_match is not None:
                if 32 >= int(mask_match.group(1)) >= 0:
                    binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
                    address = [
                        OctetFlyWeightFactory.get_octet(binary_string[index: index + 8])
                        for index in range(0, len(binary_string), 8)
                    ]
                    return super()._validate(address)
            return False
        except (ValueError, TypeError):
            return False


class IPv6IPTypeClassifierHandler(IPTypeClassifierHandler):
    """
    Abstract handler class for classifying IPv6 IP types.
    This class contains the core validation logic for determining if a request is a valid IPv6 address
    based on the number of octets (16 for IPv6).
    Subclasses implement the specific handling and validation logic.
    """

    @abstractmethod
    def handle(self, request: Any):
        """
        Handles the request to classify an IP address as IPv6. If the request cannot be classified,
        it passes it to the next handler in the chain.

        Parameters:
        request (Any): The request to handle, typically a list of octets or a string representation of an IP address.

        Returns:
        Any: The result from the next handler or the classified IP type (IPv6).
        """
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the provided request is a valid IPv6 address by checking that it contains exactly 16 octets.

        Parameters:
        request (List[Octet]): A list of octets representing an IP address.

        Returns:
        bool: True if the request contains 16 octets (valid IPv6 address), otherwise False.
        """
        octet_count = len(request)
        if octet_count != 16:
            return False
        return True


class OctetIPv6IPTypeClassifierHandler(IPv6IPTypeClassifierHandler):
    """
    Concrete handler class that classifies an IP address as IPv6 when provided as a list of octets.
    If the request contains 16 octets, it classifies the address as IPv6.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as IPv6 if it is a valid list of octets representing an IPv6 address.

        Parameters:
        request (Any): A list of octets representing an IPv6 address.

        Returns:
        IPType: IPType.IPv6 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, list) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the request is a valid IPv6 address based on the number of octets.

        Parameters:
        request (List[Octet]): A list of octets representing the IPv6 address.

        Returns:
        bool: True if the request contains 16 octets, otherwise False.
        """
        return super()._validate(request)


class ColonIPv6IPTypeClassifierHandler(IPv6IPTypeClassifierHandler):
    """
    Concrete handler class that classifies an IP address as IPv6 when provided in colon-hexadecimal notation (e.g., "2001:0db8::1").
    If the request is a valid IPv6 string, it classifies the address as IPv6.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as IPv6 if it is a valid colon-hexadecimal string representing an IPv6 address.

        Parameters:
        request (Any): A string representing an IPv6 address in colon-hexadecimal format.

        Returns:
        IPType: IPType.IPv6 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        """
        Validates whether the request is a valid IPv6 address in colon-hexadecimal notation.

        The validation involves:
        1. Expanding the IPv6 string to its full form (e.g., "2001:0db8::1" becomes "2001:0db8:0000:0000:0000:0000:0000:0001").
        2. Splitting the full string into octets, and converting each octet from hexadecimal to binary.
        3. Ensuring the resulting address is a valid IPv6 address with 16 octets.

        Parameters:
        request (str): A string representing an IPv6 address in colon-hexadecimal format.

        Returns:
        bool: True if the request is a valid IPv6 address, otherwise False.
        """
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            address = [
                OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(octet))
                for octet in octets
            ]
            return super()._validate(address)
        except (ValueError, TypeError):
            return False


class IPv6NetmaskClassifierHandler(IPTypeClassifierHandler):
    """
    Abstract handler class for classifying IPv6 netmasks. This class provides the core logic to validate IPv6 netmasks
    by ensuring that the binary representation consists of contiguous 1s followed by 0s.
    Subclasses must implement specific request handling logic.
    """

    @abstractmethod
    def handle(self, request: Any):
        """
        Handles the request to classify an IPv6 netmask. If the request cannot be classified,
        it is passed to the next handler in the chain.

        Parameters:
        request (Any): The request to handle, typically a list of octets or a string representation of a netmask.

        Returns:
        Any: The result from the next handler or the classified IP type (IPv6).
        """
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: List[Octet]) -> bool:
        """
        Validates whether the provided request is a valid IPv6 netmask by ensuring that it consists of 16 octets and
        that the binary representation is made up of contiguous 1s followed by 0s.

        Parameters:
        request (List[Octet]): A list of octets representing the netmask.

        Returns:
        bool: True if the request is a valid IPv6 netmask, otherwise False.
        """
        octet_count = len(request)
        if octet_count != 16:
            return False
        binary_digits = []
        for octet in request:
            binary_digits.extend(octet.binary_digits)
        if re.search('^1*0*$', ''.join(map(str, binary_digits))) is None:
            return False
        return True


class OctetIPv6NetmaskClassifierHandler(IPv6NetmaskClassifierHandler):
    """
    Concrete handler class for classifying IPv6 netmasks represented as a list of octets.
    If the request contains 16 valid octets, it classifies the netmask as IPv6.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as an IPv6 netmask if the request is a valid list of octets.

        Parameters:
        request (Any): A list of octets representing the IPv6 netmask.

        Returns:
        IPType: IPType.IPv6 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, list) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        """
        Validates whether the request is a valid IPv6 netmask based on the octet list.

        Parameters:
        request (Any): A list of octets representing the IPv6 netmask.

        Returns:
        bool: True if the request is valid, otherwise False.
        """
        return super()._validate(request)


class ColonIPv6NetmaskClassifierHandler(IPv6NetmaskClassifierHandler):
    """
    Concrete handler class for classifying IPv6 netmasks represented in colon-hexadecimal notation (e.g., "ffff:ffff::").
    If the request is a valid colon-hexadecimal string, it classifies the netmask as IPv6.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as an IPv6 netmask if the request is a valid colon-hexadecimal string.

        Parameters:
        request (Any): A string representing an IPv6 netmask in colon-hexadecimal format.

        Returns:
        IPType: IPType.IPv6 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        """
        Validates whether the request is a valid IPv6 netmask in colon-hexadecimal notation.

        The validation involves:
        1. Expanding the IPv6 string to its full form (e.g., "ffff:ffff::" becomes "ffff:ffff:0000:0000:0000:0000:0000:0000").
        2. Splitting the full string into octets, and converting each octet from hexadecimal to binary.
        3. Ensuring the resulting address is a valid IPv6 netmask.

        Parameters:
        request (str): A string representing the IPv6 netmask in colon-hexadecimal format.

        Returns:
        bool: True if the request is valid, otherwise False.
        """
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            address = [
                OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(octet))
                for octet in octets
            ]
            return super()._validate(address)
        except (ValueError, TypeError):
            return False


class CIDRIPv6NetmaskClassifierHandler(IPv6NetmaskClassifierHandler):
    """
    Concrete handler class that classifies an IPv6 netmask represented in CIDR notation (e.g., "/64").
    If the request is valid CIDR notation, it classifies the netmask as IPv6; otherwise, it passes the request
    to the next handler in the chain.
    """

    def handle(self, request: Any):
        """
        Handles the request and classifies it as an IPv6 netmask if the request is a valid CIDR notation string.

        Parameters:
        request (Any): A string representing the netmask in CIDR notation (e.g., "/64").

        Returns:
        IPType: IPType.IPv6 if the request is valid, otherwise the result from the next handler.
        """
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        """
        Validates whether the request is a valid IPv6 netmask in CIDR notation.

        The validation involves:
        1. Extracting the CIDR number (e.g., "/64").
        2. Generating a binary string with the corresponding number of 1s followed by 0s (up to 128 bits).
        3. Converting the binary string to octets and validating the resulting IPv6 netmask.

        Parameters:
        request (str): A string representing the IPv6 netmask in CIDR format.

        Returns:
        bool: True if the request is a valid IPv6 netmask, otherwise False.
        """
        try:
            mask_match = re.search(r'^/(\d+)$', request)
            if mask_match is not None:
                if 128 >= int(mask_match.group(1)) >= 0:
                    binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
                    address = [
                        OctetFlyWeightFactory.get_octet(binary_string[index: index + 8])
                        for index in range(0, len(binary_string), 8)
                    ]
                    return super()._validate(address)
            return False
        except (ValueError, TypeError):
            return False


class IPTypeClassifier:
    """
    A utility class that classifies IP addresses and netmasks for both IPv4 and IPv6 using the Chain of Responsibility (CoR) pattern.
    It provides static methods to classify addresses and netmasks based on the input format, applying a sequence of handler classifiers.
    """

    @staticmethod
    def classify_ipv4_address(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv4 address using the provided classifiers or a default list if none are given.

        Parameters:
        request_format (Any): The IP address to classify, which can be in different formats (list of octets or string).
        classifiers (List[IPTypeClassifierHandler], optional): A list of classifiers to apply for IPv4 address classification.

        Returns:
        Union[IPType, None]: The IP type if classified successfully, otherwise None.
        """
        if classifiers is None:
            classifiers = [
                OctetIPv4IPTypeClassifierHandler(),
                DotIPv4IPTypeClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv4_netmask(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv4 netmask using the provided classifiers or a default list if none are given.

        Parameters:
        request_format (Any): The netmask to classify, which can be in different formats (list of octets, CIDR notation, or string).
        classifiers (List[IPTypeClassifierHandler], optional): A list of classifiers to apply for IPv4 netmask classification.

        Returns:
        Union[IPType, None]: The IP type if classified successfully, otherwise None.
        """
        if classifiers is None:
            classifiers = [
                OctetIPv4NetmaskClassifierHandler(),
                DotIPv4NetmaskClassifierHandler(),
                CIDRIPv4NetmaskClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv6_address(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv6 address using the provided classifiers or a default list if none are given.

        Parameters:
        request_format (Any): The IP address to classify, which can be in different formats (list of octets or string).
        classifiers (List[IPTypeClassifierHandler], optional): A list of classifiers to apply for IPv6 address classification.

        Returns:
        Union[IPType, None]: The IP type if classified successfully, otherwise None.
        """
        if classifiers is None:
            classifiers = [
                OctetIPv6IPTypeClassifierHandler(),
                ColonIPv6IPTypeClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv6_netmask(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv6 netmask using the provided classifiers or a default list if none are given.

        Parameters:
        request_format (Any): The netmask to classify, which can be in different formats (list of octets, CIDR notation, or string).
        classifiers (List[IPTypeClassifierHandler], optional): A list of classifiers to apply for IPv6 netmask classification.

        Returns:
        Union[IPType, None]: The IP type if classified successfully, otherwise None.
        """
        if classifiers is None:
            classifiers = [
                OctetIPv6NetmaskClassifierHandler(),
                ColonIPv6NetmaskClassifierHandler(),
                CIDRIPv6NetmaskClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ip(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IP address, either IPv4 or IPv6, using the provided classifiers or a default list if none are given.

        Parameters:
        request_format (Any): The IP address to classify, which can be in different formats (list of octets, string, etc.).
        classifiers (List[IPTypeClassifierHandler], optional): A list of classifiers to apply for IP classification.

        Returns:
        Union[IPType, None]: The IP type if classified successfully, otherwise None.
        """
        if classifiers is None:
            classifiers = [
                OctetIPv4IPTypeClassifierHandler(),
                DotIPv4IPTypeClassifierHandler(),
                OctetIPv6IPTypeClassifierHandler(),
                ColonIPv6IPTypeClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)
