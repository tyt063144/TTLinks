from __future__ import annotations

import hashlib
import json
import os.path
from abc import ABC, abstractmethod
from typing import Dict, List

from ttlinks.common.algorithm.trie import TrieNode
from ttlinks.macservice import oui_file_parsers
from ttlinks.macservice.oui_db.serializers import oui_serializer
from ttlinks.macservice.oui_file_parsers import OuiFileParser
from ttlinks.macservice.oui_utils import OUIType, OUIUnitCreator, OUIDBStrategy, OUIUnit


class TrieOUIUnit(TrieNode):
    def __init__(self):
        """
        A class that extends TrieNode to store OUI (Organizationally Unique Identifier) units.
        It adds a property `oui_unit` to store specific OUI-related data.

        Parameters:
        None

        Returns:
        None: Initializes the TrieOUIUnit node with an empty `oui_unit`.
        """
        super().__init__()
        self.oui_unit = None  # Stores the OUI unit data associated with the node


class LoaderStrategy(ABC):
    @abstractmethod
    def load(self, *args) -> List[OUIUnit]:
        """
        Abstract method for loading OUI units using a specific strategy.

        Parameters:
        *args: Variable-length argument list, expected to receive data related to OUI units.

        Returns:
        None: Subclasses must implement the loading logic.
        """
        pass


class SimpleLoaderStrategy(LoaderStrategy):
    def load(self, oui_units: List[Dict]) -> List[OUIUnit]:
        """
        A concrete implementation of LoaderStrategy that loads OUI units into a simple list structure.
        This strategy does not use a trie but instead processes and returns the OUI units as products.

        Parameters:
        oui_units (List[Dict]): A list of dictionaries where each dictionary contains the details of an OUI unit.

        Returns:
        List: A list of OUI products created from the given OUI unit data.
        """
        oui_creator = OUIUnitCreator()
        return [oui_creator.create_product(**oui_unit) for oui_unit in oui_units]


class TrieLoaderStrategy(LoaderStrategy):
    def __init__(self):
        """
        Initializes a loading strategy that uses a Trie structure to organize and store OUI units.

        Parameters:
        None

        Returns:
        None: Initializes the trie with a root node of type TrieOUIUnit.
        """
        self._trie_root = TrieOUIUnit()

    def load(self, oui_units: List[Dict]):
        """
        Loads OUI units into the Trie structure, storing each OUI unit based on its OUI ID.

        Parameters:
        oui_units (List[Dict]): A list of dictionaries containing OUI unit data, including the 'oui_id' field.

        Returns:
        TrieOUIUnit: The root of the Trie structure, which now contains the loaded OUI units.
        """
        for oui_unit in oui_units:
            self._insert(oui_unit['oui_id'], oui_unit)
        return self._trie_root

    def _insert(self, oui_id: str, oui_unit: dict):
        """
        Helper method to insert an OUI unit into the Trie structure based on its OUI ID.
        The OUI ID is stripped of colons (":") and then split into individual characters,
        which are used as keys in the Trie.

        Parameters:
        oui_prefix (str): The OUI ID, used as the prefix for insertion into the Trie.
        oui_unit (dict): A dictionary containing OUI unit data, including the OUI ID and other fields.

        Returns:
        None: The method inserts the OUI unit into the Trie and marks the corresponding node
        as the end of an OUI identifier.
        """
        node = self._trie_root
        for part in oui_id.replace(":", ''):
            if part not in node.children:
                node.children[part] = TrieOUIUnit()
            node = node.children[part]
        node.is_end_of_oui = True
        oui_creator = OUIUnitCreator()
        node.oui_unit = oui_creator.create_product(**oui_unit)


