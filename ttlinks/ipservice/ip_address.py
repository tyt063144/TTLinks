from __future__ import annotations

import ipaddress
from abc import ABC, abstractmethod
from typing import Iterable, Any
from typing import List

from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.ipservice.ip_converters import IPConverter
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
from ttlinks.ipservice.ip_utils import IPType


class IPAddr(ABC):
    """
    An abstract base class (ABC) representing an IP address.
    This class provides a blueprint for implementing IP address functionalities, such as validation,
    initialization, and representation in various formats.

    Attributes:
        _address: Internal storage for the IP address representation.
    """
    _address:bytes = None

    def __init__(self, address: Any) -> None:
        """
        Initializes an IP address by validating and initializing the provided input.

        Parameters:
        address (Any): The input address to initialize.

        Raises:
        Implemented in subclasses: Subclasses must implement `_validate` and `_initialize` methods.
        """
        self._validate(address)
        self._initialize(address)

    @abstractmethod
    def _validate(self, address: Any):
        """
        Validates the provided address format.

        Parameters:
        address (Any): The address to validate.

        Returns:
        List[Octet]: A list of octets representing the address.

        Raises:
        Implemented in subclasses: Subclasses must provide specific validation logic.
        """
        pass

    @abstractmethod
    def _initialize(self, address: Any) -> None:
        """
        Initializes internal structures based on the validated address.

        Parameters:
        address (Any): The address to initialize.

        Raises:
        Implemented in subclasses: Subclasses must provide specific initialization logic.
        """
        pass

    @property
    @abstractmethod
    def address(self) -> str:
        """
        Returns the original string representation of the IP address.

        Returns:
        str: The string representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the string address representation.
        """
        pass

    @property
    @abstractmethod
    def binary_string(self) -> str:
        """
        Returns the binary representation of the IP address as a string.

        Returns:
        str: Binary representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the binary string representation.
        """
        pass

    @property
    @abstractmethod
    def binary_digits(self) -> Iterable[int]:
        """
        Returns the binary representation of the IP address as an iterable of digits.

        Returns:
        Iterable[int]: An iterable containing the binary digits of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the binary digits.
        """
        pass

    @property
    @abstractmethod
    def as_decimal(self) -> int:
        """
        Returns the decimal representation of the IP address.

        Returns:
        int: The decimal representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the decimal representation.
        """
        pass

    @property
    @abstractmethod
    def as_bytes(self) -> bytes:
        """
        Returns the byte representation of the IP address. It's useful for network operations. The format is big-endian.

        Returns:
        bytes: The byte representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the byte representation.
        """
        pass

    @property
    @abstractmethod
    def as_hexadecimal(self) -> str:
        """
        Returns the hexadecimal representation of the IP address.

        Returns:
        str: The hexadecimal representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the hexadecimal representation.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the string representation of the IP address for display purposes.

        Returns:
        str: The string representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the string conversion logic.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns the string representation of the IP address for debugging purposes.

        Returns:
        str: The string representation of the IP address.

        Raises:
        Implemented in subclasses: Subclasses must provide the debug representation logic.
        """
        pass


