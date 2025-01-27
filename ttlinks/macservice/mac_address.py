import time
from abc import ABC, abstractmethod
from typing import List, Union, Any

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice import MACType
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db import OUI_DATABASE
from ttlinks.macservice.oui_utils import OUIUnit, OUIDBStrategy


class InterfaceMACAddr(ABC):

    _address: List[Octet] = []
    _oui: Union[OUIUnit, None] = None
    _mac_type: Union[MACType, None] = None
    _oui_database = None

    def __init__(self, mac: Any, search_strategy: OUIDBStrategy = OUIDBStrategy.TRIE):
        self._initialize_oui_database(search_strategy)
        self._initialization(mac)

    @classmethod
    def _initialize_oui_database(cls, strategy: OUIDBStrategy):
        if cls._oui_database is None:
            cls._oui_database = OUI_DATABASE

    @abstractmethod
    def _initialization(self, mac: List[Octet]):
        pass

    @abstractmethod
    def _validate(self, mac: List[Octet]) -> List[Octet]:
        pass

    @property
    def address(self) -> List[Octet]:
        return self._address

    @property
    def mac_type(self) -> MACType:
        return self._mac_type

    @property
    def oui(self):
        return self._oui

    @abstractmethod
    def _classify_mac_address(self):
        pass

    @abstractmethod
    def _search_oui(self):
        pass

    @property
    @abstractmethod
    def binary_digits(self):
        pass

    @property
    @abstractmethod
    def binary_string(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class MACAddr(InterfaceMACAddr):
    def _initialization(self, mac: Any):
        self._address = self._validate(mac)
        self._mac_type = self._classify_mac_address()
        self._oui = self._search_oui()

    def _validate(self, mac: Any):
        mac_binaries = MACConverter.convert_mac(mac)
        if mac_binaries is None:
            raise ValueError(f"MAC address {str(mac)} is not valid")
        return mac_binaries

    def _classify_mac_address(self):
        return MACAddrClassifier.classify_mac(self._address)

    def _search_oui(self):
        return self._oui_database.search(self._address)

    @property
    def binary_digits(self):
        result = []
        for byte in self._address:
            result.extend(byte.binary_digits)
        return result

    @property
    def binary_string(self):
        return ''.join(map(str, self.binary_digits))

    def __str__(self):
        return ':'.join([
            NumeralConverter.binary_to_hexadecimal(str(binary)).rjust(2, '0')
            for binary in self._address
        ])
