from __future__ import annotations

import copy
import itertools
from abc import ABC, abstractmethod
from typing import Generator, List, Any, Union

from ttlinks.common.tools.network import BinaryTools
from ttlinks.ipservice import ip_subnet_type_classifiers
from ttlinks.ipservice.ip_addr_type_classifiers import IPAddrTypeClassifier
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv6Addr, IPv6NetMask
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler, BinaryDigitsIPv6ConverterHandler, DecimalIPv4ConverterHandler, \
    DecimalIPv6ConverterHandler
from ttlinks.ipservice.ip_format_standardizer import IPStandardizer


class InterfaceIPConfig(ABC):
    """
    Abstract base class for IP configuration. It defines the structure for storing and managing
    an IP address and its associated mask, supporting both IPv4 and IPv6.

    Attributes:
    _addr: Union[IPv4Addr, IPv6Addr, None]
        - The IP address (IPv4 or IPv6) associated with the interface.
    _mask: Union[IPv4NetMask, IPv6NetMask, None]
        - The subnet mask (IPv4 or IPv6) associated with the interface.

    Methods:
    - _initialize: Abstract method to initialize the IP configuration.
    - _validate: Abstract method to validate the provided IP and mask.
    - __str__: Abstract method to represent the configuration as a string.
    - __repr__: Abstract method for a detailed string representation of the configuration.
    """
    _addr: Union[IPv4Addr, IPv6Addr, None] = None
    _mask: Union[IPv4NetMask, IPv6NetMask, None] = None

    @abstractmethod
    def _initialize(self, *args) -> None:
        """
        Abstract method to initialize the IP configuration.

        Parameters:
        *args: Positional arguments required to set up the IP configuration.
        """
        pass

    @abstractmethod
    def _validate(self, *args) -> None:
        """
        Abstract method to validate the IP address and mask.

        Parameters:
        *args: Positional arguments containing the IP address and mask to validate.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Abstract method to provide a string representation of the IP configuration.

        Returns:
        str: A human-readable representation of the IP configuration.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        Abstract method to provide a detailed string representation of the IP configuration.

        Returns:
        str: A detailed representation of the IP configuration.
        """
        pass


class InterfaceIPv4Config(InterfaceIPConfig, ABC):
    """
    Abstract class for IPv4 interface configuration. It extends `InterfaceIPConfig` to
    manage IPv4-specific configurations, including the IPv4 address and subnet mask.

    Properties:
    - addr: Returns the IPv4 address associated with the interface.
    - mask: Returns the IPv4 subnet mask associated with the interface.

    Methods:
    - __str__: Provides a string representation of the IPv4 configuration in CIDR notation.
    - __repr__: Provides a detailed string representation of the IPv4 configuration.
    """

    @property
    def addr(self) -> IPv4Addr:
        """
        Returns the IPv4 address of the interface.

        Returns:
        IPv4Addr: The IPv4 address associated with the interface.
        """
        return self._addr

    @property
    def mask(self) -> IPv4NetMask:
        """
        Returns the IPv4 subnet mask of the interface.

        Returns:
        IPv4NetMask: The IPv4 subnet mask associated with the interface.
        """
        return self._mask

    def __str__(self) -> str:
        """
        Provides a string representation of the IPv4 configuration in CIDR notation.

        Returns:
        str: The IPv4 address and subnet mask in CIDR format (e.g., "192.168.1.1/24").
        """
        return f"{self.addr.address}/{self.mask.mask_size}"

    def __repr__(self):
        """
        Provides a detailed string representation of the IPv4 configuration.

        Returns:
        str: The detailed IPv4 configuration in the format
             "InterfaceIPv4Config(<address>/<mask_size>)".
        """
        return f"InterfaceIPv4Config({self.addr.address}/{self.mask.mask_size})"


