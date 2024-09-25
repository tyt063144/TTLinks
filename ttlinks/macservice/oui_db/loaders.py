from __future__ import annotations

import hashlib
import json
import os.path
from abc import ABC, abstractmethod
from typing import Dict, List

from ttlinks.macservice import oui_file_parsers
from ttlinks.macservice.oui_db.serializers import oui_enum_serializer
from ttlinks.macservice.oui_file_parsers import OuiFileParser
from ttlinks.macservice.oui_utils import OUIType, OUIUnitCreator


class OUIDBLoader(ABC):
    @abstractmethod
    def connect(self, *args):
        pass

    @abstractmethod
    def load(self, *args):
        pass


class LocalOUIDBLoader(OUIDBLoader):
    _base_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data/')
    _default_db: str = None
    _custom_db: str = None
    _loader_type = OUIType.UNKNOWN
    _official_docs: List[str] = []
    _file_parsers: List = []
    _data: Dict = {}

    @property
    def data(self) -> Dict:
        return self._data

    @property
    def loader_type(self) -> OUIType:
        return self._loader_type

    def _initialization(self) -> None:
        if os.path.exists(self._base_dir + self._default_db) is False:
            # TODO: logs: f'No local {self._default_db} is found. Creating a new one.'
            self.create_default_db()
        if not self.compare_hash():
            # TODO: logs: f'New official docs are found. Updating {self._default_db} database'
            self.create_default_db()

    def connect(self, *args):
        """
        check if default_db exists. if yes, load will load the default db. Otherwise, create_default_db will create the json file
        """
        exist_local_db = os.path.exists(self._base_dir + self._default_db)
        if exist_local_db is False:
            self.create_default_db()
        return exist_local_db

    def load(self, *args):
        if not os.path.exists(self._base_dir + self._custom_db):
            # TODO: logs: f'Loading {self._default_db} database...'
            data = json.load(open(self._base_dir + self._default_db))
            data['db'] = 'default'
        else:
            # TODO: logs: f'Loading {self._custom_db} database...'
            data = json.load(open(self._base_dir + self._custom_db))
            data['db'] = 'custom'
        oui_creator = OUIUnitCreator()
        data['oui_units'] = [oui_creator.create_product(**unit) for unit in data['oui_units']]
        self._data = data

    def compare_hash(self) -> bool:
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

    def create_default_db(self) -> None:
        for office_doc in self._official_docs:
            try:
                result = OuiFileParser.parse_oui_file(office_doc, self._file_parsers)
                if result is not None:
                    # Write result to the default database file
                    with open(os.path.join(self._base_dir, self._default_db), 'w') as db:
                        db.write(json.dumps(result, default=oui_enum_serializer))
                    return
            except FileNotFoundError:
                continue
        raise FileNotFoundError(f'{', '.join(self._official_docs)} files are not found in the resources. Failed to create {self._default_db}')


class LocalIabLoader(LocalOUIDBLoader):
    def __init__(self):
        super().__init__()
        self._default_db = 'default_iab.json'
        self._custom_db = 'custom_iab.json'
        self._loader_type = OUIType.IAB
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'test_iab.txt'),
            os.path.join(self._base_dir, '../resources', 'test_iab.csv'),
        ]
        self._file_parsers = [oui_file_parsers.IabOuiTxtFileParserHandler(), oui_file_parsers.IabOuiCsvFileParserHandler()]
        self._initialization()


class LocalMasLoader(LocalOUIDBLoader):
    def __init__(self):
        super().__init__()
        self._default_db = 'default_mas.json'
        self._custom_db = 'custom_mas.json'
        self._loader_type = OUIType.MA_S
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'test_mas.txt'),
            os.path.join(self._base_dir, '../resources', 'test_mas.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MasOuiTxtFileParserHandler(), oui_file_parsers.MasOuiCsvFileParserHandler()]
        self._initialization()


class LocalMamLoader(LocalOUIDBLoader):
    def __init__(self):
        super().__init__()
        self._default_db = 'default_mam.json'
        self._custom_db = 'custom_mam.json'
        self._loader_type = OUIType.MA_M
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'test_mam.txt'),
            os.path.join(self._base_dir, '../resources', 'test_mam.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MamOuiTxtFileParserHandler(), oui_file_parsers.MamOuiCsvFileParserHandler()]
        self._initialization()


class LocalMalLoader(LocalOUIDBLoader):
    def __init__(self):
        super().__init__()
        self._default_db = 'default_mal.json'
        self._custom_db = 'custom_mal.json'
        self._loader_type = OUIType.MA_L
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'test_mal.txt'),
            os.path.join(self._base_dir, '../resources', 'test_mal.csv'),
        ]
        self._file_parsers = [oui_file_parsers.MalOuiTxtFileParserHandler(), oui_file_parsers.MalOuiCsvFileParserHandler()]
        self._initialization()


class LocalCidLoader(LocalOUIDBLoader):
    def __init__(self):
        super().__init__()
        self._default_db = 'default_cid.json'
        self._custom_db = 'custom_cid.json'
        self._loader_type = OUIType.CID
        self._official_docs = [
            os.path.join(self._base_dir, '../resources', 'test_cid.txt'),
            os.path.join(self._base_dir, '../resources', 'test_cid.csv'),
        ]
        self._file_parsers = [oui_file_parsers.CidOuiTxtFileParserHandler(), oui_file_parsers.CidOuiCsvFileParserHandler()]
        self._initialization()
