import time
from abc import ABC, abstractmethod
from typing import List

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.tools.network import BinaryTools
from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db.loaders import LocalMalLoader
from ttlinks.macservice.oui_utils import OUIUnit, OUIType, OUIDBStrategy, OUIMask


class SearcherStrategy(ABC):
    """
    Abstract base class for search strategies. This class defines an interface for searching
    OUI data based on specific search criteria (e.g., MAC/OUI address lookup).

    Methods:
    - search(*args): Abstract method that must be implemented by subclasses to define the search logic.
    """
    @abstractmethod
    def search(self, *args):
        """
        Abstract method to perform a search based on the provided arguments.

        Parameters:
        *args: Variable-length argument list, expected to contain search criteria.

        Returns:
        OUIUnit or None: Subclasses must implement the logic to return an OUI unit that matches the search criteria, or None if not found.
        """
        pass


class SimpleSearcherStrategy(SearcherStrategy):
    """
    A concrete implementation of SearcherStrategy that performs a simple search for OUI units.
    This class is used for searching through a list of OUI units and determining if a MAC address
    is within the range defined by the OUI data.

    Methods:
    - search(mac: List[Octet], oui_data: list): Performs a search through the OUI data to find a matching OUI unit for the provided MAC address.
    - _is_within(mac: List[Octet], oui: OUIUnit) -> bool: Helper method to check if the provided MAC address falls within the range of a given OUI unit.
    """
    @staticmethod
    def _is_within(mac: List[Octet], oui: OUIUnit) -> bool:
        """
        Checks if the provided MAC address is within the range defined by the given OUI unit.
        This is done by comparing the binary digits of the MAC address and the OUI data.

        Parameters:
        mac (List[Octet]): The MAC address to check, provided as a list of Octet objects.
        oui (OUIUnit): The OUI unit containing the OUI ID and mask data, which is used to define the valid range.

        Returns:
        bool: True if the MAC address is within the range defined by the OUI unit, False otherwise.
        """
        compared_mac_digits = []
        for mac_binary in mac:
            compared_mac_digits.extend(mac_binary.binary_digits)
        oui_id_digit = oui.oui_id_binary_digits
        oui_mask_digit = oui.oui_mask_binary_digits
        return BinaryTools.is_binary_in_range(oui_id_digit, oui_mask_digit, compared_mac_digits)

    def search(self, mac: List[Octet], oui_data: list) -> OUIUnit:
        """
        Searches through the provided OUI data to find the OUI unit that matches the given MAC address.
        It uses the _is_within method to check if the MAC address is within the valid range for any OUI unit.

        Parameters:
        mac (List[Octet]): The MAC address to search for, provided as a list of Octet objects.
        oui_data (list): A list of dictionaries containing OUI data, each with 'oui_data' field that holds OUI units.

        Returns:
        OUIUnit: The OUI unit that matches the MAC address, or None if no match is found.
        """
        oui_units = []
        if len(oui_data) != 0:
            oui_units.extend(oui_data[0]['oui_data'])
        for oui_unit in oui_units:
            if self._is_within(mac, oui_unit):
                return oui_unit


class TrieSearcherStrategy(SearcherStrategy):
    """
    A concrete implementation of SearcherStrategy that performs searches using a Trie structure.
    It efficiently searches through OUI data stored in a trie to find the longest matching prefix
    for the given MAC address.

    Methods:
    - search(mac: List[Octet], oui_data: list): Searches the trie to find the OUI unit with the longest matching prefix for the provided MAC address.
    """
    def search(self, mac: List[Octet], oui_data: list):
        """
        Searches the Trie structure to find the OUI unit with the longest matching prefix for the provided MAC address.
        It traverses the trie based on the hexadecimal representation of the MAC address.

        Parameters:
        mac (List[Octet]): The MAC address to search for, provided as a list of Octet objects.
        oui_data (list): A list of dictionaries containing the root node of the trie ('oui_data').

        Returns:
        OUIUnit or None: The OUI unit with the longest matching prefix, or None if no match is found.
        """
        mac_string = ''.join([octet.hex for octet in mac])
        if len(oui_data) != 0:
            node = oui_data[0]['oui_data']
            longest_match = None
            for part in mac_string:
                if part in node.children:
                    node = node.children[part]
                    if node.is_end_of_oui:
                        longest_match = node.oui_unit
                else:
                    break
            return longest_match
        return None

