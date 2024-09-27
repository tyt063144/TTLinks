import concurrent.futures
from abc import ABC, abstractmethod
from typing import List, Any, Union

from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db.loaders import LocalIabLoader, LocalMasLoader, LocalMamLoader, LocalMalLoader, LocalCidLoader
from ttlinks.macservice.oui_db.searchers import LocalIabSearcher, LocalMasSearcher, LocalMamSearcher, LocalMalSearcher, LocalCidSearcher
from ttlinks.macservice.oui_db.updaters import LocalIabUpdater, LocalMamUpdater, LocalMalUpdater, LocalCidUpdater, LocalMasUpdater
from ttlinks.macservice.oui_utils import OUIType, OUIUnit, OUIDBStrategy


class OUIDatabase(ABC):
    """
    Abstract base class for an OUI (Organizationally Unique Identifier) database.
    This class defines the interface for loading, updating, reverting, and searching OUI data.
    It can be extended to implement different types of OUI databases.

    Methods:
    - __init__(**kwargs): Initializes the OUI database with optional parameters.
    - load(): Abstract method to load the OUI data into the database.
    - update(*args): Abstract method to update the OUI data in the database.
    - revert(*args): Abstract method to revert any changes made to the OUI data in the database.
    - search(mac: Any) -> OUIUnit: Abstract method to search for a specific OUI unit based on the MAC address.
    - bulk_search(macs: List[Any]): Abstract method to perform a bulk search for multiple MAC addresses.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Abstract method to initialize the OUI database.

        Parameters:
        **kwargs: Optional parameters that can be used to configure the database.

        This method allows subclasses to set up the initial state of the database, including configurations such as database connections, file paths, or initial settings.
        """
        pass

    @abstractmethod
    def load(self):
        """
        Abstract method to load the OUI data into the database.

        This method is responsible for loading OUI data from a source (e.g., file, database, API) into the OUIDatabase instance.

        Returns:
        None: Subclasses will implement the loading logic.
        """
        pass

    @abstractmethod
    def update(self, *args):
        """
        Abstract method to update the OUI data in the database.

        Parameters:
        *args: Variable-length argument list, expected to include details of the updates to be made to the OUI data.

        This method allows for making changes or adding new data to the OUI database. The specific update behavior will depend on the implementation in the subclass.

        Returns:
        None: Subclasses will implement the updating logic.
        """
        pass


    @abstractmethod
    def revert(self, *args):
        """
        Abstract method to revert changes made to the OUI data.

        Parameters:
        *args: Variable-length argument list, expected to include details of the changes to be reverted.

        This method allows for undoing any changes made to the OUI database. The exact revert behavior will depend on the implementation in the subclass.

        Returns:
        None: Subclasses will implement the reverting logic.
        """
        pass

    @abstractmethod
    def search(self, mac: Any) -> OUIUnit:
        """
        Abstract method to search for a specific OUI unit based on the provided MAC address.

        Parameters:
        mac (Any): The MAC address to search for. The type of `mac` may vary depending on the implementation.

        Returns:
        OUIUnit: The OUI unit that matches the MAC address, or None if no match is found.

        This method performs a search in the OUI database to find the OUI unit associated with the given MAC address.
        """
        pass

    @abstractmethod
    def bulk_search(self, macs: List[Any]):
        """
        Abstract method to perform a bulk search for multiple MAC addresses.

        Parameters:
        macs (List[Any]): A list of MAC addresses to search for.

        Returns:
        List[OUIUnit]: A list of OUI units that correspond to the given MAC addresses. Returns None for any MAC addresses without a match.

        This method allows for searching multiple MAC addresses at once, returning the corresponding OUI units for each address.
        """
        pass


class LocalOUIDatabase(OUIDatabase):
    """
    A concrete implementation of the OUIDatabase that loads, updates, reverts, and searches OUI data
    from local databases using various loaders, updaters, and searchers for different OUI types (IAB, MA-S, MA-M, MA-L, CID).

    This class uses the Singleton pattern to ensure that only one instance of the database exists.

    Attributes:
    - __instance: Singleton instance of the LocalOUIDatabase.
    - _loaders: List of loaders used to load OUI data.
    - _updaters: List of updaters used to update OUI data.
    - _searchers: List of searchers used to perform searches on the OUI data.
    - _data: List to store the loaded OUI data from the different loaders.
    """
    __instance = None

    def __new__(cls, **kwargs):
        """
        Ensures that only one instance of LocalOUIDatabase is created (Singleton pattern).

        Parameters:
        **kwargs: Optional arguments to customize the instance, such as strategy settings.

        Returns:
        LocalOUIDatabase: The single instance of the class.
        """
        if cls.__instance is None:
            cls.__instance = super(OUIDatabase, cls).__new__(cls)
        return cls.__instance

    def __init__(self, **kwargs):
        """
        Initializes the LocalOUIDatabase with loaders, updaters, and searchers for different OUI types.
        Data is loaded on initialization.

        Parameters:
        **kwargs: Optional parameters such as strategy _settings for loading/searching (default is Trie-based).
        """
        self._kwargs = kwargs
        if not hasattr(self, "_initialized"):
            self._loaders = [
                LocalIabLoader(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMasLoader(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMamLoader(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMalLoader(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalCidLoader(self._kwargs.get('strategy', OUIDBStrategy.TRIE))
            ]
            self._updaters = [LocalIabUpdater(), LocalMasUpdater(), LocalMamUpdater(), LocalMalUpdater(), LocalCidUpdater()]
            self._searchers = [
                LocalIabSearcher(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMasSearcher(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMamSearcher(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalMalSearcher(self._kwargs.get('strategy', OUIDBStrategy.TRIE)),
                LocalCidSearcher(self._kwargs.get('strategy', OUIDBStrategy.TRIE))]
            self._data: List = []
            self.load()

    def load(self) -> None:
        """
        Loads the OUI data using the loaders. Each loader connects to its data source and loads the data,
        which is then stored in the `_data` attribute.
        """
        self._data = []
        for loader in self._loaders:
            loader.connect()
            loader.load()
            self._data.append(loader.data)

    def update(self, file_path: str) -> None:
        """
        Updates the OUI data by applying updates from the specified file.

        Parameters:
        file_path (str): The path to the file containing the updates.
        """
        for updater in self._updaters:
            updater.update(file_path)

    def revert(self, updater_type: OUIType) -> None:
        """
        Reverts changes made to the OUI data of a specific type.

        Parameters:
        updater_type (OUIType): The type of OUI to revert changes for (e.g., IAB, MA-S, etc.).
        """
        for updater in self._updaters:
            if updater.updater_type == updater_type:
                updater.revert()

    def search(self, mac: Any) -> Union[OUIUnit, None]:
        """
        Searches for the OUI unit that corresponds to the provided MAC address.

        Parameters:
        mac (Any): The MAC address to search for.

        Returns:
        OUIUnit: The matching OUI unit, or None if no match is found.
        """
        mac_binary = MACConverter.convert_oui(mac)
        try:
            for searcher in self._searchers:
                oui_unit = searcher.search(mac_binary, self._data)
                if oui_unit is not None:
                    return oui_unit
        except TypeError:
            return None

    def bulk_search(self, macs: List[Any]) -> dict:
        """
        Performs a bulk search for multiple MAC addresses. It uses multi-threading for faster searches.

        Parameters:
        macs (List[Any]): A list of MAC addresses to search for.

        Returns:
        dict: A dictionary mapping MAC addresses to their corresponding OUI units.
        """
        macs = list(set(macs))
        macs.sort()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.search, macs))
        return {mac: result for mac, result in zip(macs, results)}

