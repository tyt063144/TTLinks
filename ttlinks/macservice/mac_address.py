from abc import ABC, abstractmethod
from typing import List, Union, Any

from ttlinks.common.base_utils import BinaryClass
from ttlinks.common.tools import NumeralConverter
from ttlinks.macservice import MACType
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter
from ttlinks.macservice.oui_db.database import OUIDatabase
from ttlinks.macservice.oui_utils import OUIUnit, OUIType


class InterfaceMACAddr(ABC):
    _address: List[BinaryClass] = []
    _oui: Union[OUIUnit, None] = None
    _mac_type: MACType = None
    _oui_database = OUIDatabase()

    @property
    def mac_type(self) -> MACType:
        return self._mac_type

    @property
    def oui(self):
        return self._oui

    @abstractmethod
    def _initialization(self, mac: List[BinaryClass]):
        pass

    @abstractmethod
    def _validate(self, mac: List[BinaryClass]) -> List[BinaryClass]:
        pass

    @abstractmethod
    def _classify_mac_address(self):
        pass

    @abstractmethod
    def _search_oui(self):
        pass

    @abstractmethod
    def get_binary_digits(self):
        pass

    @abstractmethod
    def get_binary_string(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class MACAddr(InterfaceMACAddr):
    def __init__(self, mac: Any):
        self._initialization(mac)

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

    def get_binary_digits(self):
        result = []
        for byte in self._address:
            result.extend(byte.binary_digits)
        return result

    def get_binary_string(self):
        return ''.join(map(str, self.get_binary_digits()))

    def __str__(self):
        return ':'.join([
            NumeralConverter.binary_to_hexadecimal(str(binary)).rjust(2, '0')
            for binary in self._address
        ])


if __name__ == '__main__':
    mac_addr1 = MACAddr("b0-fc-0d-60-5d-28")
    mac_addr2 = MACAddr("60-57-c8-98-4d-63")
    print(mac_addr1)
    print(mac_addr1.mac_type)
    print(mac_addr1.oui.record)
    print(mac_addr1.get_binary_digits())
    print(mac_addr1.get_binary_string())
    print(id(mac_addr1._oui_database))
    print(mac_addr2)
    print(mac_addr2.mac_type)
    print(mac_addr2.oui.record)
    print(mac_addr2.get_binary_digits())
    print(mac_addr2.get_binary_string())
    print(id(mac_addr2._oui_database))

