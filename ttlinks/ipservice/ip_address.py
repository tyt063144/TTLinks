from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Union
from typing import List

from ip_converters import NumeralConverter, \
    BinaryIPv4ConverterHandler, BinaryIPv6ConverterHandler, DotDecimalIPv4ConverterHandler, CIDRIPv4ConverterHandler, \
    ColonHexIPv6ConverterHandler, CIDRIPv6ConverterHandler
from ip_validators import IPv4IPBinaryValidator, \
    IPv4IPStringValidator, IPv4NetmaskBinaryValidator, IPv4NetmaskDotDecimalValidator, IPv4NetmaskCIDRValidator, \
    IPv6NetmaskBinaryValidator, IPv6NetmaskCIDRValidator, IPv6IPBinaryValidator, \
    IPv6IPColonHexValidator, IPv6NetmaskColonHexValidator
from ttlinks.ttlinks.common.base_utils import BinaryClass
from ttlinks.ttlinks.ipservice.ip_utils import IPType


class IPAddr(ABC):
    def __init__(self, address: Union[List[BinaryClass], str]) -> None:
        """
        Initialize an IP address object.

        Args:
        address (Union[List[BinaryClass], str]): The IP address in binary class list or string format.
        """
        self._address = self._validate(address)

    def get_address(self) -> List[BinaryClass]:
        """
        Return the list of BinaryClass instances representing the IP address.

        Returns:
        List[BinaryClass]: The IP address components.
        """
        return self._address

    @abstractmethod
    def _validate(self, address: List[BinaryClass]) -> List[BinaryClass]:
        """
        Validate the IP address components.

        Args:
        address (Union[List[BinaryClass], str]): A list of BinaryClass instances or string representing the IP address.

        Returns:
        List[BinaryClass]: The validated address.

        Raises:
        ValueError: If any component is out of the defined range.
        """
        pass

    @abstractmethod
    def get_binary_strings(self) -> str:
        """
        Get the concatenated binary strings of the IP address.

        Returns:
        str: The binary string of the IP address.
        """
        pass

    @abstractmethod
    def get_binary_digits(self) -> Iterable[int]:
        """
        Generate each binary digit in the IP address as integers.

        Returns:
        Iterable[int]: A generator yielding each binary digit.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Return the standard readable IP address format.

        Returns:
        str: The standard IP address format.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Return a formal string representation of the IP address, suitable for debugging.

        Returns:
        str: The debug string of the IP address.
        """
        pass


