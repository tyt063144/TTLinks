from enum import Enum
from itertools import product
from typing import List, Dict, Any


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


class IPv4AddrType(Enum):
    UNDEFINED_TYPE = 0
    UNSPECIFIED = 1
    CURRENT_NETWORK = 2
    PUBLIC = 3
    PRIVATE = 4
    MULTICAST = 5  # For 224.0.0.0/4 and others
    LINK_LOCAL = 6  # For 169.254.0.0/16
    LOOPBACK = 7  # For 127.0.0.0/8
    DOCUMENTATION = 8  # For 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, and 233.252.0.0/24
    CARRIER_GRADE_NAT = 9  # For 100.64.0.0/10
    BENCHMARK_TESTING = 10  # For 198.18.0.0/15
    IPV6_TO_IPV4_RELAY = 11  # For 192.88.99.0/24 (formerly used)
    RESERVED = 12  # For 240.0.0.0/4 and 255.255.255.255/32
    LIMITED_BROADCAST = 13  # For 255.255.255.255/32, "limited broadcast" destination address
    DS_LITE = 14  # For 255.255.255.255/32, "limited broadcast" destination address

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """Check if the provided value is a valid member of the enumeration."""
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """Retrieve a dictionary mapping of the enumeration members and their values."""
        return cls._value2member_map_


class IPv6AddrType(Enum):
    UNDEFINED_TYPE = 0
    UNSPECIFIED = 1  # ::/128
    SRV6 = 2  # 5f00::/16, IPv6 Segment Routing
    GLOBAL_UNICAST = 3
    UNIQUE_LOCAL_ADDRESS = 4  # fc00::/7
    MULTICAST = 5  # ff00::/8
    LINK_LOCAL = 6  # fe80::/64 from fe80::/10
    LOOPBACK = 7  # ::1/128
    DOCUMENTATION = 8  # 2001:db8::/32 and 3fff::/20
    IPV4_MAPPED = 9  # ::ffff:0:0/96
    IPV4_TRANSLATED = 10  # ::ffff:0:0:0/96
    IPV4_IPV6_TRANSLATION = 11  # 64:ff9b::/96 and 64:ff9b:1::/48
    DISCARD_PREFIX = 12  # 100::/64
    TO4 = 13  # 2002::/16, 6to4 addressing scheme
    TEREDO_TUNNELING = 14  # 2001::/32
    ORCHIDV2 = 15  # 2001:20::/28

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """Check if the provided value is a valid member of the enumeration."""
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """Retrieve a dictionary mapping of the enumeration members and their values."""
        return cls._value2member_map_


class NetToolsSuite:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NetToolsSuite, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def netmask_expand(ip_digits: List[int], netmask_digits: List[int]) -> List[tuple[int]]:
        """
        Expands the given IP digits based on the netmask digits to generate all possible
        combinations of IP addresses.

        This method takes a list of IP digits and a corresponding list of netmask digits.
        The netmask determines which bits of the IP address are fixed and which bits can vary.
        If a bit in the netmask is 1, the corresponding IP bit is fixed. If the netmask bit is 0,
        the corresponding IP bit can take multiple values (in this example, either 1 or 2).

        Args:
            ip_digits (List[int]): A list of binary digits representing an IP address.
            netmask_digits (List[int]): A list of binary digits representing the netmask.
                                         A 1 indicates the bit is fixed, and a 0 indicates
                                         the bit can vary.

        Returns:
            List[Tuple[int]]: A list of tuples, where each tuple represents a possible
                              combination of IP digits generated based on the netmask.

        Example:
            ip_digits = [0, 1, 0]
            netmask_digits = [1, 1, 0]
            result = SubnetCombinator.netmask_expand(ip_digits, netmask_digits)
            # result will be [(0, 1, 1), (0, 1, 2)]
        """
        expanded_ip_digits = {}
        index = 0
        for netmask_bit in netmask_digits:
            if netmask_bit == 1:
                expanded_ip_digits[index] = [ip_digits[index]]
            elif netmask_bit == 0:
                expanded_ip_digits[index] = [0, 1]
            index += 1
        # Generate all combinations using itertools.product
        combinations = list(product(*expanded_ip_digits.values()))
        return combinations

    @staticmethod
    def ip_within_range(network_digits: List[int], netmask_digits: List[int], compared_digits: List[int]) -> bool:
        matching_count = netmask_digits.count(1)
        return network_digits[:matching_count] == compared_digits[:matching_count]
