from __future__ import annotations

from abc import abstractmethod
from typing import Any, List

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.network import BinaryTools
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv6Addr, IPv6NetMask
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType


class IPv4AddrClassifierHandler(SimpleCoRHandler):
    """
    Abstract handler class in a Chain of Responsibility (CoR) pattern used to classify IPv4 addresses
    based on specific criteria. If a handler can't process the request, it forwards it to the next handler.
    """

    @abstractmethod
    def handle(self, request: Any):
        """
        Processes the IPv4 address classification request. If the current handler can't process the request,
        it forwards it to the next handler in the chain. If no handler can process it, the method returns
        a default value of 'IPv4AddrType.UNDEFINED_TYPE'.

        Parameters:
        request (Any): The request to classify the IPv4 address.

        Returns:
        Any: The result of the classification process. If no handler processes the request, it returns
        'IPv4AddrType.UNDEFINED_TYPE'.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler if self._next_handler is not None else IPv4AddrType.UNDEFINED_TYPE

    @staticmethod
    def _is_within_range(request: Any, networks: List[str]) -> bool:
        """
        Checks whether the given IPv4 address (request) falls within any of the specified network ranges.

        Parameters:
        request (Any): The IPv4 address to be checked. It is expected to have a 'binary_digits' attribute.
        networks (List[str]): A list of network address strings in CIDR notation to check the request against.

        Returns:
        bool: True if the request is within any of the provided network ranges, otherwise False.
        """
        process_networks = []
        for network in networks:
            process_networks.append([
                list(IPv4Addr(network[:network.find('/')]).binary_digits),
                list(IPv4NetMask(network[network.find('/'):]).binary_digits),
                list(request.binary_digits)
            ])
        return any(BinaryTools.is_binary_in_range(*network) for network in process_networks)


class IPv4AddrTypeUnspecifiedHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'UNSPECIFIED' if all its binary digits are zeros (i.e., 0.0.0.0).
    If the IPv4 address does not match the 'UNSPECIFIED' condition, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address is 'UNSPECIFIED' (all binary digits are zeros). If true, it returns
        'IPv4AddrType.UNSPECIFIED'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is all zeros, it returns 'IPv4AddrType.UNSPECIFIED'.
        If not, it forwards the request to the next handler in the chain.
        """
        if type(request) is IPv4Addr and all(bit == 0 for bit in list(request.get_binary_digits())):
            return IPv4AddrType.UNSPECIFIED
        else:
            return super().handle(request)


class IPv4AddrTypeLimitedBroadcastHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'LIMITED_BROADCAST' if all its binary digits are ones (i.e., 255.255.255.255).
    If the IPv4 address does not match the 'LIMITED_BROADCAST' condition, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address is 'LIMITED_BROADCAST' (all binary digits are ones). If true, it returns
        'IPv4AddrType.LIMITED_BROADCAST'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is all ones, it returns 'IPv4AddrType.LIMITED_BROADCAST'.
        If not, it forwards the request to the next handler in the chain.
        """
        if type(request) is IPv4Addr and all(bit == 1 for bit in list(request.binary_digits)):
            return IPv4AddrType.LIMITED_BROADCAST
        else:
            return super().handle(request)


class IPv4AddrTypeCurrentNetworkHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'CURRENT_NETWORK' if it falls within the '0.0.0.0/8' network range.
    If the IPv4 address does not match the 'CURRENT_NETWORK' condition, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the 'CURRENT_NETWORK' range ('0.0.0.0/8'). If true, it returns
        'IPv4AddrType.CURRENT_NETWORK'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is within '0.0.0.0/8', it returns
        'IPv4AddrType.CURRENT_NETWORK'. If not, it forwards the request to the next handler in the chain.
        """
        current_networks = ['0.0.0.0/8']
        if type(request) is IPv4Addr and self._is_within_range(request, current_networks):
            return IPv4AddrType.CURRENT_NETWORK
        else:
            return super().handle(request)


