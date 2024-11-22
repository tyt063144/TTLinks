from enum import Enum
from typing import Dict, Any



class IPType(Enum):
    """
    Enumeration for IP protocol types.
    Provides methods to validate and retrieve enumeration values.
    """
    IPv4 = 4
    IPv6 = 16

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Checks if a value exists in the enumeration.

        Parameters:
        value (Any): The value to check.

        Returns:
        bool: True if the value exists in the enum, False otherwise.
        """
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """
        Retrieves a dictionary mapping of enumeration members and their values.

        Returns:
        Dict: A dictionary of enum values.
        """
        return cls._value2member_map_

class IPv4AddrType(Enum):
    """
    Enumeration for different types of IPv4 addresses.
    Covers specific categories such as public, private, loopback, and multicast.
    """
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
    DS_LITE = 14  # For 192.0.0.0/24,

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Checks if a value exists in the enumeration.
        """
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """
        Retrieves a dictionary mapping of enumeration members and their values.
        """
        return cls._value2member_map_


class IPv6AddrType(Enum):
    """
    Enumeration for different types of IPv6 addresses.
    Covers categories like global unicast, link-local, and multicast.
    """
    UNDEFINED_TYPE = 0
    UNSPECIFIED = 1  # ::/128
    SRV6 = 2  # 5f00::/16, IPv6 Segment Routing
    GLOBAL_UNICAST = 3
    UNIQUE_LOCAL = 4  # fc00::/7
    MULTICAST = 5  # ff00::/8
    LINK_LOCAL = 6  # fe80::/64 from fe80::/10
    LOOPBACK = 7  # ::1/128
    DOCUMENTATION = 8  # 2001:db8::/32 and 3fff::/20
    IPV4_MAPPED = 9  # ::ffff:0:0/96
    IPV4_TRANSLATED = 10  # ::ffff:0:0:0/96
    IPV4_IPV6_TRANSLATION = 11  # 64:ff9b::/96 and 64:ff9b:1::/48
    DISCARD_PREFIX = 12  # 100::/64
    IP6_TO4 = 13  # 2002::/16, 6to4 addressing scheme
    TEREDO_TUNNELING = 14  # 2001::/32
    ORCHIDV2 = 15  # 2001:20::/28

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Checks if a value exists in the enumeration.
        """
        return value in (item.value for item in cls)

    @classmethod
    def get_values(cls) -> Dict:
        """
        Retrieves a dictionary mapping of enumeration members and their values.
        """
        return cls._value2member_map_



class IPv4TypeAddrBlocks(Enum):
    """
    Enumeration mapping IPv4 address types to their respective CIDR blocks.
    """
    UNSPECIFIED = ['0.0.0.0/32']
    CURRENT_NETWORK = ['0.0.0.0/8']
    PUBLIC = [
            '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
            '172.16.0.0/12', '192.0.0.0/24', '192.0.2.0/24', '192.88.99.0/24', '192.168.0.0/16',
            '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24', '224.0.0.0/4', '233.252.0.0/24',
            '240.0.0.0/4', '255.255.255.255/32'
        ]  # Public IPs generated have to avoid the blocks in the list.
    PRIVATE = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    MULTICAST = ["224.0.0.0/4"]  # For 224.0.0.0/4 and others
    LINK_LOCAL = ["169.254.0.0/16"]  # For 169.254.0.0/16
    LOOPBACK = ["127.0.0.0/8"]  # For 127.0.0.0/8
    DOCUMENTATION = ['192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '233.252.0.0/24']  # For 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, and 233.252.0.0/24
    CARRIER_GRADE_NAT = ['100.64.0.0/10']  # For 100.64.0.0/10
    BENCHMARK_TESTING = ['198.18.0.0/15']  # For 198.18.0.0/15
    IPV6_TO_IPV4_RELAY = ['192.88.99.0/24']  # For 192.88.99.0/24 (formerly used)
    RESERVED = ['240.0.0.0/4']  # For 240.0.0.0/4 and 255.255.255.255/32
    LIMITED_BROADCAST = ['255.255.255.255/32']  # For 255.255.255.255/32, "limited broadcast" destination address
    DS_LITE = ['192.0.0.0/24']  # For 192.0.0.0/24

class IPv6TypeAddrBlocks(Enum):
    """
    Enumeration mapping IPv6 address types to their respective CIDR blocks.
    """
    UNSPECIFIED = ['::/128']  # ::/128
    SRV6 = ['5f00::/16']  # 5f00::/16, IPv6 Segment Routing
    GLOBAL_UNICAST = ['2000::/3']
    UNIQUE_LOCAL = ['fc00::/7']  # fc00::/7
    MULTICAST = ['ff00::/8']  # ff00::/8
    LINK_LOCAL = ['fe80::/64']  # fe80::/64 from fe80::/10
    LOOPBACK = ['::1/128']  # ::1/128
    DOCUMENTATION = ['2001:db8::/32', '3fff::/20']  # 2001:db8::/32 and 3fff::/20
    IPV4_MAPPED = ['::ffff:0:0/96']  # ::ffff:0:0/96
    IPV4_TRANSLATED = ['::ffff:0:0:0/96']  # ::ffff:0:0:0/96
    IPV4_IPV6_TRANSLATION = ['64:ff9b::/96', '64:ff9b:1::/48']  # 64:ff9b::/96 and 64:ff9b:1::/48
    DISCARD_PREFIX = ['100::/64']  # 100::/64
    IP6_TO4 = ['2002::/16'] # 2002::/16, 6to4 addressing scheme
    TEREDO_TUNNELING = ['2001::/32']  # 2001::/32
    ORCHIDV2 = ['2001:20::/28']  # 2001:20::/28