class IPv4HostConfig(InterfaceIPv4Config):
    """
    Represents an IPv4 host configuration, including attributes such as network ID,
    broadcast IP, and host type classification. Extends `InterfaceIPv4Config`.
    """
    _ip_type: IPv4AddrType = IPv4AddrType.UNDEFINED_TYPE
    _broadcast_ip: IPv4Addr = None
    _network_id: IPv4Addr = None

    def __init__(self, *args):
        self._validate(*args)
        self._initialize(*args)

    def _validate(self, *args) -> None:
        validation_result = IPStandardizer.ipv4_interface(*args)
        if validation_result:
            self._addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv4 Interface object")

    def _initialize(self, *args) -> None:
        self._calculate_network_id()
        self._calculate_broadcast_ip()
        self._classify_ip_address_type()

    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID by applying the subnet mask to the IP address.
        """
        decimal_network_id = self._addr.as_decimal & self._mask.as_decimal
        self._network_id = IPv4Addr(DecimalIPv4ConverterHandler().handle(decimal_network_id))

    def _calculate_broadcast_ip(self) -> None:
        """
        Calculates the broadcast IP by reversing the subnet mask and applying it to the IP address.
        """
        reversed_mask = ~self._mask.as_decimal & 0xFFFFFFFF
        self._broadcast_ip = IPv4Addr(DecimalIPv4ConverterHandler().handle(self._addr.as_decimal | reversed_mask))

    def _classify_ip_address_type(self) -> None:
        """
        Classifies the type of the IP address (e.g., PRIVATE, PUBLIC, MULTICAST).
        """
        self._ip_type = IPAddrTypeClassifier.classify_ipv4_host_type(self.network_id)

    @property
    def network_id(self) -> IPv4Addr:
        """
        Returns the calculated network ID.

        Returns:
        IPv4Addr: The network ID of the configuration.
        """
        return self._network_id

    @property
    def broadcast_ip(self) -> IPv4Addr:
        """
        Returns the calculated broadcast IP.

        Returns:
        IPv4Addr: The broadcast IP of the configuration.
        """
        return self._broadcast_ip

    @property
    def ip_type(self) -> IPv4AddrType:
        """
        Returns the classified type of the IP address.

        Returns:
        IPv4AddrType: The type of the IP address (e.g., PUBLIC, PRIVATE).
        """
        return self._ip_type

    @property
    def total_hosts(self) -> int:
        """
        Calculates the total number of total hosts in the network.

        Returns:
        int: The number of total hosts, or 0 for networks with no total hosts.
        """
        netmask_host_bit_count = list(self.mask.binary_digits).count(0)
        host_count = 2 ** netmask_host_bit_count
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def usable_hosts(self) -> int:
        """
        Calculates the total number of usable hosts in the network.

        Returns:
        int: The number of usable hosts, or 0 for networks with no usable hosts.
        """
        netmask_host_bit_count = list(self.mask.binary_digits).count(0)
        host_count = (2 ** netmask_host_bit_count) - 2
        if host_count > 0:
            return host_count
        elif netmask_host_bit_count == 1:
            return 2
        else:
            return 1

    @property
    def is_unspecified(self) -> bool:
        """
        Checks if the IP address is unspecified.

        Returns:
        bool: True if the IP address is unspecified, otherwise False.
        """
        return self._ip_type == IPv4AddrType.UNSPECIFIED

    @property
    def is_public(self) -> bool:
        """
        Checks if the IP address is public.

        Returns:
        bool: True if the IP address is public, otherwise False.
        """
        return self._ip_type == IPv4AddrType.PUBLIC

    @property
    def is_private(self) -> bool:
        """
        Checks if the IP address is private.

        Returns:
        bool: True if the IP address is private, otherwise False.
        """
        return self.ip_type == IPv4AddrType.PRIVATE

    @property
    def is_multicast(self) -> bool:
        """
        Checks if the IP address is multicast.

        Returns:
        bool: True if the IP address is multicast, otherwise False.
        """
        return self.ip_type == IPv4AddrType.MULTICAST

    @property
    def is_link_local(self) -> bool:
        """
        Checks if the IP address is link-local.

        Returns:
        bool: True if the IP address is link-local, otherwise False.
        """
        return self.ip_type == IPv4AddrType.LINK_LOCAL

    @property
    def is_loopback(self) -> bool:
        """
        Checks if the IP address is a loopback address.

        Returns:
        bool: True if the IP address is loopback, otherwise False.
        """
        return self.ip_type == IPv4AddrType.LOOPBACK

    def __repr__(self):
        """
        Provides a detailed string representation of the IPv4 host configuration.

        Returns:
        str: The IPv4 configuration in the format "IPv4HostConfig(<address>/<mask_size>)".
        """
        return f"IPv4HostConfig({self.addr.address}/{self.mask.mask_size})"


class IPv4SubnetConfig(IPv4HostConfig):
    """
    Represents an IPv4 subnet configuration, extending `IPv4HostConfig` to provide additional
    subnet-specific properties and methods, such as host range, subnet division, and merging.

    Methods:
    - first_host: Returns the first usable host in the subnet.
    - last_host: Returns the last usable host in the subnet.
    - subnet_range: Returns the range of the subnet (network ID and broadcast IP).
    - ip_type: Returns the classifications of the subnet's IP types.
    - get_hosts: Generates all usable host addresses within the subnet.
    - is_within: Checks if a given IP address belongs to the subnet.
    - division: Splits the subnet into smaller subnets with a given mask size.
    - merge: Merges the current subnet with other compatible subnets into a larger subnet.
    """
    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID and sets the address (`_addr`) to the network ID.

        Overrides:
        IPv4HostConfig._calculate_network_id
        """
        super()._calculate_network_id()
        self._addr = self.network_id

    @property
    def first_host(self) -> IPv4Addr:
        """
        Returns the first usable host in the subnet.

        Special Cases:
        - /32: Raises a ValueError because there are no usable hosts.
        - /31: Returns the network ID as the first host.

        Returns:
        IPv4Addr: The first usable host in the subnet.
        """
        if self.mask.mask_size == 32:
            raise ValueError('No hosts available for a /32 subnet')
        if self.mask.mask_size == 31:
            return self.network_id
        else:
            host_iterator = self.get_hosts()
            return next(host_iterator)

    @property
    def last_host(self) -> IPv4Addr:
        """
        Returns the last usable host in the subnet.

        Special Cases:
        - /32: Raises a ValueError because there are no usable hosts.
        - /31: Returns the broadcast IP as the last host.

        Returns:
        IPv4Addr: The last usable host in the subnet.
        """
        if self.mask.mask_size == 32:
            raise ValueError('No hosts available for a /32 subnet')
        if self.mask.mask_size == 31:
            return self.broadcast_ip
        else:
            return IPv4Addr(DecimalIPv4ConverterHandler().handle(self.broadcast_ip.as_decimal - 1))

    @property
    def subnet_range(self) -> List[IPv4Addr]:
        """
        Returns the range of the subnet, including the network ID and broadcast IP.

        Returns:
        List[IPv4Addr]: A list containing the network ID and broadcast IP.
        """
        return [self.network_id, self.broadcast_ip]

    @property
    def ip_type(self) -> List[IPv4AddrType]:
        """
        Returns the classifications of the subnet's IP types.

        Returns:
        List[IPv4AddrType]: A list of classifications for all possible IP types in the subnet.
        """
        return ip_subnet_type_classifiers.IPSubnetTypeClassifier.classify_ipv4_subnet_types(self)

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generates all usable host addresses within the subnet.

        Returns:
        Generator[IPv4Addr, None, None]: A generator yielding IPv4 host addresses.
        """
        ip_decimal_range = range(self.network_id.as_decimal + 1, self.broadcast_ip.as_decimal)
        for ip_decimal in ip_decimal_range:
            yield IPv4Addr(DecimalIPv4ConverterHandler().handle(ip_decimal))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks if a given IP address belongs to the subnet.

        Parameters:
        ip_addr: Any
            - The IP address to check.

        Returns:
        bool: True if the IP address is within the subnet, otherwise False.
        """
        compared_addr = IPv4Addr(ip_addr)
        return BinaryTools.is_bytes_in_range(
            self.network_id.as_bytes,
            self.mask.as_bytes,
            compared_addr.as_bytes
        )

    def division(self, target_mask_size: int) -> List[IPv4SubnetConfig]:
        """
        Divides the subnet into smaller subnets of the specified mask size.

        Parameters:
        target_mask_size: int
            - The mask size for the new subnets.

        Returns:
        List[IPv4SubnetConfig]: A list of smaller subnets.

        Raises:
        TypeError: If the target mask size is not an integer.
        ValueError: If the target mask size is not larger than the current mask size or exceeds 32.
        """
        subnet_mask_size = self.mask.mask_size
        if type(target_mask_size) is not int:
            raise TypeError('target mask must be an integer')
        if target_mask_size <= subnet_mask_size or target_mask_size > 32:
            raise ValueError(f'target mask must be in the range of {subnet_mask_size + 1}-32')
        target_mask = IPv4NetMask(f"/{target_mask_size}")
        mask_diff = target_mask.mask_size - subnet_mask_size
        target_host_bit_count = list(target_mask.binary_digits).count(0)
        for mask_change in range(2 ** mask_diff):
            new_network_id = (mask_change << target_host_bit_count) | self.network_id.as_decimal
            yield IPv4SubnetConfig(IPv4Addr(DecimalIPv4ConverterHandler().handle(new_network_id)), target_mask)

    def merge(self, *subnets: str) -> IPv4SubnetConfig:
        """
        Merges the current subnet with other compatible subnets into a larger subnet.

        Parameters:
        *subnets: str
            - The subnets to merge, provided as strings.

        Returns:
        IPv4SubnetConfig: The merged subnet.

        Raises:
        ValueError: If the subnets cannot be merged.
        """
        # Convert input subnet strings into IPv4SubnetConfig objects
        subnets = [IPv4SubnetConfig(subnet) for subnet in subnets]

        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)

        # Find the largest and smallest mask sizes among the given subnets
        existing_largest_mask = max([subnet.mask.mask_size for subnet in subnets_need_merge])
        existing_smallest_mask = min([subnet.mask.mask_size for subnet in subnets_need_merge])

        # Initialize target_mask_size to -1 as a placeholder
        target_mask_size = -1

        # Determine the target mask size by examining the network ID bits of all subnets
        for index, network_id_bit in enumerate(zip(*[subnet.network_id.binary_string for subnet in subnets_need_merge])):
            if len(set(network_id_bit)) > 1:
                # If there are differing bits at the current position, the target mask size is reached
                break
            elif index == existing_smallest_mask:
                # If we reach the smallest mask size and all bits match, the smallest mask size is sufficient
                break
            # Increment the target mask size with each matching bit
            target_mask_size = index + 1

        # Calculate the number of bits required to cover the range between the largest and target mask sizes
        repeat = existing_largest_mask - target_mask_size

        # Generate all possible bit combinations for the range of bits required to merge the subnets
        required_bit_combo_for_merge = set([''.join(bit_combo) for bit_combo in itertools.product('01', repeat=repeat)])

        # Initialize a set to store the actual bit combinations found in the subnets
        existing_bit_combos = set()

        # Collect the actual bit combinations present in the subnets
        for subnet in subnets_need_merge:
            # Expand the network ID bits based on the mask size range to identify all covered combinations
            subnet_bit_combo = [''.join(map(str, t)) for t in BinaryTools.expand_by_mask(
                list(subnet.network_id.binary_digits)[target_mask_size: existing_largest_mask],
                list(subnet.mask.binary_digits)[target_mask_size: existing_largest_mask]
            )]
            # Add the resulting combinations to the existing bit combos set
            existing_bit_combos.update(subnet_bit_combo)

        # Check if the actual bit combinations match the required combinations for merging
        if existing_bit_combos == required_bit_combo_for_merge:
            # If all required combinations are covered, create a new merged subnet
            new_network_id = copy.deepcopy(subnets_need_merge[0].network_id)  # Use the network ID of the first subnet
            new_mask = IPv4NetMask(f"/{target_mask_size}")  # Create a mask with the target mask size
            return IPv4SubnetConfig(new_network_id, new_mask)  # Return the new merged subnet
        else:
            # If the subnets cannot be merged, raise an error
            raise ValueError('The subnets cannot be merged')

    def __repr__(self):
        return f"IPv4SubnetConfig({self.addr.address}/{self.mask.mask_size})"