class IPv4AddrClassifierPublicHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'PUBLIC' if it does not fall within any of the non-public network ranges.
    If the IPv4 address matches a non-public range, it passes the request to the next handler in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address is public by verifying that it does not fall within the non-public network ranges.
        If true, it returns 'IPv4AddrType.PUBLIC'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is public, it returns 'IPv4AddrType.PUBLIC'.
        If not, it forwards the request to the next handler in the chain.
        """
        not_public_networks = [
            '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
            '172.16.0.0/12', '192.0.0.0/24', '192.0.2.0/24', '192.88.99.0/24', '192.168.0.0/16',
            '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24', '224.0.0.0/4', '233.252.0.0/24',
            '240.0.0.0/4', '255.255.255.255/32'
        ]
        if type(request) is IPv4Addr and not self._is_within_range(request, not_public_networks):
            return IPv4AddrType.PUBLIC
        else:
            return super().handle(request)


class IPv4AddrClassifierPrivateHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'PRIVATE' if it falls within the private network ranges.
    If the IPv4 address does not match the private range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the private network ranges ('10.0.0.0/8', '172.16.0.0/12',
        '192.168.0.0/16'). If true, it returns 'IPv4AddrType.PRIVATE'. Otherwise, it forwards the request
        to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is private, it returns 'IPv4AddrType.PRIVATE'.
        If not, it forwards the request to the next handler in the chain.
        """
        private_networks = [
            '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'
        ]
        if type(request) is IPv4Addr and self._is_within_range(request, private_networks):
            return IPv4AddrType.PRIVATE
        else:
            return super().handle(request)


class IPv4AddrClassifierMulticastHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'MULTICAST' if it falls within the multicast network range.
    If the IPv4 address does not match the multicast range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the multicast network range ('224.0.0.0/4'). If true, it returns
        'IPv4AddrType.MULTICAST'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is a multicast address, it returns
        'IPv4AddrType.MULTICAST'. If not, it forwards the request to the next handler in the chain.
        """
        multicast_networks = ["224.0.0.0/4"]
        if type(request) is IPv4Addr and self._is_within_range(request, multicast_networks):
            return IPv4AddrType.MULTICAST
        else:
            return super().handle(request)


class IPv4AddrClassifierLinkLocalHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'LINK_LOCAL' if it falls within the link-local network range.
    If the IPv4 address does not match the link-local range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the link-local network range ('169.254.0.0/16'). If true, it returns
        'IPv4AddrType.LINK_LOCAL'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is a link-local address, it returns
        'IPv4AddrType.LINK_LOCAL'. If not, it forwards the request to the next handler in the chain.
        """
        link_local_networks = ["169.254.0.0/16"]
        if type(request) is IPv4Addr and self._is_within_range(request, link_local_networks):
            return IPv4AddrType.LINK_LOCAL
        else:
            return super().handle(request)


class IPv4AddrClassifierLoopbackHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'LOOPBACK' if it falls within the loopback network range.
    If the IPv4 address does not match the loopback range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the loopback network range ('127.0.0.0/8'). If true, it returns
        'IPv4AddrType.LOOPBACK'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is a loopback address, it returns
        'IPv4AddrType.LOOPBACK'. If not, it forwards the request to the next handler in the chain.
        """
        loopback_networks = ["127.0.0.0/8"]
        if type(request) is IPv4Addr and self._is_within_range(request, loopback_networks):
            return IPv4AddrType.LOOPBACK
        else:
            return super().handle(request)


class IPv4AddrClassifierDocumentationHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'DOCUMENTATION' if it falls within any of the documentation
    address ranges. These addresses are reserved for use in documentation and examples.
    If the IPv4 address does not match the documentation range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within any of the documentation address ranges
        ('192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '233.252.0.0/24'). If true, it returns
        'IPv4AddrType.DOCUMENTATION'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is a documentation address, it returns
        'IPv4AddrType.DOCUMENTATION'. If not, it forwards the request to the next handler in the chain.
        """
        documentation_networks = ['192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '233.252.0.0/24']
        if type(request) is IPv4Addr and self._is_within_range(request, documentation_networks):
            return IPv4AddrType.DOCUMENTATION
        else:
            return super().handle(request)


class IPv4AddrClassifierDSLiteHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'DS_LITE' if it falls within the DS-Lite network range.
    If the IPv4 address does not match the DS-Lite range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the DS-Lite network range ('192.0.0.0/24'). If true, it returns
        'IPv4AddrType.DS_LITE'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is a DS-Lite address, it returns
        'IPv4AddrType.DS_LITE'. If not, it forwards the request to the next handler in the chain.
        """
        ds_lite_networks = ['192.0.0.0/24']
        if type(request) is IPv4Addr and self._is_within_range(request, ds_lite_networks):
            return IPv4AddrType.DS_LITE
        else:
            return super().handle(request)


class IPv4AddrClassifierCarrierNATHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'CARRIER_GRADE_NAT' if it falls within the carrier-grade NAT
    (CGNAT) network range. If the IPv4 address does not match the CGNAT range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the carrier-grade NAT network range ('100.64.0.0/10').
        If true, it returns 'IPv4AddrType.CARRIER_GRADE_NAT'. Otherwise, it forwards the request to the next handler
        in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is within the CGNAT range, it returns
        'IPv4AddrType.CARRIER_GRADE_NAT'. If not, it forwards the request to the next handler in the chain.
        """
        carrier_grade_networks = ['100.64.0.0/10']
        if type(request) is IPv4Addr and self._is_within_range(request, carrier_grade_networks):
            return IPv4AddrType.CARRIER_GRADE_NAT
        else:
            return super().handle(request)


class IPv4AddrClassifierBenchmarkTestingHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'BENCHMARK_TESTING' if it falls within the network range
    used for benchmarking tests. If the IPv4 address does not match the benchmark testing range,
    it passes the request to the next handler in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the benchmark testing network range ('198.18.0.0/15').
        If true, it returns 'IPv4AddrType.BENCHMARK_TESTING'. Otherwise, it forwards the request to the next
        handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is within the benchmark testing range,
        it returns 'IPv4AddrType.BENCHMARK_TESTING'. If not, it forwards the request to the next handler
        in the chain.
        """
        benchmark_testing_networks = ['198.18.0.0/15']
        if type(request) is IPv4Addr and self._is_within_range(request, benchmark_testing_networks):
            return IPv4AddrType.BENCHMARK_TESTING
        else:
            return super().handle(request)


class IPv4AddrClassifierIP6To4RelayHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'IPV6_TO_IPV4_RELAY' if it falls within the 6to4 relay network range.
    If the IPv4 address does not match the 6to4 relay range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the 6to4 relay network range ('192.88.99.0/24').
        If true, it returns 'IPv4AddrType.IPV6_TO_IPV4_RELAY'. Otherwise, it forwards the request to the next
        handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is within the 6to4 relay range,
        it returns 'IPv4AddrType.IPV6_TO_IPV4_RELAY'. If not, it forwards the request to the next handler
        in the chain.
        """
        ipv6_to_ipv4_relay_networks = ['192.88.99.0/24']
        if type(request) is IPv4Addr and self._is_within_range(request, ipv6_to_ipv4_relay_networks):
            return IPv4AddrType.IPV6_TO_IPV4_RELAY
        else:
            return super().handle(request)


class IPv4AddrClassifierReservedHandler(IPv4AddrClassifierHandler):
    """
    This handler classifies an IPv4 address as 'RESERVED' if it falls within the reserved network range.
    If the IPv4 address does not match the reserved range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv4 address falls within the reserved network range ('240.0.0.0/4').
        If true, it returns 'IPv4AddrType.RESERVED'. Otherwise, it forwards the request to the next
        handler in the chain.

        Parameters:
        request (Any): The request containing the IPv4 address to classify.

        Returns:
        IPv4AddrType: The type of the IPv4 address. If the address is within the reserved range,
        it returns 'IPv4AddrType.RESERVED'. If not, it forwards the request to the next handler
        in the chain.
        """
        reserved_networks = ['240.0.0.0/4']
        if type(request) is IPv4Addr and self._is_within_range(request, reserved_networks):
            return IPv4AddrType.RESERVED
        else:
            return super().handle(request)


class IPv6AddrClassifierHandler(SimpleCoRHandler):
    """
    Abstract handler class in a Chain of Responsibility (CoR) pattern used to classify IPv6 addresses
    based on specific criteria. If a handler can't process the request, it forwards it to the next handler.
    """
    @abstractmethod
    def handle(self, request: Any):
        """
        Processes the IPv6 address classification request. If the current handler can't process the request,
        it forwards it to the next handler in the chain. If no handler can process it, the method returns
        a default value of 'IPv6AddrType.UNDEFINED_TYPE'.

        Parameters:
        request (Any): The request to classify the IPv6 address.

        Returns:
        Any: The result of the classification process. If no handler processes the request, it returns
        'IPv6AddrType.UNDEFINED_TYPE'.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler if self._next_handler is not None else IPv6AddrType.UNDEFINED_TYPE

    @staticmethod
    def _is_within_range(request: Any, networks: List[str]) -> bool:
        """
        Checks whether the given IPv6 address (request) falls within any of the specified network ranges.

        Parameters:
        request (Any): The IPv6 address to be checked. It is expected to have a 'binary_digits' attribute.
        networks (List[str]): A list of network address strings in CIDR notation to check the request against.

        Returns:
        bool: True if the request is within any of the provided network ranges, otherwise False.
        """
        process_networks = []
        for network in networks:
            process_networks.append([
                list(IPv6Addr(network[:network.find('/')]).binary_digits),
                list(IPv6NetMask(network[network.find('/'):]).binary_digits),
                list(request.binary_digits)
            ])
        return any(BinaryTools.is_binary_in_range(*network) for network in process_networks)


class IPv6AddrClassifierUnspecifiedHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'UNSPECIFIED' if it falls within the unspecified address range.
    If the IPv6 address does not match the unspecified range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address is unspecified ('::/128'). If true, it returns 'IPv6AddrType.UNSPECIFIED'.
        Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is unspecified, it returns
        'IPv6AddrType.UNSPECIFIED'. If not, it forwards the request to the next handler in the chain.
        """
        unspecified_networks = ['::/128']
        if type(request) is IPv6Addr and self._is_within_range(request, unspecified_networks):
            return IPv6AddrType.UNSPECIFIED
        else:
            return super().handle(request)


class IPv6AddrClassifierLoopbackHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'LOOPBACK' if it falls within the loopback network range.
    If the IPv6 address does not match the loopback range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the loopback network range ('::1/128'). If true, it returns
        'IPv6AddrType.LOOPBACK'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is a loopback address, it returns
        'IPv6AddrType.LOOPBACK'. If not, it forwards the request to the next handler in the chain.
        """
        loopback_networks = ['::1/128']
        if type(request) is IPv6Addr and self._is_within_range(request, loopback_networks):
            return IPv6AddrType.LOOPBACK
        else:
            return super().handle(request)


class IPv6AddrClassifierDocumentationHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'DOCUMENTATION' if it falls within the documentation address ranges.
    These addresses are reserved for use in documentation and examples. If the IPv6 address does not match the
    documentation ranges, it passes the request to the next handler in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within any of the documentation address ranges
        ('2001:db8::/32', '3fff::/20'). If true, it returns 'IPv6AddrType.DOCUMENTATION'. Otherwise,
        it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is used for documentation, it returns
        'IPv6AddrType.DOCUMENTATION'. If not, it forwards the request to the next handler in the chain.
        """
        documentation_networks = ['2001:db8::/32', '3fff::/20']
        if type(request) is IPv6Addr and self._is_within_range(request, documentation_networks):
            return IPv6AddrType.DOCUMENTATION
        else:
            return super().handle(request)


class IPv6AddrClassifierLinkLocalHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'LINK_LOCAL' if it falls within the link-local address range.
    If the IPv6 address does not match the link-local range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the link-local network range ('fe80::/64'). If true, it returns
        'IPv6AddrType.LINK_LOCAL'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is link-local, it returns
        'IPv6AddrType.LINK_LOCAL'. If not, it forwards the request to the next handler in the chain.
        """
        link_local_networks = ['fe80::/64']
        if type(request) is IPv6Addr and self._is_within_range(request, link_local_networks):
            return IPv6AddrType.LINK_LOCAL
        else:
            return super().handle(request)


class IPv6AddrClassifierMulticastHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'MULTICAST' if it falls within the multicast address range.
    If the IPv6 address does not match the multicast range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the multicast network range ('ff00::/8'). If true, it returns
        'IPv6AddrType.MULTICAST'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is a multicast address, it returns
        'IPv6AddrType.MULTICAST'. If not, it forwards the request to the next handler in the chain.
        """
        multicast_networks = ['ff00::/8']
        if type(request) is IPv6Addr and self._is_within_range(request, multicast_networks):
            return IPv6AddrType.MULTICAST
        else:
            return super().handle(request)


class IPv6AddrClassifierUniqueLocalHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'UNIQUE_LOCAL' if it falls within the unique local address range.
    If the IPv6 address does not match the unique local range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the unique local address range ('fc00::/7'). If true, it returns
        'IPv6AddrType.UNIQUE_LOCAL'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is a unique local address, it returns
        'IPv6AddrType.UNIQUE_LOCAL'. If not, it forwards the request to the next handler in the chain.
        """
        unique_local_networks = ['fc00::/7']
        if type(request) is IPv6Addr and self._is_within_range(request, unique_local_networks):
            return IPv6AddrType.UNIQUE_LOCAL
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4MappedHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'IPV4_MAPPED' if it falls within the IPv4-mapped address range.
    If the IPv6 address does not match the IPv4-mapped range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address is an IPv4-mapped address ('::ffff:0:0/96'). If true, it returns
        'IPv6AddrType.IPV4_MAPPED'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is an IPv4-mapped address, it returns
        'IPv6AddrType.IPV4_MAPPED'. If not, it forwards the request to the next handler in the chain.
        """
        ipv4_mapped_networks = ['::ffff:0:0/96']
        if type(request) is IPv6Addr and self._is_within_range(request, ipv4_mapped_networks):
            return IPv6AddrType.IPV4_MAPPED
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4TranslatedHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'IPV4_TRANSLATED' if it falls within the IPv4-translated address range.
    If the IPv6 address does not match the IPv4-translated range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address is an IPv4-translated address ('::ffff:0:0:0/96'). If true, it returns
        'IPv6AddrType.IPV4_TRANSLATED'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is an IPv4-translated address, it returns
        'IPv6AddrType.IPV4_TRANSLATED'. If not, it forwards the request to the next handler in the chain.
        """
        ipv4_translated_networks = ['::ffff:0:0:0/96']
        if type(request) is IPv6Addr and self._is_within_range(request, ipv4_translated_networks):
            return IPv6AddrType.IPV4_TRANSLATED
        else:
            return super().handle(request)


class IPv6AddrClassifierIPv4To6TranslationHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'IPV4_IPV6_TRANSLATION' if it falls within the IPv4-to-IPv6
    translation address ranges. If the IPv6 address does not match the translation range, it passes the request
    to the next handler in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the IPv4-to-IPv6 translation address range ('64:ff9b::/96' or
        '64:ff9b:1::/48'). If true, it returns 'IPv6AddrType.IPV4_IPV6_TRANSLATION'. Otherwise, it forwards the
        request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is within the IPv4-to-IPv6 translation range,
        it returns 'IPv6AddrType.IPV4_IPV6_TRANSLATION'. If not, it forwards the request to the next handler
        in the chain.
        """
        ipv4_to_ipv6_translation_networks = ['64:ff9b::/96', '64:ff9b:1::/48']
        if type(request) is IPv6Addr and self._is_within_range(request, ipv4_to_ipv6_translation_networks):
            return IPv6AddrType.IPV4_IPV6_TRANSLATION
        else:
            return super().handle(request)


class IPv6AddrClassifierDiscardPrefixHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'DISCARD_PREFIX' if it falls within the discard prefix range.
    If the IPv6 address does not match the discard prefix range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the discard prefix range ('100::/64'). If true, it returns
        'IPv6AddrType.DISCARD_PREFIX'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is within the discard prefix range, it returns
        'IPv6AddrType.DISCARD_PREFIX'. If not, it forwards the request to the next handler in the chain.
        """
        discard_prefix_networks = ['100::/64']
        if type(request) is IPv6Addr and self._is_within_range(request, discard_prefix_networks):
            return IPv6AddrType.DISCARD_PREFIX
        else:
            return super().handle(request)


class IPv6AddrClassifierSRV6Handler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'SRV6' if it falls within the SRv6 (Segment Routing over IPv6)
    address range. If the IPv6 address does not match the SRv6 range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the SRv6 address range ('5f00::/16'). If true, it returns
        'IPv6AddrType.SRV6'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is within the SRv6 range, it returns
        'IPv6AddrType.SRV6'. If not, it forwards the request to the next handler in the chain.
        """
        srv6_networks = ['5f00::/16']
        if type(request) is IPv6Addr and self._is_within_range(request, srv6_networks):
            return IPv6AddrType.SRV6
        else:
            return super().handle(request)


class IPv6AddrClassifier6To4SchemeHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'IP6_TO4' if it falls within the 6to4 address range, which
    is used to transition IPv4 to IPv6. If the IPv6 address does not match the 6to4 range, it passes the request
    to the next handler in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the 6to4 scheme address range ('2002::/16'). If true, it returns
        'IPv6AddrType.IP6_TO4'. Otherwise, it forwards the request to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is within the 6to4 scheme range, it returns
        'IPv6AddrType.IP6_TO4'. If not, it forwards the request to the next handler in the chain.
        """
        ipv6_to_ipv4_scheme_networks = ['2002::/16']
        if type(request) is IPv6Addr and self._is_within_range(request, ipv6_to_ipv4_scheme_networks):
            return IPv6AddrType.IP6_TO4
        else:
            return super().handle(request)


class IPv6AddrClassifierTeredoTunnelingHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'TEREDO_TUNNELING' if it falls within the Teredo tunneling address range.
    If the IPv6 address does not match the Teredo tunneling range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the Teredo tunneling address range ('2001::/32').
        If true, it returns 'IPv6AddrType.TEREDO_TUNNELING'. Otherwise, it forwards the request
        to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is a Teredo tunneling address, it returns
        'IPv6AddrType.TEREDO_TUNNELING'. If not, it forwards the request to the next handler in the chain.
        """
        teredo_tunneling_networks = ['2001::/32']
        if type(request) is IPv6Addr and self._is_within_range(request, teredo_tunneling_networks):
            return IPv6AddrType.TEREDO_TUNNELING
        else:
            return super().handle(request)


class IPv6AddrClassifierORCHIDV2Handler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'ORCHIDV2' if it falls within the ORCHIDv2 address range.
    If the IPv6 address does not match the ORCHIDv2 range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the ORCHIDv2 address range ('2001:20::/28').
        If true, it returns 'IPv6AddrType.ORCHIDV2'. Otherwise, it forwards the request
        to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is an ORCHIDv2 address, it returns
        'IPv6AddrType.ORCHIDV2'. If not, it forwards the request to the next handler in the chain.
        """
        orchidv2_networks = ['2001:20::/28']
        if type(request) is IPv6Addr and self._is_within_range(request, orchidv2_networks):
            return IPv6AddrType.ORCHIDV2
        else:
            return super().handle(request)


class IPv6AddrClassifierGlobalUnicastHandler(IPv6AddrClassifierHandler):
    """
    This handler classifies an IPv6 address as 'GLOBAL_UNICAST' if it falls within the global unicast address range.
    If the IPv6 address does not match the global unicast range, it passes the request to the next handler
    in the chain.
    """
    def handle(self, request: Any):
        """
        Checks if the IPv6 address falls within the global unicast address range ('2000::/3').
        If true, it returns 'IPv6AddrType.GLOBAL_UNICAST'. Otherwise, it forwards the request
        to the next handler in the chain.

        Parameters:
        request (Any): The request containing the IPv6 address to classify.

        Returns:
        IPv6AddrType: The type of the IPv6 address. If the address is a global unicast address, it returns
        'IPv6AddrType.GLOBAL_UNICAST'. If not, it forwards the request to the next handler in the chain.
        """
        global_unicast_networks = ['2000::/3']
        if type(request) is IPv6Addr and self._is_within_range(request, global_unicast_networks):
            return IPv6AddrType.GLOBAL_UNICAST
        else:
            return super().handle(request)


class IPAddrTypeClassifier:
    """
    A utility class for classifying both IPv4 and IPv6 addresses using a series of handler classes.
    It constructs a chain of responsibility pattern, where the request is passed through multiple classifiers
    until a match is found.
    """

    @staticmethod
    def classify_ipv4_type(request_format: Any, classifiers: List[IPAddrTypeClassifier] = None) -> IPv4AddrType:
        """
        Classifies the type of an IPv4 address by passing it through a series of handlers (classifiers).
        If no classifiers are provided, a default set of classifiers is used.

        Parameters:
        request_format (Any): The IPv4 address to classify.
        classifiers (List[IPAddrTypeClassifier]): Optional. A list of IPv4 address classifiers (handlers).

        Returns:
        IPv4AddrType: The type of the IPv4 address based on the classification.
        """
        if classifiers is None:
            classifiers = [
                IPv4AddrTypeLimitedBroadcastHandler(),
                IPv4AddrTypeCurrentNetworkHandler(),
                IPv4AddrClassifierPrivateHandler(),
                IPv4AddrClassifierPublicHandler(),
                IPv4AddrClassifierMulticastHandler(),
                IPv4AddrClassifierLinkLocalHandler(),
                IPv4AddrClassifierLoopbackHandler(),
                IPv4AddrClassifierDSLiteHandler(),
                IPv4AddrClassifierDocumentationHandler(),
                IPv4AddrClassifierCarrierNATHandler(),
                IPv4AddrClassifierBenchmarkTestingHandler(),
                IPv4AddrClassifierIP6To4RelayHandler(),
                IPv4AddrClassifierReservedHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)

    @staticmethod
    def classify_ipv6_type(request_format: Any, classifiers: List[IPAddrTypeClassifier] = None) -> IPv6AddrType:
        """
        Classifies the type of an IPv6 address by passing it through a series of handlers (classifiers).
        If no classifiers are provided, a default set of classifiers is used.

        Parameters:
        request_format (Any): The IPv6 address to classify.
        classifiers (List[IPAddrTypeClassifier]): Optional. A list of IPv6 address classifiers (handlers).

        Returns:
        IPv6AddrType: The type of the IPv6 address based on the classification.
        """
        if classifiers is None:
            classifiers = [
                IPv6AddrClassifierLoopbackHandler(),
                IPv6AddrClassifierIPv4MappedHandler(),
                IPv6AddrClassifierIPv4TranslatedHandler(),
                IPv6AddrClassifierIPv4To6TranslationHandler(),
                IPv6AddrClassifierDiscardPrefixHandler(),
                IPv6AddrClassifierTeredoTunnelingHandler(),
                IPv6AddrClassifierDocumentationHandler(),
                IPv6AddrClassifierORCHIDV2Handler(),
                IPv6AddrClassifier6To4SchemeHandler(),
                IPv6AddrClassifierSRV6Handler(),
                IPv6AddrClassifierLinkLocalHandler(),
                IPv6AddrClassifierMulticastHandler(),
                IPv6AddrClassifierUniqueLocalHandler(),
                IPv6AddrClassifierGlobalUnicastHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(request_format)
