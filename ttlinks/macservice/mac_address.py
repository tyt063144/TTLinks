from abc import ABC, abstractmethod
from typing import Union, Any

from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice import MACType, DB_SEARCHER
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_utils import OUIUnit


class InterfaceMACAddr(ABC):
    """
    Abstract base class for representing a MAC address.
    Defines the structure and necessary methods for handling MAC addresses.
    """

    _address: bytes = None
    _oui: Union[OUIUnit, None] = None
    _mac_type: Union[MACType, None] = None

    @abstractmethod
    def __str__(self):
        """Returns a string representation of the MAC address."""
        pass

    @abstractmethod
    def _initialize(self, mac: Any):
        """Initializes the MAC address and its associated properties."""
        pass

    @abstractmethod
    def _validate(self, mac:Any):
        """Validates the given MAC address and converts it into a standard format."""
        pass

    @abstractmethod
    def _classify_mac_address(self):
        """Classifies the MAC address type based on predefined criteria."""
        pass

    @abstractmethod
    def _search_oui(self):
        """Searches for the OUI (vendor information) associated with the MAC address."""
        pass

    @property
    @abstractmethod
    def oui(self):
        """
        Returns the Organizationally Unique Identifier (OUI) of the MAC address.
        The oui will be a list. If no result is found, an empty list is returned.
        """
        pass

    @property
    @abstractmethod
    def mac_type(self):
        """Returns the classification type of the MAC address."""
        pass

    @property
    @abstractmethod
    def binary_digits(self):
        """Returns the MAC address as a list of binary digits."""
        pass

    @property
    @abstractmethod
    def binary_string(self):
        """Returns the MAC address as a binary string."""
        pass

    @property
    @abstractmethod
    def as_hexadecimal(self):
        """Returns the MAC address in hexadecimal representation."""
        pass

    @property
    @abstractmethod
    def as_decimal(self):
        """Returns the MAC address in decimal representation."""
        pass


class MACAddr(InterfaceMACAddr):
    """
    Concrete implementation of the InterfaceMACAddr class.
    Handles MAC address initialization, validation, classification, and representation.
    """

    def __init__(self, address: Any):
        """
        Initializes a MACAddr instance with the given address.

        :param address: The MAC address input in any acceptable format.
        """
        self._address = address
        self._mac_type: Union[MACType, None] = None
        self._oui: Union[OUIUnit, None] = None
        self._initialize(self._address)

    def _initialize(self, mac: Any):
        """
        Initializes the MAC address by validating, classifying, and searching for its OUI.

        :param mac: The MAC address to be initialized.
        """
        self._address = self._validate(mac)
        self._mac_type = self._classify_mac_address()
        self._oui = self._search_oui()

    def _validate(self, mac: Any) -> bytes:
        """
        Validates the given MAC address and converts it to a standardized binary format.

        :param mac: The MAC address in any input format.
        :return: The MAC address in bytes format.
        :raises ValueError: If the given MAC address is invalid.
        """
        mac_binaries = MACConverter.convert_mac(mac)
        if mac_binaries is None:
            raise ValueError(f"MAC address {str(mac)} is not valid")
        return mac_binaries

    def _classify_mac_address(self):
        """
        Determines the type of MAC address based on its characteristics.

        :return: The classification of the MAC address.
        """
        return MACAddrClassifier.classify_mac(self._address)

    def _search_oui(self):
        """
        Searches for the Organizationally Unique Identifier (OUI) associated with the MAC address.

        :return: The OUI information of the MAC address.
        """
        return DB_SEARCHER.search_by_decimal(self.as_decimal)

    @property
    def oui(self):
        """Returns the Organizationally Unique Identifier (OUI) of the MAC address."""
        return self._oui

    @property
    def mac_type(self):
        """Returns the classification type of the MAC address."""
        return self._mac_type

    @property
    def binary_digits(self):
        """
        Returns the MAC address as a list of binary digits.

        :return: A list of 0s and 1s representing the MAC address in binary.
        """
        return list([int(bit) for bit in NumeralConverter.bytes_to_binary(self._address, 48)])

    @property
    def binary_string(self):
        """
        Returns the MAC address as a binary string.

        :return: A string representation of the MAC address in binary.
        """
        return NumeralConverter.bytes_to_binary(self._address, 48)

    @property
    def as_hexadecimal(self):
        """
        Returns the MAC address in hexadecimal representation.

        :return: A hexadecimal string representation of the MAC address.
        """
        return NumeralConverter.bytes_to_hexadecimal(self._address)

    @property
    def as_decimal(self):
        """
        Returns the MAC address as a decimal number.

        :return: The decimal equivalent of the MAC address.
        """
        return NumeralConverter.bytes_to_decimal(self._address)

    def __str__(self):
        """
        Returns a formatted string representation of the MAC address.

        :return: The MAC address in standard colon-separated hexadecimal notation.
        """
        return ':'.join([self.as_hexadecimal[i:i+2] for i in range(0, len(self.as_hexadecimal), 2)])


