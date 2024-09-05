from __future__ import annotations

import copy
import itertools
from abc import ABC, abstractmethod
from typing import Generator, List, Any
from ip_converters import BinaryDigitsIPv4ConverterHandler, BinaryDigitsIPv6ConverterHandler
from ip_address import IPv4Addr, IPv4NetMask, IPv4WildCard, IPv6Addr, IPv6NetMask, IPv6WildCard
from ip_utils import NetToolsSuite, IPv4AddrType, IPv6AddrType
from ttlinks.ttlinks.common.base_utils import CoRHandler


class IPv4AddrClassifierHandler(CoRHandler):
    _next_handler = None

    def set_next(self, h: CoRHandler) -> CoRHandler:
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler if self._next_handler is not None else IPv4AddrType.UNDEFINED_TYPE


class IPv4AddrTypeUnspecifiedHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        if type(request) is IPv4Addr and all(bit == 0 for bit in list(request.get_binary_digits())):
            return IPv4AddrType.UNSPECIFIED
        else:
            return super().handle(request)


class IPv4AddrTypeLimitedBroadcastHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        if type(request) is IPv4Addr and all(bit == 1 for bit in list(request.get_binary_digits())):
            return IPv4AddrType.LIMITED_BROADCAST
        else:
            return super().handle(request)


class IPv4AddrTypeCurrentNetworkHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        current_networks_ranges = [
            '0.0.0.0/8'
        ]
        current_networks = []
        for address in current_networks:
            current_networks_ranges.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_current_network = any(NetToolsSuite.ip_within_range(*current_network) for current_network in current_networks)
        if type(request) is IPv4Addr and is_current_network:
            return IPv4AddrType.CURRENT_NETWORK
        else:
            return super().handle(request)


class IPv4AddrClassifierPublicHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        not_public_networks = [
            '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
            '172.16.0.0/12', '192.0.0.0/24', '192.0.2.0/24', '192.88.99.0/24', '192.168.0.0/16',
            '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24', '224.0.0.0/4', '233.252.0.0/24',
            '240.0.0.0/4', '255.255.255.255/32'
        ]
        not_public_ranges = []
        for address in not_public_networks:
            not_public_ranges.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_not_public = any(NetToolsSuite.ip_within_range(*not_public) for not_public in not_public_ranges)
        if type(request) is IPv4Addr and not is_not_public:
            return IPv4AddrType.PUBLIC
        else:
            return super().handle(request)


class IPv4AddrClassifierPrivateHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        private_ranges = [
            '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'
        ]
        private_networks = []
        for address in private_ranges:
            private_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_private = any(NetToolsSuite.ip_within_range(*private_network) for private_network in private_networks)
        if type(request) is IPv4Addr and is_private:
            return IPv4AddrType.PRIVATE
        else:
            return super().handle(request)


class IPv4AddrClassifierMulticastHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        multicast_networks = [
            list(IPv4Addr('224.0.0.0').get_binary_digits()),
            list(IPv4NetMask('/4').get_binary_digits()),
            list(request.get_binary_digits())
        ]
        is_multicast = NetToolsSuite.ip_within_range(*multicast_networks)
        if type(request) is IPv4Addr and is_multicast:
            return IPv4AddrType.MULTICAST
        else:
            return super().handle(request)


class IPv4AddrClassifierLinkLocalHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        link_local_networks = [
            list(IPv4Addr('169.254.0.0').get_binary_digits()),
            list(IPv4NetMask('/16').get_binary_digits()),
            list(request.get_binary_digits())
        ]
        is_link_local = NetToolsSuite.ip_within_range(*link_local_networks)
        if type(request) is IPv4Addr and is_link_local:
            return IPv4AddrType.LINK_LOCAL
        else:
            return super().handle(request)


class IPv4AddrClassifierLoopbackHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        link_local_networks = [
            list(IPv4Addr('127.0.0.0').get_binary_digits()),
            list(IPv4NetMask('/8').get_binary_digits()),
            list(request.get_binary_digits())
        ]
        is_link_local = NetToolsSuite.ip_within_range(*link_local_networks)
        if type(request) is IPv4Addr and is_link_local:
            return IPv4AddrType.LOOPBACK
        else:
            return super().handle(request)


class IPv4AddrClassifierDocumentationHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        documentation_ranges = [
            '192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '233.252.0.0/24'
        ]
        documentation_networks = []
        for address in documentation_ranges:
            documentation_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_documentation = any(NetToolsSuite.ip_within_range(*documentation_network) for documentation_network in documentation_networks)
        if type(request) is IPv4Addr and is_documentation:
            return IPv4AddrType.DOCUMENTATION
        else:
            return super().handle(request)


class IPv4AddrClassifierDSLiteHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        ds_lite_ranges = [
            '192.0.0.0/24'
        ]
        ds_lite_networks = []
        for address in ds_lite_ranges:
            ds_lite_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ds_lite = any(NetToolsSuite.ip_within_range(*ds_lite_network) for ds_lite_network in ds_lite_networks)
        if type(request) is IPv4Addr and is_ds_lite:
            return IPv4AddrType.DS_LITE
        else:
            return super().handle(request)


class IPv4AddrClassifierCarrierNATHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        documentation_ranges = [
            '100.64.0.0/10'
        ]
        carrier_grade_nat_networks = []
        for address in documentation_ranges:
            carrier_grade_nat_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_carrier_grade_nat = any(
            NetToolsSuite.ip_within_range(*carrier_grade_nat_network)
            for carrier_grade_nat_network in carrier_grade_nat_networks
        )
        if type(request) is IPv4Addr and is_carrier_grade_nat:
            return IPv4AddrType.CARRIER_GRADE_NAT
        else:
            return super().handle(request)


class IPv4AddrClassifierBenchmarkTestingHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        benchmark_testing_ranges = [
            '198.18.0.0/15'
        ]
        benchmark_testing_networks = []
        for address in benchmark_testing_ranges:
            benchmark_testing_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_benchmark_testing = any(
            NetToolsSuite.ip_within_range(*benchmark_testing_network)
            for benchmark_testing_network in benchmark_testing_networks
        )
        if type(request) is IPv4Addr and is_benchmark_testing:
            return IPv4AddrType.BENCHMARK_TESTING
        else:
            return super().handle(request)