class IPv4Addr(IPAddr):
    def _validate(self, address: Union[List[BinaryClass], str]) -> List[BinaryClass]:
        """
        Validates the provided IPv4 address using a chain of responsibility pattern that links
        binary and string validation handlers.

        Args:
            address (Union[List[BinaryClass], str]): The IPv4 address in either binary class list or string format.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated IPv4 address.

        Raises:
            ValueError: If the address is not a valid IPv4 address.
        """
        ipv4_binary_validator = IPv4IPBinaryValidator()
        ipv4_string_validator = IPv4IPStringValidator()
        ipv4_binary_validator.set_next(ipv4_string_validator)
        if ipv4_binary_validator.handle(address) == IPType.IPv4:
            binary_ipv4_converter = BinaryIPv4ConverterHandler()
            string_ipv4_converter = DotDecimalIPv4ConverterHandler()
            binary_ipv4_converter.set_next(string_ipv4_converter)
            return binary_ipv4_converter.handle(address)
        else:
            message = ["This is not a valid IPv4 address."]
            message.extend(list(ipv4_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_binary_strings(self) -> str:
        """Concatenate the binary strings of each octet in the IPv4 address."""
        return ''.join([str(octet) for octet in self._address])

    def get_binary_digits(self) -> Iterable[int]:
        """Generate each binary digit in the IPv4 address as integers."""
        for octet in self._address:
            for bit in str(octet):
                yield int(bit)

    def __str__(self) -> str:
        """Return the standard dot-separated decimal format of the IPv4 address."""
        return '.'.join([str(NumeralConverter.binary_to_decimal(str(address))) for address in self._address])

    def __repr__(self) -> str:
        """Provide a detailed string representation of the IPv4Addr instance for debugging purposes."""
        return f"""IPv4Addr('_address={self._address})"""


class IPv6Addr(IPAddr):
    def _validate(self, address: Union[List[BinaryClass], str]) -> List[BinaryClass]:
        """
        Validates the provided IPv6 address using a chain of responsibility pattern that links
        binary and colon-separated hexadecimal validation handlers.

        Args:
            address (Union[List[BinaryClass], str]): The IPv6 address in either binary class list or string format.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated IPv6 address.

        Raises:
            ValueError: If the address is not a valid IPv6 address.
        """
        ipv6_binary_validator = IPv6IPBinaryValidator()
        ipv6_colon_hex_validator = IPv6IPColonHexValidator()
        ipv6_binary_validator.set_next(ipv6_colon_hex_validator)
        if ipv6_binary_validator.handle(address) == IPType.IPv6:
            binary_ipv6_converter = BinaryIPv6ConverterHandler()
            colon_hex_ipv6_converter = ColonHexIPv6ConverterHandler()
            binary_ipv6_converter.set_next(colon_hex_ipv6_converter)
            return binary_ipv6_converter.handle(address)
        else:
            message = ["This is not a valid IPv6 address."]
            message.extend(list(ipv6_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_binary_strings(self) -> str:
        """Concatenate the binary strings of each segment in the IPv6 address."""
        return ''.join([str(octet) for octet in self._address])

    def get_binary_digits(self) -> Iterable[int]:
        """Generate each binary digit in the IPv6 address as integers."""
        for octet in self._address:
            for bit in str(octet):
                yield int(bit)

    def __str__(self) -> str:
        """Return the standard colon-separated hexadecimal format of the IPv6 address."""
        ipv6_string = ''.join([
            str(NumeralConverter.binary_to_hexadecimal(str(address))).rjust(2, '0')
            for address in self._address
        ])
        return ':'.join([ipv6_string[index: index + 4] for index in range(0, len(ipv6_string), 4)])

    def __repr__(self) -> str:
        """Provide a detailed string representation of the IPv6Addr instance for debugging purposes."""
        return f"""IPv6Addr('_address={self._address})"""


class IPNetMask(IPAddr, ABC):
    """
    Abstract base class for IP netmask, extending IP address functionalities to specialized netmask operations.
    """

    @abstractmethod
    def _validate(self, address: List[BinaryClass]) -> List[BinaryClass]:
        """
        Validate the netmask components ensuring all parts are within acceptable ranges.

        Args:
            address (List[BinaryClass]): List of BinaryClass instances representing the netmask.

        Returns:
            List[BinaryClass]: The validated netmask as a list of BinaryClass instances.

        Raises:
            ValueError: If any part of the netmask is out of the defined acceptable range.
        """
        pass

    @abstractmethod
    def get_mask_size(self) -> str:
        """
        Retrieve the size of the netmask based on the number of leading ones in its binary representation.

        Returns:
            int: The size of the netmask.
        """
        pass

    def get_binary_strings(self) -> str:
        """Concatenate the binary strings of each segment in the netmask."""
        return ''.join([str(octet) for octet in self._address])

    def get_binary_digits(self) -> Iterable[int]:
        """Generate each binary digit in the netmask as integers."""
        for octet in self._address:
            for bit in str(octet):
                yield int(bit)


class IPv4NetMask(IPNetMask, IPv4Addr):
    """
    IPv4 netmask class, utilizing multiple validators to ensure the correctness of netmask values and formats.
    """

    def _validate(self, address: Union[List[BinaryClass], str]) -> List[BinaryClass]:
        """
        Validates the IPv4 netmask using a chain of responsibility pattern linking different format validators.

        Args:
            address (Union[List[BinaryClass], str]): The IPv4 netmask in either binary class list or string format.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated IPv4 netmask.

        Raises:
            ValueError: If the netmask is not valid in any known IPv4 netmask format.
        """
        ipv4_netmask_binary_validator = IPv4NetmaskBinaryValidator()
        ipv4_netmask_dot_decimal_validator = IPv4NetmaskDotDecimalValidator()
        ipv4_netmask_cidr_validator = IPv4NetmaskCIDRValidator()
        ipv4_netmask_binary_validator.set_next(ipv4_netmask_dot_decimal_validator).set_next(ipv4_netmask_cidr_validator)
        if ipv4_netmask_binary_validator.handle(address) == IPType.IPv4:
            binary_ipv4_converter = BinaryIPv4ConverterHandler()
            dot_decimal_ipv4_converter = DotDecimalIPv4ConverterHandler()
            cidr_ipv4_converter = CIDRIPv4ConverterHandler()
            binary_ipv4_converter.set_next(dot_decimal_ipv4_converter).set_next(cidr_ipv4_converter)
            return binary_ipv4_converter.handle(address)
        else:
            message = ["This is not a valid IPv4 netmask."]
            message.extend(list(ipv4_netmask_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_mask_size(self) -> int:
        """
        Calculate the size of the netmask by counting the number of '1's in the binary representation.

        Returns:
            int: The number of leading '1's in the netmask binary representation.
        """
        return self.get_binary_strings().count('1')

    def __str__(self) -> str:
        """
        Return the standard dot-separated decimal format of the IPv4 netmask.

        Returns:
            str: The IPv4 netmask in dot-decimal notation.
        """
        return '.'.join([str(NumeralConverter.binary_to_decimal(str(address))) for address in self._address])

    def __repr__(self) -> str:
        """
        Provide a detailed string representation of the IPv4NetMask instance for debugging purposes.

        Returns:
            str: A debug string representation of the IPv4NetMask instance.
        """
        return f"""IPv4NetMask('_address={self._address})"""


class IPv4WildCard(IPv4NetMask):
    """
    Class for handling IPv4 wildcard masks, which are used to specify bits that don't need to match
    in networking operations.
    """

    def _validate(self, address: str) -> List[BinaryClass]:
        """
        Validates the IPv4 wildcard mask using a chain of responsibility pattern designed for both binary and
        string formats.

        Args:
            address (str): The IPv4 wildcard mask in binary class list or string format.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated wildcard mask.

        Raises:
            ValueError: If the wildcard mask is not valid.
        """
        ipv4_binary_validator = IPv4IPBinaryValidator()
        ipv4_netmask_dot_decimal_validator = IPv4IPStringValidator()
        ipv4_binary_validator.set_next(ipv4_netmask_dot_decimal_validator)
        if ipv4_binary_validator.handle(address) == IPType.IPv4:
            binary_ipv4_converter = BinaryIPv4ConverterHandler()
            dot_decimal_ipv4_converter = DotDecimalIPv4ConverterHandler()
            binary_ipv4_converter.set_next(dot_decimal_ipv4_converter)
            return binary_ipv4_converter.handle(address)
        else:
            message = ["This is not a valid IPv4 wildcard mask."]
            message.extend(list(ipv4_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_mask_size(self) -> int:
        """
        Calculate the effective size of the wildcard mask by counting the number of '1' bits, which are treated
        as don't care positions.

        Returns:
            int: The count of '1' bits in the wildcard mask.
        """
        count_of_ones = self.get_binary_strings().count('1')
        return 2 ** count_of_ones

    def __str__(self) -> str:
        """ Return the standard dot-separated decimal format of the IPv4 wildcard mask. """
        return '.'.join([str(NumeralConverter.binary_to_decimal(str(address))) for address in self._address])

    def __repr__(self) -> str:
        """ Provide a detailed string representation of the IPv4WildCard instance. """
        return f"""IPv4WildCard('_address={self._address})"""


class IPv6NetMask(IPNetMask, IPv6Addr):
    """
    Class for handling IPv6 netmask, applying standard netmask validation and conversion methods for IPv6 addresses.
    """

    def _validate(self, address: Union[List[BinaryClass], str]) -> List[BinaryClass]:
        """
        Validates the IPv6 netmask using a chain of responsibility pattern that includes binary, colon-hexadecimal,
        and CIDR validators.

        Args:
            address (Union[List[BinaryClass], str]): The IPv6 netmask in binary class list or string format.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated IPv6 netmask.

        Raises:
            ValueError: If the netmask is not valid in any recognized IPv6 netmask format.
        """
        ipv6_netmask_binary_validator = IPv6NetmaskBinaryValidator()
        ipv6_netmask_colon_hex_validator = IPv6NetmaskColonHexValidator()
        ipv6_netmask_cidr_validator = IPv6NetmaskCIDRValidator()
        ipv6_netmask_binary_validator.set_next(ipv6_netmask_colon_hex_validator).set_next(ipv6_netmask_cidr_validator)
        if ipv6_netmask_binary_validator.handle(address) == IPType.IPv6:
            binary_ipv6_converter = BinaryIPv6ConverterHandler()
            colon_hex_ipv6_converter = ColonHexIPv6ConverterHandler()
            cidr_ipv6_converter = CIDRIPv6ConverterHandler()
            binary_ipv6_converter.set_next(colon_hex_ipv6_converter).set_next(cidr_ipv6_converter)
            return binary_ipv6_converter.handle(address)
        else:
            message = ["This is not a valid IPv6 netmask."]
            message.extend(list(ipv6_netmask_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_mask_size(self) -> int:
        """
        Calculate the size of the netmask by counting the number of '1' bits in the binary representation.

        Returns:
            int: The number of '1' bits, representing the effective size of the netmask.
        """
        return self.get_binary_strings().count('1')

    def __str__(self) -> str:
        """ Return the standard colon-separated hexadecimal format of the IPv6 netmask. """
        ip_hex_string = [
            str(NumeralConverter.binary_to_hexadecimal(str(address))).rjust(2, '0')
            for address in self._address
        ]
        return ':'.join([''.join(ip_hex_string[index: index + 2]) for index in range(0, len(ip_hex_string), 2)])

    def __repr__(self) -> str:
        """ Provide a detailed string representation of the IPv6NetMask instance. """
        return f"""IPv6NetMask('_address={self._address})"""


class IPv6WildCard(IPv6NetMask):
    """
    Class for handling IPv6 wildcard masks, which invert the typical usage of netmask
    by specifying bits that should not match.
    Inherits functionalities from the IPv6NetMask class.
    """

    def _validate(self, address: str) -> List[BinaryClass]:
        """
        Validates the IPv6 wildcard mask using a chain of responsibility pattern that integrates binary and
        colon-hexadecimal validators.

        Args:
            address (str): The IPv6 wildcard mask in string format, expected to be in colon-separated hexadecimal.

        Returns:
            List[BinaryClass]: A list of BinaryClass instances representing the validated IPv6 wildcard mask.

        Raises:
            ValueError: If the wildcard mask is not valid, including detailed error messages from validators.
        """
        ipv6_binary_validator = IPv6IPBinaryValidator()
        ipv6_netmask_colon_hex_validator = IPv6IPColonHexValidator()
        ipv6_binary_validator.set_next(ipv6_netmask_colon_hex_validator)
        if ipv6_binary_validator.handle(address) == IPType.IPv6:
            binary_ipv6_converter = BinaryIPv6ConverterHandler()
            colon_hex_ipv6_converter = ColonHexIPv6ConverterHandler()
            binary_ipv6_converter.set_next(colon_hex_ipv6_converter)
            return binary_ipv6_converter.handle(address)
        else:
            message = ["This is not a valid IPv6 wildcard mask."]
            message.extend(list(ipv6_binary_validator.get_errors()))
            raise ValueError("\n".join(message))

    def get_mask_size(self) -> int:
        """
        Calculate the effective size of the wildcard mask based on the count of '1' bits,
        which are interpreted as 'do not care' bits in wildcard context.

        Returns:
            int: The effective size of the wildcard mask, calculated as 2^count_of_ones.
        """
        count_of_ones = self.get_binary_strings().count('1')
        return 2 ** count_of_ones

    def __str__(self) -> str:
        """
        Return the standard colon-separated hexadecimal format of the IPv6 wildcard mask.

        Returns:
            str: The IPv6 wildcard mask in colon-separated format, suitable for display and further processing.
        """
        ip_hex_string = [
            str(NumeralConverter.binary_to_hexadecimal(str(address))).rjust(2, '0')
            for address in self._address
        ]
        return ':'.join([''.join(ip_hex_string[index: index + 2]) for index in range(0, len(ip_hex_string), 2)])

    def __repr__(self) -> str:
        """
        Provide a detailed string representation of the IPv6WildCard instance for debugging purposes.

        Returns:
            str: A debug string representation of the IPv6WildCard instance.
        """
        return f"""IPv6WildCard('_address={self._address})"""
