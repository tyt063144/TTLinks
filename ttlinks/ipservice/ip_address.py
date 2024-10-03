from __future__ import annotations

import ipaddress
from abc import ABC, abstractmethod
from typing import Iterable, Any
from typing import List

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.ipservice.ip_converters import IPConverter
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier, IPType


class IPAddr(ABC):
    """
    Abstract base class for representing an IP address. This class defines the structure
    for IP address-related functionality, including validation, conversion to binary formats,
    and string representations.

    Attributes:
    _address : Any
        The internal representation of the IP address, set through the initialization.
    """
    _address = None

    def __init__(self, address: Any) -> None:
        """
        Initializes the IP address by calling the _initialize method, which in turn validates
        the provided address.

        Parameters:
        address : Any
            The IP address to be initialized, provided in any format (e.g., string, number).
        """
        self._initialize(address)

    @abstractmethod
    def _validate(self, address: Any) -> List[Octet]:
        """
        Abstract method that validates the provided IP address. This method should be implemented
        by subclasses to ensure the given address adheres to the format of a valid IP address.

        Parameters:
        address : Any
            The IP address to be validated.

        Returns:
        List[Octet]
            A list of octets representing the validated address.
        """
        pass

    def _initialize(self, address: Any) -> None:
        """
        Private method to initialize the IP address by validating the provided address.

        Parameters:
        address : Any
            The IP address to be validated and set.
        """
        self._validate(address)


    @property
    @abstractmethod
    def binary_digits(self) -> Iterable[int]:
        """
        Abstract property that returns the binary digits of the IP address. Subclasses
        must implement this to provide the address in binary form as a sequence of integers.

        Returns:
        Iterable[int]
            A sequence of integers representing the binary digits of the IP address.
        """
        pass

    @property
    @abstractmethod
    def binary_string(self) -> str:
        """
        Abstract property that returns the binary representation of the IP address as a string.

        Returns:
        str
            A string representing the binary form of the IP address.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Abstract method to return a user-friendly string representation of the IP address.

        Returns:
        str
            The string representation of the IP address.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method to return the official string representation of the IP address, useful for debugging.

        Returns:
        str
            The official string representation of the IP address.
        """
        pass


