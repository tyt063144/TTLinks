from __future__ import annotations

from abc import abstractmethod
from typing import Any, List

from ttlinks.common.design_template.cor import ListBasedCoRHandler
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType, IPv4TypeAddrBlocks, IPv6TypeAddrBlocks
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv6Addr, IPv6NetMask
from ttlinks.ipservice import ip_configs


class IPv4SubnetClassifierHandler(ListBasedCoRHandler):
    """
    A handler for classifying IPv4 subnets using the Chain of Responsibility (CoR) pattern.
    This class is specifically designed for subnet configurations and overlaps with predefined subnet ranges.

    Methods:
        - _validate: Validates the input request as an IPv4SubnetConfig object.
        - handle: Processes the request or delegates it to the next handler.
        - _has_overlap: Checks if two numerical ranges overlap.
        - _check_range_overlap: Checks if a given IPv4 subnet overlaps with a list of predefined subnet ranges.
    """

    @staticmethod
    def _validate(request: Any, *args, **kwargs):
        """
        Validates that the request is an instance of `IPv4SubnetConfig`.

        Parameters:
        request (Any): The input request to validate.

        Raises:
        ValueError: If the request is not of type `IPv4SubnetConfig`.
        """
        if kwargs.get('validated') is True:
            return True
        if not isinstance(request, ip_configs.IPv4SubnetConfig) and kwargs.get('validated') is False:
            raise ValueError(f"Expected IPv4SubnetConfig object, got {type(request)}")
        return True

    @staticmethod
    def _has_overlap(given: List[int], compared: List[int]) -> bool:
        """
        Determines whether two numerical ranges overlap.

        Parameters:
        given (List[int]): A list representing a numerical range [start, end].
        compared (List[int]): A list representing another numerical range [start, end].

        Returns:
        bool: True if the ranges overlap, False otherwise.

        Raises:
        ValueError: If either input list does not contain exactly two elements.
        """
        if len(given) != 2 or len(compared) != 2:
            raise ValueError("Both given and compared must be lists of length 2.")
        return not (given[1] < compared[0] or compared[1] < given[0])

    def _check_range_overlap(self, request: ip_configs.IPv4SubnetConfig, networks: List[str]) -> bool:
        """
        Checks whether the given IPv4 subnet overlaps with any network in the list.

        Parameters:
        request (ip_configs.IPv4SubnetConfig): The IPv4 subnet to check.
        networks (List[str]): A list of networks in CIDR notation (e.g., "192.168.0.0/16").

        Returns:
        bool: True if the IPv4 subnet overlaps with any of the predefined networks, False otherwise.
        """
        result = []
        for network in networks:
            addr = network[:network.find('/')]
            mask = network[network.find('/') + 1:]
            network_subnet = ip_configs.IPv4SubnetConfig(IPv4Addr(addr), IPv4NetMask(f"/{mask}"))
            network_range = [given_ipv4_addr.as_decimal for given_ipv4_addr in network_subnet.subnet_range]
            if self._has_overlap(network_range, [compare_ipv4_addr.as_decimal for compare_ipv4_addr in request.subnet_range]):
                result.append(True)
            else:
                result.append(False)
        return any(result)

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Processes the request or passes it to the next handler in the chain.

        Parameters:
        request (Any): The input subnet configuration to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The classification result for the IPv4 subnet. If no handler processes the request,
        it returns IPv4AddrType.UNDEFINED_TYPE or the result from the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request, *args, **kwargs)
        return self._next_handler if self._next_handler is not None else IPv4AddrType.UNDEFINED_TYPE

class IPv4SubnetTypeUnspecifiedHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'CURRENT_NETWORK' address block.
    If it does, it classifies the subnet as 'UNSPECIFIED' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.UNSPECIFIED.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.UNSPECIFIED)
        return super().handle(request, validated=validated)

class IPv4SubnetTypeLimitedBroadcastHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'LIMITED_BROADCAST' address block.
    If it does, it classifies the subnet as 'LIMITED_BROADCAST' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.LIMITED_BROADCAST.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.LIMITED_BROADCAST)
        return super().handle(request, validated=validated)

class IPv4SubnetTypeCurrentNetworkHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'CURRENT_NETWORK' address block.
    If it does, it classifies the subnet as 'CURRENT_NETWORK' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.CURRENT_NETWORK.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.CURRENT_NETWORK)
        return super().handle(request, validated=validated)

class IPv4SubnetClassifierPrivateHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'PRIVATE' address block.
    If it does, it classifies the subnet as 'PRIVATE' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.PRIVATE.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.PRIVATE)
        return super().handle(request, validated=validated)

