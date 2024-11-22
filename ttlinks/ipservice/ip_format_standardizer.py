from __future__ import annotations

import re
from abc import abstractmethod
from typing import Tuple, List, Union

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv4WildCard, IPv6Addr, IPv6NetMask, IPv6WildCard, IPAddr, IPMask


class IPStandardizerHandler(SimpleCoRHandler):
    """
    Abstract base class for IP standardization handlers using the Chain of Responsibility (CoR) pattern.
    This handler standardizes IP addresses and their associated masks into a unified format.

    Methods:
        - handle: Processes a standardization request or delegates it to the next handler in the chain.
        - _standardize: Abstract method for implementing IP and mask standardization logic.
    """
    @abstractmethod
    def handle(self, *args) -> Union[Tuple[IPAddr, IPMask], IPStandardizerHandler]:
        """
        Processes a standardization request. If the current handler cannot process the request,
        it delegates to the next handler in the chain.

        Parameters:
        *args: Positional arguments containing the data to be standardized.

        Returns:
        Union[Tuple[IPAddr, IPMask], IPStandardizerHandler]:
            - A tuple containing a standardized IP address and mask if successful.
            - The next handler in the chain if the request cannot be processed.
        """
        if self._next_handler:
            return self._next_handler.handle(*args)
        return self._next_handler

    @abstractmethod
    def _standardize(self, *args) -> Tuple[IPAddr, IPMask]:
        """
        Abstract method to be implemented by subclasses for standardizing an IP address and mask.

        Parameters:
        *args: Positional arguments containing the IP address and mask to standardize.

        Returns:
        Tuple[IPAddr, IPMask]: A tuple containing the standardized IP address and mask.

        Raises:
        NotImplementedError: If the method is not implemented by the subclass.
        """
        pass


class CIDRInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv4 addresses provided in CIDR notation.

    Example:
    Input: "192.168.1.1/24"
    Output: (IPv4Addr('_address=192.168.1.1'), IPv4NetMask('_address=255.255.255.0'))
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
        if len(args) == 1 and isinstance(args[0], str) and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', args[0]):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4NetMask]:
        ip_addr, netmask = args[0].strip().split('/')
        return IPv4Addr(ip_addr), IPv4NetMask('/' + netmask)


class DotInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv4 addresses provided in dot notation.

    Example:
    Input: "192.168.1.1 255.255.255.0"
    Output: (IPv4Addr('_address=192.168.1.1'), IPv4NetMask('_address=255.255.255.0'))
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
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
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv4Addr(ip_addr), IPv4NetMask(netmask)


class IPAddrInterfaceIPv4StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv4 addresses provided as separate objects for the address and netmask.

    Example:
    Input: IPv4Addr('192.168.1.1'), IPv4NetMask('255.255.255.0')
    Output: (IPv4Addr('_address=192.168.1.1'), IPv4NetMask('_address=255.255.255.0'))
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4NetMask], IPStandardizerHandler]:
        if len(args) == 2 and type(args[0]) is IPv4Addr and type(args[1]) is IPv4NetMask:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4NetMask]:
        return args[0], args[1]


class DotWildcardIPv4StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv4 addresses provided in dot notation with wildcard masks.

    Example:
    Input: "192.168.1.1 0.0.0.255"
    Output: (IPv4Addr('_address=192.168.1.1'), IPv4WildCard('_address=0.0.0.255'))
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4WildCard], IPStandardizerHandler]:
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
        ip_addr, wildcard = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv4Addr(ip_addr), IPv4WildCard(wildcard)