class IPv4Addr(IPAddr):
    """
    A concrete implementation of the IPAddr abstract base class for IPv4 addresses.
    Provides validation, initialization, and representation functionalities specific to IPv4.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided address format to ensure it is a valid IPv4 address.
        """
        if IPTypeClassifier.classify_ipv4_address(address) != IPType.IPv4:
            raise ValueError(str(address) + " is not a valid IPv4 address.")

    def _initialize(self, address: Any) -> None:
        """
        Initializes internal structures based on the validated IPv4 address. The address is stored as bytes.
        """
        self._address = IPConverter.convert_to_ipv4_bytes(address)

    @property
    def binary_string(self) -> str:
        """
        Returns the binary representation of the IPv4 address as a string.
        For example, the binary representation of the IPv4 address '192.168.1.1' is '11000000101010000000000100000001'.
        """
        return ''.join([NumeralConverter.decimal_to_binary(octet) for octet in self._address])

    @property
    def binary_digits(self) -> List[int]:
        """
        Returns the binary representation of the IPv4 address as a list of digits.
        For example, the binary representation of the IPv4 address '192.168.1.1' is
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1].
        """
        result = []
        for octet in self.binary_string:
            for bit in str(octet):
                result.append(int(bit))
        return result

    @property
    def as_decimal(self) -> int:
        """
        Returns the decimal representation of the IPv4 address.
        For example, the decimal representation of the IPv4 address '192.168.1.1' is 3232235777.
        """
        return NumeralConverter.binary_to_decimal(self.binary_string)

    @property
    def address(self) -> str:
        """
        Returns the dotted-decimal string representation of the IPv4 address.
        """
        return self.__str__()

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the byte representation of the IPv4 address. It's useful for network operations. The format is big-endian.
        For example, the byte representation of the IPv4 address '192.168.1.1' is b'\xc0\xa8\x01\x01'.
        """
        return self._address

    @property
    def as_hexadecimal(self) -> str:
        """
        Returns the hexadecimal representation of the IPv4 address.
        For example, the hexadecimal representation of the IPv4 address '
        """
        return ''.join([NumeralConverter.decimal_to_hexadecimal(octet) for octet in self._address])

    def __str__(self) -> str:
        """
        Returns the string representation of the IPv4 address for display purposes.
        """
        return '.'.join([str(octet) for octet in self._address])

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv4 address for debugging purposes.
        """
        return f"""IPv4Addr('_address={self.__str__()}')"""


class IPv6Addr(IPAddr):
    """
    A concrete implementation of the IPAddr abstract base class for IPv6 addresses.
    Provides validation, initialization, and representation functionalities specific to IPv6.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided address format to ensure it is a valid IPv6 address.
        """
        if IPTypeClassifier.classify_ipv6_address(address) != IPType.IPv6:
            raise ValueError(str(address) + " is not a valid IPv6 address.")

    def _initialize(self, address: Any) -> None:
        """
        Initializes internal structures based on the validated IPv6 address. The address is stored as bytes.
        """
        self._address = IPConverter.convert_to_ipv6_bytes(address)

    @property
    def address(self) -> str:
        """
        Returns the colon-separated string representation of the IPv6 address.
        """
        return self.__str__()

    @property
    def binary_string(self) -> str:
        """
        Returns the binary representation of the IPv6 address as a string.
        For example, the binary representation of the IPv6 address '2001:0db8:85a3:0000:0000:8a2e:0370:7334' is
        '00100000000000010000110110111000100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110100
        """
        return ''.join([NumeralConverter.decimal_to_binary(octet) for octet in self._address])

    @property
    def binary_digits(self) -> List[int]:
        """
        Returns the binary representation of the IPv6 address as a list of digits.
        For example, the binary representation of the IPv6 address '2001:0db8:85a3:0000:0000:8a2e:0370:7334' is
        [
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,
            1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0
        ]
        """
        result = []
        for octet in self.binary_string:
            for bit in str(octet):
                result.append(int(bit))
        return result

    @property
    def as_decimal(self) -> int:
        """
        Returns the decimal representation of the IPv6 address.
        For example, the decimal representation of the IPv6 address '2001:0db8:85a3:0000:0000:8a2e:0370:7334' is
        42540766452641154071740215577757643572.
        """
        return NumeralConverter.binary_to_decimal(self.binary_string)

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the byte representation of the IPv6 address. It's useful for network operations. The format is big-endian.
        For example, the byte representation of the IPv6 address '2001:0db8:85a3:0000:0000:8a2e:0370:7334' is
        b' \x01\r\xb8\x85\xa3\x00\x00\x00\x00\x8a.\x03ps4'.
        """
        return self._address

    @property
    def as_hexadecimal(self) -> str:
        """
        Returns the hexadecimal representation of the IPv6 address.
        For example, the hexadecimal representation of the IPv6 address '2001:0db8:85a3:0000:0000:8a2e:0370:7334' is
        '20010DB885A3000000008A2E03707334'.
        """
        raw_ipv6_bytes = [NumeralConverter.bytes_to_hexadecimal(self._address[octet: octet + 2]) for octet in range(0, len(self._address), 2)]
        return ''.join(raw_ipv6_bytes).upper()

    def __str__(self) -> str:
        """
        Returns the string representation of the IPv6 address for display purposes.
        """
        raw_ipv6_bytes = [NumeralConverter.bytes_to_hexadecimal(self._address[octet: octet + 2]) for octet in range(0, len(self._address), 2)]
        return ipaddress.IPv6Address(':'.join(raw_ipv6_bytes)).compressed.upper()

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv6 address for debugging purposes.
        """
        return f"""IPv6Addr('_address={self.__str__()}')"""


