from __future__ import annotations

import ipaddress
import re
from abc import abstractmethod
from typing import Set, Any, List

import inflect

from ip_converters import NumeralConverter
from ttlinks.ttlinks.common.base_utils import CoRHandler, BinaryClass, BinaryFlyWeightFactory
from ttlinks.ttlinks.ipservice.ip_utils import IPType


# from ip_utils import BinaryClass, BinaryFlyWeightFactory


class IPValidatorHandler(CoRHandler):
    """
    Abstract base class for IP address validation handlers in a Chain of Responsibility pattern.
    This class handles the common functionality of setting up a chain, managing error states, and providing
    a framework for validating IP addresses.
    """
    _next_handler = None  # Reference to the next handler in the chain
    _previous_handler = None  # Reference to the previous handler in the chain

    def __init__(self):
        self._errors = set()

    def set_next(self, h: CoRHandler) -> CoRHandler:
        """
        Set the next handler in the chain and share the error set with it.

        Args:
        h (CoRHandler): The next handler in the chain.

        Returns:
        CoRHandler: The next handler for chaining.
        """
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        h._errors = self._errors
        h._previous_handler = self
        return h

    def get_errors(self) -> Set[str]:
        """Retrieve the set of accumulated validation errors."""
        return self._errors

    def clear_errors(self) -> None:
        """
        Clear the validation errors in this handler and propagate the clearing upstream.
        """
        self._errors = set()
        if self._previous_handler is not None:
            self._previous_handler.clear_errors()

    @abstractmethod
    def handle(self, request: Any):
        """
        Abstract method to process the request; should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def validate(self, request: Any):
        """
        Abstract method to validate an IP address; should be implemented by specific handler subclasses.
        """
        pass


class IPv4IPValidatorHandler(IPValidatorHandler):
    """
    Abstract handler for validating IPv4 addresses. This class provides a framework for handling validation,
    allowing extension by more specific IPv4 validation logic.
    """

    def handle(self, request: Any):
        """
        Handle the validation request by passing it to the next handler if it exists.

        Args:
        request (Any): The request to validate.

        Returns:
        Any: The result of the next handler or None if there is no next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def validate(self, request: List[BinaryClass]) -> bool:
        """
        Validate the list of binary class instances representing IPv4 octets.

        Args:
        request (List[BinaryClass]): The list of binary class instances representing IPv4 octets.

        Returns:
        bool: True if the validation is successful, otherwise False.
        """
        p = inflect.engine()
        octet_count = len(request)
        if octet_count != 4:
            self._errors.add(f"Unexpected number of octets: {octet_count}")
            return False
        for index, octet in enumerate(request, start=1):
            decimal_value = NumeralConverter.binary_to_decimal(str(octet))
            if not 0 <= decimal_value <= 255:
                ordinal = p.ordinal(index)
                self._errors.add(f"The {ordinal} octet is out of the allowed range (0-255): {octet}")
                return False
        return True


class IPv4IPBinaryValidator(IPv4IPValidatorHandler):
    """
    Concrete IPv4 binary validator that processes lists of binary class instances and validates each octet.
    """
    def handle(self, request: Any):
        """
        Validate the IPv4 binary representation if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        Any: IPType.IPv4 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, list) and self.validate(request):
            self.clear_errors()
            return IPType.IPv4
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate the IPv4 binary representation by calling the super class validate method.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        bool: True if valid, otherwise False.
        """
        return super().validate(request)


class IPv4IPStringValidator(IPv4IPValidatorHandler):
    """
    Concrete handler to validate IPv4 addresses provided as dot-decimal strings.
    """
    def handle(self, request: Any):
        """
        Validate the IPv4 address string if it meets the dot-decimal format, otherwise pass to the next handler.

        Args:
        request (Any): The IPv4 address string to validate.

        Returns:
        Any: IPType.IPv4 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv4
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a dot-decimal string by converting it to binary classes and using the superclass validation.

        Args:
        request (Any): The dot-decimal string to validate.

        Returns:
        bool: True if the string represents a valid IPv4 address, otherwise False.
        """
        try:
            address = [
                BinaryFlyWeightFactory.get_binary_class(NumeralConverter.decimal_to_binary(octet))
                for octet in map(int, request.split('.'))
            ]
            return super().validate(address)
        except ValueError:
            self._errors.add(f"{request} does not appear to be an IPv4 address")
            return False