class IPv4Addr(IPAddr):
    """
    A concrete class that implements the abstract base class IPAddr for IPv4 addresses. This class
    handles the validation, conversion, and binary representation of an IPv4 address.

    Methods:
    _validate(address: Any) -> None:
        Validates the given address to ensure it's a valid IPv4 address.

    binary_digits -> Iterable[int]:
        Returns the binary digits of the IPv4 address as a sequence of integers.

    binary_string -> str:
        Returns the binary representation of the IPv4 address as a string.

    __str__() -> str:
        Returns a string representation of the IPv4 address in the standard dotted decimal format.

    __repr__() -> str:
        Returns the official string representation of the IPv4 address, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the given address to ensure it is a valid IPv4 address. If valid, the address
        is converted into a list of octets; otherwise, raises a ValueError.

        Parameters:
        address : Any
            The IP address to be validated, in string or other format.

        Raises:
        ValueError:
            If the provided address is not a valid IPv4 address.
        """
        if IPTypeClassifier.classify_ipv4_address(address) == IPType.IPv4:
            self._address = IPConverter.convert_to_ipv4_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv4 address.")

    @property
    def binary_digits(self) -> Iterable[int]:
        """
        Generates the binary digits of the IPv4 address by iterating over each octet and converting it to binary.

        Returns:
        Iterable[int]
            A generator yielding the binary digits of the IP address.
        """
        for octet in self._address:
            for bit in str(octet):
                yield int(bit)

    @property
    def binary_string(self) -> str:
        """
        Returns the binary representation of the IPv4 address as a concatenated string of all octets.

        Returns:
        str
            A string of binary digits representing the entire IPv4 address.
        """
        return ''.join([str(octet) for octet in self._address])

    @property
    def decimal(self) -> int:
        """
        Returns the decimal representation of the IPv4 address as an integer.

        Returns:
        int
            The IPv4 address as an integer.
        """
        return int(self.binary_string, 2)

    def __str__(self) -> str:
        """
        Returns the IPv4 address in the standard dotted decimal notation.

        Returns:
        str
            The IPv4 address as a string in dotted decimal format.
        """
        return '.'.join([str(octet.decimal) for octet in self._address])

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv4 address object for debugging.

        Returns:
        str
            A string showing the internal representation of the IPv4 address.
        """
        return f"""IPv4Addr('_address={self._address})"""


class IPv6Addr(IPAddr):
    """
    A concrete class that implements the abstract base class IPAddr for IPv6 addresses. This class
    handles the validation, conversion, and binary representation of an IPv6 address.

    Methods:
    _validate(address: Any) -> None:
        Validates the given address to ensure it's a valid IPv6 address.

    binary_digits -> Iterable[int]:
        Returns the binary digits of the IPv6 address as a sequence of integers.

    binary_string -> str:
        Returns the binary representation of the IPv6 address as a string.

    __str__() -> str:
        Returns a string representation of the IPv6 address in the standard colon-hexadecimal format.

    __repr__() -> str:
        Returns the official string representation of the IPv6 address, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the given address to ensure it is a valid IPv6 address. If valid, the address
        is converted into a list of octets; otherwise, raises a ValueError.

        Parameters:
        address : Any
            The IP address to be validated, in string or other format.

        Raises:
        ValueError:
            If the provided address is not a valid IPv6 address.
        """
        if IPTypeClassifier.classify_ipv6_address(address) == IPType.IPv6:
            self._address = IPConverter.convert_to_ipv6_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv6 address.")

    @property
    def binary_digits(self) -> Iterable[int]:
        """
        Generates the binary digits of the IPv6 address by iterating over each octet and converting it to binary.

        Returns:
        Iterable[int]
            A generator yielding the binary digits of the IPv6 address.
        """
        for octet in self._address:
            for bit in str(octet):
                yield int(bit)

    @property
    def binary_string(self) -> str:
        """
        Returns the binary representation of the IPv6 address as a concatenated string of all octets.

        Returns:
        str
            A string of binary digits representing the entire IPv6 address.
        """
        return ''.join([str(octet) for octet in self._address])

    @property
    def decimal(self) -> int:
        """
        Returns the decimal representation of the IPv4 address as an integer.

        Returns:
        int
            The IPv4 address as an integer.
        """
        return int(self.binary_string, 2)

    def __str__(self) -> str:
        """
        Returns the IPv6 address in the standard colon-hexadecimal notation. The octets are grouped into
        colon-separated segments in hexadecimal format.

        Returns:
        str
            The IPv6 address as a string in colon-hexadecimal format.
        """
        ipv6_string = ''.join([
            octet.hex.rjust(2, '0')
            for octet in self._address
        ])
        colon_ipv6 = ':'.join([ipv6_string[index: index + 4] for index in range(0, len(ipv6_string), 4)])
        return str(ipaddress.IPv6Address(colon_ipv6))

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv6 address object for debugging.

        Returns:
        str
            A string showing the internal representation of the IPv6 address.
        """
        return f"""IPv6Addr('_address={self._address})"""


class IPMask(IPAddr):

    """
    A concrete class that implements mask functionality for IP addresses.
    This class extends the abstract base class IPAddr and provides an additional method
    to retrieve the mask size. It does not directly represent an IP address but
    rather the network mask associated with an IP address.

    Methods:
    _validate(address: Any) -> None:
        Abstract method to validate if the given address is a valid network mask.

    get_mask_size() -> str:
        Abstract method to return the size of the network mask in the form of a string.
    """
    @abstractmethod
    def _validate(self, address: Any) -> None:
        """
        Abstract method to validate the provided network mask.
        Subclasses should implement this to ensure the network mask is valid.

        Parameters:
        address : Any
            The network mask to be validated, provided in any format (e.g., CIDR or dotted decimal).
        """
        pass

    @abstractmethod
    def get_mask_size(self) -> str:
        """
        Abstract method to return the size of the network mask in bits.
        Subclasses should implement this to return the mask size (e.g., "24" for a /24 mask).

        Returns:
        str:
            A string representing the size of the network mask in bits.
        """
        pass


class IPv4NetMask(IPMask, IPv4Addr):

    """
    A class that represents an IPv4 network mask, inheriting from both IPNetMask and IPv4Addr.
    This class implements the validation, size calculation, and binary representation of the IPv4 network mask.

    Methods:
    _validate(address: Any) -> None:
        Validates the given network mask to ensure it is a valid IPv4 netmask.

    get_mask_size() -> int:
        Returns the size of the network mask by counting the number of '1' bits in its binary representation.

    __repr__() -> str:
        Returns the official string representation of the IPv4 network mask, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided IPv4 netmask. If valid, the netmask is converted into a list of octets;
        otherwise, raises a ValueError.

        Parameters:
        address : Any
            The network mask to be validated, in string or other format (e.g., "255.255.255.0" or CIDR notation).

        Raises:
        ValueError:
            If the provided address is not a valid IPv4 netmask.
        """
        if IPTypeClassifier.classify_ipv4_netmask(address) == IPType.IPv4:
            self._address = IPConverter.convert_to_ipv4_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv4 netmask.")

    def get_mask_size(self) -> int:
        """
        Returns the size of the IPv4 network mask by counting the number of '1' bits in its binary string representation.

        Returns:
        int:
            The number of '1' bits in the binary representation of the netmask, which corresponds to the network size.
        """
        return self.binary_string.count('1')

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv4 network mask object for debugging.

        Returns:
        str:
            A string showing the internal representation of the IPv4 network mask.
        """
        return f"""IPv4NetMask('_address={self._address})"""


class IPv4WildCard(IPv4NetMask):
    """
    A class that represents an IPv4 wildcard mask, inheriting from both IPv4NetMask and IPAddr.
    A wildcard mask is used in networking to define ranges in IP addresses. This class implements
    the validation, size calculation, and string representation of the wildcard mask.

    Methods:
    _validate(address: Any) -> None:
        Validates the given wildcard mask to ensure it is a valid IPv4 wildcard mask.

    get_mask_size() -> int:
        Returns the wildcard mask size by calculating the number of possible IPs based on
        the count of '1' bits in its binary string.

    __repr__() -> str:
        Returns the official string representation of the IPv4 wildcard mask, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided IPv4 wildcard mask. If valid, the mask is converted into
        a list of octets; otherwise, raises a ValueError.

        Parameters:
        address : Any
            The wildcard mask to be validated, in string or other format.

        Raises:
        ValueError:
            If the provided address is not a valid IPv4 wildcard mask.
        """
        if IPTypeClassifier.classify_ipv4_address(address) == IPType.IPv4:
            self._address = IPConverter.convert_to_ipv4_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv4 wildcard mask.")

    def get_mask_size(self) -> int:
        """
        Returns the size of the wildcard mask by counting the number of '1' bits in the binary
        string and calculating the number of possible IP addresses. The number of IP addresses
        is 2 raised to the power of the count of '1' bits.

        Returns:
        int:
            The number of possible IP addresses the wildcard mask covers.
        """
        count_of_ones = self.binary_string.count('1')
        return 2 ** count_of_ones

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv4 wildcard mask object for debugging.

        Returns:
        str:
            A string showing the internal representation of the IPv4 wildcard mask.
        """
        return f"""IPv4WildCard('_address={self._address})"""


class IPv6NetMask(IPMask, IPv6Addr):
    """
    A class that represents an IPv6 network mask, inheriting from both IPNetMask and IPv6Addr.
    This class handles the validation, size calculation, and binary representation of the IPv6 network mask.

    Methods:
    _validate(address: Any) -> None:
        Validates the given network mask to ensure it's a valid IPv6 netmask.

    get_mask_size() -> int:
        Returns the size of the network mask by counting the number of '1' bits in its binary representation.

    __repr__() -> str:
        Returns the official string representation of the IPv6 network mask, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided IPv6 netmask. If valid, the netmask is converted into a list of octets;
        otherwise, raises a ValueError.

        Parameters:
        address : Any
            The network mask to be validated, in string or other format (e.g., in hexadecimal or CIDR notation).

        Raises:
        ValueError:
            If the provided address is not a valid IPv6 netmask.
        """
        if IPTypeClassifier.classify_ipv6_netmask(address) == IPType.IPv6:
            self._address = IPConverter.convert_to_ipv6_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv6 netmask.")

    def get_mask_size(self) -> int:
        """
        Returns the size of the IPv6 network mask by counting the number of '1' bits in its binary representation.
        The size of the mask determines the number of bits used for the network portion of the address.

        Returns:
        int:
            The number of '1' bits in the binary representation of the netmask, which corresponds to the network size.
        """
        return self.binary_string.count('1')

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv6 network mask object for debugging.

        Returns:
        str:
            A string showing the internal representation of the IPv6 network mask.
        """
        return f"""IPv6NetMask('_address={self._address})"""


class IPv6WildCard(IPv6NetMask):

    """
    A class that represents an IPv6 wildcard mask, inheriting from both IPv6NetMask and IPAddr.
    A wildcard mask is used to specify ranges of IP addresses for matching purposes in networking,
    where '1' bits represent "don't care" positions. This class handles validation, size calculation,
    and binary representation of the IPv6 wildcard mask.

    Methods:
    _validate(address: Any) -> None:
        Validates the given wildcard mask to ensure it is a valid IPv6 wildcard mask.

    get_mask_size() -> int:
        Returns the wildcard mask size by calculating the number of possible IPs based on
        the count of '1' bits in its binary string.

    __repr__() -> str:
        Returns the official string representation of the IPv6 wildcard mask, used for debugging.
    """
    def _validate(self, address: Any) -> None:
        """
        Validates the provided IPv6 wildcard mask. If valid, the mask is converted into
        a list of octets; otherwise, raises a ValueError.

        Parameters:
        address : Any
            The wildcard mask to be validated, in string or other format.

        Raises:
        ValueError:
            If the provided address is not a valid IPv6 wildcard mask.
        """
        if IPTypeClassifier.classify_ipv6_address(address) == IPType.IPv6:
            self._address = IPConverter.convert_to_ipv6_octets(address)
        else:
            raise ValueError(str(address) + " is not a valid IPv6 wildcard mask.")

    def get_mask_size(self) -> int:
        """
        Returns the size of the wildcard mask by counting the number of '1' bits in the binary
        string and calculating the number of possible IP addresses. The number of IP addresses
        is 2 raised to the power of the count of '1' bits.

        Returns:
        int:
            The number of possible IP addresses the wildcard mask covers.
        """
        count_of_ones = self.binary_string.count('1')
        return 2 ** count_of_ones

    def __repr__(self) -> str:
        """
        Returns the official string representation of the IPv6 wildcard mask object for debugging.

        Returns:
        str:
            A string showing the internal representation of the IPv6 wildcard mask.
        """
        return f"""IPv6WildCard('_address={self._address})"""
