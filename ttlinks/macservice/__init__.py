from enum import Enum

from ttlinks.macservice.oui_db_manager import OUIDBLoader, OUIDBUpdater, OUIDBSearcher


class MACType(Enum):
    UNICAST = 1
    MULTICAST = 2
    BROADCAST = 3


DB_LOADER = OUIDBLoader()
DB_SEARCHER = OUIDBSearcher(DB_LOADER)
DB_UPDATER = OUIDBUpdater(DB_LOADER)
DB_UPDATER.batch_upsert()