class IPv4SubnetClassifierPublicHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'PUBLIC' address block.
    If it does, it classifies the subnet as 'PUBLIC' and adds it to the list of items.
    Rewrite the _check_range_overlap method to check if the given range overlaps with any reserved ranges.
    """
    def _check_range_overlap(self, request: ip_configs.IPv4SubnetConfig, reserved_ranges: List[List[int]]) -> bool:
        start_ip, end_ip = [ipv4_addr.as_decimal for ipv4_addr in request.subnet_range]
        for reserved in reserved_ranges:
            reserved_start, reserved_end = reserved
            # If the given range is completely within the reserved range, it cannot be public
            if reserved_start <= start_ip <= reserved_end and reserved_start <= end_ip <= reserved_end:
                return False
        # Check if either the start or end exceeds any reserved range's boundaries
        for reserved in reserved_ranges:
            reserved_start, reserved_end = reserved
            if start_ip < reserved_start or end_ip > reserved_end:
                return True
        return False

    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.PUBLIC.value
        subnet_ranges = []
        for network in networks:
            addr = network[:network.find('/')]
            mask = network[network.find('/') + 1:]
            subnet = ip_configs.IPv4SubnetConfig(IPv4Addr(addr), IPv4NetMask(f"/{mask}"))
            subnet_range = [given_ipv4_addr.as_decimal for given_ipv4_addr in subnet.subnet_range]
            subnet_ranges.append(subnet_range)
        if self._check_range_overlap(request, subnet_ranges):
            self._items.append(IPv4AddrType.PUBLIC)
        return super().handle(request, validated=validated)

class IPv4SubnetClassifierMulticastHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'MULTICAST' address block.
    If it does, it classifies the subnet as 'MULTICAST' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.MULTICAST.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.MULTICAST)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierLinkLocalHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'LINK_LOCAL' address block.
    If it does, it classifies the subnet as 'LINK_LOCAL' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.LINK_LOCAL.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.LINK_LOCAL)
        return super().handle(request, validated=validated)

class IPv4SubnetClassifierLoopbackHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'LOOPBACK' address block.
    If it does, it classifies the subnet as 'LOOPBACK' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.LOOPBACK.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.LOOPBACK)
        return super().handle(request, validated=validated)

class IPv4SubnetClassifierDocumentationHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'DOCUMENTATION' address block.
    If it does, it classifies the subnet as 'DOCUMENTATION' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.DOCUMENTATION.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.DOCUMENTATION)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierDSLiteHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'DS_LITE' address block.
    If it does, it classifies the subnet as 'DS_LITE' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.DS_LITE.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.DS_LITE)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierCarrierNATHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'CARRIER_GRADE_NAT' address block.
    If it does, it classifies the subnet as 'CARRIER_GRADE_NAT' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.CARRIER_GRADE_NAT.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.CARRIER_GRADE_NAT)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierBenchmarkTestingHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'BENCHMARK_TESTING' address block.
    If it does, it classifies the subnet as 'BENCHMARK_TESTING' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.BENCHMARK_TESTING.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.BENCHMARK_TESTING)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierIP6To4RelayHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'IP6_TO4_RELAY' address block.
    If it does, it classifies the subnet as 'IP6_TO4_RELAY' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.IPV6_TO_IPV4_RELAY.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.IPV6_TO_IPV4_RELAY)
        return super().handle(request, validated=validated)


class IPv4SubnetClassifierReservedHandler(IPv4SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'RESERVED' address block.
    If it does, it classifies the subnet as 'RESERVED' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.RESERVED.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv4AddrType.RESERVED)
        return super().handle(request, validated=validated)

class IPv6SubnetClassifierHandler(ListBasedCoRHandler):
    """
    A handler for classifying IPv6 subnets using the Chain of Responsibility (CoR) pattern.
    This class is specifically designed for subnet configurations and checks overlaps with predefined IPv6 subnet ranges.

    Methods:
        - _validate: Ensures the input request is a valid IPv6SubnetConfig object.
        - handle: Processes the request or delegates it to the next handler in the chain.
        - _has_overlap: Determines if two numerical ranges overlap.
        - _check_range_overlap: Verifies if a given IPv6 subnet overlaps with predefined subnet ranges.
    """

    def _validate(self, request: Any, *args, **kwargs):
        """
        Validates that the request is an instance of `IPv6SubnetConfig`.

        Parameters:
        request (Any): The input request to validate.

        Raises:
        ValueError: If the request is not of type `IPv6SubnetConfig`.
        """
        if kwargs.get('validated') is True:
            return True
        if not isinstance(request, ip_configs.IPv4SubnetConfig) and kwargs.get('validated') is False:
            raise ValueError(f"Expected IPv6SubnetConfig object, got {type(request)}")
        return True

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Processes the given request or passes it to the next handler in the chain if unhandled.

        Parameters:
        request (Any): The IPv6 subnet configuration to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The classification result for the IPv6 subnet. If no handler processes the request,
        it returns IPv6AddrType.UNDEFINED_TYPE or the result from the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request, *args, **kwargs)
        return self._next_handler if self._next_handler is not None else IPv6AddrType.UNDEFINED_TYPE

    @staticmethod
    def _has_overlap(given: List[int], compared: List[int]) -> bool:
        """
        Determines whether two numerical ranges overlap.

        Parameters:
        given (List[int]): A list representing a numerical range [start, end].
        compared (List[int]): A list representing another numerical range [start, end].

        Returns:
        bool: True if the ranges overlap, False otherwise.

        Raises:
        ValueError: If either input list does not contain exactly two elements.
        """
        if len(given) != 2 or len(compared) != 2:
            raise ValueError("Both given and compared must be lists of length 2.")
        return not (given[1] < compared[0] or compared[1] < given[0])

    def _check_range_overlap(self, request: ip_configs.IPv6SubnetConfig, networks: List[str]) -> bool:
        """
        Checks whether the given IPv6 subnet overlaps with any network in the list.

        Parameters:
        request (ip_configs.IPv6SubnetConfig): The IPv6 subnet to check.
        networks (List[str]): A list of networks in CIDR notation (e.g., "2001:db8::/32").

        Returns:
        bool: True if the IPv6 subnet overlaps with any of the predefined networks, False otherwise.
        """
        result = []
        for network in networks:
            addr = network[:network.find('/')]
            mask = network[network.find('/') + 1:]
            network_subnet = ip_configs.IPv6SubnetConfig(IPv6Addr(addr), IPv6NetMask(f"/{mask}"))
            network_range = [given_ipv6_addr.as_decimal for given_ipv6_addr in network_subnet.subnet_range]
            if self._has_overlap(network_range, [compare_ipv6_addr.as_decimal for compare_ipv6_addr in request.subnet_range]):
                result.append(True)
            else:
                result.append(False)
        return any(result)

class IPv6SubnetClassifierUnspecifiedHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'UNSPECIFIED' address block.
    If it does, it classifies the subnet as 'UNSPECIFIED' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.UNSPECIFIED.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.UNSPECIFIED)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierLoopbackHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'LOOPBACK' address block.
    If it does, it classifies the subnet as 'LOOPBACK' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.LOOPBACK.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.LOOPBACK)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierDocumentationHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'DOCUMENTATION' address block.
    If it does, it classifies the subnet as 'DOCUMENTATION' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.DOCUMENTATION.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.DOCUMENTATION)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierLinkLocalHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'LINK_LOCAL' address block.
    If it does, it classifies the subnet as 'LINK_LOCAL' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.LINK_LOCAL.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.LINK_LOCAL)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierMulticastHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'MULTICAST' address block.
    If it does, it classifies the subnet as 'MULTICAST' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.MULTICAST.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.MULTICAST)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierUniqueLocalHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'UNIQUE_LOCAL' address block.
    If it does, it classifies the subnet as 'UNIQUE_LOCAL' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.UNIQUE_LOCAL.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.UNIQUE_LOCAL)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierIPv4MappedHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'IPV4_MAPPED' address block.
    If it does, it classifies the subnet as 'IPV4_MAPPED' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_MAPPED.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.IPV4_MAPPED)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierIPv4TranslatedHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'IPV4_TRANSLATED' address block.
    If it does, it classifies the subnet as 'IPV4_TRANSLATED' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_TRANSLATED.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.IPV4_TRANSLATED)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierIPv4To6TranslationHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'IPV4_IPV6_TRANSLATION' address block.
    If it does, it classifies the subnet as 'IPV4_IPV6_TRANSLATION' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_IPV6_TRANSLATION.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.IPV4_IPV6_TRANSLATION)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierDiscardPrefixHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'DISCARD_PREFIX' address block.
    If it does, it classifies the subnet as 'DISCARD_PREFIX' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.DISCARD_PREFIX.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.DISCARD_PREFIX)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierSRV6Handler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'SRV6' address block.
    If it does, it classifies the subnet as 'SRV6' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.SRV6.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.SRV6)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifier6To4SchemeHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'IP6_TO4' address block.
    If it does, it classifies the subnet as 'IP6_TO4' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IP6_TO4.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.IP6_TO4)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierTeredoTunnelingHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'TEREDO_TUNNELING' address block.
    If it does, it classifies the subnet as 'TEREDO_TUNNELING' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.TEREDO_TUNNELING.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.TEREDO_TUNNELING)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierORCHIDV2Handler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'ORCHIDV2' address block.
    If it does, it classifies the subnet as 'ORCHIDV2' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.ORCHIDV2.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.ORCHIDV2)
        return super().handle(request, validated=validated)


class IPv6SubnetClassifierGlobalUnicastHandler(IPv6SubnetClassifierHandler):
    """
    Checks if the subnet overlaps with the 'GLOBAL_UNICAST' address block.
    If it does, it classifies the subnet as 'GLOBAL_UNICAST' and adds it to the list of items.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.GLOBAL_UNICAST.value
        if self._check_range_overlap(request, networks):
            self._items.append(IPv6AddrType.GLOBAL_UNICAST)
        return super().handle(request, validated=validated)