class IPv4WildCardConfig(InterfaceIPv4Config):
    """
    Represents an IPv4 wildcard configuration, which includes handling wildcard masks and
    operations related to generating hosts or checking membership within a wildcard-based range.

    Methods:
    - _initialize: Recalculates the address based on the wildcard mask.
    - _validate: Validates and standardizes the input IPv4 address and wildcard mask.
    - _recalculate_addr: Recalculates the IP address by applying the wildcard mask.
    - total_hosts: Calculates the total number of addresses in the wildcard range.
    - get_hosts: Generates all addresses covered by the wildcard configuration.
    - is_within: Checks if a given IP address falls within the wildcard configuration range.
    """
    def __init__(self, *args):
        self._validate(*args)
        self._initialize(*args)

    def _initialize(self, *args) -> None:
        self._recalculate_addr()

    def _validate(self, *args) -> None:
        validation_result = IPStandardizer.ipv4_wildcard(*args)
        if validation_result:
            self._addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv4 wildcard object")

    def _recalculate_addr(self):
        """
        Recalculates the address by applying the wildcard mask to the current address.

        For wildcard bits (mask=1), the address bit is set to 0.
        For fixed bits (mask=0), the corresponding address bit is preserved.
        """
        mapped_binary_digits = []
        index = 0
        for mask_bit in self.mask.binary_digits:
            if mask_bit == 1:
                mapped_binary_digits.append(0)
            elif mask_bit == 0:
                mapped_binary_digits.append(list(self._addr.binary_digits)[index])
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._addr = IPv4Addr(binary_bit_ipv4_converter.handle(mapped_binary_digits))

    @property
    def total_hosts(self) -> int:
        """
        Calculates the total number of addresses in the wildcard range.

        Returns:
        int: The total number of addresses represented by the wildcard configuration.
        """
        wildcard_host_bit_count = list(self.mask.binary_digits).count(1)
        host_count = (2 ** wildcard_host_bit_count)
        return host_count

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generates all addresses covered by the wildcard configuration.

        Returns:
        Generator[IPv4Addr, None, None]: A generator yielding all possible IPv4 addresses in the range.
        """
        addr_binary_digits = list(self.addr.binary_digits)
        mask_binary_digits = list(self.mask.binary_digits)
        match_bit_index = []
        binary_digits_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        for mask_i, mask_bit in enumerate(mask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv4Addr(binary_digits_ipv4_converter.handle(addr_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks if a given IP address falls within the wildcard configuration range.

        Parameters:
        ip_addr: Any
            - The IP address to check.

        Returns:
        bool: True if the IP address is within the wildcard range, otherwise False.

        Raises:
        TypeError: If the provided IP address is not an `IPv4Addr` object.
        """
        ip_addr = IPv4Addr(ip_addr)
        if type(ip_addr) is not IPv4Addr:
            raise TypeError('ip_addr must be an IPv4Addr object')
        wildcard_ip_addr_binary_digits = list(self.addr.binary_digits)
        validate_ip_addr_binary_digits = list(ip_addr.binary_digits)
        wildcard_mask_binary_digits = list(self.mask.binary_digits)
        match_validation = []
        for mask_i, wildcard_mask_bit in enumerate(wildcard_mask_binary_digits):
            if wildcard_mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        Returns a string representation of the IPv4 wildcard configuration.

        Returns:
        str: A string showing the address and wildcard mask (e.g., "192.168.0.0 0.0.255.255").
        """
        return f"{str(self.addr)} {str(self.mask)}"

    def __repr__(self):
        """
        Returns a detailed string representation of the IPv4 wildcard configuration.

        Returns:
        str: A string in the format "IPv4WildCardConfig(<address> <wildcard_mask>)".
        """
        return f"IPv4WildCardConfig({self.__str__()})"


class InterfaceIPv6Config(InterfaceIPConfig, ABC):
    """
    Abstract class for IPv6 interface configuration. Extends `InterfaceIPConfig`
    to handle IPv6-specific configurations, including the IPv6 address and subnet mask.

    Properties:
    - addr: Returns the IPv6 address associated with the interface.
    - mask: Returns the IPv6 subnet mask associated with the interface.

    Methods:
    - __str__: Provides a string representation of the IPv6 configuration in CIDR notation.
    - __repr__: Provides a detailed string representation of the IPv6 configuration.
    """

    @property
    def addr(self) -> IPv6Addr:
        """
        Returns the IPv6 address of the interface.

        Returns:
        IPv6Addr: The IPv6 address associated with the interface.
        """
        return self._addr

    @property
    def mask(self) -> IPv6NetMask:
        """
        Returns the IPv6 subnet mask of the interface.

        Returns:
        IPv6NetMask: The IPv6 subnet mask associated with the interface.
        """
        return self._mask

    def __str__(self) -> str:
        """
        Provides a string representation of the IPv6 configuration in CIDR notation.

        Returns:
        str: The IPv6 address and subnet mask in CIDR format (e.g., "2001:db8::/64").
        """
        return f"{str(self.addr)}/{str(self.mask.mask_size)}"

    def __repr__(self):
        """
        Provides a detailed string representation of the IPv6 configuration.

        Returns:
        str: A detailed IPv6 configuration in the format
             "InterfaceIPv6Config(<address>/<mask_size>)".
        """
        return f"InterfaceIPv6Config({self.addr.address}/{self.mask.mask_size})"


class IPv6HostConfig(InterfaceIPv6Config):
    """
    Represents an IPv6 host configuration, including attributes like network ID
    and host type classification. Extends `InterfaceIPv6Config`.

    Properties:
    - network_id: Returns the calculated network ID.
    - ip_type: Returns the classification type of the IPv6 address.
    - total_hosts: Calculates the total number of addresses in the subnet.
    - is_unspecified: Checks if the IPv6 address is unspecified.
    - is_loopback: Checks if the IPv6 address is a loopback address.
    - is_multicast: Checks if the IPv6 address is a multicast address.
    - is_link_local: Checks if the IPv6 address is a link-local address.
    - is_global_unicast: Checks if the IPv6 address is a global unicast address.

    Methods:
    - _validate: Validates and standardizes the input IPv6 address and subnet mask.
    - _initialize: Initializes the configuration by calculating the network ID and classifying the IP type.
    - _calculate_network_id: Computes the network ID by applying the subnet mask to the address.
    - _classify_ip_address_type: Classifies the IPv6 address type.
    """
    _ip_type: IPv6AddrType = IPv6AddrType.UNDEFINED_TYPE
    _network_id: IPv6Addr = None

    def __init__(self, *args):
        self._validate(*args)
        self._initialize(*args)

    def _validate(self, *args) -> None:
        validation_result = IPStandardizer.ipv6_interface(*args)
        if validation_result:
            self._addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv6 Interface object")

    def _initialize(self, *args) -> None:
        self._calculate_network_id()
        self._classify_ip_address_type()

    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID by applying the subnet mask to the IPv6 address.
        """
        decimal_network_id = self._addr.as_decimal & self._mask.as_decimal
        self._network_id = IPv6Addr(DecimalIPv6ConverterHandler().handle(decimal_network_id))

    def _classify_ip_address_type(self) -> None:
        """
        Classifies the IPv6 address type (e.g., GLOBAL_UNICAST, LINK_LOCAL).
        """
        self._ip_type = IPAddrTypeClassifier.classify_ipv6_host_type(self.network_id)

    @property
    def network_id(self) -> IPv6Addr:
        """
        Returns the calculated network ID.

        Returns:
        IPv6Addr: The network ID of the configuration.
        """
        return self._network_id

    @property
    def ip_type(self) -> IPv6AddrType:
        """
        Returns the classified type of the IPv6 address.

        Returns:
        IPv6AddrType: The type of the IPv6 address (e.g., GLOBAL_UNICAST, LINK_LOCAL).
        """
        return self._ip_type

    @property
    def total_hosts(self) -> int:
        """
        Calculates the total number of addresses in the subnet.

        Returns:
        int: The total number of addresses in the subnet.
        """
        netmask_host_bit_count = list(self.mask.binary_digits).count(0)
        host_count = 2 ** netmask_host_bit_count
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def is_unspecified(self) -> bool:
        """
        Checks if the IPv6 address is unspecified.

        Returns:
        bool: True if the IPv6 address is unspecified, otherwise False.
        """
        return self._ip_type == IPv6AddrType.UNSPECIFIED

    @property
    def is_loopback(self) -> bool:
        """
        Checks if the IPv6 address is a loopback address.

        Returns:
        bool: True if the IPv6 address is a loopback address, otherwise False.
        """
        return self.ip_type == IPv6AddrType.LOOPBACK

    @property
    def is_multicast(self) -> bool:
        """
        Checks if the IPv6 address is a multicast address.

        Returns:
        bool: True if the IPv6 address is multicast, otherwise False.
        """
        return self.ip_type == IPv6AddrType.MULTICAST

    @property
    def is_link_local(self) -> bool:
        """
        Checks if the IPv6 address is a link-local address.

        Returns:
        bool: True if the IPv6 address is link-local, otherwise False.
        """
        return self.ip_type == IPv6AddrType.LINK_LOCAL

    @property
    def is_global_unicast(self) -> bool:
        """
        Checks if the IPv6 address is a global unicast address.

        Returns:
        bool: True if the IPv6 address is global unicast, otherwise False.
        """
        return self._ip_type == IPv6AddrType.GLOBAL_UNICAST

    def __repr__(self):
        """
        Provides a detailed string representation of the IPv6 host configuration.

        Returns:
        str: The IPv6 configuration in the format "IPv6HostConfig(<address>/<mask_size>)".
        """
        return f"IPv6HostConfig({self.addr.address}/{self.mask.mask_size})"


