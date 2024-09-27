import json
import os
from abc import ABC, abstractmethod
from typing import List

from ttlinks.macservice import oui_file_parsers
from ttlinks.macservice.oui_db.serializers import oui_serializer
from ttlinks.macservice.oui_file_parsers import OuiFileParser
from ttlinks.macservice.oui_utils import OUIType


class OUIDBUpdater(ABC):
    """
    Abstract base class for updating OUI (Organizationally Unique Identifier) databases.
    This class defines two abstract methods, `update` and `revert`, which must be
    implemented by subclasses.

    Methods:
    - update(new_official_doc: str): Abstract method for updating the database using a new official document.
    - revert(): Abstract method for reverting to the default database by removing custom databases.
    """

    @abstractmethod
    def update(self, new_official_doc: str) -> None:
        """
        Abstract method to update the OUI database with a new official document.

        Parameters:
        - new_official_doc (str): Path to the new official OUI document.

        Returns:
        None
        """
        pass

    @abstractmethod
    def revert(self) -> None:
        """
        Abstract method to revert the database to the default version by removing the custom database.

        Returns:
        None
        """
        pass


class LocalOUIDBUpdater(OUIDBUpdater):
    """
    A concrete implementation of OUIDBUpdater for handling local OUI databases.
    This class allows users to update or revert a custom local OUI database.

    Attributes:
    - _base_dir (str): Base directory where the database files are stored.
    - _custom_db (str): Name of the custom database that can be updated or reverted.
    - _updater_type (OUIType): Type of the updater (e.g., IAB, CID, MA-L).
    - _file_parsers (List): List of file parsers used for handling different document formats.
    """
    _base_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data/')
    _custom_db: str = None
    _updater_type: OUIType = OUIType.UNKNOWN
    _file_parsers: List = []

    @property
    def updater_type(self) -> OUIType:
        """
        Property to return the type of the updater (e.g., IAB, CID, MA-L).

        Returns:
        OUIType: The type of updater used for handling the database.
        """
        return self._updater_type

    def update(self, new_official_doc: str) -> None:
        """
        Updates the custom OUI database with the data from the new official document.
        If a custom database already exists, it will be replaced with the new data.

        Parameters:
        - new_official_doc (str): Path to the new official document to update the database.

        Returns:
        None

        Functionality:
        - Parses the new official document using available file parsers.
        - If parsing is successful, writes the result to the custom database file.
        - The system will prioritize loading the custom database over the default database after an update.
        """
        result = OuiFileParser.parse_oui_file(new_official_doc, self._file_parsers)
        if result is not None:
            # Write result to the default database file
            with open(os.path.join(self._base_dir, self._custom_db), 'w') as db:
                db.write(json.dumps(result, default=oui_serializer))
            print(f'New custom database: {self._custom_db} is created or updated. Future lookups will use this database.')

    def revert(self):
        """
        Reverts to the default OUI database by removing the custom database.
        After this operation, the system will load the default_xxx.json instead of the custom database.

        Returns:
        None

        Functionality:
        - Checks if the custom database exists.
        - If it exists, deletes the custom database file, causing the system to use the default one provided by the package.
        """
        if os.path.exists(self._base_dir + self._custom_db):
            os.remove(os.path.join(self._base_dir, self._custom_db))
            print(f'Custom database: {self._custom_db} is removed.')


class LocalIabUpdater(LocalOUIDBUpdater):
    """
    A concrete implementation of LocalOUIDBUpdater specifically for handling updates to
    the Industrial Automation and Building (IAB) OUI database.

    This class allows users to update or revert the custom IAB OUI database with new official
    documentation in `.txt` or `.csv` formats.

    Attributes:
    - _custom_db (str): Name of the custom IAB database file ('custom_iab.json').
    - _updater_type (OUIType): The type of the updater, set to OUIType.IAB.
    - _file_parsers (List): A list of file parsers to handle official IAB documentation
      in both `.txt` and `.csv` formats.
    """

    def __init__(self):
        """
        Initializes the LocalIabUpdater class by setting the specific database names and
        parsers for handling IAB OUI data.

        Sets:
        - _custom_db: 'custom_iab.json', which will be updated or reverted.
        - _updater_type: OUIType.IAB, indicating that this is for the IAB OUI type.
        - _file_parsers: A list of parsers for handling `.txt` and `.csv` IAB files.

        Parameters:
        None
        """
        self._custom_db: str = 'custom_iab.json'
        self._updater_type: OUIType = OUIType.IAB
        self._file_parsers = [oui_file_parsers.IabOuiTxtFileParserHandler(), oui_file_parsers.IabOuiCsvFileParserHandler()]