class IPAddrWildcardIPv4StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv4 addresses provided as separate objects for the address and wildcard mask.

    Example:
    Input: IPv4Addr('192.168.1.1'), IPv4WildCard('0.0.0.255')
    Output: (IPv4Addr('_address=192.168.1.1'), IPv4WildCard('_address=0.0.0.255'))
    """
    def handle(self, *args) -> Union[Tuple[IPv4Addr, IPv4WildCard], IPStandardizerHandler]:
        if len(args) == 2 and type(args[0]) is IPv4Addr and type(args[1]) is IPv4WildCard:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv4Addr, IPv4WildCard]:
        return args[0], args[1]


class CIDRInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv6 addresses provided in CIDR notation.

    Example:
    Input: "2001:db8::1/64"
    Output: (IPv6Addr('_address=2001:DB8::1'), IPv6NetMask('_address=FFFF:FFFF:FFFF:FFFF::'))
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        if len(args) == 1 and isinstance(args[0], str) and re.match(r'^[a-fA-F0-9:.]+/\d{1,3}$', args[0]):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        ip_addr, netmask = args[0].strip().split('/')
        return IPv6Addr(ip_addr), IPv6NetMask('/' + netmask)


class ColonInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv6 addresses provided in colon notation.

    Example:
    Input: "2001:db8::1 FFFF:FFFF:FFFF:FFFF::"
    Output: (IPv6Addr('_address=2001:DB8::1'), IPv6NetMask('_address=FFFF:FFFF:FFFF:FFFF::'))
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^[a-fA-F0-9:.]+\s+[a-fA-F0-9:.]+$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        ip_addr, netmask = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv6Addr(ip_addr), IPv6NetMask(netmask)


class IPAddrInterfaceIPv6StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv6 addresses provided as separate objects for the address and netmask.

    Example:
    Input: IPv6Addr('2001:db8::1'), IPv6NetMask('FFFF:FFFF:FFFF:FFFF::')
    Output: (IPv6Addr('_address=2001:DB8::1'), IPv6NetMask('_address=FFFF:FFFF:FFFF:FFFF::'))
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6NetMask], IPStandardizerHandler]:
        if len(args) == 2 and type(args[0]) is IPv6Addr and type(args[1]) is IPv6NetMask:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6NetMask]:
        return args[0], args[1]


class ColonWildcardIPv6StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv6 addresses provided in colon notation with wildcard masks.

    Example:
    Input: "2001:db8::1234:1 ::FF:FFFF"
    Output: (IPv6Addr('_address=2001:DB8::1234:1'), IPv6WildCard('_address=::FF:FFFF'))
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6WildCard], IPStandardizerHandler]:
        if (
                len(args) == 1
                and isinstance(args[0], str)
                and re.match(r'^[a-fA-F0-9:.]+\s+[a-fA-F0-9:.]+$', args[0])
        ):
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6WildCard]:
        ip_addr, wildcard = re.sub(r'\s+', '/', args[0].strip()).split('/')
        return IPv6Addr(ip_addr), IPv6WildCard(wildcard)


class IPAddrWildcardIPv6StandardizerHandler(IPStandardizerHandler):
    """
    Handles the standardization of IPv6 addresses provided as separate objects for the address and wildcard mask.

    Example:
    Input: IPv6Addr('2001:db8::1234:1'), IPv6WildCard('::FF:FFFF')
    Output: (IPv6Addr('_address=2001:DB8::1234:1'), IPv6WildCard('_address=::FF:FFFF'))
    """
    def handle(self, *args) -> Union[Tuple[IPv6Addr, IPv6WildCard], IPStandardizerHandler]:
        if len(args) == 2 and type(args[0]) is IPv6Addr and type(args[1]) is IPv6WildCard:
            try:
                return self._standardize(*args)
            except (ValueError, TypeError):
                return super().handle(*args)
        else:
            return super().handle(*args)

    def _standardize(self, *args) -> Tuple[IPv6Addr, IPv6WildCard]:
        return args[0], args[1]


class IPStandardizer:
    """
    Provides static methods for standardizing IPv4 and IPv6 addresses into their respective formats
    using different handlers in a Chain of Responsibility (CoR) pattern.

    Methods:
        - ipv4_interface: Standardizes IPv4 addresses with subnet masks in various formats.
        - ipv4_wildcard: Standardizes IPv4 addresses with wildcard masks.
        - ipv6_interface: Standardizes IPv6 addresses with subnet masks in various formats.
        - ipv6_wildcard: Standardizes IPv6 addresses with wildcard masks.
    """
    @staticmethod
    def ipv4_interface(*args, standardizer: List[IPStandardizer] = None) -> Tuple[IPv4Addr, IPv4NetMask]:
        """
        Standardizes IPv4 addresses with subnet masks using a chain of handlers.

        Parameters:
        *args: Positional arguments representing the input to be standardized.
            - This could be a string in CIDR notation, dot notation, or an address-mask tuple.
        standardizer: Optional[List[IPStandardizer]]
            - A list of IP standardizer handlers. If not provided, defaults to:
                - CIDRInterfaceIPv4StandardizerHandler
                - DotInterfaceIPv4StandardizerHandler
                - IPAddrInterfaceIPv4StandardizerHandler

        Returns:
        Tuple[IPv4Addr, IPv4NetMask]:
            A tuple containing a standardized IPv4 address and subnet mask.
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
        Standardizes IPv4 addresses with wildcard masks using a chain of handlers.

        Parameters:
        *args: Positional arguments representing the input to be standardized.
            - This could be a string in dot notation with a wildcard mask or an address-mask tuple.
        standardizer: Optional[List[IPStandardizer]]
            - A list of IP standardizer handlers. If not provided, defaults to:
                - DotWildcardIPv4StandardizerHandler
                - IPAddrWildcardIPv4StandardizerHandler

        Returns:
        Tuple[IPv4Addr, IPv4WildCard]:
            A tuple containing a standardized IPv4 address and wildcard mask.
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
        Standardizes IPv6 addresses with subnet masks using a chain of handlers.

        Parameters:
        *args: Positional arguments representing the input to be standardized.
            - This could be a string in CIDR notation, colon notation, or an address-mask tuple.
        standardizer: Optional[List[IPStandardizer]]
            - A list of IP standardizer handlers. If not provided, defaults to:
                - CIDRInterfaceIPv6StandardizerHandler
                - ColonInterfaceIPv6StandardizerHandler
                - IPAddrInterfaceIPv6StandardizerHandler

        Returns:
        Tuple[IPv6Addr, IPv6NetMask]:
            A tuple containing a standardized IPv6 address and subnet mask.
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
        Standardizes IPv6 addresses with wildcard masks using a chain of handlers.

        Parameters:
        *args: Positional arguments representing the input to be standardized.
            - This could be a string in colon notation with a wildcard mask or an address-mask tuple.
        standardizer: Optional[List[IPStandardizer]]
            - A list of IP standardizer handlers. If not provided, defaults to:
                - ColonWildcardIPv6StandardizerHandler
                - IPAddrWildcardIPv6StandardizerHandler

        Returns:
        Tuple[IPv6Addr, IPv6WildCard]:
            A tuple containing a standardized IPv6 address and wildcard mask.
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