class OUIDBSearcher(ABC):
    """
    Abstract base class for OUI database searchers. This class defines the interface for
    setting a search strategy and performing searches in an OUI database.

    Methods:
    - _set_strategy(strategy: OUIDBStrategy): Abstract method to set the search strategy.
    - search(mac: List[Octet], database: any): Abstract method to search for the OUI unit in the database using the provided MAC address.
    """
    @abstractmethod
    def _set_strategy(self, strategy: OUIDBStrategy) -> SearcherStrategy:
        """
        Abstract method to set the search strategy. This method allows setting different search strategies,
        such as searching using a trie or a simple iteration approach.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used.

        Returns:
        SearcherStrategy: The selected search strategy to be used for the search operation.
        """
        pass
    @abstractmethod
    def search(self, mac: List[Octet], database: any) -> OUIUnit:
        """
        Abstract method to perform a search for the OUI unit in the database using the provided MAC address.
        The search logic will depend on the search strategy that is set.

        Parameters:
        mac (List[Octet]): The MAC address to search for, provided as a list of Octet objects.
        database (any): The OUI database to search in.

        Returns:
        OUIUnit or None: The OUI unit that matches the MAC address, or None if no match is found.
        """
        pass


class LocalOUIDBSearcher(OUIDBSearcher):
    """
    A concrete implementation of OUIDBSearcher for searching through local OUI databases.
    This class supports different search strategies (Simple Iteration and Trie-based) and allows
    the use of masks to adjust MAC addresses before performing the search.

    Attributes:
    _searcher_type (OUIType): The type of OUI being searched for (default is UNKNOWN).
    _mask (List[Octet]): A list of octets that represent the mask used for adjusting the MAC address.
    _strategy (SearcherStrategy): The current search strategy used to search the OUI data.
    """
    _searcher_type: OUIType = OUIType.UNKNOWN
    _mask: List[Octet] = []

    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalOUIDBSearcher with the given search strategy (either Trie or Simple Iteration).
        The default strategy is Trie-based searching.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for searching OUI data. Defaults to Trie.
        """
        self._strategy = self._set_strategy(strategy)

    def _set_strategy(self, strategy: OUIDBStrategy) -> SearcherStrategy:
        """
        Sets the search strategy based on the provided OUIDBStrategy.
        It can either be a simple iteration or trie-based search.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for searching OUI data.

        Returns:
        SearcherStrategy: The selected search strategy to use.
        """
        if strategy == OUIDBStrategy.SIMPLE_ITERATION:
            return SimpleSearcherStrategy()
        elif strategy == OUIDBStrategy.TRIE:
            return TrieSearcherStrategy()

    def search(self, mac: List[Octet], oui_datas: list) -> OUIUnit:
        """
        Searches for the matching OUI unit in the OUI database based on the provided MAC address.
        The MAC address is first adjusted by applying any masks, and then the appropriate search
        strategy is used to perform the search.

        Parameters:
        mac (List[Octet]): The MAC address to search for, provided as a list of Octet objects.
        oui_datas (list): A list of dictionaries containing OUI data from different sources.

        Returns:
        OUIUnit or None: The matching OUI unit, or None if no match is found.
        """
        # Adjust the MAC address using the specified mask before searching
        adjusted_mac = BinaryTools.apply_mask_variations(mac, self._mask)

        # Filter the OUI data to match the searcher type
        filtered_oui_datas = list(filter(lambda oui_data: self._searcher_type.name == oui_data['type'], oui_datas))

        # Perform the search using the selected strategy
        return self._strategy.search(adjusted_mac, filtered_oui_datas)


class LocalIabSearcher(LocalOUIDBSearcher):
    """
    A concrete implementation of LocalOUIDBSearcher for searching IAB (Internet Architecture Board) OUI data.
    This searcher uses the specified strategy (either Trie or Simple Iteration) and applies the appropriate mask for IAB searches.

    Attributes:
    _searcher_type (OUIType): Specifies that this searcher is for IAB OUI data.
    _mask (List[Octet]): The mask used for adjusting MAC addresses in IAB searches.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalIabSearcher with the given search strategy. It sets the searcher type to IAB and
        applies the appropriate mask for IAB MAC addresses.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used (either Trie or Simple Iteration).
                                  Defaults to Trie-based searching.
        """
        self._searcher_type = OUIType.IAB
        self._mask: List[Octet] = OUIMask.IAB.value
        super().__init__(strategy)


class LocalMasSearcher(LocalOUIDBSearcher):
    """
    A concrete implementation of LocalOUIDBSearcher for searching MA-S (Manufacturer Assigned - Small) OUI data.
    This searcher uses the specified strategy (either Trie or Simple Iteration) and applies the appropriate mask for MA-S searches.

    Attributes:
    _searcher_type (OUIType): Specifies that this searcher is for MA-S OUI data.
    _mask (List[Octet]): The mask used for adjusting MAC addresses in MA-S searches.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMasSearcher with the given search strategy. It sets the searcher type to MA-S and
        applies the appropriate mask for MA-S MAC addresses.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used (either Trie or Simple Iteration).
                                  Defaults to Trie-based searching.
        """
        self._searcher_type = OUIType.MA_S
        self._mask: List[Octet] = OUIMask.MA_S.value
        super().__init__(strategy)


class LocalMamSearcher(LocalOUIDBSearcher):
    """
    A concrete implementation of LocalOUIDBSearcher for searching MA-M (Manufacturer Assigned - Medium) OUI data.
    This searcher uses the specified strategy (either Trie or Simple Iteration) and applies the appropriate mask for MA-M searches.

    Attributes:
    _searcher_type (OUIType): Specifies that this searcher is for MA-M OUI data.
    _mask (List[Octet]): The mask used for adjusting MAC addresses in MA-M searches.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMamSearcher with the given search strategy. It sets the searcher type to MA-M and
        applies the appropriate mask for MA-M MAC addresses.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used (either Trie or Simple Iteration).
                                  Defaults to Trie-based searching.
        """
        self._searcher_type = OUIType.MA_M
        self._mask: List[Octet] = OUIMask.MA_M.value
        super().__init__(strategy)


class LocalMalSearcher(LocalOUIDBSearcher):
    """
    A concrete implementation of LocalOUIDBSearcher for searching MA-L (Manufacturer Assigned - Large) OUI data.
    This searcher uses the specified strategy (either Trie or Simple Iteration) and applies the appropriate mask for MA-L searches.

    Attributes:
    _searcher_type (OUIType): Specifies that this searcher is for MA-L OUI data.
    _mask (List[Octet]): The mask used for adjusting MAC addresses in MA-L searches.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMalSearcher with the given search strategy. It sets the searcher type to MA-L and
        applies the appropriate mask for MA-L MAC addresses.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used (either Trie or Simple Iteration).
                                  Defaults to Trie-based searching.
        """
        self._searcher_type = OUIType.MA_L
        self._mask: List[Octet] = OUIMask.MA_L.value
        super().__init__(strategy)


class LocalCidSearcher(LocalOUIDBSearcher):
    """
    A concrete implementation of LocalOUIDBSearcher for searching CID (Company Identifier) OUI data.
    This searcher uses the specified strategy (either Trie or Simple Iteration) and applies the appropriate mask for CID searches.

    Attributes:
    _searcher_type (OUIType): Specifies that this searcher is for CID OUI data.
    _mask (List[Octet]): The mask used for adjusting MAC addresses in CID searches.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalCidSearcher with the given search strategy. It sets the searcher type to CID and
        applies the appropriate mask for CID MAC addresses.

        Parameters:
        strategy (OUIDBStrategy): The search strategy to be used (either Trie or Simple Iteration).
                                  Defaults to Trie-based searching.
        """
        self._searcher_type = OUIType.CID
        self._mask: List[Octet] = OUIMask.CID.value
        super().__init__(strategy)
