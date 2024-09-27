from enum import Enum
from typing import Dict, List, Union

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.design_template.factory import Factory
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice.mac_converters import MACConverter


class OUIType(Enum):
    """
    An enumeration to categorize different types of Organizationally Unique Identifiers (OUIs).
    OUI types include:
    UNKNOWN: Unidentified or unspecified OUI type.
    IAB: Individual Address Block for smaller requirements.
    MA_S: Standard MAC Address block size typically used by most organizations.
    MA_M: Medium-sized MAC Address block for larger organizational needs.
    MA_L: Large MAC Address block allocated for extensive hardware requirements.
    CID: Company ID, often used to identify specific entities or manufacturers beyond the usual MAC address allocations.
    """
    UNKNOWN = 0
    IAB = 1
    MA_S = 2
    MA_M = 3
    MA_L = 4
    CID = 5


class OUIUnit:
    """
    Represents an Organizational Unique Identifier (OUI) unit that is used for identifying the manufacturer
    or organization by a unique MAC prefix in network technologies. This class utilizes the flyweight design pattern
    to manage instances efficiently by ensuring that identical objects are shared rather than duplicated.

    Attributes:
        _oui_units (dict): A class-level dictionary that stores unique OUIUnit instances indexed by a tuple key.
    """
    _oui_units = {}

    def __new__(
            cls,
            oui_id: List[Octet],
            oui_mask: List[Octet],
            oui_type: OUIType,
            organization: Union[str, None],
            mac_range: Union[str, None],
            oui_hex: Union[str, None],
            address: Union[str, None]
    ):
        """
        Ensures that only one instance of OUIUnit is created for each unique combination of start binaries,
        MAC mask, and OUI type. If an instance with the same key already exists, it returns the existing instance
        instead of creating a new one.

        Parameters:
            oui_id (List[BinaryClass]): Binary representations of the start of the OUI.
            oui_mask (List[BinaryClass]): Binary mask that applies to the OUI.
            oui_type (OUIType): The type of the OUI, indicating its use.
            organization (Union[str, None]): Name of the organization associated with the OUI.
            mac_range (Union[str, None]): The MAC range associated with the OUI.
            oui_hex (Union[str, None]): The hexadecimal representation of the OUI.
            address (Union[str, None]): The address of the organization owning the OUI.

        Returns:
            OUIUnit: A new or existing instance of the OUIUnit.
        """
        key = (tuple(oui_id), tuple(oui_mask), oui_type)
        if key not in cls._oui_units.keys():
            instance = super().__new__(cls)
            cls._oui_units[key] = instance
            instance.__oui_id = oui_id
            instance.__oui_mask = oui_mask
            instance.__oui_type = oui_type
            instance.__organization = organization
            instance.__mac_range = mac_range
            instance.__oui_hex = oui_hex
            instance.__address = address
            return instance
        return cls._oui_units[key]

    def __init__(
            self,
            oui_id: List[Octet],
            oui_mask: List[Octet],
            oui_type: OUIType,
            organization: Union[str, None],
            mac_range: Union[str, None],
            oui_hex: Union[str, None],
            address: Union[str, None],
    ):
        """
        Initializes the OUIUnit instance with provided parameters. This method is typically called only
        once when the instance is first created.

        Parameters:
            oui_id, oui_mask, oui_type, organization, mac_range, oui_hex, address: See __new__ for details.
        """
        self.__oui_id = oui_id
        self.__oui_mask = oui_mask
        self.__oui_type = oui_type
        self.__organization = organization
        self.__mac_range = mac_range
        self.__oui_hex = oui_hex
        self.__address = address

    @property
    def oui_id_binary_digits(self) -> List[int]:
        """
        Returns the binary digits for the OUI's identifier as a list of integers.

        Returns:
        - List[int]: Binary digits of the OUI ID.
        """
        result = []
        for octet in self.__oui_id:
            result.extend(octet.binary_digits)
        return result

    @property
    def oui_mask_binary_digits(self) -> List[int]:
        """
        Returns the binary digits for the OUI's mask as a list of integers.

        Returns:
        - List[int]: Binary digits of the OUI mask.
        """
        result = []
        for octet in self.__oui_mask:
            result.extend(octet.binary_digits)
        return result

    @property
    def record(self) -> Dict:
        """
        Returns a dictionary containing the hexadecimal representation of the OUI details.

        Returns:
        - Dict: A dictionary with keys 'oui_id', 'oui_mask', 'oui_type', 'organization', 'mac_range', 'oui_hex', 'address'.
        """
        return {
            'oui_id': ':'.join([
                NumeralConverter.binary_to_hexadecimal(str(start_bin)).rjust(2, '0')
                for start_bin in self.__oui_id
            ]),
            'oui_mask': ':'.join([
                NumeralConverter.binary_to_hexadecimal(str(mask_bin)).rjust(2, '0')
                for mask_bin in self.__oui_mask
            ]),
            'oui_type': self.__oui_type.name,
            'organization': self.__organization,
            'mac_range': self.__mac_range,
            'oui_hex': self.__oui_hex,
            'address': self.__address
        }


class OUIUnitCreator(Factory):
    """
    A factory class for creating instances of OUIUnit. It processes the raw input and creates the appropriate OUIUnit.

    Method:
    - create_product: Creates a new OUIUnit based on the provided arguments (oui_id, oui_mask, oui_type, etc.).
    """

    def create_product(self, **kwargs):
        """
        Converts the provided OUI data to octets and creates an OUIUnit instance.

        Parameters:
        - kwargs (dict): Contains raw input like 'oui_id', 'oui_mask', 'oui_type', etc., which is processed before creating the OUIUnit.

        Returns:
        - OUIUnit: A new instance of the OUIUnit class.
        """
        data = {
            'oui_id': MACConverter.convert_oui(kwargs['oui_id']),
            'oui_mask': MACConverter.convert_oui(kwargs['oui_mask']),
            'oui_type': OUIType[kwargs['oui_type']]
        }
        kwargs.update(data)
        return OUIUnit(**kwargs)


class OUIDBStrategy(Enum):
    """
    An enumeration to categorize different strategies for loading or searching OUI data.
    OUI loader strategies include:
    - SIMPLE_ITERATION: A simple iteration strategy for loading or searching OUI data.
    - TRIE: A trie-based strategy for loading or searching OUI data.
    """
    SIMPLE_ITERATION = 0
    TRIE = 1

class OUIMask(Enum):
    """
    An enumeration to categorize different types of masks used for OUI search.
    OUI masks include:
    """
    IAB = (
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
    )
    MA_S = (
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
    )
    MA_M = (
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 2
    )
    MA_L = (
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
    )
    CID = (
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
            [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
    )
