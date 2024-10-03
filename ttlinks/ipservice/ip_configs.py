from __future__ import annotations

import copy
import itertools
from abc import ABC, abstractmethod
from typing import Generator, List, Any, Union

from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.tools.network import BinaryTools
from ttlinks.ipservice.ip_addr_type_classifiers import IPAddrTypeClassifier
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler, BinaryDigitsIPv6ConverterHandler
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv4WildCard, IPv6Addr, IPv6NetMask, IPv6WildCard
from ttlinks.ipservice.ip_format_standardizer import IPStandardizer
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType


class InterfaceIPConfig(ABC):
    """
    InterfaceIPConfig is an abstract base class (ABC) that defines the structure for configuring IP interfaces.
    It requires any subclass to implement methods for initialization, validation, and string representation.
    This class serves as a blueprint for configuring IP interfaces in both IPv4 and IPv6 formats.

    Methods:
    - _initialize(*args): Initializes the configuration of the interface.
    - _validate(*args): Validates the configuration parameters provided.
    - __str__(): Returns a string representation of the IP configuration.

    Parameters:
    *args: A variable-length argument list that can include specific configuration parameters like IP address and mask.

    Returns:
    None (for abstract methods, implementation is left to subclasses).
    """
    @abstractmethod
    def _initialize(self, *args) -> None:
        """
        Initializes the IP interface configuration. This method is abstract and must be implemented by subclasses.
        It sets up the required parameters such as IP address and mask.

        Parameters:
        *args: Variable-length argument list that contains configuration parameters like IP address, subnet mask, etc.

        Returns:
        None
        """
        pass

    @abstractmethod
    def _validate(self, *args) -> None:
        """
        Validates the provided IP configuration parameters. This method is abstract and must be implemented by subclasses.
        The method checks whether the IP address and mask are correctly formatted and valid.

        Parameters:
        *args: Variable-length argument list that contains IP configuration values to be validated.

        Returns:
        None
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Provides a string representation of the IP configuration. This method is abstract and must be implemented by subclasses.
        It typically returns a formatted string combining IP address and mask/subnet.

        Returns:
        str: A string representation of the IP address and mask, formatted such as "IP/mask" in IPv4 host or subnet
        or "IP Wildcard" for wildcard configuration.
        """
        pass


class InterfaceIPv4Config(InterfaceIPConfig):

    """
    InterfaceIPv4Config provides an abstract structure for configuring IPv4 interfaces. It inherits from InterfaceIPConfig
    and requires subclasses to implement initialization and validation methods. This class stores the IPv4 address and netmask
    and provides access to them through properties.

    Attributes:
    _ip_addr (IPv4Addr): Stores the IPv4 address of the interface.
    _mask (IPv4NetMask): Stores the netmask or wildcard mask associated with the IPv4 address.

    Methods:
    - _initialize(*args): Initializes the IPv4 configuration, requiring subclasses to validate the provided IP address and netmask.
    - _validate(*args): Abstract method for validating the provided IPv4 configuration.
    - ip_addr: Property method that returns the current IPv4 address.
    - mask: Property method that returns the current netmask.
    - __str__(): Returns a string representation of the IPv4 configuration as "IP/Netmask size".

    Parameters:
    *args: Variable-length argument list to provide the necessary configuration parameters (e.g., IPv4 address and netmask).

    Returns:
    None
    """
    def __init__(self, *args):
        """
        Initializes the InterfaceIPv4Config by setting up the IPv4 address and netmask.
        Calls the _initialize method with the provided arguments.

        Parameters:
        *args: Variable-length argument list to initialize the IP address and netmask.

        Returns:
        None
        """
        self._ip_addr: Union[IPv4Addr, None] = None
        self._mask: Union[IPv4NetMask, None] = None
        self._initialize(*args)

    @abstractmethod
    def _initialize(self, *args) -> None:
        """
        Initializes the IPv4 interface configuration. This method is abstract and must be implemented by subclasses.
        It also calls the _validate method to ensure the provided parameters are valid.

        Parameters:
        *args: A variable-length argument list that includes the IP address and netmask for initialization.

        Returns:
        None
        """
        self._validate(*args)

    @abstractmethod
    def _validate(self, *args) -> None:
        """
        Validates the provided IPv4 address and netmask. This method is abstract and must be implemented by subclasses
        to ensure that the input parameters are in the correct format.

        Parameters:
        *args: A variable-length argument list that includes the IP address and netmask for validation.

        Returns:
        None
        """
        pass

    @property
    def ip_addr(self) -> IPv4Addr:
        """
        Returns the currently configured IPv4 address.

        Returns:
        IPv4Addr: The IPv4 address assigned to the interface.
        """
        return self._ip_addr

    @property
    def mask(self) -> IPv4NetMask:
        """
        Returns the currently configured IPv4 netmask.

        Returns:
        IPv4NetMask: The netmask associated with the IPv4 address.
        """
        return self._mask

    def __str__(self) -> str:
        """
        Returns a string representation of the IPv4 configuration.
        The format is "IP/Netmask size", showing the IP address and the length of the netmask.

        Returns:
        str: A string formatted as "IP/Netmask size" (e.g., "192.168.0.1/24").
        """
        return f"{str(self.ip_addr)}/{str(self.mask.get_mask_size())}"