class IPv4NetmaskValidatorHandler(IPValidatorHandler):
    """
    Abstract handler for validating IPv4 netmask. This class provides a framework for handling validation,
    allowing extension by more specific netmask validation logic.
    """

    def handle(self, request: Any):
        """
        Handle the validation request by passing it to the next handler if it exists.

        Args:
        request (Any): The request to validate.

        Returns:
        Any: The result of the next handler or None if there is no next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def validate(self, request: List[BinaryClass]) -> bool:
        """
        Validate a list of binary class instances representing IPv4 netmask octets.

        Args:
        request (List[BinaryClass]): The list of binary class instances representing netmask octets.

        Returns:
        bool: True if the netmask is a valid consecutive sequence of 1s followed by 0s.
        """
        octet_count = len(request)
        if octet_count != 4:
            self._errors.add(f"Unexpected number of octets: {octet_count}")
            return False
        binary_digits = []
        for octet in request:
            binary_digits.extend(octet.binary_digits())
        binary_string = '.'.join([str(NumeralConverter.binary_to_decimal(str(binary))) for binary in request])
        if re.search('^1*0*$', ''.join(map(str, binary_digits))) is None:
            self._errors.add(f"The IPv4 netmask is invalid '{binary_string}'")
            return False
        return True


class IPv4NetmaskBinaryValidator(IPv4NetmaskValidatorHandler):
    """
    Concrete IPv4 netmask binary validator that processes lists of binary class instances and validates the netmask.
    """
    def handle(self, request: Any):
        """
        Validate the IPv4 netmask binary representation if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        Any: IPType.IPv4 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, list) and self.validate(request):
            self.clear_errors()
            return IPType.IPv4
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate the IPv4 netmask binary representation by calling the super class validate method.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        bool: True if valid, otherwise False.
        """
        return super().validate(request)


class IPv4NetmaskDotDecimalValidator(IPv4NetmaskValidatorHandler):
    """
    Concrete handler to validate IPv4 netmask provided in dot-decimal notation.
    """
    def handle(self, request: Any):
        """
        Validate the IPv4 netmask in dot-decimal format if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The IPv4 netmask in dot-decimal format to validate.

        Returns:
        Any: IPType.IPv4 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv4
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a dot-decimal string by converting it to binary classes and using the superclass validation.

        Args:
        request (Any): The dot-decimal string to validate.

        Returns:
        bool: True if the string represents a valid IPv4 netmask, otherwise False.
        """
        try:
            address = [
                BinaryFlyWeightFactory.get_binary_class(NumeralConverter.decimal_to_binary(octet))
                for octet in map(int, request.split('.'))
            ]
            return super().validate(address)
        except ValueError:
            self._errors.add(f"{request} does not appear to be a valid IPv4 netmask")
            return False


class IPv4NetmaskCIDRValidator(IPv4NetmaskValidatorHandler):
    """
    Concrete handler to validate IPv4 netmask provided in CIDR notation.
    """
    def handle(self, request: Any):
        """
        Validate the IPv4 netmask in CIDR format if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The CIDR netmask to validate.

        Returns:
        Any: IPType.IPv4 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv4
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a CIDR notation by constructing the binary mask and using the superclass validation.

        Args:
        request (Any): The CIDR notation string to validate.

        Returns:
        bool: True if the CIDR represents a valid IPv4 netmask, otherwise False.
        """
        try:
            mask_match = re.search(r'/(\d+)', request)
            if mask_match is not None:
                if 32 >= int(mask_match.group(1)) >= 0:
                    binary_string = ('1' * int(mask_match.group(1))).ljust(32, '0')
                    address = [
                        BinaryFlyWeightFactory.get_binary_class(binary_string[index: index + 8])
                        for index in range(0, len(binary_string), 8)
                    ]
                    return super().validate(address)
                else:
                    raise ValueError(f'Invalid IPv4 netmask')
            else:
                raise ValueError('Invalid IPv4 netmask')
        except ValueError:
            self._errors.add(f"{request} does not appear to be a valid IPv4 netmask")
            return False


class IPv6IPValidatorHandler(IPValidatorHandler):
    """
    Abstract handler for validating IPv6 addresses. This class provides a framework for handling validation,
    allowing extension by more specific IPv6 validation logic.
    """

    def handle(self, request: Any):
        """
        Handle the validation request by passing it to the next handler if it exists.

        Args:
        request (Any): The request to validate.

        Returns:
        Any: The result of the next handler or None if there is no next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def validate(self, request: List[BinaryClass]) -> bool:
        """
        Validate the list of binary class instances representing IPv6 octets.

        Args:
        request (List[BinaryClass]): The list of binary class instances representing IPv6 octets.

        Returns:
        bool: True if the validation is successful, otherwise False.
        """
        p = inflect.engine()
        octet_count = len(request)
        if octet_count != 16:
            self._errors.add(f"Unexpected number of octets: {octet_count}")
            return False
        for index, octet in enumerate(request, start=1):
            decimal_value = NumeralConverter.binary_to_decimal(str(octet))
            if not 0 <= decimal_value <= 255:
                ordinal = p.ordinal(index)
                self._errors.add(f"The {ordinal} octet is out of the allowed range (0-255): [00->FF]")
                return False
        return True


