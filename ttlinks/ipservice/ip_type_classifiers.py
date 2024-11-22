from __future__ import annotations

import ipaddress
import re
from abc import abstractmethod
from typing import Any, List, Union

from ttlinks.common.design_template.cor import BidirectionalCoRHandler
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.ipservice.ip_utils import IPType


class IPTypeClassifierHandler(BidirectionalCoRHandler):
    """
    An abstract base class for IP type classification handlers using the Bidirectional Chain of Responsibility (CoR) pattern.
    This class serves as a blueprint for handling IP classification requests and passing them through a chain of handlers.

    Methods:
        - handle: Processes the classification request or delegates it to the next handler in the chain.
    """
    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Processes the IP classification request. If the current handler cannot process the request,
        it delegates to the next handler in the chain.

        Parameters:
        request (Any): The input request to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The result of the classification or the result from the next handler in the chain.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler


class IPv4IPTypeClassifierHandler(IPTypeClassifierHandler):
    """
    A concrete implementation of IPTypeClassifierHandler for classifying IPv4 addresses.
    This class validates and processes IPv4-specific requests in the classification chain.

    Methods:
        - handle: Delegates the request to the base class's handle method.
        - _validate: Validates the input as a valid IPv4 address.
    """

    @abstractmethod
    def _validate(self, request: Any) -> bool:
        """
        Validates the provided input to ensure it is a valid IPv4 address.

        Parameters:
        request (Any): The input request to validate.

        Returns:
        bool: True if the input is a valid IPv4 address, False otherwise.

        Validation Conditions:
        - The input must have exactly 4 octets.
        - Each octet must be an integer between 0 and 32 (inclusive).
        """
        octet_count = len(request)
        if octet_count != 4 and all(32 >= octet >= 0 for octet in request):
            return False
        return True

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        """
        Processes the IPv4 classification request by delegating it to the parent class's handle method.

        Parameters:
        request (Any): The input IP address to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The result of the classification or the result from the next handler in the chain.
        """
        return super().handle(request)


class DotIPv4IPTypeClassifierHandler(IPv4IPTypeClassifierHandler):
    """
    A handler for classifying IPv4 addresses represented in dotted-decimal notation.
    This handler processes requests where the input is a string in the format 'x.x.x.x'.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in map(int, request.split('.'))
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class BytesIPv4IPTypeClassifierHandler(IPv4IPTypeClassifierHandler):
    """
    A handler for classifying IPv4 addresses represented as byte sequences.
    This handler processes requests where the input is a bytes object of length 4.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in request
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class IPv4NetmaskClassifierHandler(IPTypeClassifierHandler):
    """
    A handler for classifying IPv4 netmask addresses.
    This handler ensures the input adheres to the structure and rules of IPv4 netmasks.

    Methods:
        - handle: Processes requests or delegates them to the next handler in the chain.
        - _validate: Ensures the input is a valid IPv4 netmask.
    """

    @abstractmethod
    def _validate(self, request: Any) -> bool:
        """
        Validates the input as a valid IPv4 netmask.

        Parameters:
        request (Any): The input request to validate.

        Returns:
        bool: True if the input is a valid IPv4 netmask, False otherwise.

        Validation Steps:
        1. The input must have exactly 4 octets.
        2. Each octet must be an integer between 0 and 32.
        3. The binary representation must follow the IPv4 netmask pattern:
           - A series of '1's followed by '0's (e.g., 11111111111111110000000000000000).

        Raises:
        ValueError: If any validation step fails.
        """
        octet_count = len(request)
        if octet_count != 4 and all(32 >= octet >= 0 for octet in request):
            return False
        binary_string = NumeralConverter.bytes_to_binary(b''.join(request), 32)
        if re.search('^1*0*$', binary_string) is None:
            return False
        return True

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        """
        Processes the IPv4 netmask classification request.
        If the current handler cannot process the request, it delegates to the next handler in the chain.

        Parameters:
        request (Any): The input request to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The result of the classification or the result from the next handler in the chain.
        """
        return super().handle(request)


class DotIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    A handler for classifying IPv4 netmasks represented in dotted-decimal notation.
    This handler processes requests where the input is a string in the format 'x.x.x.x'.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in map(int, request.split('.'))
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class CIDRIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    A handler for classifying IPv4 netmasks represented in CIDR notation.
    This handler processes requests where the input is a string in the format '/x'.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            mask_match = re.search(r'^/(\d+)$', request)
            if mask_match is not None and 32 >= int(mask_match.group(1)) >= 0:
                binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
                bytes_list = [
                    NumeralConverter.binary_to_bytes(binary_string[index: index + 8], 1)
                    for index in range(0, len(binary_string), 8)
                ]
                return super()._validate(bytes_list)
            return False
        except (ValueError, TypeError):
            return False


class BytesIPv4NetmaskClassifierHandler(IPv4NetmaskClassifierHandler):
    """
    A handler for classifying IPv4 netmasks represented as byte sequences.
    This handler processes requests where the input is a bytes object of length 4.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and self._validate(request):
            return IPType.IPv4
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in request
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class IPv6IPTypeClassifierHandler(IPTypeClassifierHandler):
    """
    A handler for classifying IPv6 addresses.
    This class provides a base for processing IPv6 requests and validating them.
    """

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        """
        Processes the IPv6 classification request.
        If the current handler cannot process the request, it delegates to the next handler in the chain.

        Parameters:
        request (Any): The input request to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The result of the classification or the result from the next handler in the chain.
        """
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: Any) -> bool:
        """
        Validates the input as a valid IPv6 address.

        Parameters:
        request (Any): The input request to validate.

        Returns:
        bool: True if the input is a valid IPv6 address, False otherwise.

        Validation Conditions:
        - The input must have exactly 16 octets.
        - Each octet must be an integer between 0 and 128 (inclusive).
        """
        octet_count = len(request)
        if octet_count != 16 and all(128 >= octet >= 0 for octet in request):
            return False
        return True


class ColonIPv6IPTypeClassifierHandler(IPv6IPTypeClassifierHandler):
    """
    A handler for classifying IPv6 addresses represented in colon-hexadecimal notation.
    This handler processes requests where the input is a string (e.g., '2001:db8::1').
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            bytes_list = [
                NumeralConverter.hexadecimal_to_bytes(octet, 1)
                for octet in [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class BytesIPv6IPTypeClassifierHandler(IPv6IPTypeClassifierHandler):
    """
    A handler for classifying IPv6 addresses represented as byte sequences.
    This handler processes requests where the input is a bytes object of length 16.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in request
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False


class IPv6NetmaskClassifierHandler(IPTypeClassifierHandler):
    """
    A handler for classifying IPv6 netmask addresses.
    This class provides a base for validating IPv6 netmask representations.
    """

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        return super().handle(request)

    @abstractmethod
    def _validate(self, request: Any) -> bool:
        octet_count = len(request)
        if octet_count != 16 and all(128 >= octet >= 0 for octet in request):
            return False
        binary_string = NumeralConverter.bytes_to_binary(b''.join(request), 128)
        if re.search('^1*0*$', binary_string) is None:
            return False
        return True


class ColonIPv6NetmaskClassifierHandler(IPv6NetmaskClassifierHandler):
    """
    A handler for classifying IPv6 netmasks represented in colon-hexadecimal notation.
    This handler processes requests where the input is a string (e.g., 'FFFF:FFFF::').
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            bytes_list = [
                NumeralConverter.hexadecimal_to_bytes(octet, 1)
                for octet in [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError):
            return False


class CIDRIPv6NetmaskClassifierHandler(IPv6NetmaskClassifierHandler):
    """
    A handler for classifying IPv6 netmasks represented in CIDR notation.
    This handler processes requests where the input is a string (e.g., '/64').
    """

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)


    def _validate(self, request: Any) -> bool:
        try:
            mask_match = re.search(r'^/(\d+)$', request)
            if mask_match is not None and 128 >= int(mask_match.group(1)) >= 0:
                binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
                bytes_list = [
                    NumeralConverter.binary_to_bytes(binary_string[index: index + 8], 1)
                    for index in range(0, len(binary_string), 8)
                ]
                return super()._validate(bytes_list)
            return False
        except (ValueError, TypeError):
            return False


class BytesIPv6NetmaskClassifierHandler(IPv6IPTypeClassifierHandler):
    """
    A handler for classifying IPv6 netmasks represented as byte sequences.
    This handler processes requests where the input is a bytes object of length 16.
    """
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and self._validate(request):
            return IPType.IPv6
        else:
            return super().handle(request)

    def _validate(self, request: Any) -> bool:
        try:
            bytes_list = [
                NumeralConverter.decimal_to_bytes(int(octet), 1)
                for octet in request
            ]
            return super()._validate(bytes_list)
        except (ValueError, TypeError, OverflowError):
            return False

class IPTypeClassifier:
    """
    A utility class to classify IP addresses and netmasks for both IPv4 and IPv6.
    This class utilizes a Chain of Responsibility pattern with configurable classifiers for extensibility.

    Methods:
        - classify_ipv4_address: Classifies an IPv4 address based on its format.
        - classify_ipv4_netmask: Classifies an IPv4 netmask based on its format.
        - classify_ipv6_address: Classifies an IPv6 address based on its format.
        - classify_ipv6_netmask: Classifies an IPv6 netmask based on its format.
    """
    @staticmethod
    def classify_ipv4_address(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv4 address into its respective type using a chain of classifiers.

        Parameters:
        request_format (Any): The input IPv4 address to classify. Supported formats include:
                              - Dotted-decimal strings (e.g., "192.168.1.1")
                              - Byte sequences (e.g., b'\xc0\xa8\x01\x01')
        classifiers (List[IPTypeClassifierHandler], optional): A custom list of IPv4 address classifiers.
                                                               Defaults to standard classifiers.

        Returns:
        Union[IPType, None]: The type of the IPv4 address, or None if no match is found.
        """
        if classifiers is None:
            classifiers = [
                DotIPv4IPTypeClassifierHandler(),
                BytesIPv4IPTypeClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv4_netmask(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv4 netmask into its respective type using a chain of classifiers.

        Parameters:
        request_format (Any): The input IPv4 netmask to classify. Supported formats include:
                              - Dotted-decimal strings (e.g., "255.255.255.0")
                              - CIDR notation (e.g., "/24")
                              - Byte sequences (e.g., b'\xff\xff\xff\x00')
        classifiers (List[IPTypeClassifierHandler], optional): A custom list of IPv4 netmask classifiers.
                                                               Defaults to standard classifiers.

        Returns:
        Union[IPType, None]: The type of the IPv4 netmask, or None if no match is found.
        """
        if classifiers is None:
            classifiers = [
                DotIPv4NetmaskClassifierHandler(),
                CIDRIPv4NetmaskClassifierHandler(),
                BytesIPv4NetmaskClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv6_address(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv6 address into its respective type using a chain of classifiers.

        Parameters:
        request_format (Any): The input IPv6 address to classify. Supported formats include:
                              - Colon-hexadecimal strings (e.g., "2001:db8::1")
                              - Byte sequences (e.g., b'\x20\x01\x0d\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
        classifiers (List[IPTypeClassifierHandler], optional): A custom list of IPv6 address classifiers.
                                                               Defaults to standard classifiers.

        Returns:
        Union[IPType, None]: The type of the IPv6 address, or None if no match is found.
        """
        if classifiers is None:
            classifiers = [
                ColonIPv6IPTypeClassifierHandler(),
                BytesIPv6IPTypeClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv6_netmask(request_format: Any, classifiers: List[IPTypeClassifierHandler] = None) -> Union[IPType, None]:
        """
        Classifies an IPv6 netmask into its respective type using a chain of classifiers.

        Parameters:
        request_format (Any): The input IPv6 netmask to classify. Supported formats include:
                              - Colon-hexadecimal strings (e.g., "FFFF:FFFF::")
                              - CIDR notation (e.g., "/64")
                              - Byte sequences (e.g., b'\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        classifiers (List[IPTypeClassifierHandler], optional): A custom list of IPv6 netmask classifiers.
                                                               Defaults to standard classifiers.

        Returns:
        Union[IPType, None]: The type of the IPv6 netmask, or None if no match is found.
        """
        if classifiers is None:
            classifiers = [
                ColonIPv6NetmaskClassifierHandler(),
                CIDRIPv6NetmaskClassifierHandler(),
                BytesIPv6NetmaskClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)