class IPv6SubnetConfig(IPv6HostConfig):
    """
    Represents an IPv6 subnet configuration, extending `IPv6HostConfig` to provide
    subnet-specific functionalities such as host range, subnet division, and merging.

    Methods:
    - _calculate_network_id: Calculates and assigns the network ID.
    - first_host: Returns the first usable host in the subnet.
    - last_host: Returns the last usable host in the subnet.
    - ip_type: Returns the classifications of the subnet's IP types.
    - subnet_range: Returns the range of the subnet (network ID and last host).
    - get_hosts: Generates all addresses within the subnet.
    - is_within: Checks if a given IP address belongs to the subnet.
    - division: Divides the subnet into smaller subnets with a specified mask size.
    - merge: Merges the current subnet with other compatible subnets.
    """

    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID and sets the address (`_addr`) to the network ID.

        Overrides:
        IPv6HostConfig._calculate_network_id
        """
        super()._calculate_network_id()
        self._addr = self._network_id

    @property
    def first_host(self) -> IPv6Addr:
        """
        Returns the first usable host in the subnet.

        Returns:
        IPv6Addr: The first host address in the subnet.
        """
        host_iterator = self.get_hosts()
        return next(host_iterator)

    @property
    def last_host(self) -> IPv6Addr:
        """
        Returns the last usable host in the subnet.

        Returns:
        IPv6Addr: The last host address in the subnet.
        """
        reversed_mask = ~self.mask.as_decimal & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        return IPv6Addr(DecimalIPv6ConverterHandler().handle(self.addr.as_decimal | reversed_mask))

    @property
    def subnet_range(self) -> list[IPv6Addr]:
        """
        Returns the range of the subnet, including the network ID and the last host.

        Returns:
        list[IPv6Addr]: A list containing the network ID and the last host.
        """
        return [self.network_id, self.last_host]

    @property
    def ip_type(self) -> List[IPv6AddrType]:
        """
        Returns the classifications of the subnet's IP types.

        Returns:
        List[IPv6AddrType]: A list of classifications for all possible IP types in the subnet.
        """
        return ip_subnet_type_classifiers.IPSubnetTypeClassifier.classify_ipv6_subnet_types(self)

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generates all addresses within the subnet.

        Returns:
        Generator[IPv6Addr, None, None]: A generator yielding IPv6 addresses within the subnet.
        """
        ip_decimal_range = range(self.network_id.as_decimal, self.last_host.as_decimal + 1)
        for ip_decimal in ip_decimal_range:
            yield IPv6Addr(DecimalIPv6ConverterHandler().handle(ip_decimal))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks if a given IP address belongs to the subnet.

        Parameters:
        ip_addr: Any
            - The IP address to check.

        Returns:
        bool: True if the IP address is within the subnet, otherwise False.
        """
        compared_addr = IPv6Addr(ip_addr)
        return BinaryTools.is_bytes_in_range(
            self.network_id.as_bytes,
            self.mask.as_bytes,
            compared_addr.as_bytes
        )

    def division(self, target_mask_size: int) -> List[IPv6SubnetConfig]:
        """
        Divides the subnet into smaller subnets with the specified mask size.

        Parameters:
        target_mask_size: int
            - The desired mask size for the new subnets.

        Returns:
        List[IPv6SubnetConfig]: A list of smaller subnets.

        Raises:
        TypeError: If the target mask size is not an integer.
        ValueError: If the target mask size is invalid (e.g., smaller than the current mask size).
        """
        subnet_mask_size = self.mask.mask_size
        if type(target_mask_size) is not int:
            raise TypeError('target mask must be an integer')
        if target_mask_size <= subnet_mask_size or target_mask_size > 128:
            raise ValueError(f'target mask must be in the range of {subnet_mask_size + 1}-128')
        target_mask = IPv6NetMask(f"/{target_mask_size}")
        mask_diff = target_mask.mask_size - subnet_mask_size
        target_host_bit_count = list(target_mask.binary_digits).count(0)
        for mask_change in range(2 ** mask_diff):
            new_network_id = (mask_change << target_host_bit_count) | self.network_id.as_decimal
            yield IPv6SubnetConfig(IPv6Addr(DecimalIPv6ConverterHandler().handle(new_network_id)), target_mask)

    def merge(self, *subnets: str) -> IPv6SubnetConfig:
        """
        Merges the current subnet with other compatible subnets into a larger subnet.

        Parameters:
        *subnets: str
            - The subnets to merge, provided as strings.

        Returns:
        IPv6SubnetConfig: The merged subnet.

        Raises:
        ValueError: If the subnets cannot be merged.
        """
        # Convert input subnet strings into IPv6SubnetConfig objects
        subnets = [IPv6SubnetConfig(subnet) for subnet in subnets]

        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)

        # Find the largest and smallest mask sizes among the given subnets
        existing_largest_mask = max([subnet.mask.mask_size for subnet in subnets_need_merge])
        existing_smallest_mask = min([subnet.mask.mask_size for subnet in subnets_need_merge])

        # Initialize target_mask_size to -1 as a placeholder
        target_mask_size = -1

        # Determine the target mask size by examining the network ID bits of all subnets
        for index, network_id_bit in enumerate(zip(*[subnet.network_id.binary_string for subnet in subnets_need_merge])):
            if len(set(network_id_bit)) > 1:
                # If there are differing bits at the current position, the target mask size is reached
                break
            elif index == existing_smallest_mask:
                # If we reach the smallest mask size and all bits match, the smallest mask size is sufficient
                break
            # Increment the target mask size with each matching bit
            target_mask_size = index + 1

        # Calculate the number of bits required to cover the range between the largest and target mask sizes
        repeat = existing_largest_mask - target_mask_size

        # Generate all possible bit combinations for the range of bits required to merge the subnets
        required_bit_combo_for_merge = set([''.join(bit_combo) for bit_combo in itertools.product('01', repeat=repeat)])

        # Initialize a set to store the actual bit combinations found in the subnets
        existing_bit_combos = set()

        # Collect the actual bit combinations present in the subnets
        for subnet in subnets_need_merge:
            # Expand the network ID bits based on the mask size range to identify all covered combinations
            subnet_bit_combo = [''.join(map(str, t)) for t in BinaryTools.expand_by_mask(
                list(subnet.network_id.binary_digits)[target_mask_size: existing_largest_mask],
                list(subnet.mask.binary_digits)[target_mask_size: existing_largest_mask]
            )]
            # Add the resulting combinations to the existing bit combos set
            existing_bit_combos.update(subnet_bit_combo)

        # Check if the actual bit combinations match the required combinations for merging
        if existing_bit_combos == required_bit_combo_for_merge:
            # If all required combinations are covered, create a new merged subnet
            new_network_id = copy.deepcopy(subnets_need_merge[0].network_id)
            new_mask = IPv6NetMask(f"/{target_mask_size}")
            return IPv6SubnetConfig(new_network_id, new_mask)
        else:
            # If the subnets cannot be merged, raise an error
            raise ValueError('The subnets cannot be merged')

    def __repr__(self):
        """
        Provides a detailed string representation of the IPv6 subnet configuration.

        Returns:
        str: The IPv6 configuration in the format "IPv6SubnetConfig(<address>/<mask_size>)".
        """
        return f"IPv6SubnetConfig({self.addr.address}/{self.mask.mask_size})"


class IPv6WildCardConfig(InterfaceIPv6Config):
    """
    Represents an IPv6 wildcard configuration, handling wildcard masks and operations
    related to generating hosts or checking membership within a wildcard-based range.

    Methods:
    - _initialize: Initializes the configuration by recalculating the IPv6 address.
    - _validate: Validates and standardizes the IPv6 wildcard configuration.
    - _recalculate_addr: Recalculates the IPv6 address based on the wildcard mask.
    - total_hosts: Calculates the total number of addresses in the wildcard range.
    - get_hosts: Generates all addresses covered by the wildcard configuration.
    - is_within: Checks if a given IPv6 address falls within the wildcard configuration range.
    """
    def __init__(self, *args):
        self._validate(*args)
        self._initialize(*args)

    def _initialize(self, *args) -> None:
        self._recalculate_addr()

    def _validate(self, *args) -> None:
        validation_result = IPStandardizer.ipv6_wildcard(*args)
        if validation_result:
            self._addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv6 wildcard object")

    def _recalculate_addr(self):
        """
        Recalculates the IPv6 address by applying the wildcard mask to the address.

        For wildcard bits (mask=1), the address bit is set to 0.
        For fixed bits (mask=0), the corresponding address bit is preserved.
        """
        mapped_binary_digits = []
        index = 0
        for mask_bit in self.mask.binary_digits:
            if mask_bit == 1:
                mapped_binary_digits.append(0)
            elif mask_bit == 0:
                mapped_binary_digits.append(list(self._addr.binary_digits)[index])
            index += 1
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        self._addr = IPv6Addr(binary_bit_ipv6_converter.handle(mapped_binary_digits))

    @property
    def total_hosts(self) -> int:
        """
        Calculates the total number of addresses in the wildcard range.

        Returns:
        int: The total number of addresses represented by the wildcard configuration.
        """
        wildcard_host_bit_count = list(self.mask.binary_digits).count(1)
        host_count = (2 ** wildcard_host_bit_count)
        return host_count

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generates all addresses covered by the wildcard configuration.

        Returns:
        Generator[IPv6Addr, None, None]: A generator yielding all possible IPv6 addresses in the range.
        """
        addr_binary_digits = list(self.addr.binary_digits)
        mask_binary_digits = list(self.mask.binary_digits)
        match_bit_index = []
        binary_digits_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        for mask_i, mask_bit in enumerate(mask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv6Addr(binary_digits_ipv6_converter.handle(addr_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks if a given IPv6 address falls within the wildcard configuration range.

        Parameters:
        ip_addr: Any
            - The IPv6 address to check.

        Returns:
        bool: True if the IPv6 address is within the wildcard range, otherwise False.

        Raises:
        TypeError: If the provided IPv6 address is not an `IPv6Addr` object.
        """
        ip_addr = IPv6Addr(ip_addr)
        if type(ip_addr) is not IPv6Addr:
            raise TypeError('ip_addr must be an IPv6Addr object')
        wildcard_ip_addr_binary_digits = list(self.addr.binary_digits)
        validate_ip_addr_binary_digits = list(ip_addr.binary_digits)
        wildcard_mask_binary_digits = list(self.mask.binary_digits)
        match_validation = []
        for mask_i, wildcard_mask_bit in enumerate(wildcard_mask_binary_digits):
            if wildcard_mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        Returns a string representation of the IPv6 wildcard configuration.

        Returns:
        str: A string showing the address and wildcard mask (e.g., "2001:db8:: 0:0:ffff:ffff:ffff:ffff").
        """
        return f"{str(self.addr)} {str(self.mask)}"


    def __repr__(self):
        """
        Returns a detailed string representation of the IPv6 wildcard configuration.

        Returns:
        str: A string in the format "IPv6WildCardConfig(<address> <wildcard_mask>)".
        """
        return f"IPv6WildCardConfig({self.__str__()})"