class IPv4AddrClassifierIP6To4RelayHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        ipv6_to_ipv4_relay_ranges = [
            '192.88.99.0/24'
        ]
        ipv6_to_ipv4_relay_networks = []
        for address in ipv6_to_ipv4_relay_ranges:
            ipv6_to_ipv4_relay_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ipv6_to_ipv4_relay = any(
            NetToolsSuite.ip_within_range(*ipv6_to_ipv4_relay_network)
            for ipv6_to_ipv4_relay_network in ipv6_to_ipv4_relay_networks
        )
        if type(request) is IPv4Addr and is_ipv6_to_ipv4_relay:
            return IPv4AddrType.IPV6_TO_IPV4_RELAY
        else:
            return super().handle(request)


class IPv4AddrClassifierReservedHandler(IPv4AddrClassifierHandler):
    def handle(self, request: Any):
        reserved_ranges = [
            '240.0.0.0/4'
        ]
        reserved_networks = []
        for address in reserved_ranges:
            reserved_networks.append([
                list(IPv4Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv4NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_reserved = any(
            NetToolsSuite.ip_within_range(*reserved_network)
            for reserved_network in reserved_networks
        )
        if type(request) is IPv4Addr and is_reserved:
            return IPv4AddrType.RESERVED
        else:
            return super().handle(request)


class IPv6AddrClassifierHandler(CoRHandler):
    _next_handler = None

    def set_next(self, h: CoRHandler) -> CoRHandler:
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler if self._next_handler is not None else IPv6AddrType.UNDEFINED_TYPE


class IPv6AddrClassifierUnspecifiedHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        unspecified_ranges = ['::/128']
        unspecified_networks = []
        for address in unspecified_ranges:
            unspecified_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_unspecified = any(
            NetToolsSuite.ip_within_range(*unspecified_network)
            for unspecified_network in unspecified_networks
        )
        if type(request) is IPv6Addr and is_unspecified:
            return IPv6AddrType.UNSPECIFIED
        else:
            return super().handle(request)


class IPv6AddrClassifierLoopbackHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        loopback_ranges = ['::1/128']
        loopback_networks = []
        for address in loopback_ranges:
            loopback_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_loopback = any(
            NetToolsSuite.ip_within_range(*loopback_network)
            for loopback_network in loopback_networks
        )
        if type(request) is IPv6Addr and is_loopback:
            return IPv6AddrType.LOOPBACK
        else:
            return super().handle(request)


class IPv6AddrClassifierDocumentationHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        documentation_ranges = ['2001:db8::/32', '3fff::/20']
        documentation_networks = []
        for address in documentation_ranges:
            documentation_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_documentation = any(
            NetToolsSuite.ip_within_range(*documentation_network)
            for documentation_network in documentation_networks
        )
        if type(request) is IPv6Addr and is_documentation:
            return IPv6AddrType.DOCUMENTATION
        else:
            return super().handle(request)


class IPv6AddrClassifierLinkLocalHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        link_local_ranges = ['fe80::/64']
        link_local_networks = []
        for address in link_local_ranges:
            link_local_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_link_local = any(
            NetToolsSuite.ip_within_range(*link_local_network)
            for link_local_network in link_local_networks
        )
        if type(request) is IPv6Addr and is_link_local:
            return IPv6AddrType.LINK_LOCAL
        else:
            return super().handle(request)


class IPv6AddrClassifierMulticastHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        multicast_ranges = ['ff00::/8']
        multicast_networks = []
        for address in multicast_ranges:
            multicast_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_multicast = any(
            NetToolsSuite.ip_within_range(*multicast_network)
            for multicast_network in multicast_networks
        )
        if type(request) is IPv6Addr and is_multicast:
            return IPv6AddrType.MULTICAST
        else:
            return super().handle(request)


class IPv6AddrClassifierUniqueLocalHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        unique_local_ranges = ['fc00::/7']
        unique_local_networks = []
        for address in unique_local_ranges:
            unique_local_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_unique_local = any(
            NetToolsSuite.ip_within_range(*unique_local_network)
            for unique_local_network in unique_local_networks
        )
        if type(request) is IPv6Addr and is_unique_local:
            return IPv6AddrType.UNIQUE_LOCAL_ADDRESS
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4MappedHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        ipv4_mapped_ranges = ['::ffff:0:0/96']
        ipv4_mapped_networks = []
        for address in ipv4_mapped_ranges:
            ipv4_mapped_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ipv4_mapped = any(
            NetToolsSuite.ip_within_range(*ipv4_mapped_network)
            for ipv4_mapped_network in ipv4_mapped_networks
        )
        if type(request) is IPv6Addr and is_ipv4_mapped:
            return IPv6AddrType.IPV4_MAPPED
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4TranslatedHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        ipv4_translated_ranges = ['::ffff:0:0:0/96']
        ipv4_translated_networks = []
        for address in ipv4_translated_ranges:
            ipv4_translated_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ipv4_translated = any(
            NetToolsSuite.ip_within_range(*ipv4_translated_network)
            for ipv4_translated_network in ipv4_translated_networks
        )
        if type(request) is IPv6Addr and is_ipv4_translated:
            return IPv6AddrType.IPV4_TRANSLATED
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4To6TranslationHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        ipv4_to_ipv6_translation_ranges = ['64:ff9b::/96', '64:ff9b:1::/48']
        ipv4_to_ipv6_translation_networks = []
        for address in ipv4_to_ipv6_translation_ranges:
            ipv4_to_ipv6_translation_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ipv4_to_ipv6_translation = any(
            NetToolsSuite.ip_within_range(*ipv4_to_ipv6_translation_network)
            for ipv4_to_ipv6_translation_network in ipv4_to_ipv6_translation_networks
        )
        if type(request) is IPv6Addr and is_ipv4_to_ipv6_translation:
            return IPv6AddrType.IPV4_IPV6_TRANSLATION
        else:
            return super().handle(request)


class IPv6AddrClassifierDiscardPrefixHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        discard_prefix_ranges = ['100::/64']
        discard_prefix_networks = []
        for address in discard_prefix_ranges:
            discard_prefix_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_discard_prefix = any(
            NetToolsSuite.ip_within_range(*discard_prefix_network)
            for discard_prefix_network in discard_prefix_networks
        )
        if type(request) is IPv6Addr and is_discard_prefix:
            return IPv6AddrType.DISCARD_PREFIX
        else:
            return super().handle(request)


class IPv6AddrClassifierSRV6Handler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        srv6_ranges = ['5f00::/16']
        srv6_networks = []
        for address in srv6_ranges:
            srv6_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_srv6 = any(
            NetToolsSuite.ip_within_range(*srv6_network)
            for srv6_network in srv6_networks
        )
        if type(request) is IPv6Addr and is_srv6:
            return IPv6AddrType.SRV6
        else:
            return super().handle(request)


class IPv6AddrClassifier6To4SchemeHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        ipv6_to_ipv4_scheme_ranges = ['2002::/16']
        ipv6_to_ipv4_scheme_networks = []
        for address in ipv6_to_ipv4_scheme_ranges:
            ipv6_to_ipv4_scheme_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_ipv6_to_ipv4_scheme = any(
            NetToolsSuite.ip_within_range(*ipv6_to_ipv4_scheme_network)
            for ipv6_to_ipv4_scheme_network in ipv6_to_ipv4_scheme_networks
        )
        if type(request) is IPv6Addr and is_ipv6_to_ipv4_scheme:
            return IPv6AddrType.TO4
        else:
            return super().handle(request)


class IPv6AddrClassifierTeredoTunnelingHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        teredo_tunneling_ranges = ['2001::/32']
        teredo_tunneling_networks = []
        for address in teredo_tunneling_ranges:
            teredo_tunneling_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_teredo_tunneling = any(
            NetToolsSuite.ip_within_range(*teredo_tunneling_network)
            for teredo_tunneling_network in teredo_tunneling_networks
        )
        if type(request) is IPv6Addr and is_teredo_tunneling:
            return IPv6AddrType.TEREDO_TUNNELING
        else:
            return super().handle(request)


class IPv6AddrClassifierORCHIDV2Handler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        orchidv2_ranges = ['2001:20::/28']
        orchidv2_networks = []
        for address in orchidv2_ranges:
            orchidv2_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_orchidv2 = any(
            NetToolsSuite.ip_within_range(*orchidv2_network)
            for orchidv2_network in orchidv2_networks
        )
        if type(request) is IPv6Addr and is_orchidv2:
            return IPv6AddrType.ORCHIDV2
        else:
            return super().handle(request)


class IPv6AddrClassifierGlobalUnicastHandler(IPv6AddrClassifierHandler):
    def handle(self, request: Any):
        global_unicast_ranges = ['2000::/3']
        global_unicast_networks = []
        for address in global_unicast_ranges:
            global_unicast_networks.append([
                list(IPv6Addr(address[:address.find('/')]).get_binary_digits()),
                list(IPv6NetMask(address[address.find('/'):]).get_binary_digits()),
                list(request.get_binary_digits())
            ])
        is_global_unicast = any(
            NetToolsSuite.ip_within_range(*global_unicast_network)
            for global_unicast_network in global_unicast_networks
        )
        if type(request) is IPv6Addr and is_global_unicast:
            return IPv6AddrType.GLOBAL_UNICAST
        else:
            return super().handle(request)


class InterfaceIPConfig(ABC):
    """
    Abstract base class for interface IP configuration, providing a structure for IP configuration classes.
    This class defines methods to validate IP addresses and netmask, retrieve netmask,
    and represent the configuration as a string.
    """

    @abstractmethod
    def _validate(self, ip_addr: IPv4Addr, netmask: IPv4NetMask) -> bool:
        """
        Validate the provided IP address and netmask.

        Args:
        ip_addr (IPv4Addr): The IP address to validate.
        netmask (IPv4NetMask): The netmask to validate.

        Returns:
        bool: True if the IP address and netmask are valid, otherwise False.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of the IP configuration.

        Returns:
        str: The string representation of the IP configuration.
        """
        pass


class InterfaceIPv4Config(InterfaceIPConfig):
    """
    Concrete class for IPv4 interface configurations, implementing the necessary validation and adjustment methods.
    """

    def __init__(self, ip_addr: IPv4Addr, netmask: IPv4NetMask):
        """
        Initialize the interface configuration with an IP address and a netmask. Validates and adjusts the IP address
        based on the netmask.

        Args:
        ip_addr (IPv4Addr): The IP address for the configuration.
        netmask (IPv4NetMask): The netmask for the configuration.
        """
        self._validate(ip_addr, netmask)
        self._ip_addr = ip_addr
        self._netmask = netmask
        self._adjust_ip()

    @abstractmethod
    def _validate(self, ip_addr: IPv4Addr, netmask: IPv4NetMask) -> bool:
        """
        Validate the provided IP address and netmask. This method should ensure that the IP address
        is compatible with the netmask.

        Args:
        ip_addr (IPv4Addr): The IP address to validate.
        netmask (IPv4NetMask): The netmask to validate.

        Returns:
        bool: True if the IP address and netmask are valid, otherwise False.
        """
        pass

    @abstractmethod
    def _adjust_ip(self) -> None:
        """
        Adjust the IP address to ensure it is within the network defined by the netmask.
        This typically involves masking the IP address with the netmask.
        """
        pass

    @property
    def ip_addr(self) -> IPv4Addr:
        """
        Get the IP address of the configuration.

        Returns:
        IPv4Addr: The IP address.
        """
        return self._ip_addr

    @property
    def netmask(self) -> IPv4NetMask:
        """
        Get the netmask of the configuration.

        Returns:
        IPv4NetMask: The netmask.
        """
        return self._netmask

    def __str__(self) -> str:
        """
        Represent the IP configuration as a string in the CIDR format.

        Returns:
        str: The IP address and netmask in CIDR notation.
        """
        return f"{str(self.ip_addr)}/{str(self.netmask.get_mask_size())}"


class IPv4HostIPConfig(InterfaceIPv4Config):
    """
    Concrete class for configuring IPv4 addresses specifically for host IPs, with additional functionality
    to calculate and store network details such as the broadcast address and network ID.
    """
    _ip_type: IPv4AddrType = IPv4AddrType.UNDEFINED_TYPE

    def __init__(self, ip_addr: IPv4Addr, netmask: IPv4NetMask):
        """
        Initializes the IPv4HostIPConfig with an IP address and a netmask. Also calculates broadcast and network ID.

        Args:
        ip_addr (IPv4Addr): The IP address of the host.
        netmask (IPv4NetMask): The netmask associated with the IP address.
        """
        self._broadcast_ip = None
        self._network_id = None
        super().__init__(ip_addr, netmask)

    @property
    def broadcast_ip(self) -> IPv4Addr:
        """
        Get the calculated broadcast IP address for the subnet.

        Returns:
        IPv4Addr: The broadcast IP address.
        """
        return self._broadcast_ip

    @property
    def network_id(self) -> IPv4Addr:
        """
        Get the calculated network ID for the subnet.

        Returns:
        IPv4Addr: The network ID.
        """
        return self._network_id

    @property
    def host_counts(self) -> int:
        """
        Calculate the number of possible hosts in the subnet, excluding the network and broadcast addresses.

        Returns:
        int: The number of usable host addresses.
        """
        netmask_host_bit_count = list(self.netmask.get_binary_digits()).count(0)
        host_count = (2 ** netmask_host_bit_count) - 2
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def ip_type(self) -> IPv4AddrType:
        return self._ip_type

    @property
    def is_unspecified(self) -> bool:
        """
        Determine whether the IP address is an unspecified address.

        Returns:
        bool: True if the IP address is unspecified, otherwise False.
        """
        return self._ip_type == IPv4AddrType.UNSPECIFIED

    @property
    def is_public(self) -> bool:
        """
        Determine whether the IP address is a public IP address.

        Returns:
        bool: True if the IP address is public, otherwise False.
        """
        return self._ip_type == IPv4AddrType.PUBLIC

    @property
    def is_private(self) -> bool:
        """
        Determine whether the IP address is a private IP address.

        Returns:
        bool: True if the IP address is private, otherwise False.
        """
        return self.ip_type == IPv4AddrType.PRIVATE

    @property
    def is_multicast(self) -> bool:
        """
        Determine whether the IP address is a multicast IP address.

        Returns:
        bool: True if the IP address is multicast, otherwise False.
        """
        return self.ip_type == IPv4AddrType.MULTICAST

    @property
    def is_link_local(self) -> bool:
        """
        Determine whether the IP address is a link local IP address.

        Returns:
        bool: True if the IP address is link local, otherwise False.
        """
        return self.ip_type == IPv4AddrType.LINK_LOCAL

    @property
    def is_loopback(self) -> bool:
        """
        Determine whether the IP address is a loopback IP address.

        Returns:
        bool: True if the IP address is loopback, otherwise False.
        """
        return self.ip_type == IPv4AddrType.LOOPBACK

    def _adjust_ip(self) -> None:
        """
        Adjusts the internal IP address based on the netmask by calculating the broadcast IP and network ID.
        """
        self.calculate_broadcast_ip()
        self.calculate_network_id()
        self._classify_ip_address()

    def _classify_ip_address(self) -> None:
        classifier_ipv4_unspecified = IPv4AddrTypeUnspecifiedHandler()
        (
            classifier_ipv4_unspecified.set_next(IPv4AddrTypeLimitedBroadcastHandler())
            .set_next(IPv4AddrTypeCurrentNetworkHandler())
            .set_next(IPv4AddrClassifierPrivateHandler())
            .set_next(IPv4AddrClassifierPublicHandler())
            .set_next(IPv4AddrClassifierMulticastHandler())
            .set_next(IPv4AddrClassifierLinkLocalHandler())
            .set_next(IPv4AddrClassifierLoopbackHandler())
            .set_next(IPv4AddrClassifierDSLiteHandler())
            .set_next(IPv4AddrClassifierDocumentationHandler())
            .set_next(IPv4AddrClassifierCarrierNATHandler())
            .set_next(IPv4AddrClassifierBenchmarkTestingHandler())
            .set_next(IPv4AddrClassifierIP6To4RelayHandler())
            .set_next(IPv4AddrClassifierReservedHandler())
        )
        self._ip_type = classifier_ipv4_unspecified.handle(self.network_id)

    def _validate(self, ip_addr: IPv4Addr, netmask: IPv4NetMask) -> bool:
        """
        Validate that the provided IP address and netmask are instances of the appropriate classes.

        Args:
        ip_addr (IPv4Addr): The IP address to validate.
        netmask (IPv4NetMask): The netmask to validate.

        Returns:
        bool: True if both the IP address and netmask are valid, otherwise raises a ValueError.

        Raises:
        ValueError: If the IP address or netmask is not an instance of the expected classes.
        """
        validation = all([isinstance(ip_addr, IPv4Addr), type(netmask) is IPv4NetMask])
        if validation:
            return True
        else:
            raise ValueError(f"{str(ip_addr)} {str(netmask)} is not a valid IPv4 object")

    def calculate_broadcast_ip(self) -> IPv4Addr:
        """
        Calculates the broadcast IP address by setting all host bits to 1.

        Returns:
        IPv4Addr: The calculated broadcast IP address.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        broadcast_binary_digits = []
        index = 0
        for netmask_bit in self.netmask.get_binary_digits():
            if netmask_bit == 1:
                broadcast_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                broadcast_binary_digits.append(1)
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._broadcast_ip = IPv4Addr(binary_bit_ipv4_converter.handle(broadcast_binary_digits))
        return self._broadcast_ip

    def calculate_network_id(self) -> IPv4Addr:
        """
        Calculates the network ID by setting all host bits to 0.

        Returns:
        IPv4Addr: The calculated network ID.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        network_id_binary_digits = []
        index = 0
        for netmask_bit in self.netmask.get_binary_digits():
            if netmask_bit == 1:
                network_id_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                network_id_binary_digits.append(0)
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._network_id = IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))
        return self._network_id


class IPv4SubnetConfig(IPv4HostIPConfig):
    """
    Concrete class for configuring IPv4 addresses specifically for subnets, with functionalities to manage
    network details such as the first and last hosts, subnet range, and operations like subnet division and merging.
    """

    @property
    def first_host(self) -> IPv4Addr:
        """
        Get the first usable host IP address in the subnet.

        Returns:
        IPv4Addr: The first usable host IP address.
        """
        host_iterator = self.get_hosts()
        next(host_iterator)
        return next(host_iterator)

    @property
    def last_host(self) -> IPv4Addr:
        """
        Get the last usable host IP address in the subnet by calculating the second-to-last
        binary digits and adjusting the last bit.

        Returns:
        IPv4Addr: The last usable host IP address.
        """
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        non_matching_indices = netmask_binary_digits.count(0)
        network_id_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [0]
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        return IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))

    @property
    def subnet_range(self) -> str:
        """
        Get the IP address range of the subnet.

        Returns:
        str: The range from the network ID to the broadcast IP address.
        """
        return f"{self.network_id}-{self.broadcast_ip}"

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generate all possible host addresses within the subnet.

        Returns:
        Generator[IPv4Addr, None, None]: A generator that yields each host IP address in the subnet.
        """
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        non_matching_indices = netmask_binary_digits.count(0)
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        for matched_digits in itertools.product([0, 1], repeat=non_matching_indices):
            network_id_binary_digits[-non_matching_indices:] = matched_digits
            yield IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits))

    def calculate_network_id(self) -> IPv4Addr:
        """
        Recalculate and set the network ID when adjusting IP settings.

        Returns:
        IPv4Addr: The network ID of the subnet.
        """
        self._network_id = super().calculate_network_id()
        self._ip_addr = self._network_id
        return self._network_id

    def is_within(self, ip_addr: IPv4Addr) -> bool:
        """
        Check if the given IP address is within the subnet defined by this configuration.

        Args:
        ip_addr (IPv4Addr): The IP address to check.

        Returns:
        bool: True if the IP address is within the subnet, False otherwise.

        Raises:
        TypeError: If the input is not of type IPv4Addr.
        """
        if type(ip_addr) is not IPv4Addr:
            raise TypeError('ip_addr must be of type IPv4Addr')
        return NetToolsSuite.ip_within_range(
            list(self.network_id.get_binary_digits()),
            list(self.netmask.get_binary_digits()),
            list(ip_addr.get_binary_digits())
        )

    def subnet_division(self, mask: int) -> List[IPv4SubnetConfig]:
        """
        Divide the current subnet into smaller subnets based on a new mask, assuming the new mask is
        greater than the current mask.

        Args:
        mask (int): The new subnet mask size.

        Returns:
        List[IPv4SubnetConfig]: A list of new subnet configurations according to the new mask.

        Raises:
        TypeError: If mask is not an integer.
        ValueError: If mask is not larger than the current subnet mask size.
        """
        subnet_mask_size = self.netmask.get_mask_size()
        if type(mask) is not int:
            raise TypeError('mask must be of type int')
        if mask <= subnet_mask_size or mask > 32:
            raise ValueError(f'mask must be in the range of {subnet_mask_size + 1}-32')
        re_subnetting_length = mask - subnet_mask_size
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        netmask_binary_digits[subnet_mask_size: mask] = [1] * re_subnetting_length
        for subnetting_bit_combination in itertools.product([0, 1], repeat=re_subnetting_length):
            network_id_binary_digits[subnet_mask_size: mask] = subnetting_bit_combination
            yield IPv4SubnetConfig(
                IPv4Addr(binary_bit_ipv4_converter.handle(network_id_binary_digits)),
                IPv4NetMask(binary_bit_ipv4_converter.handle(netmask_binary_digits))
            )

    def subnet_merge(self, *subnets: IPv4SubnetConfig) -> IPv4SubnetConfig:
        """
        Merges the current subnet with additional subnets into a larger subnet configuration if possible.

        Args:
        *subnets (IPv4SubnetConfig): Additional subnet configurations to be merged.

        Returns:
        IPv4SubnetConfig: A new subnet configuration representing the merged subnet.

        Raises:
        ValueError: If the subnets cannot be merged due to overlapping ranges or incompatible masks.
        """
        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)
        # Ensure not all subnets are the same to prevent meaningless merging
        if len(set(map(str, subnets_need_merge))) == 1:
            raise ValueError("Merged subnets can not be the same.")
        # Extract network ID and netmask binary digits from all subnets
        network_id_binary_digits_list = [list(subnet.network_id.get_binary_digits()) for subnet in subnets_need_merge]
        netmask_binary_digits_list = [list(subnet.netmask.get_binary_digits()) for subnet in subnets_need_merge]
        # Identify bits that differ among the subnets' network IDs
        corresponding_network_id_bits = [list(bits) for bits in zip(*network_id_binary_digits_list)]
        smallest_subnetting_mask_bit = next(
            (i for i, bits in enumerate(corresponding_network_id_bits) if len(set(bits)) != 1), None
        )
        # Determine the range for possible new masks
        subnet_largest_mask = max(subnet.netmask.get_mask_size() for subnet in subnets_need_merge)
        subnet_smallest_mask = min(subnet.netmask.get_mask_size() for subnet in subnets_need_merge)
        for n in range(subnet_largest_mask - smallest_subnetting_mask_bit, 0, -1):
            subnets_matching_combination = []
            desired_matching_combination = list(itertools.product([0, 1], repeat=n))
            # Check if all combinations of network bits are covered for the new potential mask
            for network_id_binary_digits, netmask_binary_digits in zip(
                    network_id_binary_digits_list,
                    netmask_binary_digits_list
            ):
                matching_combination = NetToolsSuite.netmask_expand(
                    network_id_binary_digits[subnet_largest_mask - n: subnet_largest_mask],
                    netmask_binary_digits[subnet_largest_mask - n: subnet_largest_mask]
                )
                subnets_matching_combination.extend(matching_combination)
            # Validate the potential new mask based on the smallest mask bit position
            if smallest_subnetting_mask_bit > subnet_smallest_mask:
                raise ValueError('Provided subnets cannot be merged with current one')
            # If all combinations are matched, create a new subnet configuration with the adjusted mask
            if set(subnets_matching_combination) == set(desired_matching_combination):
                new_mask = copy.deepcopy(list(self.netmask.get_binary_digits()))
                new_mask[subnet_largest_mask - n: subnet_largest_mask] = [0] * n
                return IPv4SubnetConfig(self.ip_addr, IPv4NetMask(BinaryDigitsIPv4ConverterHandler().handle(new_mask)))
            elif len(set(subnets_matching_combination)) < len(set(desired_matching_combination)):
                raise ValueError('Provided subnets cannot be merged with current one')
        # If no valid merging configuration is found, raise an error
        raise ValueError('No valid merging configuration found for the provided subnets')


class IPv4WildcardConfig(InterfaceIPv4Config):
    """
    Concrete class for configuring IPv4 addresses using wildcard masks. This class allows for
    manipulating and querying IPv4 addresses based on the concept of wildcard masking typically used
    in network configurations.
    """

    def _validate(self, ip_addr: IPv4Addr, netmask: IPv4WildCard) -> bool:
        """
        Validate the IP address and wildcard mask to ensure they are instances of the correct classes.

        Args:
        ip_addr (IPv4Addr): The IP address to validate.
        netmask (IPv4WildCard): The wildcard mask to validate.

        Returns:
        bool: True if both the IP address and wildcard mask are valid.

        Raises:
        ValueError: If either the IP address or wildcard mask is not of the expected type.
        """
        validation = all([isinstance(ip_addr, IPv4Addr), type(netmask) is IPv4WildCard])
        if validation:
            return True
        else:
            raise ValueError(f"{str(ip_addr)} {str(netmask)} is not a valid IPv4 wildcard object")

    def _adjust_ip(self) -> None:
        """
        Adjust the IP address based on the wildcard mask by setting masked bits to zero.
        """
        self.calculate_ip_addr()

    def calculate_ip_addr(self):
        """
        Recalculate the IP address by applying the wildcard mask where wildcard bits are set to zero
        and non-wildcard bits retain the original IP address bits.

        Returns:
        IPv4Addr: The recalculated IP address.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        mapped_binary_digits = []
        index = 0
        for netmask_bit in self.netmask.get_binary_digits():
            if netmask_bit == 1:
                mapped_binary_digits.append(0)
            elif netmask_bit == 0:
                mapped_binary_digits.append(ip_addr_binary_digits[index])
            index += 1
        binary_bit_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        self._ip_addr = IPv4Addr(binary_bit_ipv4_converter.handle(mapped_binary_digits))
        return self._ip_addr

    def get_hosts(self) -> Generator[IPv4Addr, None, None]:
        """
        Generate all possible host addresses within the subnet defined by applying the wildcard mask.

        Returns:
        Generator[IPv4Addr, None, None]: A generator that yields each possible host address.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        binary_digits_ipv4_converter = BinaryDigitsIPv4ConverterHandler()
        match_bit_index = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                ip_addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv4Addr(binary_digits_ipv4_converter.handle(ip_addr_binary_digits))

    def is_within(self, ip_addr: IPv4Addr) -> bool:
        """
        Check if a given IP address falls within the range defined by the wildcard mask applied to
        the configured IP address.

        Args:
        ip_addr (IPv4Addr): The IP address to check.

        Returns:
        bool: True if the IP address is within the range, otherwise False.

        Raises:
        TypeError: If the provided IP address is not of type IPv4Addr.
        """
        if type(ip_addr) is not IPv4Addr:
            raise TypeError('ip_addr must be of type IPv4Addr')
        wildcard_ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        validate_ip_addr_binary_digits = list(ip_addr.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        match_validation = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        String representation of the IPv4 wildcard configuration.

        Returns:
        str: The IP address and wildcard mask in a readable format.
        """
        return f"{str(self.ip_addr)} {str(self.netmask)}"


