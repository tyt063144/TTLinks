from abc import ABC, abstractmethod
from typing import List

from ttlinks.common.base_utils import BinaryClass
from ttlinks.common.tools import BinaryTools
from ttlinks.macservice.oui_utils import OUIUnit, OUIType


class OUIDBSearcher(ABC):
    @abstractmethod
    def search(self, mac: List[BinaryClass], database: any) -> OUIUnit:
        pass


class LocalOUIDBSearcher(OUIDBSearcher):
    _searcher_type = OUIType.UNKNOWN

    @staticmethod
    def _is_within(mac: List[BinaryClass], oui: OUIUnit) -> bool:
        compared_mac_digits = []
        for mac_binary in mac:
            compared_mac_digits.extend(mac_binary.binary_digits)
        oui_id_digit = oui.oui_id_binary_digits
        oui_mask_digit = oui.oui_mask_binary_digits
        return BinaryTools.binary_within_range(oui_id_digit, oui_mask_digit, compared_mac_digits)

    def search(self, mac: List[BinaryClass], oui_datas: any) -> OUIUnit:
        oui_units = []
        for oui_data in oui_datas:
            if self._searcher_type.name == oui_data['type']:
                oui_units.extend(oui_data['oui_units'])
        for oui_unit in oui_units:
            if self._is_within(mac, oui_unit):
                return oui_unit


class LocalIabSearcher(LocalOUIDBSearcher):
    def __init__(self):
        self._searcher_type = OUIType.IAB


class LocalMasSearcher(LocalOUIDBSearcher):
    def __init__(self):
        self._searcher_type = OUIType.MA_S


class LocalMamSearcher(LocalOUIDBSearcher):
    def __init__(self):
        self._searcher_type = OUIType.MA_M


class LocalMalSearcher(LocalOUIDBSearcher):
    def __init__(self):
        self._searcher_type = OUIType.MA_L


class LocalCidSearcher(LocalOUIDBSearcher):
    def __init__(self):
        self._searcher_type = OUIType.CID