class OUIDBLoader(ABC):
    _connected: bool = False
    """
    Abstract base class that defines a blueprint for a loader responsible for
    connecting to a data source and loading OUI (Organizationally Unique Identifier) data.
    This class follows a strategy pattern, allowing different data loading strategies to be set and used.

    Subclasses must implement methods to:
    - Set the loading strategy
    - Connect to the data source
    - Load the OUI data using the chosen strategy
    """
    @abstractmethod
    def _set_strategy(self, strategy: OUIDBStrategy) -> LoaderStrategy:
        """
        Abstract method to set the strategy for loading OUI data. This method allows setting different
        strategies, such as simple loading or Trie-based loading, depending on the needs.

        Parameters:
        strategy (OUIDBStrategy): An instance of a strategy class that defines how the OUI data will be loaded.

        Returns:
        LoaderStrategy: The selected loading strategy that will be used for subsequent data loading.
        """
        pass

    @abstractmethod
    def connect(self, *args):
        """
        Abstract method for establishing a connection to the data source, such as a database, file,
        or other input sources containing OUI data.

        Parameters:
        *args: Variable-length argument list, expected to contain connection parameters required
               to establish a link to the data source (e.g., connection strings, file paths).

        Returns:
        None: Subclasses will implement the connection logic based on the data source type.
        """
        pass

    @abstractmethod
    def load(self, *args):
        """
        Abstract method for loading the OUI data into the system. This method leverages the previously
        set strategy to load and store the data in the desired structure (e.g., a list, trie).

        Parameters:
        *args: Variable-length argument list, expected to contain the data that will be loaded
               into the system (e.g., OUI units or data files).

        Returns:
        None: Subclasses will implement the specific loading behavior using the set strategy.
        """
        if not self._connected:
            raise ConnectionError("Must connect to the data source before loading data.")
        pass