class LocalMasUpdater(LocalOUIDBUpdater):
    """
    A concrete implementation of LocalOUIDBUpdater specifically for handling updates to
    the Manufacturer Assigned - Small (MA-S) OUI database.

    This class allows users to update or revert the custom MA-S OUI database with new official
    documentation in `.txt` or `.csv` formats.

    Attributes:
    - _custom_db (str): Name of the custom MA-S database file ('custom_mas.json').
    - _updater_type (OUIType): The type of the updater, set to OUIType.MA_S.
    - _file_parsers (List): A list of file parsers to handle official MA-S documentation
      in both `.txt` and `.csv` formats.
    """

    def __init__(self):
        """
        Initializes the LocalMasUpdater class by setting the specific database names and
        parsers for handling MA-S OUI data.

        Sets:
        - _custom_db: 'custom_mas.json', which will be updated or reverted.
        - _updater_type: OUIType.MA_S, indicating that this is for the MA-S OUI type.
        - _file_parsers: A list of parsers for handling `.txt` and `.csv` MA-S files.

        Parameters:
        None
        """
        self._custom_db: str = 'custom_mas.json'
        self._updater_type: OUIType = OUIType.MA_S
        self._file_parsers = [oui_file_parsers.MasOuiTxtFileParserHandler(), oui_file_parsers.MasOuiCsvFileParserHandler()]


class LocalMamUpdater(LocalOUIDBUpdater):
    """
    A concrete implementation of LocalOUIDBUpdater specifically for handling updates to
    the Manufacturer Assigned - Medium (MA-M) OUI database.

    This class allows users to update or revert the custom MA-M OUI database with new official
    documentation in `.txt` or `.csv` formats.

    Attributes:
    - _custom_db (str): Name of the custom MA-M database file ('custom_mam.json').
    - _updater_type (OUIType): The type of the updater, set to OUIType.MA_M.
    - _file_parsers (List): A list of file parsers to handle official MA-M documentation
      in both `.txt` and `.csv` formats.
    """

    def __init__(self):
        """
        Initializes the LocalMamUpdater class by setting the specific database names and
        parsers for handling MA-M OUI data.

        Sets:
        - _custom_db: 'custom_mam.json', which will be updated or reverted.
        - _updater_type: OUIType.MA_M, indicating that this is for the MA-M OUI type.
        - _file_parsers: A list of parsers for handling `.txt` and `.csv` MA-M files.

        Parameters:
        None
        """
        self._custom_db: str = 'custom_mam.json'
        self._updater_type: OUIType = OUIType.MA_M
        self._file_parsers = [oui_file_parsers.MamOuiTxtFileParserHandler(), oui_file_parsers.MamOuiCsvFileParserHandler()]


class LocalMalUpdater(LocalOUIDBUpdater):
    """
    A concrete implementation of LocalOUIDBUpdater specifically for handling updates to
    the Manufacturer Assigned - Large (MA-L) OUI database.

    This class allows users to update or revert the custom MA-L OUI database with new official
    documentation in `.txt` or `.csv` formats.

    Attributes:
    - _custom_db (str): Name of the custom MA-L database file ('custom_mal.json').
    - _updater_type (OUIType): The type of the updater, set to OUIType.MA_L.
    - _file_parsers (List): A list of file parsers to handle official MA-L documentation
      in both `.txt` and `.csv` formats.
    """

    def __init__(self):
        """
        Initializes the LocalMalUpdater class by setting the specific database names and
        parsers for handling MA-L OUI data.

        Sets:
        - _custom_db: 'custom_mal.json', which will be updated or reverted.
        - _updater_type: OUIType.MA_L, indicating that this is for the MA-L OUI type.
        - _file_parsers: A list of parsers for handling `.txt` and `.csv` MA-L files.

        Parameters:
        None
        """
        self._custom_db: str = 'custom_mal.json'
        self._updater_type: OUIType = OUIType.MA_L
        self._file_parsers = [oui_file_parsers.MalOuiTxtFileParserHandler(), oui_file_parsers.MalOuiCsvFileParserHandler()]


class LocalCidUpdater(LocalOUIDBUpdater):
    """
    A concrete implementation of LocalOUIDBUpdater specifically for handling updates to
    the Company Identifier (CID) OUI database.

    This class allows users to update or revert the custom CID OUI database with new official
    documentation in `.txt` or `.csv` formats.

    Attributes:
    - _custom_db (str): Name of the custom CID database file ('custom_cid.json').
    - _updater_type (OUIType): The type of the updater, set to OUIType.CID.
    - _file_parsers (List): A list of file parsers to handle official CID documentation
      in both `.txt` and `.csv` formats.
    """

    def __init__(self):
        """
        Initializes the LocalCidUpdater class by setting the specific database names and
        parsers for handling CID OUI data.

        Sets:
        - _custom_db: 'custom_cid.json', which will be updated or reverted.
        - _updater_type: OUIType.CID, indicating that this is for the CID OUI type.
        - _file_parsers: A list of parsers for handling `.txt` and `.csv` CID files.

        Parameters:
        None
        """
        self._custom_db: str = 'custom_cid.json'
        self._updater_type: OUIType = OUIType.CID
        self._file_parsers = [oui_file_parsers.CidOuiTxtFileParserHandler(), oui_file_parsers.CidOuiCsvFileParserHandler()]
