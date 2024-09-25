from __future__ import annotations
import re
from abc import abstractmethod
from typing import Tuple, List, Union

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv4WildCard, IPv6Addr, IPv6NetMask, IPv6WildCard, IPAddr, IPNetMask


class IPStandardizerHandler(SimpleCoRHandler):
    """
    An abstract base handler class in a Chain of Responsibility (CoR) pattern used to standardize different
    formats of IP addresses. If a handler can't process the standardization, it forwards it to the next
    handler in the chain.
    """
    @abstractmethod
    def handle(self, *args) -> Union[Tuple[IPAddr, IPNetMask], IPStandardizerHandler]:
        """
        Processes the standardization request. If the current handler can't process the request, it forwards it
        to the next handler in the chain. If there is no next handler, it returns None.

        Parameters:
        *args: The arguments passed to the handler, typically including an IP address in various formats.

        Returns:
        Any: The standardized IP address or None if no handler processes the request.
        """
        if self._next_handler:
            return self._next_handler.handle(*args)
        return self._next_handler

    @abstractmethod
    def _standardize(self, *args) -> Tuple[IPAddr, IPNetMask]:
        """
        Abstract method that each subclass must implement to define how it standardizes the IP address.

        Parameters:
        *args: The arguments passed to the standardizer.

        Returns:
        Any: The standardized IP address.
        """
        pass


class CIDRInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv4 addresses provided in CIDR format (e.g., '192.168.1.1/24').
    If the format doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
        """
        Checks if the argument matches the CIDR IPv4 address format (e.g., '192.168.1.1/24'). If it does,
        the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be an IPv4 address in CIDR format.

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and network mask.
        """
        if len(args) == 1 and isinstance(args[0], str) and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', args[0]):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4NetMask]:
        """
        Splits the CIDR string into an IP address and a netmask, and returns them in standardized formats.

        Parameters:
        *args: The CIDR string (e.g., '192.168.1.1/24').

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and netmask.
        """
        ip_addr, netmask = args[0].strip().split('/')
        return IPv4Addr(ip_addr), IPv4NetMask('/' + netmask)


class DotInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv4 addresses provided in dotted-decimal format with a space-separated netmask
    (e.g., '192.168.1.1 255.255.255.0'). If the format doesn't match, it passes the request to the next handler
    in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
        """
        Checks if the input matches the dotted-decimal IPv4 address format (e.g., '192.168.1.1 255.255.255.0').
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be a string in the dotted-decimal format
        with a space-separated netmask.

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and network mask.
        """
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4NetMask]:
        """
        Converts a string containing an IPv4 address and a space-separated netmask into a standardized tuple.

        Parameters:
        *args: The dotted-decimal IPv4 address and netmask string.

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and netmask.
        """
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv4Addr(ip_addr), IPv4NetMask(netmask)


class IPAddrInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv4 addresses provided as objects of types IPv4Addr and IPv4NetMask.
    If the input doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
        """
        Checks if the input consists of an IPv4 address and a network mask as objects (IPv4Addr, IPv4NetMask).
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be an IPv4Addr object and an IPv4NetMask object.

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and network mask.
        """
        if len(args) == 2 and type(args[0]) is IPv4Addr and type(args[1]) is IPv4NetMask:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4NetMask]:
        """
        Standardizes and returns the provided IPv4 address and netmask.

        Parameters:
        *args: The IPv4 address and netmask as objects (IPv4Addr, IPv4NetMask).

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and netmask.
        """
        return args[0], args[1]


class DotWildcardIPv4StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv4 addresses provided in dotted-decimal format with a space-separated wildcard
    (e.g., '192.168.1.1 0.0.1.255'). If the format doesn't match, it passes the request to the next handler
    in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4WildCard], IPStandardizerHandler]:
        """
        Checks if the input matches the dotted-decimal IPv4 address format with a space-separated wildcard
        (e.g., '192.168.1.1 0.0.1.255'). If it does, the standardization process begins. Otherwise,
        the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be a string in the dotted-decimal format
        with a space-separated wildcard.

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]: The standardized IPv4 address and wildcard mask.
        """
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4WildCard]:
        """
        Converts a string containing an IPv4 address and a space-separated wildcard into a standardized tuple.

        Parameters:
        *args: The dotted-decimal IPv4 address and wildcard string.

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]: The standardized IPv4 address and wildcard.
        """
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv4Addr(ip_addr), IPv4WildCard(netmask)


