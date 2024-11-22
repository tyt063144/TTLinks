from __future__ import annotations

from abc import abstractmethod
from typing import Any, List

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.network import BinaryTools
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv6Addr, IPv6NetMask
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType, IPv4TypeAddrBlocks, IPv6TypeAddrBlocks


class IPv4AddrClassifierHandler(SimpleCoRHandler):
    """
    A handler for classifying IPv4 addresses using the Chain of Responsibility (CoR) pattern.
    This class processes requests and delegates them to the next handler if applicable.

    Methods:
        - _validate: Validates if the request is an IPv4Addr object.
        - handle: Processes the request or passes it to the next handler.
        - _is_within_range: Determines if the IPv4 address falls within a specified range of networks.
    """
    @staticmethod
    def _validate(request: Any, *args, **kwargs):
        """
        Validates that the provided request is of type IPv4Addr.

        Parameters:
        request (Any): The input request to be validated.

        Raises:
        ValueError: If the request is not an instance of IPv4Addr.
        """
        if kwargs.get('validated') is True:
            return True
        if not isinstance(request, IPv4Addr) and kwargs.get('validated') is False:
            raise ValueError(f"Expected IPv4Addr object, got {type(request)}")
        return True

    @staticmethod
    def _is_within_range(request: Any, networks: List[str]) -> bool:
        """
        Checks whether the given IPv4 address is within any of the specified network ranges.

        Parameters:
        request (Any): The IPv4 address to be checked.
        networks (List[str]): A list of network strings in CIDR notation (e.g., "192.168.0.0/16").

        Returns:
        bool: True if the IPv4 address is within the range of any provided network, otherwise False.
        """
        comparison_network_groups = []
        for network in networks:
            comparison_network_groups.append([
                IPv4Addr(network[:network.find('/')]).as_bytes,
                IPv4NetMask(network[network.find('/'):]).as_bytes,
                request.as_bytes
            ])
        return any(BinaryTools.is_bytes_in_range(*network) for network in comparison_network_groups)

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Handles the request by processing it or delegating it to the next handler in the chain.

        Parameters:
        request (Any): The input request to be processed.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        Any: The result of the request processing. If no handler processes the request, returns
        IPv4AddrType.UNDEFINED_TYPE.
        """
        if self._next_handler:
            return self._next_handler.handle(request, *args, **kwargs)
        return self._next_handler if self._next_handler is not None else IPv4AddrType.UNDEFINED_TYPE


class IPv4AddrTypeUnspecifiedHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses that are unspecified (all bits in the address are `0`).
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        if type(request) is IPv4Addr and all(bit == 0 for bit in list(request.binary_digits)):
            return IPv4AddrType.UNSPECIFIED
        else:
            return super().handle(request, validated=validated)


class IPv4AddrTypeLimitedBroadcastHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses used for limited broadcast (all bits in the address are `1`).
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        if type(request) is IPv4Addr and all(bit == 1 for bit in list(request.binary_digits)):
            return IPv4AddrType.LIMITED_BROADCAST
        else:
            return super().handle(request, validated=validated)


class IPv4AddrTypeCurrentNetworkHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses belonging to the "current network" range defined in CURRENT_NETWORK.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.CURRENT_NETWORK.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.CURRENT_NETWORK
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierPrivateHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as private addresses within the PRIVATE network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.PRIVATE.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.PRIVATE
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierPublicHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as public addresses within the PUBLIC network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.PUBLIC.value
        if type(request) is IPv4Addr and not self._is_within_range(request, networks):
            return IPv4AddrType.PUBLIC
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierMulticastHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as multicast addresses within the MULTICAST network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.MULTICAST.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.MULTICAST
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierLinkLocalHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as link-local addresses within the LINK_LOCAL network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.LINK_LOCAL.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.LINK_LOCAL
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierLoopbackHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as loopback addresses within the LOOPBACK network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.LOOPBACK.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.LOOPBACK
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierDocumentationHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as documentation addresses within the DOCUMENTATION network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.DOCUMENTATION.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.DOCUMENTATION
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierDSLiteHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as DS-Lite addresses within the DS_LITE network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.DS_LITE.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.DS_LITE
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierCarrierNATHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as Carrier-Grade NAT addresses within the CARRIER_GRADE_NAT network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.CARRIER_GRADE_NAT.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.CARRIER_GRADE_NAT
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierBenchmarkTestingHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as benchmark testing addresses within the BENCHMARK_TESTING network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.BENCHMARK_TESTING.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.BENCHMARK_TESTING
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierIP6To4RelayHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as IPv6-to-IPv4 relay addresses within the IPV6_TO_IPV4_RELAY network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.IPV6_TO_IPV4_RELAY.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.IPV6_TO_IPV4_RELAY
        else:
            return super().handle(request, validated=validated)


class IPv4AddrClassifierReservedHandler(IPv4AddrClassifierHandler):
    """
    Handles IPv4 addresses classified as reserved addresses within the RESERVED network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv4TypeAddrBlocks.RESERVED.value
        if type(request) is IPv4Addr and self._is_within_range(request, networks):
            return IPv4AddrType.RESERVED
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierHandler(SimpleCoRHandler):
    """
    A base handler for classifying IPv6 addresses using the Chain of Responsibility (CoR) pattern.
    This class defines the common behavior for all IPv6 address classification handlers.

    Methods:
        - _validate: Ensures the request is a valid IPv6Addr object.
        - handle: Processes the request or delegates it to the next handler in the chain.
        - _is_within_range: Checks if an IPv6 address falls within a specified range of network blocks.
    """
    @staticmethod
    def _validate(request: Any, *args, **kwargs):
        """
        Validates that the provided request is an instance of IPv6Addr.

        Parameters:
        request (Any): The input request to validate.

        Raises:
        ValueError: If the request is not of type IPv6Addr.
        """
        if kwargs.get('validated') is True:
            return True
        if not isinstance(request, IPv6Addr):
            raise ValueError(f"Expected IPv6Addr object, got {type(request)}")
        return True

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """
        Processes the given request or passes it to the next handler in the chain if unhandled.

        Parameters:
        request (Any): The IPv6 address to classify.
        *args: Additional positional arguments for the handler.
        **kwargs: Additional keyword arguments for the handler.

        Returns:
        Any: The classification result for the IPv6 address. If no handler processes the request,
        it returns IPv6AddrType.UNDEFINED_TYPE or the result from the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler if self._next_handler is not None else IPv6AddrType.UNDEFINED_TYPE

    @staticmethod
    def _is_within_range(request: Any, networks: List[str]) -> bool:
        """
        Checks whether the given IPv6 address falls within any of the specified network blocks.

        Parameters:
        request (Any): The IPv6 address to check.
        networks (List[str]): A list of network strings in CIDR notation (e.g., "2001:db8::/32").

        Returns:
        bool: True if the IPv6 address is within any of the specified network ranges, False otherwise.
        """
        comparison_network_groups = []
        for network in networks:
            comparison_network_groups.append([
                IPv6Addr(network[:network.find('/')]).as_bytes,
                IPv6NetMask(network[network.find('/'):]).as_bytes,
                request.as_bytes
            ])
        return any(BinaryTools.is_bytes_in_range(*network) for network in comparison_network_groups)


class IPv6AddrClassifierUnspecifiedHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses that are unspecified (all bits in the address are `0`).
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.UNSPECIFIED.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.UNSPECIFIED
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierLoopbackHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as loopback addresses within the LOOPBACK network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.LOOPBACK.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.LOOPBACK
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierDocumentationHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as documentation addresses within the DOCUMENTATION network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.DOCUMENTATION.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.DOCUMENTATION
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierLinkLocalHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as link-local addresses within the LINK_LOCAL network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.LINK_LOCAL.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.LINK_LOCAL
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierMulticastHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as multicast addresses within the MULTICAST network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.MULTICAST.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.MULTICAST
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierUniqueLocalHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as unique local addresses within the UNIQUE_LOCAL network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.UNIQUE_LOCAL.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.UNIQUE_LOCAL
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierIPv4MappedHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as IPv4-mapped addresses within the IPV4_MAPPED network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_MAPPED.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.IPV4_MAPPED
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierIPv4TranslatedHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as IPv4-translated addresses within the IPV4_TRANSLATED network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_TRANSLATED.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.IPV4_TRANSLATED
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierIPv4To6TranslationHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as IPv4-to-IPv6 translation addresses within the IPV4_IPV6_TRANSLATION network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IPV4_IPV6_TRANSLATION.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.IPV4_IPV6_TRANSLATION
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierDiscardPrefixHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as discard prefix addresses within the DISCARD_PREFIX network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.DISCARD_PREFIX.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.DISCARD_PREFIX
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierSRV6Handler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as SRv6 addresses within the SRV6 network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.SRV6.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.SRV6
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifier6To4SchemeHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as 6to4 scheme addresses within the 6TO4_SCHEME network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.IP6_TO4.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.IP6_TO4
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierTeredoTunnelingHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as Teredo tunneling addresses within the TEREDO_TUNNELING network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.TEREDO_TUNNELING.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.TEREDO_TUNNELING
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierORCHIDV2Handler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as ORCHIDv2 addresses within the ORCHIDV2 network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.ORCHIDV2.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.ORCHIDV2
        else:
            return super().handle(request, validated=validated)


class IPv6AddrClassifierGlobalUnicastHandler(IPv6AddrClassifierHandler):
    """
    Handles IPv6 addresses classified as global unicast addresses within the GLOBAL_UNICAST network range.
    """
    def handle(self, request: Any, *args, **kwargs) -> Any:
        validated = self._validate(request, *args, **kwargs)
        networks = IPv6TypeAddrBlocks.GLOBAL_UNICAST.value
        if type(request) is IPv6Addr and self._is_within_range(request, networks):
            return IPv6AddrType.GLOBAL_UNICAST
        else:
            return super().handle(request, validated=validated)


class IPAddrTypeClassifier:
    """
    A utility class to classify IPv4 and IPv6 addresses into their respective types.
    This class builds a chain of responsibility using handlers to process address classifications.

    Methods:
        - classify_ipv4_host_type: Classifies an IPv4 address based on a predefined chain of handlers.
        - classify_ipv6_host_type: Classifies an IPv6 address based on a predefined chain of handlers.
    """
    @staticmethod
    def classify_ipv4_host_type(request_format: Any, classifiers: List[IPAddrTypeClassifier] = None) -> IPv4AddrType:
        """
        Classifies an IPv4 address into its appropriate type using a chain of IPv4 handlers.

        Parameters:
        request_format (Any): The input IPv4 address to classify.
        classifiers (List[IPAddrTypeClassifier], optional): A custom list of IPv4 classifiers.
            If not provided, a default list of IPv4 handlers is used.

        Returns:
        IPv4AddrType: The classification type of the IPv4 address.
        """
        if classifiers is None:
            classifiers = [
                IPv4AddrTypeUnspecifiedHandler(),
                IPv4AddrTypeLimitedBroadcastHandler(),
                IPv4AddrTypeCurrentNetworkHandler(),
                IPv4AddrClassifierPrivateHandler(),
                IPv4AddrClassifierPublicHandler(),
                IPv4AddrClassifierDocumentationHandler(),
                IPv4AddrClassifierMulticastHandler(),
                IPv4AddrClassifierLinkLocalHandler(),
                IPv4AddrClassifierLoopbackHandler(),
                IPv4AddrClassifierDSLiteHandler(),
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
    def classify_ipv6_host_type(request_format: Any, classifiers: List[IPAddrTypeClassifier] = None) -> IPv6AddrType:
        """
        Classifies an IPv6 address into its appropriate type using a chain of IPv6 handlers.

        Parameters:
        request_format (Any): The input IPv6 address to classify.
        classifiers (List[IPAddrTypeClassifier], optional): A custom list of IPv6 classifiers.
            If not provided, a default list of IPv6 handlers is used.

        Returns:
        IPv6AddrType: The classification type of the IPv6 address.
        """
        if classifiers is None:
            classifiers = [
                IPv6AddrClassifierUnspecifiedHandler(),
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