class LocalOUIDBLoader(OUIDBLoader):
    """
    A concrete implementation of the OUIDBLoader that loads OUI data from a local database.
    It supports two loading strategies (simple iteration and Trie) and can load OUI data from either
    a default database or a custom one. This class also handles the creation of the default database
    and compares data integrity using MD5 hashes.

    Attributes:
    _base_dir (str): Base directory where OUI data files are stored.
    _default_db (str): Path to the default database file.
    _custom_db (str): Path to a custom database file (if provided).
    _loader_type (OUIType): Type of loader being used (e.g., UNKNOWN, SIMPLE_ITERATION, TRIE).
    _official_docs (List[str]): List of official document file paths used to create the default database.
    _file_parsers (List): List of parser classes used to parse official OUI files.
    _data (Dict): Dictionary containing loaded OUI data.
    _strategy (LoaderStrategy): The current strategy used to load OUI data.
    """
    _base_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data/')
    _default_db: str = None
    _custom_db: str = None
    _loader_type = OUIType.UNKNOWN
    _official_docs: List[str] = []
    _file_parsers: List = []
    _data: Dict = {}

    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the loader with the specified loading strategy. The default strategy is Trie-based.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Options include SIMPLE_ITERATION and TRIE.
        """
        self._strategy = self._set_strategy(strategy)

    def _set_strategy(self, strategy: OUIDBStrategy) -> LoaderStrategy:
        """
        Sets the loading strategy based on the provided OUIDBStrategy enum.

        Parameters:
        strategy (OUIDBStrategy): The strategy to use for loading data (SIMPLE_ITERATION, TRIE or other potential strategies developed in the future).

        Returns:
        LoaderStrategy: The loader strategy that will be used to load OUI data.
        """
        if strategy == OUIDBStrategy.SIMPLE_ITERATION:
            return SimpleLoaderStrategy()
        elif strategy == OUIDBStrategy.TRIE:
            return TrieLoaderStrategy()

    def _initialization(self) -> None:
        """
        Initializes the OUI database by creating the default database if it doesn't exist
        or if the hash comparison indicates the data has changed.

        Returns:
        None
        """
        if os.path.exists(self._base_dir + self._default_db) is False:
            self._create_default_db()
        if not self._compare_hash():
            self._create_default_db()

    @property
    def data(self) -> Dict:
        """
        Property to access the loaded OUI data.

        Returns:
        Dict: The loaded OUI data stored in the class instance.
        """
        return self._data

    @property
    def loader_type(self) -> OUIType:
        """
        Property to access the type of loader being used.

        Returns:
        OUIType: The type of loader (e.g., UNKNOWN, SIMPLE_ITERATION, TRIE).
        """
        return self._loader_type

    def connect(self, *args) -> bool:
        """
        Connects to the local database. If the default database does not exist, it creates one.

        Parameters:
        *args: Additional arguments for the connection (not used in this implementation).

        Returns:
        bool: True if the default database exists, False otherwise.
        """
        exist_local_db = os.path.exists(self._base_dir + self._default_db)
        if exist_local_db is False:
            self._create_default_db()
        self._connected = True
        return exist_local_db

    def load(self, *args):
        """
        Loads OUI data from either the default or custom database file, and applies the specified loading strategy.

        Parameters:
        *args: Additional arguments for loading (not used in this implementation).

        Returns:
        None: The loaded data is stored in the `_data` attribute.
        """
        super().load()
        result = {}
        if not os.path.exists(self._base_dir + self._custom_db):
            data = json.load(open(self._base_dir + self._default_db))
            data['db'] = 'default'
        else:
            data = json.load(open(self._base_dir + self._custom_db))
            data['db'] = 'custom'
        result['md5'] = data['md5']
        result['type'] = data['type']
        result['oui_data'] = self._strategy.load(data['oui_units'])
        self._data = result

    def _compare_hash(self) -> bool:
        """
        Compares the MD5 hash of official documents with the hash stored in the default database
        to verify data integrity.

        Returns:
        bool: True if the current document's hash matches the hash in the database, False otherwise.
        """
        existing_default_db = json.load(open(self._base_dir + self._default_db))
        hashes = []
        for file_path in self._official_docs:
            hash_object = hashlib.md5()
            try:
                hash_object.update(open(file_path).read().encode('utf-8'))
                hashes.append(hash_object.hexdigest())
            except FileNotFoundError:
                continue
        return existing_default_db['md5'] in hashes

    def _create_default_db(self) -> None:
        """
        Creates the default database by parsing official OUI documents using the provided file parsers.

        Returns:
        None: Writes the parsed OUI data to the default database file.

        Raises:
        FileNotFoundError: If none of the official documents can be found.
        """
        for office_doc in self._official_docs:
            try:
                result = OuiFileParser.parse_oui_file(office_doc, self._file_parsers)
                if result is not None:
                    # Write result to the default database file
                    with open(os.path.join(self._base_dir, self._default_db), 'w') as db:
                        db.write(json.dumps(result, default=oui_serializer))
                    return
            except FileNotFoundError:
                continue
        raise FileNotFoundError(f"{', '.join(self._official_docs)} files are not found in the resources. Failed to create {self._default_db}")


class LocalIabLoader(LocalOUIDBLoader):
    """
    A concrete implementation of LocalOUIDBLoader specialized for loading IAB (Internet Architecture Board)
    OUI data. This loader uses predefined database and resource files specific to IAB data and supports
    both Simple Iteration and Trie-based loading strategies.

    Attributes:
    _default_db (str): The name of the default database file for IAB data (default_iab.json).
    _custom_db (str): The name of the custom database file for IAB data (custom_iab.json).
    _loader_type (OUIType): Specifies the loader type as OUIType.IAB, indicating it is for IAB data.
    _official_docs (List[str]): List of paths to the official IAB document files (e.g., .txt, .csv).
    _file_parsers (List): List of parser handlers for parsing the official IAB documents.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalIabLoader with the specific database paths, document resources, and file parsers
        for IAB data. The loader will use the provided strategy to load the OUI data, defaulting to the Trie-based strategy.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Defaults to Trie-based loading (OUIDBStrategy.TRIE).
        """
        self._default_db = 'default_iab.json'
        self._custom_db = 'custom_iab.json'
        self._loader_type = OUIType.IAB
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'default_iab.txt'),
            os.path.join(self._base_dir, '../resources', 'default_iab.csv'),
        ]
        self._file_parsers = [oui_file_parsers.IabOuiTxtFileParserHandler(), oui_file_parsers.IabOuiCsvFileParserHandler()]
        self._initialization()
        super().__init__(strategy)


class LocalMasLoader(LocalOUIDBLoader):
    """
    A concrete implementation of LocalOUIDBLoader specialized for loading MA-S (MAC Address Small)
    OUI data. This loader uses predefined database and resource files specific to MA-S data and supports
    both Simple Iteration and Trie-based loading strategies.

    Attributes:
    _default_db (str): The name of the default database file for MA-S data (default_mas.json).
    _custom_db (str): The name of the custom database file for MA-S data (custom_mas.json).
    _loader_type (OUIType): Specifies the loader type as OUIType.MA_S, indicating it is for MA-S data.
    _official_docs (List[str]): List of paths to the official MA-S document files (e.g., .txt, .csv).
    _file_parsers (List): List of parser handlers for parsing the official MA-S documents.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMasLoader with the specific database paths, document resources, and file parsers
        for MA-S data. The loader will use the provided strategy to load the OUI data, defaulting to the Trie-based strategy.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Defaults to Trie-based loading (OUIDBStrategy.TRIE).
        """
        self._default_db = 'default_mas.json'
        self._custom_db = 'custom_mas.json'
        self._loader_type = OUIType.MA_S
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'default_mas.txt'),
            os.path.join(self._base_dir, '../resources', 'default_mas.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MasOuiTxtFileParserHandler(), oui_file_parsers.MasOuiCsvFileParserHandler()]
        self._initialization()
        super().__init__(strategy)


class LocalMamLoader(LocalOUIDBLoader):
    """
    A concrete implementation of LocalOUIDBLoader specialized for loading MA-M (MAC Address Medium)
    OUI data. This loader uses predefined database and resource files specific to MA-M data and supports
    both Simple Iteration and Trie-based loading strategies.

    Attributes:
    _default_db (str): The name of the default database file for MA-M data (default_mam.json).
    _custom_db (str): The name of the custom database file for MA-M data (custom_mam.json).
    _loader_type (OUIType): Specifies the loader type as OUIType.MA_M, indicating it is for MA-M data.
    _official_docs (List[str]): List of paths to the official MA-M document files (e.g., .txt, .csv).
    _file_parsers (List): List of parser handlers for parsing the official MA-M documents.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMamLoader with the specific database paths, document resources, and file parsers
        for MA-M data. The loader will use the provided strategy to load the OUI data, defaulting to the Trie-based strategy.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Defaults to Trie-based loading (OUIDBStrategy.TRIE).
        """
        self._default_db = 'default_mam.json'
        self._custom_db = 'custom_mam.json'
        self._loader_type = OUIType.MA_M
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'default_mam.txt'),
            os.path.join(self._base_dir, '../resources', 'default_mam.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MamOuiTxtFileParserHandler(), oui_file_parsers.MamOuiCsvFileParserHandler()]
        self._initialization()
        super().__init__(strategy)


class LocalMalLoader(LocalOUIDBLoader):
    """
    A concrete implementation of LocalOUIDBLoader specialized for loading MA-L (MAC Address Large)
    OUI data. This loader uses predefined database and resource files specific to MA-L data and supports
    both Simple Iteration and Trie-based loading strategies.

    Attributes:
    _default_db (str): The name of the default database file for MA-L data (default_mal.json).
    _custom_db (str): The name of the custom database file for MA-L data (custom_mal.json).
    _loader_type (OUIType): Specifies the loader type as OUIType.MA_L, indicating it is for MA-L data.
    _official_docs (List[str]): List of paths to the official MA-L document files (e.g., .txt, .csv).
    _file_parsers (List): List of parser handlers for parsing the official MA-L documents.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalMalLoader with the specific database paths, document resources, and file parsers
        for MA-L data. The loader will use the provided strategy to load the OUI data, defaulting to the Trie-based strategy.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Defaults to Trie-based loading (OUIDBStrategy.TRIE).
        """
        self._default_db = 'default_mal.json'
        self._custom_db = 'custom_mal.json'
        self._loader_type = OUIType.MA_L
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'default_mal.txt'),
            os.path.join(self._base_dir, '../resources', 'default_mal.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MalOuiTxtFileParserHandler(), oui_file_parsers.MalOuiCsvFileParserHandler()]
        self._initialization()
        super().__init__(strategy)


class LocalCidLoader(LocalOUIDBLoader):
    """
    A concrete implementation of LocalOUIDBLoader specialized for loading CID (Company ID)
    OUI data. This loader uses predefined database and resource files specific to CID data and supports
    both Simple Iteration and Trie-based loading strategies.

    Attributes:
    _default_db (str): The name of the default database file for CID data (default_cid.json).
    _custom_db (str): The name of the custom database file for CID data (custom_cid.json).
    _loader_type (OUIType): Specifies the loader type as OUIType.CID, indicating it is for CID data.
    _official_docs (List[str]): List of paths to the official CID document files (e.g., .txt, .csv).
    _file_parsers (List): List of parser handlers for parsing the official CID documents.
    """
    def __init__(self, strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        """
        Initializes the LocalCidLoader with the specific database paths, document resources, and file parsers
        for CID data. The loader will use the provided strategy to load the OUI data, defaulting to the Trie-based strategy.

        Parameters:
        strategy (OUIDBStrategy): The strategy to be used for loading OUI data.
                                  Defaults to Trie-based loading (OUIDBStrategy.TRIE).
        """
        self._default_db = 'default_cid.json'
        self._custom_db = 'custom_cid.json'
        self._loader_type = OUIType.CID
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'default_cid.txt'),
            os.path.join(self._base_dir, '../resources', 'default_cid.csv'),
        ]
        self._file_parsers = [oui_file_parsers.CidOuiTxtFileParserHandler(), oui_file_parsers.CidOuiCsvFileParserHandler()]
        self._initialization()
        super().__init__(strategy)