class IPMask(IPAddr, ABC):
    """
    An abstract base class (ABC) representing an IP address mask.
    Inherits from IPAddr and provides an additional abstract property for the mask size.

    This class serves as a blueprint for IP mask implementations, including validation and mask size retrieval.
    """

    @property
    @abstractmethod
    def mask_size(self) -> str:
        """
        Abstract property to return the size of the mask as a string.
        This typically represents the number of bits in the mask (e.g., '/24' for IPv4 or '/64' for IPv6).

        Returns:
        str: The size of the mask in CIDR notation.

        Raises:
        Implemented in subclasses: Subclasses must provide specific logic to calculate or retrieve the mask size.
        """
        pass


class IPv4NetMask(IPMask, IPv4Addr):
    """
    A concrete implementation of the IPMask and IPv4Addr classes for IPv4 network masks.
    This class provides validation and representation functionalities specific to IPv4 netmasks.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided address format to ensure it is a valid IPv4 netmask.
        """
        if IPTypeClassifier.classify_ipv4_netmask(address) != IPType.IPv4:
            raise ValueError(str(address) + " is not a valid IPv4 netmask.")

    @property
    def mask_size(self) -> int:
        """
        Returns the size of the IPv4 netmask as an integer.
        This represents the number of bits set to '1' in the netmask.
        """
        return self.binary_string.count('1')

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv4 netmask for debugging purposes.
        """
        return f"""IPv4NetMask('_address={self.__str__()}')"""


class IPv4WildCard(IPv4NetMask):
    """
    A concrete implementation of IPv4NetMask for wildcard masks.
    Wildcard masks are the inverse of subnet masks and are often used in access control lists (ACLs).
    """
    def _validate(self, address: Any) -> None:
        if IPTypeClassifier.classify_ipv4_address(address) != IPType.IPv4:
            raise ValueError(str(address) + " is not a valid IPv4 wildcard mask.")

    @property
    def mask_size(self) -> int:
        """
        Returns the size of the IPv4 wildcard mask as an integer. This represents the number of bits set to '1' in the mask.
        """
        count_of_ones = self.binary_string.count('1')
        return count_of_ones

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv4 wildcard mask for debugging purposes.
        """
        return f"""IPv4WildCard('_address={self.__str__()}')"""


class IPv6NetMask(IPMask, IPv6Addr):
    """
    A concrete implementation of the IPMask and IPv6Addr classes for IPv6 network masks.
    This class provides validation and representation functionalities specific to IPv6 netmasks.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided address format to ensure it is a valid IPv6 netmask.
        """
        if IPTypeClassifier.classify_ipv6_netmask(address) != IPType.IPv6:
            raise ValueError(str(address) + " is not a valid IPv6 netmask.")

    @property
    def mask_size(self) -> int:
        """
        Returns the size of the IPv6 netmask as an integer. This represents the number of bits set to '1' in the netmask.
        """
        return self.binary_string.count('1')

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv6 netmask for debugging purposes.
        """
        return f"""IPv6NetMask('_address={self.__str__()}')"""


class IPv6WildCard(IPv6NetMask):
    """
    A concrete implementation of IPv6NetMask for wildcard masks.
    Wildcard masks are the inverse of subnet masks and are often used in access control lists (ACLs).
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided address format to ensure it is a valid IPv6 wildcard mask.
        """
        if IPTypeClassifier.classify_ipv6_address(address) != IPType.IPv6:
            raise ValueError(str(address) + " is not a valid IPv6 wildcard mask.")

    @property
    def mask_size(self) -> int:
        """
        Returns the size of the IPv6 wildcard mask as an integer. This represents the number of bits set to '1' in the mask.
        """
        count_of_ones = self.binary_string.count('1')
        return count_of_ones

    def __repr__(self) -> str:
        """
        Returns the string representation of the IPv6 wildcard mask for debugging purposes.
        """
        return f"""IPv6WildCard('_address={self.__str__()}')"""