class IPv4HostConfig(InterfaceIPv4Config):
    """
    IPv4HostConfig is a subclass of InterfaceIPv4Config that represents a host configuration for an IPv4 network.
    It includes additional methods for calculating the network ID, broadcast address, and classifying the IP address type.
    This class is used to handle IPv4-specific host configurations, including determining the network range and broadcast address.

    Attributes:
    _ip_type (IPv4AddrType): The type of the IPv4 address (e.g., public, private, multicast).
    _broadcast_ip (IPv4Addr): The broadcast IP address for the configured network.
    _network_id (IPv4Addr): The network ID calculated from the IPv4 address and netmask.

    Methods:
    - _initialize(*args): Initializes the IPv4 host configuration and calculates the network ID, broadcast IP, and IP type.
    - _validate(*args): Validates the provided IPv4 address and netmask.
    - _calculate_network_id(): Calculates the network ID based on the IP address and netmask.
    - _calculate_broadcast_ip(): Calculates the broadcast IP address for the network.
    - _classify_ip_address_type(): Classifies the IP address type (e.g., private, public).
    - broadcast_ip: Returns the broadcast IP address.
    - network_id: Returns the network ID.
    - host_counts: Calculates and returns the number of usable host addresses in the network.
    - ip_type: Returns the classified IP address type.
    - is_unspecified: Checks if the IP type is unspecified.
    - is_public: Checks if the IP type is public.
    - is_private: Checks if the IP type is private.
    - is_multicast: Checks if the IP type is multicast.
    - is_link_local: Checks if the IP type is link-local.
    - is_loopback: Checks if the IP type is a loopback address.
    """
    _ip_type: IPv4AddrType = IPv4AddrType.UNDEFINED_TYPE

    def __init__(self, *args):
        """
        Initializes the IPv4HostConfig class by calling the parent class's initialization and setting up the network-specific
        attributes such as broadcast IP and network ID.

        Parameters:
        *args: Variable-length argument list for the IPv4 address and netmask.

        Returns:
        None
        """
        self._broadcast_ip = None
        self._network_id = None
        super().__init__(*args)

    def _initialize(self, *args) -> None:
        """
        Initializes the IPv4 host configuration by validating the input and calculating
        the network ID, broadcast IP, and IP address type.

        Parameters:
        *args: A variable-length argument list containing the IP address and netmask.

        Returns:
        None
        """
        self._validate(*args)
        self._calculate_network_id()
        self._calculate_broadcast_ip()
        self._classify_ip_address_type()

    def _validate(self, *args) -> None:
        """
        Validates the provided IPv4 address and netmask by using an external standardizer.
        Raises a ValueError if the inputs are not valid.

        Parameters:
        *args: A variable-length argument list containing the IPv4 address and netmask for validation.

        Returns:
        None

        Raises:
        ValueError: If the IPv4 address or netmask is invalid.
        """
        validation_result = IPStandardizer.ipv4_interface(*args)
        if validation_result:
            self._ip_addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv4 object")

    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID for the given IPv4 address and netmask.
        The network ID is derived by applying the netmask to the IP address.

        Returns:
        None
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        network_id_binary_digits = []
        index = 0
        for netmask_bit in self.mask.binary_digits:
            if netmask_bit == 1:
                network_id_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                network_id_binary_digits.append(0)
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._network_id = IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))

    def _calculate_broadcast_ip(self) -> None:
        """
        Calculates the broadcast IP address for the network.
        The broadcast address is derived by setting the host bits to 1 in the IP address.

        Returns:
        None
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        broadcast_binary_digits = []
        index = 0
        for netmask_bit in self.mask.binary_digits:
            if netmask_bit == 1:
                broadcast_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                broadcast_binary_digits.append(1)
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._broadcast_ip = IPv4Addr(binary_bit_ipv4_converter.handle(broadcast_binary_digits))

    def _classify_ip_address_type(self) -> None:
        """
        Classifies the IP address type (e.g., private, public, multicast, etc.)
        by using the IPAddrTypeClassifier.

        Returns:
        None
        """
        self._ip_type = IPAddrTypeClassifier.classify_ipv4_type(self.network_id)

    @property
    def broadcast_ip(self) -> IPv4Addr:
        """
        Returns the broadcast IP address for the configured network.

        Returns:
        IPv4Addr: The broadcast IP address.
        """
        return self._broadcast_ip

    @property
    def network_id(self) -> IPv4Addr:
        """
        Returns the network ID for the configured network.

        Returns:
        IPv4Addr: The network ID.
        """
        return self._network_id

    @property
    def host_counts(self) -> int:
        """
        Calculates the number of usable hosts in the network.
        The number is derived from the netmask, by counting the number of host bits.

        Returns:
        int: The number of usable hosts in the network.
        """
        netmask_host_bit_count = list(self.mask.binary_digits).count(0)
        host_count = (2 ** netmask_host_bit_count) - 2
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def ip_type(self) -> IPv4AddrType:
        """
        Returns the type of the IP address (e.g., public, private, multicast).

        Returns:
        IPv4AddrType: The type of the IP address.
        """
        return self._ip_type

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


class IPv4SubnetConfig(IPv4HostConfig):
    """
    IPv4SubnetConfig is a subclass of IPv4HostConfig that represents a subnet configuration for an IPv4 network.
    It adds functionality for working with subnet ranges and hosts within a subnet, allowing operations such as retrieving
    the first and last host, iterating over all hosts, and performing subnetting tasks like division and merging.

    Attributes:
    Inherits all attributes from IPv4HostConfig, including:
    - _ip_type (IPv4AddrType): The type of the IPv4 address (e.g., public, private).
    - _broadcast_ip (IPv4Addr): The broadcast IP address for the subnet.
    - _network_id (IPv4Addr): The network ID for the subnet.

    Methods:
    - first_host: Returns the first usable host address within the subnet.
    - last_host: Returns the last usable host address within the subnet.
    - subnet_range: Returns the range of the subnet, from the network ID to the broadcast address.
    - get_hosts: Generator function that yields each host within the subnet.
    - is_within(ip_addr): Checks whether a given IP address falls within the subnet.
    - subnet_division(mask): Divides the current subnet into smaller subnets based on a new mask size.
    - subnet_merge(*subnets): Attempts to merge multiple subnets into a larger subnet.

    Parameters:
    Inherits the parameters from IPv4HostConfig, which include the IPv4 address and netmask.
    """
    @property
    def first_host(self) -> IPv4Addr:
        """
        Returns the first usable host address within the subnet by skipping the network ID.

        Returns:
        IPv4Addr: The first usable host address.
        """
        host_iterator = self.get_hosts()
        next(host_iterator)
        return next(host_iterator)

    @property
    def last_host(self) -> IPv4Addr:
        """
        Returns the last usable host address within the subnet. The last host is derived
        by setting all host bits to 1 except for the least significant bit.

        Returns:
        IPv4Addr: The last usable host address.
        """
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        non_matching_indices = netmask_binary_digits.count(0)
        network_id_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [0]
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        return IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))

    @property
    def subnet_range(self) -> str:
        """
        Returns the range of the subnet, from the network ID to the broadcast IP address.

        Returns:
        str: A string representing the subnet range in the format "network_id-broadcast_ip".
        """
        return f"{self.network_id}-{self.broadcast_ip}"

    def _calculate_network_id(self) -> None:
        """
        Overrides the parent class method to also set the IP address to the network ID.
        This ensures that the network ID is used for further subnet operations.

        Returns:
        None
        """
        super()._calculate_network_id()
        self._ip_addr = self.network_id

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generates all usable hosts within the subnet by iterating over the possible combinations of host bits.

        Returns:
        Generator[IPv4Addr, None, None]: A generator yielding all host addresses in the subnet.
        """
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        non_matching_indices = netmask_binary_digits.count(0)
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        for matched_digits in itertools.product([0, 1], repeat=non_matching_indices):
            network_id_binary_digits[-non_matching_indices:] = matched_digits
            yield IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks whether a given IP address is within the current subnet by comparing
        the binary representations of the network ID, netmask, and the target IP address.

        Parameters:
        ip_addr (Any): The IP address to check.

        Returns:
        bool: True if the IP address is within the subnet, otherwise False.
        """
        ip_addr = IPv4Addr(ip_addr)
        if type(ip_addr) is not IPv4Addr:
            raise TypeError('ip_addr must be of type IPv4Addr')
        return BinaryTools.is_binary_in_range(
            list(self.network_id.binary_digits),
            list(self.mask.binary_digits),
            list(ip_addr.binary_digits)
        )

    def subnet_division(self, mask: int) -> List[IPv4SubnetConfig]:
        """
        Divides the current subnet into smaller subnets based on the provided mask size.
        It generates new subnets that fit within the current subnet's range.

        Parameters:
        mask (int): The new mask size for the smaller subnets.

        Returns:
        List[IPv4SubnetConfig]: A list of newly created IPv4SubnetConfig objects.

        Raises:
        TypeError: If the mask is not an integer.
        ValueError: If the mask is not valid (i.e., too large or too small).
        """
        subnet_mask_size = self.mask.get_mask_size()
        if type(mask) is not int:
            raise TypeError('mask must be of type int')
        if mask <= subnet_mask_size or mask > 32:
            raise ValueError(f'mask must be in the range of {subnet_mask_size + 1}-32')
        re_subnetting_length = mask - subnet_mask_size
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        netmask_binary_digits[subnet_mask_size: mask] = [1] * re_subnetting_length
        for subnetting_bit_combination in itertools.product([0, 1], repeat=re_subnetting_length):
            network_id_binary_digits[subnet_mask_size: mask] = subnetting_bit_combination
            yield IPv4SubnetConfig(
                IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits)),
                IPv4NetMask(binary_bit_ipv4_converter.handle(netmask_binary_digits))
            )

    def subnet_merge(self, *subnets: str) -> IPv4SubnetConfig:
        """
        Merges the current subnet with the provided subnets, creating a larger subnet that encompasses them all.
        The method ensures that the subnets are valid for merging and checks that their network bits match.

        Parameters:
        *subnets (str): A variable-length argument list of subnet strings to merge.

        Returns:
        IPv4SubnetConfig: A new IPv4SubnetConfig representing the merged subnet.

        Raises:
        ValueError: If the provided subnets cannot be merged.
        """
        subnets = [IPv4SubnetConfig(subnet) for subnet in subnets]
        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)
        # Ensure not all subnets are the same to prevent meaningless merging
        if len(set(map(str, subnets_need_merge))) == 1:
            raise ValueError("Merged subnets can not be the same.")
        # Extract network ID and netmask binary digits from all subnets
        network_id_binary_digits_list = [list(subnet.network_id.binary_digits) for subnet in subnets_need_merge]
        netmask_binary_digits_list = [list(subnet.mask.binary_digits) for subnet in subnets_need_merge]
        # Identify bits that differ among the subnets' network IDs
        corresponding_network_id_bits = [list(bits) for bits in zip(*network_id_binary_digits_list)]
        smallest_subnetting_mask_bit = next(
            (i for i, bits in enumerate(corresponding_network_id_bits) if len(set(bits)) != 1), None
        )
        # Determine the range for possible new masks
        subnet_largest_mask = max(subnet.mask.get_mask_size() for subnet in subnets_need_merge)
        subnet_smallest_mask = min(subnet.mask.get_mask_size() for subnet in subnets_need_merge)
        for n in range(subnet_largest_mask - smallest_subnetting_mask_bit, 0, -1):
            subnets_matching_combination = []
            desired_matching_combination = list(itertools.product([0, 1], repeat=n))
            # Check if all combinations of network bits are covered for the new potential mask
            for network_id_binary_digits, netmask_binary_digits in zip(
                    network_id_binary_digits_list,
                    netmask_binary_digits_list
            ):
                matching_combination = BinaryTools.expand_by_mask(
                    network_id_binary_digits[subnet_largest_mask - n: subnet_largest_mask],
                    netmask_binary_digits[subnet_largest_mask - n: subnet_largest_mask]
                )
                subnets_matching_combination.extend(matching_combination)
            # Validate the potential new mask based on the smallest mask bit position
            if smallest_subnetting_mask_bit > subnet_smallest_mask:
                raise ValueError('Provided subnets cannot be merged with current one')
            # If all combinations are matched, create a new subnet configuration with the adjusted mask
            if set(subnets_matching_combination) == set(desired_matching_combination):
                new_mask = copy.deepcopy(list(self.mask.binary_digits))
                new_mask[subnet_largest_mask - n: subnet_largest_mask] = [0] * n
                return IPv4SubnetConfig(self.ip_addr, IPv4NetMask(BinaryDigitsIPv4ConverterHandler().handle(new_mask)))
            elif len(set(subnets_matching_combination)) < len(set(desired_matching_combination)):
                raise ValueError('Provided subnets cannot be merged with current one')
        # If no valid merging configuration is found, raise an error
        raise ValueError('No valid merging configuration found for the provided subnets')


class IPv4WildCardConfig(InterfaceIPv4Config):
    """
    IPv4WildCardConfig is a subclass of InterfaceIPv4Config designed to handle wildcard configurations for IPv4 addresses.
    Wildcard addresses are used to match ranges of IP addresses by allowing certain bits of the address to "wildcard" or vary.
    This class provides methods for initializing, validating, and recalculating wildcard IP addresses, as well as
    checking if a given IP address falls within the wildcard range.

    Attributes:
    Inherits attributes from InterfaceIPv4Config, such as:
    - _ip_addr (IPv4Addr): The wildcard IPv4 address.
    - _mask (IPv4NetMask): The wildcard netmask associated with the IPv4 address.

    Methods:
    - _initialize(*args): Initializes the wildcard IP configuration and recalculates the IP address.
    - _validate(*args): Validates the wildcard IP address and mask.
    - _recalculate_ip_addr(): Recalculates the IP address based on the wildcard mask.
    - get_hosts(): Generator function that yields all possible host IPs matching the wildcard pattern.
    - is_within(ip_addr): Checks whether a given IP address matches the wildcard range.
    - __str__(): Returns a string representation of the wildcard configuration in the format "IP mask".

    Parameters:
    *args: Variable-length argument list for initializing the wildcard IP address and mask.
    """
    def _initialize(self, *args) -> None:
        """
        Initializes the IPv4 wildcard configuration by validating the input arguments and recalculating
        the wildcard IP address based on the mask.

        Parameters:
        *args: A variable-length argument list containing the IP address and wildcard mask.

        Returns:
        None
        """
        self._validate(*args)
        self._recalculate_ip_addr()

    def _validate(self, *args) -> None:
        """
        Validates the IPv4 wildcard address and mask by using an external IP standardizer.
        Raises a ValueError if the inputs are not valid wildcard objects.

        Parameters:
        *args: A variable-length argument list containing the IPv4 address and wildcard mask for validation.

        Returns:
        None

        Raises:
        ValueError: If the wildcard address or mask is invalid.
        """
        validation_result = IPStandardizer.ipv4_wildcard(*args)
        if validation_result:
            self._ip_addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv4 wildcard object")

    def _recalculate_ip_addr(self):
        """
        Recalculates the IP address based on the wildcard mask.
        For each bit in the mask, a 1 bit indicates a fixed value, and a 0 bit allows variability in the corresponding IP bit.

        Returns:
        None
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        mapped_binary_digits = []
        index = 0
        for mask_bit in self.mask.binary_digits:
            if mask_bit == 1:
                mapped_binary_digits.append(0)
            elif mask_bit == 0:
                mapped_binary_digits.append(ip_addr_binary_digits[index])
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._ip_addr = IPv4Addr(binary_bit_ipv4_converter.handle(mapped_binary_digits))

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generates all possible host IPs that match the wildcard pattern by iterating over every possible combination of variable bits.

        Returns:
        Generator[IPv4Addr, None, None]: A generator yielding all matching host addresses within the wildcard range.
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        mask_binary_digits = list(self.mask.binary_digits)
        binary_digits_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        match_bit_index = []
        for mask_i, mask_bit in enumerate(mask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                ip_addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv4Addr(binary_digits_ipv4_converter.handle(ip_addr_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks whether a given IP address falls within the range specified by the wildcard IP and mask.

        Parameters:
        ip_addr (Any): The IP address to check.

        Returns:
        bool: True if the IP address matches the wildcard pattern, otherwise False.

        Raises:
        TypeError: If the provided ip_addr is not of type IPv4Addr.
        """
        ip_addr = IPv4Addr(ip_addr)
        if type(ip_addr) is not IPv4Addr:
            raise TypeError('ip_addr must be of type IPv4Addr')
        wildcard_ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        validate_ip_addr_binary_digits = list(ip_addr.binary_digits)
        mask_binary_digits = list(self.mask.binary_digits)
        match_validation = []
        for mask_i, mask_bit in enumerate(mask_binary_digits):
            if mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        Returns a string representation of the IPv4 wildcard configuration, formatted as "IP Wildcard-mask".

        Returns:
        str: A string representing the wildcard IP address and mask.
        """
        return f"{str(self.ip_addr)} {str(self.mask)}"


class InterfaceIPv6Config(InterfaceIPConfig):
    """
    InterfaceIPv6Config is an abstract base class for configuring IPv6 interfaces.
    It inherits from InterfaceIPConfig and provides a basic structure for managing an IPv6 address and its associated netmask.
    Subclasses must implement initialization and validation logic specific to IPv6 addresses.

    Attributes:
    _ip_addr (IPv6Addr): Stores the IPv6 address of the interface.
    _mask (IPv6NetMask): Stores the netmask or wildcard mask associated with the IPv6 address.

    Methods:
    - _initialize(*args): Initializes the IPv6 interface by setting the IPv6 address and netmask.
    - _validate(*args): Validates the provided IPv6 address and netmask.
    - ip_addr: Property method that returns the configured IPv6 address.
    - mask: Property method that returns the configured IPv6 mask.
    - __str__(): Returns a string representation of the IPv6 configuration as "IP/Netmask size".

    Parameters:
    *args: Variable-length argument list that includes the IPv6 address and netmask for initialization.

    Returns:
    None
    """
    def __init__(self, *args):
        """
        Initializes the InterfaceIPv6Config class by calling the _initialize method with the provided arguments.

        Parameters:
        *args: A variable-length argument list that contains the IPv6 address and netmask.

        Returns:
        None
        """
        self._ip_addr = None
        self._mask = None
        self._initialize(*args)

    @abstractmethod
    def _initialize(self, *args) -> None:
        """
        Initializes the IPv6 interface by assigning an IPv6 address and netmask to the configuration.
        The method is abstract and must be implemented by subclasses.

        Parameters:
        *args: A variable-length argument list that includes the IPv6 address and netmask.

        Returns:
        None
        """
        self._validate(*args)

    @abstractmethod
    def _validate(self, *args) -> None:
        """
        Validates the provided IPv6 address and netmask. This method is abstract and must be implemented by subclasses
        to ensure that the IPv6 address and netmask conform to the expected format.

        Parameters:
        *args: A variable-length argument list that includes the IPv6 address and netmask for validation.

        Returns:
        None
        """
        pass

    @property
    def ip_addr(self) -> IPv6Addr:
        """
        Returns the currently configured IPv6 address.

        Returns:
        IPv6Addr: The configured IPv6 address.
        """
        return self._ip_addr

    @property
    def mask(self) -> IPv6NetMask:
        """
        Returns the currently configured IPv6 netmask.

        Returns:
        IPv6NetMask: The configured IPv6 netmask.
        """
        return self._mask

    def __str__(self) -> str:
        """
        Returns a string representation of the IPv6 configuration.
        The format is "IP/Netmask size", showing the IPv6 address and the length of the netmask.

        Returns:
        str: A string formatted as "IP/Netmask size" (e.g., "2001:db8::/64").
        """
        return f"{str(self.ip_addr)}/{str(self.mask.get_mask_size())}"


class IPv6HostConfig(InterfaceIPv6Config):
    """
    IPv6HostConfig is a subclass of InterfaceIPv6Config that represents an IPv6 host configuration.
    It includes methods for calculating the network ID, classifying the IP address type (e.g., global unicast, link-local),
    and determining the number of hosts in the network. This class is used to configure and manage IPv6 addresses
    for a specific host.

    Attributes:
    _ip_type (IPv6AddrType): The type of the IPv6 address (e.g., global unicast, link-local, multicast).
    _network_id (IPv6Addr): The network ID derived from the IPv6 address and netmask.

    Methods:
    - _initialize(*args): Initializes the IPv6 host configuration, validating the input and calculating the network ID and IP type.
    - _validate(*args): Validates the provided IPv6 address and netmask.
    - _calculate_network_id(): Calculates the network ID based on the IPv6 address and netmask.
    - _classify_ip_address_type(): Classifies the type of the IPv6 address (e.g., global unicast, link-local).
    - network_id: Returns the network ID.
    - host_counts: Calculates and returns the number of usable hosts in the network.
    - ip_type: Returns the classified IP address type.
    - is_unspecified: Checks if the IP type is unspecified.
    - is_loopback: Checks if the IP type is loopback.
    - is_multicast: Checks if the IP type is multicast.
    - is_link_local: Checks if the IP type is link-local.
    - is_global_unicast: Checks if the IP type is global unicast.

    Parameters:
    *args: A variable-length argument list that includes the IPv6 address and netmask for initialization.

    Returns:
    None
    """
    _ip_type: IPv6AddrType = IPv6AddrType.UNDEFINED_TYPE

    def __init__(self, *args):
        """
        Initializes the IPv6HostConfig by calling the parent class's initialization method
        and setting up the attributes related to network-specific data like network ID.

        Parameters:
        *args: A variable-length argument list containing the IPv6 address and netmask.

        Returns:
        None
        """
        self._broadcast_ip = None
        self._network_id = None
        super().__init__(*args)

    def _initialize(self, *args) -> None:
        """
        Initializes the IPv6 host configuration by validating the input parameters (IPv6 address and netmask),
        then calculating the network ID and classifying the IP address type.

        Parameters:
        *args: A variable-length argument list containing the IPv6 address and netmask.

        Returns:
        None
        """
        self._validate(*args)
        self._calculate_network_id()
        self._classify_ip_address_type()

    def _validate(self, *args) -> None:
        """
        Validates the IPv6 address and netmask by using an external standardizer.
        Raises a ValueError if the inputs are not valid.

        Parameters:
        *args: A variable-length argument list containing the IPv6 address and netmask for validation.

        Returns:
        None

        Raises:
        ValueError: If the IPv6 address or netmask is invalid.
        """
        validation_result = IPStandardizer.ipv6_interface(*args)
        if validation_result:
            self._ip_addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv6 object")

    def _calculate_network_id(self) -> None:
        """
        Calculates the network ID for the IPv6 address and netmask by applying the netmask to the IP address.

        Returns:
        None
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        network_id_binary_digits = []
        index = 0
        for netmask_bit in self.mask.binary_digits:
            if netmask_bit == 1:
                network_id_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                network_id_binary_digits.append(0)
            index += 1
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        self._network_id = IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))

    def _classify_ip_address_type(self) -> None:
        """
        Classifies the IPv6 address type (e.g., global unicast, link-local, multicast)
        by using the IPAddrTypeClassifier.

        Returns:
        None
        """
        self._ip_type = IPAddrTypeClassifier.classify_ipv6_type(self.network_id)

    @property
    def network_id(self) -> IPv6Addr:
        """
        Returns the network ID for the configured IPv6 network.

        Returns:
        IPv6Addr: The network ID of the IPv6 address.
        """
        return self._network_id

    @property
    def host_counts(self) -> int:
        """
        Calculates and returns the number of usable hosts in the IPv6 network.
        The count is determined by the number of host bits available in the netmask.

        Returns:
        int: The number of usable hosts in the network.
        """
        netmask_host_bit_count = list(self.mask.binary_digits).count(0)
        host_count = 2 ** netmask_host_bit_count
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def ip_type(self) -> IPv6AddrType:
        """
        Returns the classified type of the IPv6 address (e.g., global unicast, link-local, multicast).

        Returns:
        IPv6AddrType: The type of the IPv6 address.
        """
        return self._ip_type

    @property
    def is_unspecified(self) -> bool:
        """
        Checks if the IPv6 address type is unspecified.

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
        bool: True if the IPv6 address is a multicast address, otherwise False.
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
        bool: True if the IPv6 address is a global unicast address, otherwise False.
        """
        return self._ip_type == IPv6AddrType.GLOBAL_UNICAST


class IPv6SubnetConfig(IPv6HostConfig):
    """
    IPv6SubnetConfig is a subclass of IPv6HostConfig that represents an IPv6 subnet configuration.
    It adds functionality for working with IPv6 subnet ranges and hosts within a subnet, allowing for operations
    such as retrieving the first and last host, iterating over all hosts, and dividing or merging subnets.

    Attributes:
    Inherits attributes from IPv6HostConfig, including:
    - _ip_type (IPv6AddrType): The type of the IPv6 address (e.g., global unicast, link-local).
    - _network_id (IPv6Addr): The network ID derived from the IPv6 address and netmask.

    Methods:
    - first_host: Returns the first usable host address within the subnet.
    - last_host: Returns the last usable host address within the subnet.
    - subnet_range: Returns the range of the subnet, from the first host to the last host.
    - get_hosts: Generator function that yields each host within the subnet.
    - is_within(ip_addr): Checks whether a given IPv6 address falls within the subnet.
    - subnet_division(mask): Divides the current subnet into smaller subnets based on a new mask size.
    - subnet_merge(*subnets): Attempts to merge multiple subnets into a larger subnet.

    Parameters:
    *args: A variable-length argument list that includes the IPv6 address and netmask for initialization.

    Returns:
    None
    """
    @property
    def first_host(self) -> IPv6Addr:
        """
        Returns the first usable host address within the subnet. The first host is the network ID incremented by one.

        Returns:
        IPv6Addr: The first usable host address within the subnet.
        """
        host_iterator = self.get_hosts()
        return next(host_iterator)

    @property
    def last_host(self) -> IPv6Addr:
        """
        Returns the last usable host address within the subnet. This is calculated by setting all host bits to 1 except for
        the least significant bit, which is set to 0 to exclude the broadcast address.

        Returns:
        IPv6Addr: The last usable host address within the subnet.
        """
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        non_matching_indices = netmask_binary_digits.count(0)
        network_id_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        return IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))

    @property
    def subnet_range(self) -> str:
        """
        Returns the range of the subnet, from the first usable host to the last usable host.

        Returns:
        str: A string representing the subnet range in the format "first_host - last_host".
        """
        return f"{self.first_host} - {self.last_host}"

    def _calculate_network_id(self) -> None:
        """
        Overrides the parent class method to also set the IP address to the network ID.
        This ensures that the network ID is used for further subnet operations.

        Returns:
        None
        """
        super()._calculate_network_id()
        self._ip_addr = self._network_id

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generates all usable host addresses within the subnet by iterating over the possible combinations of host bits.

        Returns:
        Generator[IPv6Addr, None, None]: A generator yielding all host addresses in the subnet.
        """
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        non_matching_indices = netmask_binary_digits.count(0)
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        for matched_digits in itertools.product([0, 1], repeat=non_matching_indices):
            network_id_binary_digits[-non_matching_indices:] = matched_digits
            yield IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks whether a given IPv6 address falls within the current subnet by comparing
        the binary representations of the network ID, netmask, and the target IPv6 address.

        Parameters:
        ip_addr (Any): The IPv6 address to check.

        Returns:
        bool: True if the IPv6 address is within the subnet, otherwise False.
        """
        ip_addr = IPv6Addr(ip_addr)
        if type(ip_addr) is not IPv6Addr:
            raise TypeError('ip_addr must be of type IPv6Addr')
        return BinaryTools.is_binary_in_range(
            list(self.network_id.binary_digits),
            list(self.mask.binary_digits),
            list(ip_addr.binary_digits)
        )

    def subnet_division(self, mask: int) -> List[IPv6SubnetConfig]:
        """
        Divides the current subnet into smaller subnets based on the provided mask size.
        It generates new subnets that fit within the current subnet's range.

        Parameters:
        mask (int): The new mask size for the smaller subnets.

        Returns:
        List[IPv6SubnetConfig]: A list of newly created IPv6SubnetConfig objects.

        Raises:
        TypeError: If the mask is not an integer.
        ValueError: If the mask is not valid (i.e., too large or too small).
        """
        subnet_mask_size = self.mask.get_mask_size()
        if type(mask) is not int:
            raise TypeError('mask must be of type int')
        if mask <= subnet_mask_size or mask > 128:
            raise ValueError(f'mask must be in the range of {subnet_mask_size + 1}-128')
        re_subnetting_length = mask - subnet_mask_size
        network_id_binary_digits = list(self.network_id.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        netmask_binary_digits[subnet_mask_size: mask] = [1] * re_subnetting_length
        for subnetting_bit_combination in itertools.product([0, 1], repeat=re_subnetting_length):
            network_id_binary_digits[subnet_mask_size: mask] = subnetting_bit_combination
            yield IPv6SubnetConfig(
                IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits)),
                IPv6NetMask(binary_bit_ipv6_converter.handle(netmask_binary_digits))
            )

    def subnet_merge(self, *subnets: Any) -> IPv6SubnetConfig:
        """
        Merges the current subnet with the provided subnets, creating a larger subnet that encompasses them all.
        The method ensures that the subnets are valid for merging and checks that their network bits match.

        Parameters:
        *subnets (Any): A variable-length argument list of subnet objects to merge.

        Returns:
        IPv6SubnetConfig: A new IPv6SubnetConfig representing the merged subnet.

        Raises:
        ValueError: If the provided subnets cannot be merged.
        """
        subnets = [IPv6SubnetConfig(subnet) for subnet in subnets]
        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)
        # Ensure not all subnets are the same to prevent meaningless merging
        if len(set(map(str, subnets_need_merge))) == 1:
            raise ValueError("Merged subnets can not be the same.")
        # Extract network ID and netmask binary digits from all subnets
        network_id_binary_digits_list = [list(subnet.network_id.binary_digits) for subnet in subnets_need_merge]
        netmask_binary_digits_list = [list(subnet.mask.binary_digits) for subnet in subnets_need_merge]
        # Identify bits that differ among the subnets' network IDs
        corresponding_network_id_bits = [list(bits) for bits in zip(*network_id_binary_digits_list)]
        smallest_subnetting_mask_bit = next(
            (i for i, bits in enumerate(corresponding_network_id_bits) if len(set(bits)) != 1), None
        )
        # Determine the range for possible new masks
        subnet_largest_mask = max(subnet.mask.get_mask_size() for subnet in subnets_need_merge)
        subnet_smallest_mask = min(subnet.mask.get_mask_size() for subnet in subnets_need_merge)
        for n in range(subnet_largest_mask - smallest_subnetting_mask_bit, 0, -1):
            subnets_matching_combination = []
            desired_matching_combination = list(itertools.product([0, 1], repeat=n))
            # Check if all combinations of network bits are covered for the new potential mask
            for network_id_binary_digits, netmask_binary_digits in zip(
                    network_id_binary_digits_list,
                    netmask_binary_digits_list
            ):
                matching_combination = BinaryTools.expand_by_mask(
                    network_id_binary_digits[subnet_largest_mask - n: subnet_largest_mask],
                    netmask_binary_digits[subnet_largest_mask - n: subnet_largest_mask]
                )
                subnets_matching_combination.extend(matching_combination)
            # Validate the potential new mask based on the smallest mask bit position
            if smallest_subnetting_mask_bit > subnet_smallest_mask:
                raise ValueError('Provided subnets cannot be merged with current one')
            # If all combinations are matched, create a new subnet configuration with the adjusted mask
            if set(subnets_matching_combination) == set(desired_matching_combination):
                new_mask = copy.deepcopy(list(self.mask.binary_digits))
                new_mask[subnet_largest_mask - n: subnet_largest_mask] = [0] * n
                return IPv6SubnetConfig(self.ip_addr, IPv6NetMask(BinaryDigitsIPv6ConverterHandler().handle(new_mask)))
            elif len(set(subnets_matching_combination)) < len(set(desired_matching_combination)):
                raise ValueError('Provided subnets cannot be merged with current one')
        # If no valid merging configuration is found, raise an error
        raise ValueError('No valid merging configuration found for the provided subnets')


class IPv6WildCardConfig(InterfaceIPv6Config):
    """
    IPv6WildCardConfig is a subclass of InterfaceIPv6Config designed to handle wildcard configurations for IPv6 addresses.
    Wildcard addresses are used to match ranges of IPv6 addresses by allowing certain bits of the address to "wildcard" or vary.
    This class provides methods for initializing, validating, recalculating the wildcard IPv6 address, and checking if a given IP
    address falls within the wildcard range.

    Attributes:
    Inherits attributes from InterfaceIPv6Config, such as:
    - _ip_addr (IPv6Addr): The wildcard IPv6 address.
    - _mask (IPv6NetMask): The wildcard netmask associated with the IPv6 address.

    Methods:
    - _initialize(*args): Initializes the wildcard IPv6 configuration and recalculates the IP address.
    - _validate(*args): Validates the wildcard IPv6 address and netmask.
    - _recalculate_ip_addr(): Recalculates the wildcard IP address based on the netmask.
    - get_hosts(): Generator function that yields all possible host IPs matching the wildcard pattern.
    - is_within(ip_addr): Checks whether a given IP address matches the wildcard range.
    - __str__(): Returns a string representation of the wildcard configuration in the format "IP Netmask".

    Parameters:
    *args: A variable-length argument list for initializing the wildcard IPv6 address and netmask.

    Returns:
    None
    """
    def _initialize(self, *args) -> None:
        """
        Initializes the IPv6 wildcard configuration by validating the input arguments and recalculating
        the wildcard IPv6 address based on the netmask.

        Parameters:
        *args: A variable-length argument list containing the IPv6 address and wildcard netmask.

        Returns:
        None
        """
        self._validate(*args)
        self._recalculate_ip_addr()

    def _validate(self, *args) -> None:
        """
        Validates the IPv6 wildcard address and netmask using an external standardizer.
        Raises a ValueError if the inputs are not valid wildcard objects.

        Parameters:
        *args: A variable-length argument list containing the IPv6 address and wildcard netmask for validation.

        Returns:
        None

        Raises:
        ValueError: If the wildcard address or netmask is invalid.
        """
        validation_result = IPStandardizer.ipv6_wildcard(*args)
        if validation_result:
            self._ip_addr = validation_result[0]
            self._mask = validation_result[1]
        else:
            raise ValueError(f"{str(args)} is not a valid IPv6 wildcard object")

    def _recalculate_ip_addr(self):
        """
        Recalculates the wildcard IPv6 address based on the wildcard netmask. For each bit in the netmask, a 1 bit
        indicates a fixed value, while a 0 bit allows variability in the corresponding IP bit.

        Returns:
        None
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        mapped_binary_digits = []
        index = 0
        for netmask_bit in self.mask.binary_digits:
            if netmask_bit == 1:
                mapped_binary_digits.append(0)
            elif netmask_bit == 0:
                mapped_binary_digits.append(ip_addr_binary_digits[index])
            index += 1
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        self._ip_addr = IPv6Addr(binary_bit_ipv6_converter.handle(mapped_binary_digits))

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generates all possible host IPs that match the wildcard pattern by iterating over every possible combination of variable bits.

        Returns:
        Generator[IPv6Addr, None, None]: A generator yielding all matching host addresses within the wildcard range.
        """
        ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        binary_digits_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        match_bit_index = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                ip_addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv6Addr(binary_digits_ipv6_converter.handle(ip_addr_binary_digits))

    def is_within(self, ip_addr: Any) -> bool:
        """
        Checks whether a given IPv6 address falls within the range specified by the wildcard IPv6 address and netmask.

        Parameters:
        ip_addr (Any): The IPv6 address to check.

        Returns:
        bool: True if the IPv6 address matches the wildcard pattern, otherwise False.

        Raises:
        TypeError: If the provided ip_addr is not of type IPv6Addr.
        """
        ip_addr = IPv6Addr(ip_addr)
        if type(ip_addr) is not IPv6Addr:
            raise TypeError('ip_addr must be of type IPv6Addr')
        wildcard_ip_addr_binary_digits = list(self.ip_addr.binary_digits)
        validate_ip_addr_binary_digits = list(ip_addr.binary_digits)
        netmask_binary_digits = list(self.mask.binary_digits)
        match_validation = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        Returns a string representation of the IPv6 wildcard configuration, formatted as "IP Netmask".

        Returns:
        str: A string representing the wildcard IPv6 address and netmask.
        """
        return f"{str(self.ip_addr)} {str(self.mask)}"


class IPWildCardCalculator:
    """
    IPWildCardCalculator provides static methods for calculating the minimum wildcard configuration
    for a given set of subnets, both for IPv4 and IPv6 addresses. The goal of these methods is to generate
    wildcard addresses that can cover all the provided subnets with minimal complexity.

    Methods:
    - calculate_minimum_ipv4_wildcard(*subnets): Calculates the minimum IPv4 wildcard configuration for a set of subnets.
    - calculate_minimum_ipv6_wildcard(*subnets): Calculates the minimum IPv6 wildcard configuration for a set of subnets.

    Returns:
    None (These are static methods for generating wildcard configurations).
    """
    @staticmethod
    def calculate_minimum_ipv4_wildcard(*subnets: Any) -> IPv4WildCardConfig:
        """
        Calculates the minimum IPv4 wildcard configuration for a set of IPv4 subnets.
        The method identifies the bits that are common across all subnets and creates a wildcard
        configuration that encompasses all subnets.

        Parameters:
        *subnets (Any): A variable-length argument list of IPv4 subnet strings.

        Returns:
        IPv4WildCardConfig: A new IPv4WildCardConfig object that represents the wildcard configuration covering the provided subnets.

        Raises:
        ValueError: If the subnets are invalid or cannot be merged into a single wildcard configuration.
        """
        ipv4_subnets = [IPv4SubnetConfig(subnet) for subnet in subnets]
        network_id_bits_list = [list(subnet.network_id.binary_digits) for subnet in ipv4_subnets]
        netmask_bits_list = [list(subnet.mask.binary_digits) for subnet in ipv4_subnets]
        max_host_bits = max([netmask_bits.count(0) for netmask_bits in netmask_bits_list])
        wildcard_address_bits = []
        wildcard_mask_bits = []
        for network_id_bits in zip(*network_id_bits_list):
            if len(set(network_id_bits)) == 1:
                wildcard_address_bits.append(network_id_bits[0])
                wildcard_mask_bits.append(0)
            else:
                wildcard_address_bits.append(0)
                wildcard_mask_bits.append(1)
        wildcard_mask_bits[-max_host_bits:] = [1] * max_host_bits
        address_digits = [
            OctetFlyWeightFactory.get_octet(''.join(map(str, wildcard_address_bits))[index: index + 8])
            for index in range(0, len(wildcard_address_bits), 8)
        ]
        wildcard_digits = [
            OctetFlyWeightFactory.get_octet(''.join(map(str, wildcard_mask_bits))[index: index + 8])
            for index in range(0, len(wildcard_mask_bits), 8)
        ]
        return IPv4WildCardConfig(IPv4Addr(address_digits), IPv4WildCard(wildcard_digits))

    @staticmethod
    def calculate_minimum_ipv6_wildcard(*subnets: Any) -> IPv6WildCardConfig:
        """
        Calculates the minimum IPv6 wildcard configuration for a set of IPv6 subnets.
        The method identifies the bits that are common across all subnets and creates a wildcard
        configuration that encompasses all subnets.

        Parameters:
        *subnets (Any): A variable-length argument list of IPv6 subnet strings.

        Returns:
        IPv6WildCardConfig: A new IPv6WildCardConfig object that represents the wildcard configuration covering the provided subnets.

        Raises:
        ValueError: If the subnets are invalid or cannot be merged into a single wildcard configuration.
        """
        ipv6_subnets = [IPv6SubnetConfig(subnet) for subnet in subnets]
        network_id_bits_list = [list(subnet.network_id.binary_digits) for subnet in ipv6_subnets]
        netmask_bits_list = [list(subnet.mask.binary_digits) for subnet in ipv6_subnets]
        max_host_bits = max([netmask_bits.count(0) for netmask_bits in netmask_bits_list])
        wildcard_address_bits = []
        wildcard_mask_bits = []
        for network_id_bits in zip(*network_id_bits_list):
            if len(set(network_id_bits)) == 1:
                wildcard_address_bits.append(network_id_bits[0])
                wildcard_mask_bits.append(0)
            else:
                wildcard_address_bits.append(0)
                wildcard_mask_bits.append(1)
        wildcard_mask_bits[-max_host_bits:] = [1] * max_host_bits
        address_digits = [
            OctetFlyWeightFactory.get_octet(''.join(map(str, wildcard_address_bits))[index: index + 8])
            for index in range(0, len(wildcard_address_bits), 8)
        ]
        wildcard_digits = [
            OctetFlyWeightFactory.get_octet(''.join(map(str, wildcard_mask_bits))[index: index + 8])
            for index in range(0, len(wildcard_mask_bits), 8)
        ]
        return IPv6WildCardConfig(IPv6Addr(address_digits), IPv6WildCard(wildcard_digits))