class IPv6IPBinaryValidator(IPv6IPValidatorHandler):
    """
    Concrete handler to validate IPv6 addresses provided as lists of binary class instances.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 binary representation if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, list) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate the IPv6 binary representation by calling the superclass validate method.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        bool: True if valid, otherwise False.
        """
        return super().validate(request)


class IPv6IPStringValidator(IPv6IPValidatorHandler):
    """
    Concrete handler to validate IPv6 addresses provided as colon-hex strings.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 address string if it meets the colon-hex format, otherwise pass to the next handler.

        Args:
        request (Any): The IPv6 address string to validate.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a colon-hex string by converting it to binary classes and using the superclass validation.

        Args:
        request (Any): The colon-hex string to validate.

        Returns:
        bool: True if the string represents a valid IPv6 address, otherwise False.
        """
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            address = [
                BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(octet))
                for octet in octets
            ]
            return super().validate(address)
        except ValueError:
            self._errors.add(f"{request} does not appear to be an IPv6 address")
            return False

class IPv6IPColonHexValidator(IPv6IPValidatorHandler):
    """
    Concrete handler to validate IPv6 addresses provided in colon-separated hexadecimal notation.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 address in colon-separated hexadecimal format if it meets the format,
        otherwise pass to the next handler.

        Args:
        request (Any): The IPv6 address string in hexadecimal format to validate.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a colon-separated hexadecimal string by converting it to binary classes
        and using the superclass validation.

        Args:
        request (Any): The colon-separated hexadecimal string to validate.

        Returns:
        bool: True if the string represents a valid IPv6 address, otherwise False.
        """
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            address = [
                BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(octet))
                for octet in octets
            ]
            return super().validate(address)
        except ValueError:
            self._errors.add(f"'{request}' does not appear to be an IPv6 address")
            return False


