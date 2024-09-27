from abc import ABC, abstractmethod
from typing import List, Union, Any

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice import MACType
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db.database import LocalOUIDatabase
from ttlinks.macservice.oui_utils import OUIUnit, OUIDBStrategy


class InterfaceMACAddr(ABC):
    """
    Abstract base class for representing and processing MAC addresses.
    This class defines the structure and behavior for handling MAC addresses, including validation, classification,
    and searching the OUI database. It uses the Chain of Responsibility pattern for MAC address classification
    and interacts with the OUI database to determine the organization associated with the MAC address.

    The class includes a method to initialize the OUI database (`_initialize_oui_database`), ensuring that
    the OUI database is loaded only once or updated when the strategy changes.

    Attributes:
    - _address (List[Octet]): Stores the validated MAC address as a list of Octet objects.
    - _oui (OUIUnit or None): Stores the corresponding OUI (Organizationally Unique Identifier) information after searching the OUI database.
    - _mac_type (MACType or None): Stores the type of the MAC address (UNICAST, MULTICAST, BROADCAST) after classification.
    - _oui_database (LocalOUIDatabase or None): Reference to the local OUI database for searching OUI information.
    - _current_strategy (OUIDBStrategy or None): Stores the current OUI database strategy.

    Methods:
    - _initialize_oui_database(strategy: OUIDBStrategy): Initializes or updates the OUI database based on the search strategy.
    - _initialization(mac: List[Octet]): Abstract method to initialize the MAC address and validate it.
    - _validate(mac: List[Octet]) -> List[Octet]: Abstract method to validate the MAC address format.
    - _classify_mac_address(): Abstract method to classify the MAC address as unicast, multicast, or broadcast.
    - _search_oui(): Abstract method to search the OUI database and find the associated OUI for the MAC address.
    - binary_digits: Abstract property to get the MAC address in binary format as a list of bits.
    - binary_string: Abstract property to get the MAC address as a binary string.
    - __str__(): Abstract method to get the MAC address as a human-readable string format.
    """

    _address: List[Octet] = []
    _oui: Union[OUIUnit, None] = None
    _mac_type: MACType | None = None
    _oui_database = None
    _current_strategy = None

    def __init__(self, mac: Any, search_strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Constructor that initializes the MAC address by calling the abstract _initialization method.
        The MAC address is validated and classified during initialization.

        Attributes:
        - _address (List[Octet]): Stores the validated MAC address as a list of Octet objects.
        - _oui (OUIUnit or None): Stores the corresponding OUI (Organizationally Unique Identifier) information after searching the OUI database.
        - _mac_type (MACType): Stores the type of the MAC address (UNICAST, MULTICAST, BROADCAST) after classification.
        - _oui_database (LocalOUIDatabase): Reference to the local OUI database for searching OUI information.

        Parameters:
        - mac (Any): The input MAC address in any format (hexadecimal, octets, etc.).
        - search_strategy (OUIDBStrategy): The strategy for OUI database searching. Default is TRIE.
        """
        self._initialize_oui_database(search_strategy)
        self._initialization(mac)

    @classmethod
    def _initialize_oui_database(cls, strategy: OUIDBStrategy):
        """
        Class method to initialize or change the OUI database strategy. If the strategy
        is different from the current one, it reloads the database with the new strategy.

        This ensures that the OUI database is loaded only once, and reloaded only if
        the strategy changes.

        Parameters:
        - strategy (OUIDBStrategy): The search strategy to use for the OUI database.
        """
        if cls._oui_database is None or cls._current_strategy != strategy:
            cls._oui_database = LocalOUIDatabase(strategy=strategy)
            cls._current_strategy = strategy

    @abstractmethod
    def _initialization(self, mac: List[Octet]):
        """
        Abstract method to initialize and validate the MAC address.

        Parameters:
        - mac (List[Octet]): The MAC address to initialize and validate.
        """
        pass

    @abstractmethod
    def _validate(self, mac: List[Octet]) -> List[Octet]:
        """
        Abstract method to validate the provided MAC address.

        Parameters:
        - mac (List[Octet]): The MAC address to validate.

        Returns:
        - List[Octet]: The validated MAC address as a list of Octet objects.
        """
        pass

    @property
    def mac_type(self) -> MACType:
        """
        Property that returns the type of the MAC address (UNICAST, MULTICAST, BROADCAST).

        Returns:
        - MACType: The type of the MAC address.
        """
        return self._mac_type

    @property
    def oui(self):
        """
        Property that returns the OUI (Organizationally Unique Identifier) associated with the MAC address.

        Returns:
        - OUIUnit or None: The OUI associated with the MAC address, or None if no OUI is found.
        """
        return self._oui

    @abstractmethod
    def _classify_mac_address(self):
        """
        Abstract method to classify the MAC address as UNICAST, MULTICAST, or BROADCAST.
        """
        pass

    @abstractmethod
    def _search_oui(self):
        """
        Abstract method to search for the OUI associated with the MAC address by looking it up in the local OUI database.
        """
        pass

    @property
    @abstractmethod
    def binary_digits(self):
        """
        Abstract property to return the binary representation of the MAC address as a list of bits (binary digits).

        Returns:
        - List[int]: The MAC address represented as binary digits.
        """
        pass

    @property
    @abstractmethod
    def binary_string(self):
        """
        Abstract property to return the binary representation of the MAC address as a binary string.

        Returns:
        - str: The MAC address as a binary string.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Abstract method to return the MAC address as a human-readable string.

        Returns:
        - str: The MAC address as a formatted string.
        """
        pass


class MACAddr(InterfaceMACAddr):
    """
    Concrete implementation of the InterfaceMACAddr abstract class.
    This class provides the logic for initializing, validating, classifying, and searching
    OUI (Organizationally Unique Identifier) information for a given MAC address. It also provides
    methods to convert the MAC address into its binary form and return it as a string.

    The class ensures that the OUI database is initialized based on the specified strategy.
    """
    def _initialization(self, mac: Any):
        """
        Initializes the MAC address by validating it, classifying its type (unicast, multicast, broadcast),
        and searching for its associated OUI in the OUI database.

        Parameters:
        - mac (Any): The input MAC address, which can be in any valid format (e.g., hexadecimal, binary, etc.).
        """
        self._address = self._validate(mac)
        self._mac_type = self._classify_mac_address()
        self._oui = self._search_oui()

    def _validate(self, mac: Any):
        """
        Validates the MAC address by converting it into binary format. If the conversion fails, an error is raised.

        Parameters:
        - mac (Any): The input MAC address to validate.

        Returns:
        - List[Octet]: A list of Octet objects representing the binary form of the MAC address.

        Raises:
        - ValueError: If the MAC address is invalid and cannot be converted.
        """
        mac_binaries = MACConverter.convert_mac(mac)
        if mac_binaries is None:
            raise ValueError(f"MAC address {str(mac)} is not valid")
        return mac_binaries

    def _classify_mac_address(self):
        """
        Classifies the MAC address as unicast, multicast, or broadcast using the MACAddrClassifier.

        Returns:
        - MACType: The type of the MAC address (UNICAST, MULTICAST, or BROADCAST).
        """
        return MACAddrClassifier.classify_mac(self._address)

    def _search_oui(self):
        """
        Searches the OUI database for the OUI associated with the given MAC address.

        Returns:
        - OUIUnit or None: The OUI associated with the MAC address, or None if not found.
        """
        return self._oui_database.search(self._address)

    @property
    def binary_digits(self):
        """
        Property that returns the binary representation of the MAC address as a list of bits (binary digits).

        Returns:
        - List[int]: A list of binary digits representing the MAC address.
        """
        result = []
        for byte in self._address:
            result.extend(byte.binary_digits)
        return result

    @property
    def binary_string(self):
        """
        Property that returns the binary representation of the MAC address as a single binary string.

        Returns:
        - str: A binary string representing the MAC address.
        """
        return ''.join(map(str, self.binary_digits))

    def __str__(self):
        """
        Returns the MAC address as a human-readable hexadecimal string, formatted with colons.

        Returns:
        - str: The MAC address formatted as a colon-separated hexadecimal string (e.g., AA:BB:CC:DD:EE:FF).
        """
        return ':'.join([
            NumeralConverter.binary_to_hexadecimal(str(binary)).rjust(2, '0')
            for binary in self._address
        ])