class InterfaceIPv6Config(InterfaceIPConfig):
    """
    Concrete class for IPv6 interface configurations, implementing the necessary validation and adjustment methods.
    """

    def __init__(self, ip_addr: IPv6Addr, netmask: IPv6NetMask):
        """
        Initialize the interface configuration with an IP address and a netmask. Validates and adjusts the IP address
        based on the netmask.

        Args:
        ip_addr (IPv6Addr): The IP address for the configuration.
        netmask (IPv6NetMask): The netmask for the configuration.
        """
        self._validate(ip_addr, netmask)
        self._ip_addr = ip_addr
        self._netmask = netmask
        self._adjust_ip()

    @abstractmethod
    def _validate(self, ip_addr: IPv6Addr, netmask: IPv6NetMask) -> bool:
        """
        Validate the provided IP address and netmask. This method should ensure that the IP address
        is compatible with the netmask.

        Args:
        ip_addr (IPv6Addr): The IP address to validate.
        netmask (IPv6NetMask): The netmask to validate.

        Returns:
        bool: True if the IP address and netmask are valid, otherwise False.
        """
        pass

    @abstractmethod
    def _adjust_ip(self) -> None:
        """
        Adjust the IP address to ensure it is within the network defined by the netmask.
        This typically involves masking the IP address with the netmask.
        """
        pass

    @property
    def ip_addr(self) -> IPv6Addr:
        """
        Get the IP address of the configuration.

        Returns:
        IPv6Addr: The IP address.
        """
        return self._ip_addr

    @property
    def netmask(self) -> IPv6NetMask:
        """
        Get the netmask of the configuration.

        Returns:
        IPv6NetMask: The netmask.
        """
        return self._netmask

    def __str__(self) -> str:
        """
        Represent the IP configuration as a string in the CIDR format.

        Returns:
        str: The IP address and netmask in CIDR notation.
        """
        return f"{str(self.ip_addr)}/{str(self.netmask.get_mask_size())}"


