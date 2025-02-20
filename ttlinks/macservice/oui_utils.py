from enum import Enum
from typing import Dict, Union
from ttlinks.common.tools.converters import NumeralConverter

class OUIType(Enum):
    """
    Enumeration representing different Organizationally Unique Identifier (OUI) types.

    Each type has a specific block size and a corresponding value.
    """
    UNKNOWN = {"block_size": 0, "value": 'UNKNOWN'}
    IAB = {"block_size": 4095, "value": 'IAB'}
    MA_S = {"block_size": 4095, "value": 'MA_S'}
    MA_M = {"block_size": 1048575, "value": 'MA_M'}
    MA_L = {"block_size": 16777215, "value": 'MA_L'}
    CID = {"block_size": 16777215, "value": 'CID'}


class OUIUnit:
    """
    A class representing an OUI unit, which defines a range of MAC addresses assigned to an organization.

    This class implements the Singleton pattern for unique OUI units based on a combination of
    `oui_id`, `start_hex`, `end_hex`, and `oui_type`.

    Attributes:
        __oui_id (str): The OUI identifier (prefix of the MAC address).
        __start_hex (str): The starting hexadecimal value of the MAC address range.
        __end_hex (str): The ending hexadecimal value of the MAC address range.
        __block_size (int): The block size allocated to this OUI.
        __oui_type (OUIType): The type of OUI (IAB, MA_S, MA_M, etc.).
        __organization (str, optional): The name of the organization owning the OUI.
        __address (str, optional): The address of the organization.
    """

    _oui_units = {}

    def __new__(
            cls,
            oui_id: str,
            start_hex: str,
            end_hex: str,
            block_size: int,
            oui_type: OUIType,
            organization: str,
            address: str
    ):
        """
        Ensures that only one instance exists for each unique OUI unit.

        Args:
            oui_id (str): OUI identifier (prefix of the MAC address).
            start_hex (str): Start of the OUI's hexadecimal MAC range.
            end_hex (str): End of the OUI's hexadecimal MAC range.
            block_size (int): The block size allocated to this OUI.
            oui_type (OUIType): Type of OUI.
            organization (str): Organization name associated with the OUI.
            address (str): Organization's address.

        Returns:
            OUIUnit: A unique instance corresponding to the provided parameters.
        """
        key = (oui_id, start_hex, end_hex, oui_type)
        if key not in cls._oui_units.keys():
            instance = super().__new__(cls)
            cls._oui_units[key] = instance
            instance.__oui_id = oui_id
            instance.__start_hex = start_hex
            instance.__end_hex = end_hex
            instance.__block_size = block_size
            instance.__oui_type = oui_type
            instance.__organization = organization
            instance.__address = address
            return instance
        return cls._oui_units[key]

    def __init__(
            self,
            oui_id: str,
            start_hex: str,
            end_hex: str,
            block_size: int,
            oui_type: OUIType,
            organization: Union[str, None],
            address: Union[str, None],
    ):
        """
        Initializes an OUIUnit instance.

        Args:
            oui_id (str): OUI identifier (prefix of the MAC address).
            start_hex (str): Start of the OUI's hexadecimal MAC range.
            end_hex (str): End of the OUI's hexadecimal MAC range.
            block_size (int): The block size allocated to this OUI.
            oui_type (OUIType): Type of OUI.
            organization (Union[str, None]): Organization name (optional).
            address (Union[str, None]): Organization's address (optional).
        """
        self.__oui_id = oui_id
        self.__start_hex = start_hex
        self.__end_hex = end_hex
        self.__block_size = block_size
        self.__oui_type = oui_type
        self.__organization = organization
        self.__address = address

    @property
    def first_mac_hex(self) -> str:
        """
        Returns the first MAC address in hexadecimal format.

        Returns:
            str: The first MAC address as a concatenation of OUI ID and start hex.
        """
        return self.__oui_id + self.__start_hex

    @property
    def last_mac_hex(self) -> str:
        """
        Returns the last MAC address in hexadecimal format.

        Returns:
            str: The last MAC address as a concatenation of OUI ID and end hex.
        """
        return self.__oui_id + self.__end_hex

    @property
    def first_mac_decimal(self) -> int:
        """
        Converts the first MAC address from hexadecimal to decimal.

        Returns:
            int: The decimal representation of the first MAC address.
        """
        return NumeralConverter.hexadecimal_to_decimal(self.first_mac_hex)

    @property
    def last_mac_decimal(self) -> int:
        """
        Converts the last MAC address from hexadecimal to decimal.

        Returns:
            int: The decimal representation of the last MAC address.
        """
        return NumeralConverter.hexadecimal_to_decimal(self.last_mac_hex)

    @property
    def record(self) -> Dict:
        """
        Returns a dictionary representation of the OUI unit.

        Returns:
            Dict: Dictionary containing OUI details, including MAC address range and organization info.
        """
        return {
            'oui_id': self.__oui_id,
            'start_hex': self.__start_hex,
            'end_hex': self.__end_hex,
            'start_decimal': self.first_mac_decimal,
            'end_decimal': self.last_mac_decimal,
            'block_size': self.__block_size,
            'oui_type': self.__oui_type.name,
            'organization': self.__organization,
            'address': self.__address,
        }
