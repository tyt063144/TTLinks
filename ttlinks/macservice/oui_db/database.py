from typing import List, Any

from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db.loaders import LocalIabLoader, LocalMasLoader, LocalMamLoader, LocalMalLoader, LocalCidLoader
from ttlinks.macservice.oui_db.searchers import LocalIabSearcher, LocalMasSearcher, LocalMamSearcher, LocalMalSearcher, LocalCidSearcher
from ttlinks.macservice.oui_db.updaters import LocalIabUpdater, LocalMamUpdater, LocalMalUpdater, LocalCidUpdater, LocalMasUpdater
from ttlinks.macservice.oui_utils import OUIType, OUIUnit


class OUIDatabase:
    __instance = None
    _loaded = False
    _loaders = [LocalIabLoader(), LocalMasLoader(), LocalMamLoader(), LocalMalLoader(), LocalCidLoader()]
    _updaters = [LocalIabUpdater(), LocalMasUpdater(), LocalMamUpdater(), LocalMalUpdater(), LocalCidUpdater()]
    _searchers = [LocalIabSearcher(), LocalMasSearcher(), LocalMamSearcher(), LocalMalSearcher(), LocalCidSearcher()]
    _data: List = []

    def __new__(cls):
        """
        Ensures that only one instance of BinaryFlyWeightFactory exists.
        """
        if cls.__instance is None:
            cls.__instance = super(OUIDatabase, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.load()

    @classmethod
    def loaded(cls):
        return cls._loaded

    @classmethod
    def load(cls) -> None:
        cls._data = []
        for loader in cls._loaders:
            loader.connect()
            loader.load()
            cls._data.append(loader.data)
        cls._loaded = True
        # TODO: logs: 'database loading is complete.'

    def update(self, file_path: str) -> None:
        for updater in self._updaters:
            updater.update(file_path)
        # TODO: logs: 'database update is complete.'

    def revert(self, updater_type: OUIType) -> None:
        for updater in self._updaters:
            if updater.updater_type == updater_type:
                updater.revert()
        # TODO: logs: 'database revert is complete.'

    def search(self, mac: Any) -> OUIUnit:
        mac_binary = MACConverter.convert_oui(mac)
        for searcher in self._searchers:
            oui_unit = searcher.search(mac_binary, self._data)
            if oui_unit is not None:
                return oui_unit


if __name__ == '__main__':
    db = OUIDatabase()
    # search an oui
    print(db.search('00:60:9F:AA:7D:55').record)
    # update with official oui document
    db.update('../test_folder/new_mal.txt')
    db.load()
    try:
        print(db.search('00:60:9F:AA:7D:55').record)
    except Exception as e:
        print(e)
    # revert database to factory default
    db.revert(OUIType.MA_L)
    db.load()
    print(db.search('00:60:9F').record)