class IPAddrWildcardIPv4StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv4 addresses provided as objects of types IPv4Addr and IPv4WildCard.
    If the input doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4WildCard], IPStandardizerHandler]:
        """
        Checks if the input consists of an IPv4 address and a wildcard mask as objects (IPv4Addr, IPv4WildCard).
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be an IPv4Addr object and an IPv4WildCard object.

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]: The standardized IPv4 address and wildcard.
        """
        if len(args) == 2 and type(args[0]) is IPv4Addr and type(args[1]) is IPv4WildCard:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4WildCard]:
        """
        Standardizes and returns the provided IPv4 address and wildcard.

        Parameters:
        *args: The IPv4 address and wildcard as objects (IPv4Addr, IPv4WildCard).

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]: The standardized IPv4 address and wildcard.
        """
        return args[0], args[1]


class CIDRInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv6 addresses provided in CIDR format (e.g., 'fe00::1/64').
    If the format doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        """
        Checks if the input matches the CIDR IPv6 address format (e.g., 'fe00::1/64').
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be a string in the CIDR IPv6 format.

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and network mask.
        """
        if len(args) == 1 and isinstance(args[0], str) and re.match(r'^[a-fA-F0-9:\.]+/\d{1,3}$', args[0]):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        """
        Splits the CIDR string into an IPv6 address and a netmask, and returns them in standardized formats.

        Parameters:
        *args: The CIDR string (e.g., 'fe00::1/64').

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and netmask.
        """
        ip_addr, netmask = args[0].strip().split('/')
        return IPv6Addr(ip_addr), IPv6NetMask('/' + netmask)


class ColonInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv6 addresses provided in colon-hexadecimal format with a space-separated netmask
    (e.g., 'fe00::1 ff00::'). If the format doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        """
        Checks if the input matches the colon-hexadecimal IPv6 address format with a space-separated netmask
        (e.g., 'fe00::1 ff00::'). If it does, the standardization process begins. Otherwise, the request is passed
        to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be a string in the colon-hexadecimal format
        with a space-separated netmask.

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and network mask.
        """
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^[a-fA-F0-9:\.]+\s+[a-fA-F0-9:\.]+$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        """
        Converts a string containing an IPv6 address and a space-separated netmask into a standardized tuple.

        Parameters:
        *args: The colon-hexadecimal IPv6 address and netmask string.

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and netmask.
        """
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv6Addr(ip_addr), IPv6NetMask(netmask)


class IPAddrInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv6 addresses provided as objects of types IPv6Addr and IPv6NetMask.
    If the input doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        """
        Checks if the input consists of an IPv6 address and a network mask as objects (IPv6Addr, IPv6NetMask).
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be an IPv6Addr object and an IPv6NetMask object.

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and network mask.
        """
        if len(args) == 2 and type(args[0]) is IPv6Addr and type(args[1]) is IPv6NetMask:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        """
        Standardizes and returns the provided IPv6 address and netmask.

        Parameters:
        *args: The IPv6 address and netmask as objects (IPv6Addr, IPv6NetMask).

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and netmask.
        """
        return args[0], args[1]


class ColonWildcardIPv6StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv6 addresses provided in colon-hexadecimal format with a space-separated wildcard
    (e.g., 'fe00::1 ff00::'). If the format doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6WildCard], IPStandardizerHandler]:
        """
        Checks if the input matches the colon-hexadecimal IPv6 address format with a space-separated wildcard
        (e.g., 'fe00::1 ff00::'). If it does, the standardization process begins. Otherwise, the request
        is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be a string in the colon-hexadecimal format
        with a space-separated wildcard.

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]: The standardized IPv6 address and wildcard mask.
        """
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^[a-fA-F0-9:\.]+\s+[a-fA-F0-9:\.]+$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6WildCard]:
        """
        Converts a string containing an IPv6 address and a space-separated wildcard into a standardized tuple.

        Parameters:
        *args: The colon-hexadecimal IPv6 address and wildcard string.

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]: The standardized IPv6 address and wildcard.
        """
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv6Addr(ip_addr), IPv6WildCard(netmask)