class IPSubnetTypeClassifier:
    """
    A utility class to classify IPv4 and IPv6 subnets into their respective types.
    This class uses a chain of responsibility to process subnet classifications.

    Methods:
        - classify_ipv4_subnet_types: Classifies IPv4 subnets using a predefined chain of handlers.
        - classify_ipv6_subnet_types: Classifies IPv6 subnets using a predefined chain of handlers.
    """
    @staticmethod
    def classify_ipv4_subnet_types(request_format: ip_configs.IPv4SubnetConfig, classifiers: List[IPSubnetTypeClassifier] = None) -> List[IPv4AddrType]:
        """
        Classifies an IPv4 subnet into its applicable types using a chain of IPv4 handlers.

        Parameters:
        request_format (ip_configs.IPv4SubnetConfig): The IPv4 subnet configuration to classify.
        classifiers (List[IPSubnetTypeClassifier], optional): A custom list of IPv4 classifiers.
            If not provided, a default list of IPv4 subnet handlers is used.

        Returns:
        List[IPv4AddrType]: A list of all matching IPv4 address types for the given subnet.
        """
        if classifiers is None:
            classifiers = [
                IPv4SubnetTypeUnspecifiedHandler(),
                IPv4SubnetTypeLimitedBroadcastHandler(),
                IPv4SubnetTypeCurrentNetworkHandler(),
                IPv4SubnetClassifierPrivateHandler(),
                IPv4SubnetClassifierPublicHandler(),
                IPv4SubnetClassifierDocumentationHandler(),
                IPv4SubnetClassifierMulticastHandler(),
                IPv4SubnetClassifierLinkLocalHandler(),
                IPv4SubnetClassifierLoopbackHandler(),
                IPv4SubnetClassifierDSLiteHandler(),
                IPv4SubnetClassifierCarrierNATHandler(),
                IPv4SubnetClassifierBenchmarkTestingHandler(),
                IPv4SubnetClassifierIP6To4RelayHandler(),
                IPv4SubnetClassifierReservedHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        classifiers[0].handle(request_format)
        return classifiers[0].get_items()

    @staticmethod
    def classify_ipv6_subnet_types(request_format: ip_configs.IPv6SubnetConfig, classifiers: List[IPSubnetTypeClassifier] = None) -> List[IPv6AddrType]:
        """
        Classifies an IPv6 subnet into its applicable types using a chain of IPv6 handlers.

        Parameters:
        request_format (ip_configs.IPv6SubnetConfig): The IPv6 subnet configuration to classify.
        classifiers (List[IPSubnetTypeClassifier], optional): A custom list of IPv6 classifiers.
            If not provided, a default list of IPv6 subnet handlers is used.

        Returns:
        List[IPv6AddrType]: A list of all matching IPv6 address types for the given subnet.
        """
        if classifiers is None:
            classifiers = [
                IPv6SubnetClassifierUnspecifiedHandler(),
                IPv6SubnetClassifierLoopbackHandler(),
                IPv6SubnetClassifierIPv4MappedHandler(),
                IPv6SubnetClassifierIPv4TranslatedHandler(),
                IPv6SubnetClassifierIPv4To6TranslationHandler(),
                IPv6SubnetClassifierDiscardPrefixHandler(),
                IPv6SubnetClassifierTeredoTunnelingHandler(),
                IPv6SubnetClassifierDocumentationHandler(),
                IPv6SubnetClassifierORCHIDV2Handler(),
                IPv6SubnetClassifier6To4SchemeHandler(),
                IPv6SubnetClassifierSRV6Handler(),
                IPv6SubnetClassifierLinkLocalHandler(),
                IPv6SubnetClassifierMulticastHandler(),
                IPv6SubnetClassifierUniqueLocalHandler(),
                IPv6SubnetClassifierGlobalUnicastHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        classifiers[0].handle(request_format)
        return classifiers[0].get_items()