class IPv6NetmaskValidatorHandler(IPValidatorHandler):
    """
    Abstract handler for validating IPv6 netmask. This class provides a framework for handling validation,
    allowing extension by more specific netmask validation logic.
    """

    def handle(self, request: Any):
        """
        Handle the validation request by passing it to the next handler if it exists.

        Args:
        request (Any): The request to validate.

        Returns:
        Any: The result of the next handler or None if there is no next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def validate(self, request: List[BinaryClass]) -> bool:
        """
        Validate the list of binary class instances representing an IPv6 netmask.

        Args:
        request (List[BinaryClass]): The list of binary class instances representing an IPv6 netmask.

        Returns:
        bool: True if the netmask is a valid consecutive sequence of 1s followed by 0s.
        """
        octet_count = len(request)
        if octet_count != 16:
            self._errors.add(f"Unexpected number of octets: {octet_count}")
            return False
        binary_digits = []
        for octet in request:
            binary_digits.extend(octet.binary_digits())
        binary_string = '.'.join([str(NumeralConverter.binary_to_decimal(str(binary))) for binary in request])
        if re.search('^1*0*$', ''.join(map(str, binary_digits))) is None:
            self._errors.add(f"The IPv6 netmask is invalid '{binary_string}'")
            return False
        return True


class IPv6NetmaskBinaryValidator(IPv6NetmaskValidatorHandler):
    """
    Concrete handler to validate IPv6 netmask provided as lists of binary class instances.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 netmask binary representation if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The list of binary class instances representing an IPv6 netmask.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, list) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate the IPv6 netmask binary representation by calling the superclass validate method.

        Args:
        request (Any): The list of binary class instances to validate.

        Returns:
        bool: True if valid, otherwise False.
        """
        return super().validate(request)


class IPv6NetmaskColonHexValidator(IPv6NetmaskValidatorHandler):
    """
    Concrete handler to validate IPv6 netmask provided in colon-separated hexadecimal notation.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 netmask in colon-separated hexadecimal format if it meets the format,
        otherwise pass to the next handler.

        Args:
        request (Any): The IPv6 netmask string in hexadecimal format to validate.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a colon-separated hexadecimal string by converting it to binary classes and
        using the superclass validation.

        Args:
        request (Any): The colon-separated hexadecimal string to validate.

        Returns:
        bool: True if the string represents a valid IPv6 netmask, otherwise False.
        """
        try:
            ipv6_full_string = ipaddress.ip_address(request).exploded.upper().replace(':', '')
            octets = [ipv6_full_string[i:i + 2] for i in range(0, len(ipv6_full_string), 2)]
            address = [
                BinaryFlyWeightFactory.get_binary_class(NumeralConverter.hexadecimal_to_binary(octet))
                for octet in octets
            ]
            return super().validate(address)
        except ValueError:
            self._errors.add(f"'{request}' does not appear to be an IPv6 netmask")
            return False


class IPv6NetmaskCIDRValidator(IPv6NetmaskValidatorHandler):
    """
    Concrete handler to validate IPv6 netmask provided in CIDR notation.
    """
    def handle(self, request: Any):
        """
        Validate the IPv6 netmask in CIDR format if it meets the format, otherwise pass to the next handler.

        Args:
        request (Any): The CIDR netmask to validate.

        Returns:
        Any: IPType.IPv6 if valid, otherwise the result of the next handler.
        """
        if isinstance(request, str) and self.validate(request):
            self.clear_errors()
            return IPType.IPv6
        else:
            return super().handle(request)

    def validate(self, request: Any):
        """
        Validate a CIDR notation by constructing the binary mask and using the superclass validation.

        Args:
        request (Any): The CIDR notation string to validate.

        Returns:
        bool: True if the CIDR represents a valid IPv6 netmask, otherwise False.
        """
        try:
            mask_match = re.search(r'/(\d+)', request)
            if mask_match is not None:
                if 128 >= int(mask_match.group(1)) >= 0:
                    binary_string = ('1' * int(mask_match.group(1))).ljust(128, '0')
                    address = [
                        BinaryFlyWeightFactory.get_binary_class(binary_string[index: index + 8])
                        for index in range(0, len(binary_string), 8)
                    ]
                    return super().validate(address)
                else:
                    raise ValueError(f'Invalid IPv6 netmask')
            else:
                raise ValueError('Invalid IPv6 netmask')
        except ValueError:
            self._errors.add(f"{request} does not appear to be a valid IPv6 netmask")
            return False