class IPAddrWildcardIPv6StandardizerHandler(IPStandardizerHandler):
    """
    This handler standardizes IPv6 addresses provided as objects of types IPv6Addr and IPv6WildCard.
    If the input doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6WildCard], IPStandardizerHandler]:
        """
        Checks if the input consists of an IPv6 address and a wildcard mask as objects (IPv6Addr, IPv6WildCard).
        If it does, the standardization process begins. Otherwise, the request is passed to the next handler.

        Parameters:
        *args: The arguments passed to the handler, expected to be an IPv6Addr object and an IPv6WildCard object.

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]: The standardized IPv6 address and wildcard mask.
        """
        if len(args) == 2 and type(args[0]) is IPv6Addr and type(args[1]) is IPv6WildCard:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6WildCard]:
        """
        Standardizes and returns the provided IPv6 address and wildcard mask.

        Parameters:
        *args: The IPv6 address and wildcard mask as objects (IPv6Addr, IPv6WildCard).

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]: The standardized IPv6 address and wildcard mask.
        """
        return args[0], args[1]


class IPStandardizer:
    """
    A utility class that provides static methods to standardize both IPv4 and IPv6 addresses using
    a chain of handlers.
    """
    @staticmethod
    def ipv4_interface(*args, standardizer: List[IPStandardizer] = None) -> Tuple[IPv4Addr, IPv4NetMask]:
        """
        Standardizes an IPv4 interface (IP address and netmask) using the appropriate handlers.

        Parameters:
        *args: The arguments passed to the standardizer.
        standardizer (List[IPStandardizerHandler]): Optional. A list of handlers for standardizing the IPv4 address.

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]: The standardized IPv4 address and netmask.
        """
        if standardizer is None:
            standardizer = [
                CIDRInterfaceIPv4StandardizerHandler(),
                DotInterfaceIPv4StandardizerHandler(),
                IPAddrInterfaceIPv4StandardizerHandler(),
            ]
        standardizer_handler = standardizer[0]
        for next_handler in standardizer[1:]:
            standardizer_handler.set_next(next_handler)
            standardizer_handler = next_handler
        return standardizer[0].handle(*args)

    @staticmethod
    def ipv4_wildcard(*args, standardizer: List[IPStandardizer] = None) -> Tuple[IPv4Addr, IPv4WildCard]:
        """
        Standardizes an IPv4 address and wildcard mask using the appropriate handlers.

        Parameters:
        *args: The arguments passed to the standardizer.
        standardizer (List[IPStandardizerHandler]): Optional. A list of handlers for standardizing the IPv4 address
        and wildcard mask.

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]: The standardized IPv4 address and wildcard.
        """
        if standardizer is None:
            standardizer = [
                DotWildcardIPv4StandardizerHandler(),
                IPAddrWildcardIPv4StandardizerHandler()
            ]
        standardizer_handler = standardizer[0]
        for next_handler in standardizer[1:]:
            standardizer_handler.set_next(next_handler)
            standardizer_handler = next_handler
        return standardizer[0].handle(*args)

    @staticmethod
    def ipv6_interface(*args, standardizer: List[IPStandardizer] = None) -> Tuple[IPv6Addr, IPv6NetMask]:
        """
        Standardizes an IPv6 interface (IP address and netmask) using the appropriate handlers.

        Parameters:
        *args: The arguments passed to the standardizer.
        standardizer (List[IPStandardizerHandler]): Optional. A list of handlers for standardizing the IPv6 address.

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]: The standardized IPv6 address and netmask.
        """
        if standardizer is None:
            standardizer = [
                CIDRInterfaceIPv6StandardizerHandler(),
                ColonInterfaceIPv6StandardizerHandler(),
                IPAddrInterfaceIPv6StandardizerHandler(),
            ]
        standardizer_handler = standardizer[0]
        for next_handler in standardizer[1:]:
            standardizer_handler.set_next(next_handler)
            standardizer_handler = next_handler
        return standardizer[0].handle(*args)

    @staticmethod
    def ipv6_wildcard(*args, standardizer: List[IPStandardizer] = None) -> Tuple[IPv6Addr, IPv6WildCard]:
        """
        Standardizes an IPv6 address and wildcard mask using the appropriate handlers.

        Parameters:
        *args: The arguments passed to the standardizer.
        standardizer (List[IPStandardizerHandler]): Optional. A list of handlers for standardizing the IPv6 address
        and wildcard mask.

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]: The standardized IPv6 address and wildcard mask.
        """
        if standardizer is None:
            standardizer = [
                ColonWildcardIPv6StandardizerHandler(),
                IPAddrWildcardIPv6StandardizerHandler()
            ]
        standardizer_handler = standardizer[0]
        for next_handler in standardizer[1:]:
            standardizer_handler.set_next(next_handler)
            standardizer_handler = next_handler
        return standardizer[0].handle(*args)
