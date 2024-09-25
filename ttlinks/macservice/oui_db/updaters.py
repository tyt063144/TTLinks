import json
import os
from abc import ABC, abstractmethod
from typing import List

from ttlinks.macservice import oui_file_parsers
from ttlinks.macservice.oui_db.serializers import oui_enum_serializer
from ttlinks.macservice.oui_file_parsers import OuiFileParser
from ttlinks.macservice.oui_utils import OUIType


class OUIDBUpdater(ABC):
    @abstractmethod
    def update(self, new_official_doc: str) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass


class LocalOUIDBUpdater(OUIDBUpdater):
    _base_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data/')
    _custom_db: str = None
    _updater_type: OUIType = OUIType.UNKNOWN
    _file_parsers: List = []

    @property
    def updater_type(self) -> OUIType:
        return self._updater_type

    def update(self, new_official_doc: str) -> None:
        """
        Create custom database json according to updater user selects.
        When custom_xxx.json exists, system will always load this file instead of default_xxx.json
        """
        result = OuiFileParser.parse_oui_file(new_official_doc, self._file_parsers)
        if result is not None:
            # Write result to the default database file
            with open(os.path.join(self._base_dir, self._custom_db), 'w') as db:
                db.write(json.dumps(result, default=oui_enum_serializer))
            print(f'New custom database: {self._custom_db} is created or updated.')

    def revert(self):
        """
        Delete custom database so system will load default_xxx.json which ttlinks package provides along updates
        """
        if os.path.exists(self._base_dir + self._custom_db):
            os.remove(os.path.join(self._base_dir, self._custom_db))
            print(f'Custom database: {self._custom_db} is removed.')


class LocalIabUpdater(LocalOUIDBUpdater):
    def __init__(self):
        self._custom_db: str = 'custom_iab.json'
        self._updater_type: OUIType = OUIType.IAB
        self._file_parsers = [oui_file_parsers.IabOuiTxtFileParserHandler(), oui_file_parsers.IabOuiCsvFileParserHandler()]


class LocalMasUpdater(LocalOUIDBUpdater):
    def __init__(self):
        self._custom_db: str = 'custom_mas.json'
        self._updater_type: OUIType = OUIType.MA_S
        self._file_parsers = [oui_file_parsers.MasOuiTxtFileParserHandler(), oui_file_parsers.MasOuiCsvFileParserHandler()]


class LocalMamUpdater(LocalOUIDBUpdater):
    def __init__(self):
        self._custom_db: str = 'custom_mam.json'
        self._updater_type: OUIType = OUIType.MA_M
        self._file_parsers = [oui_file_parsers.MamOuiTxtFileParserHandler(), oui_file_parsers.MamOuiCsvFileParserHandler()]


class LocalMalUpdater(LocalOUIDBUpdater):
    def __init__(self):
        self._custom_db: str = 'custom_mal.json'
        self._updater_type: OUIType = OUIType.MA_L
        self._file_parsers = [oui_file_parsers.MalOuiTxtFileParserHandler(), oui_file_parsers.MalOuiCsvFileParserHandler()]


class LocalCidUpdater(LocalOUIDBUpdater):
    def __init__(self):
        self._custom_db: str = 'custom_cid.json'
        self._updater_type: OUIType = OUIType.CID
        self._file_parsers = [oui_file_parsers.CidOuiTxtFileParserHandler(), oui_file_parsers.CidOuiCsvFileParserHandler()]