class IPv6HostIPConfig(InterfaceIPv6Config):
    """
    Concrete class for configuring IPv6 addresses specifically for host IPs, with additional functionality
    to calculate and store network details.
    """
    _ip_type: IPv6AddrType = IPv6AddrType.UNDEFINED_TYPE

    def __init__(self, ip_addr: IPv6Addr, netmask: IPv6NetMask):
        """
        Initializes the IPv6HostIPConfig with an IP address and a netmask. Also calculates network ID.

        Args:
        ip_addr (IPv6Addr): The IP address of the host.
        netmask (IPv6NetMask): The netmask associated with the IP address.
        """
        self._broadcast_ip = None
        self._network_id = None
        super().__init__(ip_addr, netmask)

    @property
    def ip_type(self) -> IPv6AddrType:
        return self._ip_type

    @property
    def network_id(self) -> IPv6Addr:
        """
        Get the calculated network ID for the subnet.

        Returns:
        IPv6Addr: The network ID.
        """
        return self._network_id

    @property
    def host_counts(self) -> int:
        """
        Calculate the number of possible hosts in the subnet, excluding the network and broadcast addresses.

        Returns:
        int: The number of usable host addresses.
        """
        netmask_host_bit_count = list(self.netmask.get_binary_digits()).count(0)
        host_count = 2 ** netmask_host_bit_count
        if host_count > 0:
            return host_count
        else:
            return 0

    @property
    def is_unspecified(self) -> bool:
        """
        Determine whether the IP address is an unspecified address.

        Returns:
        bool: True if the IP address is unspecified, otherwise False.
        """
        return self._ip_type == IPv6AddrType.UNSPECIFIED

    @property
    def is_loopback(self) -> bool:
        """
        Determine whether the IP address is a loopback IP address.

        Returns:
        bool: True if the IP address is loopback, otherwise False.
        """
        return self.ip_type == IPv6AddrType.LOOPBACK

    @property
    def is_multicast(self) -> bool:
        """
        Determine whether the IP address is a multicast IP address.

        Returns:
        bool: True if the IP address is multicast, otherwise False.
        """
        return self.ip_type == IPv6AddrType.MULTICAST

    @property
    def is_link_local(self) -> bool:
        """
        Determine whether the IP address is a link local IP address.

        Returns:
        bool: True if the IP address is link local, otherwise False.
        """
        return self.ip_type == IPv6AddrType.LINK_LOCAL

    @property
    def is_global_unicast(self) -> bool:
        """
        Determine whether the IP address is a Global Unicast IP address.

        Returns:
        bool: True if the IP address is Global Unicast, otherwise False.
        """
        return self._ip_type == IPv6AddrType.GLOBAL_UNICAST

    def _adjust_ip(self) -> None:
        """
        Adjusts the internal IP address based on the netmask by calculating the network ID and classify the IP types.
        """
        self.calculate_network_id()
        self._classify_ip_address()

    def _validate(self, ip_addr: IPv6Addr, netmask: IPv6NetMask) -> bool:
        """
        Validate that the provided IP address and netmask are instances of the appropriate classes.

        Args:
        ip_addr (IPv6Addr): The IP address to validate.
        netmask (IPv6NetMask): The netmask to validate.

        Returns:
        bool: True if both the IP address and netmask are valid, otherwise raises a ValueError.

        Raises:
        ValueError: If the IP address or netmask is not an instance of the expected classes.
        """
        validation = all([isinstance(ip_addr, IPv6Addr), type(netmask) is IPv6NetMask])
        if validation:
            return True
        else:
            raise ValueError(f"{str(ip_addr)} {str(netmask)} is not a valid IPv6 object")

    def _classify_ip_address(self) -> None:
        ipv6_type_unspecified = IPv6AddrClassifierUnspecifiedHandler()

        (
            ipv6_type_unspecified.set_next(IPv6AddrClassifierLoopbackHandler())
            .set_next(IPv6AddrClassifierIPv4MappedHandler())
            .set_next(IPv6AddrClassifierIPv4TranslatedHandler())
            .set_next(IPv6AddrClassifierIPv4To6TranslationHandler())
            .set_next(IPv6AddrClassifierDiscardPrefixHandler())
            .set_next(IPv6AddrClassifierTeredoTunnelingHandler())
            .set_next(IPv6AddrClassifierDocumentationHandler())
            .set_next(IPv6AddrClassifierORCHIDV2Handler())
            .set_next(IPv6AddrClassifier6To4SchemeHandler())
            .set_next(IPv6AddrClassifierSRV6Handler())
            .set_next(IPv6AddrClassifierLinkLocalHandler())
            .set_next(IPv6AddrClassifierMulticastHandler())
            .set_next(IPv6AddrClassifierUniqueLocalHandler())
            .set_next(IPv6AddrClassifierGlobalUnicastHandler())
        )

        self._ip_type = ipv6_type_unspecified.handle(self.network_id)

    def calculate_network_id(self) -> IPv6Addr:
        """
        Calculates the network ID by setting all host bits to 0.

        Returns:
        IPv6Addr: The calculated network ID.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        network_id_binary_digits = []
        index = 0
        for netmask_bit in self.netmask.get_binary_digits():
            if netmask_bit == 1:
                network_id_binary_digits.append(ip_addr_binary_digits[index])
            elif netmask_bit == 0:
                network_id_binary_digits.append(0)
            index += 1
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        self._network_id = IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))
        return self._network_id


class IPv6SubnetConfig(IPv6HostIPConfig):
    """
    Concrete class for configuring IPv6 addresses specifically for subnets, with functionalities to manage
    network details such as the first and last hosts, subnet range, and operations like subnet division and merging.
    """

    @property
    def first_host(self) -> IPv6Addr:
        """
        Get the first usable host IP address in the subnet.

        Returns:
        IPv6Addr: The first usable host IP address.
        """
        host_iterator = self.get_hosts()
        return next(host_iterator)

    @property
    def last_host(self) -> IPv6Addr:
        """
        Get the last usable host IP address in the subnet by calculating the second-to-last
        binary digits and adjusting the last bit.

        Returns:
        IPv6Addr: The last usable host IP address.
        """
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        non_matching_indices = netmask_binary_digits.count(0)
        network_id_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        return IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))

    @property
    def subnet_range(self) -> str:
        """
        Get the IP address range of the subnet.

        Returns:
        str: The range from the network ID to the broadcast IP address.
        """
        return f"{self.first_host} - {self.last_host}"

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generate all possible host addresses within the subnet.

        Returns:
        Generator[IPv6Addr, None, None]: A generator that yields each host IP address in the subnet.
        """
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        non_matching_indices = netmask_binary_digits.count(0)
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        for matched_digits in itertools.product([0, 1], repeat=non_matching_indices):
            network_id_binary_digits[-non_matching_indices:] = matched_digits
            yield IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits))

    def calculate_network_id(self) -> IPv6Addr:
        """
        Recalculate and set the network ID when adjusting IP settings.

        Returns:
        IPv6Addr: The network ID of the subnet.
        """
        self._network_id = super().calculate_network_id()
        self._ip_addr = self._network_id
        return self._network_id

    def is_within(self, ip_addr: IPv6Addr) -> bool:
        """
        Check if the given IP address is within the subnet defined by this configuration.

        Args:
        ip_addr (IPv6Addr): The IP address to check.

        Returns:
        bool: True if the IP address is within the subnet, False otherwise.

        Raises:
        TypeError: If the input is not of type IPv6Addr.
        """
        if type(ip_addr) is not IPv6Addr:
            raise TypeError('ip_addr must be of type IPv6Addr')
        return NetToolsSuite.ip_within_range(
            list(self.network_id.get_binary_digits()),
            list(self.netmask.get_binary_digits()),
            list(ip_addr.get_binary_digits())
        )

    def subnet_division(self, mask: int) -> List[IPv6SubnetConfig]:
        """
        Divide the current subnet into smaller subnets based on a new mask, assuming the new mask is
        greater than the current mask.

        Args:
        mask (int): The new subnet mask size.

        Returns:
        List[IPv6SubnetConfig]: A list of new subnet configurations according to the new mask.

        Raises:
        TypeError: If mask is not an integer.
        ValueError: If mask is not larger than the current subnet mask size.
        """
        subnet_mask_size = self.netmask.get_mask_size()
        if type(mask) is not int:
            raise TypeError('mask must be of type int')
        if mask <= subnet_mask_size or mask > 128:
            raise ValueError(f'mask must be in the range of {subnet_mask_size + 1}-128')
        re_subnetting_length = mask - subnet_mask_size
        network_id_binary_digits = list(self.network_id.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        netmask_binary_digits[subnet_mask_size: mask] = [1] * re_subnetting_length
        for subnetting_bit_combination in itertools.product([0, 1], repeat=re_subnetting_length):
            network_id_binary_digits[subnet_mask_size: mask] = subnetting_bit_combination
            yield IPv6SubnetConfig(
                IPv6Addr(binary_bit_ipv6_converter.handle(network_id_binary_digits)),
                IPv6NetMask(binary_bit_ipv6_converter.handle(netmask_binary_digits))
            )

    def subnet_merge(self, *subnets: IPv6SubnetConfig) -> IPv6SubnetConfig:
        """
        Merges the current subnet with additional subnets into a larger subnet configuration if possible.

        Args:
        *subnets (IPv6SubnetConfig): Additional subnet configurations to be merged.

        Returns:
        IPv6SubnetConfig: A new subnet configuration representing the merged subnet.

        Raises:
        ValueError: If the subnets cannot be merged due to overlapping ranges or incompatible masks.
        """
        # Collect the current subnet and additional subnets into a list
        subnets_need_merge = [self] + list(subnets)
        # Ensure not all subnets are the same to prevent meaningless merging
        if len(set(map(str, subnets_need_merge))) == 1:
            raise ValueError("Merged subnets can not be the same.")
        # Extract network ID and netmask binary digits from all subnets
        network_id_binary_digits_list = [list(subnet.network_id.get_binary_digits()) for subnet in subnets_need_merge]
        netmask_binary_digits_list = [list(subnet.netmask.get_binary_digits()) for subnet in subnets_need_merge]
        # Identify bits that differ among the subnets' network IDs
        corresponding_network_id_bits = [list(bits) for bits in zip(*network_id_binary_digits_list)]
        smallest_subnetting_mask_bit = next(
            (i for i, bits in enumerate(corresponding_network_id_bits) if len(set(bits)) != 1), None
        )
        # Determine the range for possible new masks
        subnet_largest_mask = max(subnet.netmask.get_mask_size() for subnet in subnets_need_merge)
        subnet_smallest_mask = min(subnet.netmask.get_mask_size() for subnet in subnets_need_merge)
        for n in range(subnet_largest_mask - smallest_subnetting_mask_bit, 0, -1):
            subnets_matching_combination = []
            desired_matching_combination = list(itertools.product([0, 1], repeat=n))
            # Check if all combinations of network bits are covered for the new potential mask
            for network_id_binary_digits, netmask_binary_digits in zip(
                    network_id_binary_digits_list,
                    netmask_binary_digits_list
            ):
                matching_combination = NetToolsSuite.netmask_expand(
                    network_id_binary_digits[subnet_largest_mask - n: subnet_largest_mask],
                    netmask_binary_digits[subnet_largest_mask - n: subnet_largest_mask]
                )
                subnets_matching_combination.extend(matching_combination)
            # Validate the potential new mask based on the smallest mask bit position
            if smallest_subnetting_mask_bit > subnet_smallest_mask:
                raise ValueError('Provided subnets cannot be merged with current one')
            # If all combinations are matched, create a new subnet configuration with the adjusted mask
            if set(subnets_matching_combination) == set(desired_matching_combination):
                new_mask = copy.deepcopy(list(self.netmask.get_binary_digits()))
                new_mask[subnet_largest_mask - n: subnet_largest_mask] = [0] * n
                return IPv6SubnetConfig(self.ip_addr, IPv6NetMask(BinaryDigitsIPv6ConverterHandler().handle(new_mask)))
            elif len(set(subnets_matching_combination)) < len(set(desired_matching_combination)):
                raise ValueError('Provided subnets cannot be merged with current one')
        # If no valid merging configuration is found, raise an error
        raise ValueError('No valid merging configuration found for the provided subnets')


class IPv6WildcardConfig(InterfaceIPv6Config):
    """
    Concrete class for configuring IPv6 addresses using wildcard masks. This class allows for
    manipulating and querying IPv6 addresses based on the concept of wildcard masking typically used
    in network configurations.
    """

    def _validate(self, ip_addr: IPv6Addr, netmask: IPv6WildCard) -> bool:
        """
        Validate the IP address and wildcard mask to ensure they are instances of the correct classes.

        Args:
        ip_addr (IPv6Addr): The IP address to validate.
        netmask (IPv6WildCard): The wildcard mask to validate.

        Returns:
        bool: True if both the IP address and wildcard mask are valid.

        Raises:
        ValueError: If either the IP address or wildcard mask is not of the expected type.
        """
        validation = all([isinstance(ip_addr, IPv6Addr), type(netmask) is IPv6WildCard])
        if validation:
            return True
        else:
            raise ValueError(f"{str(ip_addr)} {str(netmask)} is not a valid IPv6 wildcard object")

    def _adjust_ip(self) -> None:
        """
        Adjust the IP address based on the wildcard mask by setting masked bits to zero.
        """
        self.calculate_ip_addr()

    def calculate_ip_addr(self):
        """
        Recalculate the IP address by applying the wildcard mask where wildcard bits are set to zero
        and non-wildcard bits retain the original IP address bits.

        Returns:
        IPv4Addr: The recalculated IP address.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        mapped_binary_digits = []
        index = 0
        for netmask_bit in self.netmask.get_binary_digits():
            if netmask_bit == 1:
                mapped_binary_digits.append(0)
            elif netmask_bit == 0:
                mapped_binary_digits.append(ip_addr_binary_digits[index])
            index += 1
        binary_bit_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        self._ip_addr = IPv6Addr(binary_bit_ipv6_converter.handle(mapped_binary_digits))
        return self._ip_addr

    def get_hosts(self) -> Generator[IPv6Addr, None, None]:
        """
        Generate all possible host addresses within the subnet defined by applying the wildcard mask.

        Returns:
        Generator[IPv6Addr, None, None]: A generator that yields each possible host address.
        """
        ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        binary_digits_ipv6_converter = BinaryDigitsIPv6ConverterHandler()
        match_bit_index = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 1:
                match_bit_index.append(mask_i)
        for wildcard_bit_combination in itertools.product([0, 1], repeat=len(match_bit_index)):
            for i, mask_i in enumerate(match_bit_index):
                ip_addr_binary_digits[mask_i] = wildcard_bit_combination[i]
            yield IPv6Addr(binary_digits_ipv6_converter.handle(ip_addr_binary_digits))

    def is_within(self, ip_addr: IPv6Addr) -> bool:
        """
        Check if a given IP address falls within the range defined by the wildcard mask applied to
        the configured IP address.

        Args:
        ip_addr (IPv6Addr): The IP address to check.

        Returns:
        bool: True if the IP address is within the range, otherwise False.

        Raises:
        TypeError: If the provided IP address is not of type IPv6Addr.
        """
        if type(ip_addr) is not IPv6Addr:
            raise TypeError('ip_addr must be of type IPv6Addr')
        wildcard_ip_addr_binary_digits = list(self.ip_addr.get_binary_digits())
        validate_ip_addr_binary_digits = list(ip_addr.get_binary_digits())
        netmask_binary_digits = list(self.netmask.get_binary_digits())
        match_validation = []
        for mask_i, mask_bit in enumerate(netmask_binary_digits):
            if mask_bit == 0:
                match_validation.append(
                    wildcard_ip_addr_binary_digits[mask_i] == validate_ip_addr_binary_digits[mask_i]
                )
        return all(match_validation)

    def __str__(self):
        """
        String representation of the IPv4 wildcard configuration.

        Returns:
        str: The IP address and wildcard mask in a readable format.
        """
        return f"{str(self.ip_addr)} {str(self.netmask)}"
