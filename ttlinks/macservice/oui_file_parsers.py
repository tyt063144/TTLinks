import copy
import hashlib
import os
import re
from abc import abstractmethod, ABC
from typing import List, Dict, Union

from ttlinks.Files.file_classifiers import FileType
from ttlinks.Files.file_utils import File
from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.design_template.cor import BidirectionalCoRHandler
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice.mac_converters import BinaryDigitsMAC48ConverterHandler
from ttlinks.macservice.oui_utils import OUIType, OUIUnit


class IEEEOuiFile(File):
    """
    A concrete implementation of the File abstract class, specifically designed to handle IEEE OUI (Organizationally
    Unique Identifier) files. This class reads the content of an IEEE OUI file and makes it available through the
    file_content property.

    The IEEEOuiFile class is typically used to pass along OUI file content to parsers and other processes that
    handle such data, allowing for dynamic changes to the properties as necessary during runtime.
    """

    def _validate(self):
        super()._validate()

    def _read(self):
        """
        Reads the contents of the OUI file specified by the file path using the method specified by _read_method.
        The content is stored in the _file_content attribute, making it accessible via the file_content property.
        """
        self._file_content = open(self._file_path, self._read_method).read()


class OUIFileParserHandler(BidirectionalCoRHandler):
    """
    Abstract base class for handling the parsing of OUI files in a chain of responsibility pattern.
    This class provides common functionality for parsing both CSV and TXT OUI files, allowing
    concrete implementations to define specific parsing logic for different OUI file types.

    Properties:
        _file: Stores the OUI file being processed.
        _mask (List[Octet]): A list of octets used to mask MAC addresses during parsing.
        _oui_type (OUIType): Specifies the type of OUI being parsed (e.g., UNKNOWN, IAB, MA-S).
    """
    _file = None

    @abstractmethod
    def __init__(self):
        """
        Initializes the OUIFileParserHandler with a default mask and OUI type.

        Properties:
            _mask (List[Octet]): A list of octets used to mask certain parts of the MAC address.
            _oui_type (OUIType): Defines the type of OUI, defaulting to UNKNOWN.
        """
        self._mask: List[Octet] = []
        self._oui_type: OUIType = OUIType.UNKNOWN

    @abstractmethod
    def handle(self, oui_doc_path: str):
        """
        Abstract method to handle the OUI document processing. This method passes the file
        to the next handler in the chain if one exists.

        Parameters:
            oui_doc_path (str): The path to the OUI document.

        Returns:
            The result from the next handler if one exists, otherwise None.
        """
        if self._next_handler:
            return self._next_handler.handle(oui_doc_path)
        return self._next_handler

    @abstractmethod
    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Abstract method to parse the OUI document. This method must be implemented
        by concrete subclasses to handle specific OUI file formats.

        Parameters:
            oui_doc (str): The contents of the OUI file.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary with parsed OUI units and related information.
        """
        pass

    @abstractmethod
    def _parse_mac_range(self, mac: List[Octet], oui_mask: List[Octet]) -> List[str]:
        """
        Abstract method to parse the MAC address range using the provided OUI mask.

        Parameters:
            mac (List[Octet]): A list of Octet objects representing the MAC address.
            oui_mask (List[Octet]): A list of Octet objects representing the mask to be applied to the MAC.

        Returns:
            List[str]: The parsed MAC range in string format.
        """
        pass

    @abstractmethod
    def _parse_physical_address(self, *args: str) -> str:
        """
        Abstract method to parse physical address information from the OUI file.

        Parameters:
            args (str): The components of the physical address (e.g., line 1, line 2, country).

        Returns:
            str: The formatted physical address as a string.
        """
        pass

    @property
    def file(self):
        """
        Property to retrieve the file being processed by the handler.

        Returns:
            The OUI file (IEEEOuiFile) being handled.
        """
        return self._file

    def _generate_file_information(self, oui_doc_path: str):
        """
        Generates file information for the current handler. If a previous handler exists,
        it will use the file from that handler. Otherwise, it creates a new `IEEEOuiFile`
        based on the provided path.

        Parameters:
            oui_doc_path (str): The path to the OUI document to be processed.
        """
        if self._previous_handler and self._previous_handler.file:
            self._file = self._previous_handler.file
        else:
            self._file = IEEEOuiFile(oui_doc_path)




class OUITxtFileParserHandler(OUIFileParserHandler, ABC):
    """
    A concrete implementation of the OUIFileParserHandler class for handling OUI data in text (.txt) format.
    This class provides methods to parse MAC ranges and physical addresses from OUI files using predefined masks.

    Inherits from:
        OUIFileParserHandler: Base class for handling OUI files with a chain of responsibility pattern.

    Methods:
        _parse_mac_range(mac: List[Octet], oui_mask: List[Octet]) -> List[str]: Parses the MAC address range using the provided mask.
        _parse_physical_address(address_line1: str, address_line2: str, country: str) -> str: Parses and formats the physical address.
    """

    def _parse_mac_range(self, mac: List[Octet], oui_mask: List[Octet]) -> List[str]:
        """
        Parses the MAC address range based on the provided MAC and OUI mask.

        The method applies the OUI mask to the original MAC binary digits, generating both the original
        MAC address and a modified address that reflects the mask. It converts these binary representations
        to hexadecimal format for readable MAC addresses.

        Parameters:
            mac (List[Octet]): A list of Octet objects representing the MAC address to be parsed.
            oui_mask (List[Octet]): A list of Octet objects representing the mask to apply to the MAC address.

        Returns:
            List[str]: A list containing two MAC addresses:
                        1. The original MAC address with the applied mask.
                        2. The modified MAC address with the masked range.
        """
        original_mac_binary_digits = []
        mask_binary_digits = []
        for mac_octet in mac:
            original_mac_binary_digits += mac_octet.binary_digits
        for mask_octet in oui_mask:
            mask_binary_digits += mask_octet.binary_digits
        non_matching_indices = mask_binary_digits.count(0)
        after_matching_mac_binary_digits = copy.deepcopy(original_mac_binary_digits)
        after_matching_mac_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_digits_mac48_converter = BinaryDigitsMAC48ConverterHandler()
        return [
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(original_mac_binary_digits)),
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(after_matching_mac_binary_digits)),
        ]

    def _parse_physical_address(self, address_line1: str, address_line2: str, country: str) -> str:
        """
        Parses and formats the physical address from the OUI file's data.

        If the address is empty, indicating a private OUI range, it returns an empty string. Otherwise,
        the method processes and formats address lines and the country into a single string.

        Parameters:
            address_line1 (str): The first line of the address.
            address_line2 (str): The second line of the address, may include additional details like city and postal code.
            country (str): The country part of the address.

        Returns:
            str: A formatted address string including the address lines and country.
                 If no address is provided, returns an empty string.
        """
        if address_line1 == '':  # skip if there is no address. meaning a private OUI range
            return ''
        full_address = f"{address_line1}, "
        address_line2_component = re.split(r'\s{2,}', address_line2)
        if len(address_line2_component) == 2:
            full_address += ' '.join(address_line2_component)
        if len(address_line2_component) == 3:
            full_address += f"{address_line2_component[0]}, "
            full_address += ' '.join(address_line2_component[1:])
        full_address += f", {country}"
        return full_address.replace('  ', ' ').replace('"', '').replace(',,', ',').strip()


class OUICsvFileParserHandler(OUIFileParserHandler, ABC):
    """
    A concrete implementation of the OUIFileParserHandler class designed to handle OUI data in CSV (.csv) format.
    This class provides methods to parse MAC ranges and physical addresses from OUI CSV files using predefined masks.

    Inherits from:
        OUIFileParserHandler: Base class for handling OUI files in a chain of responsibility pattern.

    Methods:
        _parse_mac_range(mac: List[Octet], oui_mask: List[Octet]) -> List[str]: Parses the MAC address range using the provided mask.
        _parse_physical_address(address_line: str) -> str: Parses and formats a single-line physical address from the CSV data.
    """

    def _parse_mac_range(self, mac: List[Octet], oui_mask: List[Octet]) -> List[str]:
        """
        Parses the MAC address range based on the provided MAC and OUI mask from a CSV file.

        This method applies the OUI mask to the binary digits of the MAC address and generates both the
        original MAC address and the modified MAC address reflecting the mask. It converts these binary
        digits into hexadecimal format for readable MAC addresses.

        Parameters:
            mac (List[Octet]): A list of Octet objects representing the MAC address.
            oui_mask (List[Octet]): A list of Octet objects representing the mask applied to the MAC address.

        Returns:
            List[str]: A list containing two MAC addresses:
                        1. The original MAC address with the applied mask.
                        2. The modified MAC address reflecting the masked range.
        """
        original_mac_binary_digits = []
        mask_binary_digits = []
        for mac_octet in mac:
            original_mac_binary_digits += mac_octet.binary_digits
        for mask_octet in oui_mask:
            mask_binary_digits += mask_octet.binary_digits
        non_matching_indices = mask_binary_digits.count(0)
        after_matching_mac_binary_digits = copy.deepcopy(original_mac_binary_digits)
        after_matching_mac_binary_digits[-non_matching_indices:] = ([1] * (non_matching_indices - 1)) + [1]
        binary_digits_mac48_converter = BinaryDigitsMAC48ConverterHandler()
        return [
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(original_mac_binary_digits)),
            ':'.join(NumeralConverter.binary_to_hexadecimal(str(mac_binary)).rjust(2, '0')
                     for mac_binary in binary_digits_mac48_converter.handle(after_matching_mac_binary_digits)),
        ]

    def _parse_physical_address(self, address_line: str) -> str:
        """
        Parses and formats a physical address from a single-line CSV entry.

        This method cleans up the address string by removing any extra spaces or unnecessary characters.
        It replaces double spaces, quotes, and commas to ensure a properly formatted address.

        Parameters:
            address_line (str): The physical address as a single line from the CSV file.

        Returns:
            str: A cleaned and formatted physical address.
        """
        return address_line.replace('  ', ' ').replace('"', '').replace(',,', ',').strip()


class IabOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A concrete implementation of the OUITxtFileParserHandler class, specifically designed to parse OUI data
    in text (.txt) format related to IAB (Individual Address Block) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from the IAB-related
    OUI entries found in a text file, such as MAC ranges, company names, and physical addresses.

    Inherits from:
        OUITxtFileParserHandler: Base class for handling text-based OUI files.

    Methods:
        handle(oui_doc_path: str) -> Dict[str, List[OUIUnit]]: Handles and processes the OUI text file for IAB ranges.
        parse(oui_doc: str) -> Dict[str, List[OUIUnit]]: Parses the contents of the OUI document, extracting relevant data.
    """

    def __init__(self):
        """
        Initializes the IabOuiTxtFileParserHandler with a predefined OUI mask and OUI type for IAB ranges.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for the IAB OUI range.
            _oui_type (OUIType): Specifies the OUI type as IAB.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI text file to determine if it contains IAB OUI entries. If the file matches
        the expected format, it proceeds with parsing; otherwise, it passes the handling to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed IAB-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'IAB Range\s+Organization', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the IAB OUI document, extracting details such as MAC address ranges, company names, and physical addresses.
        The method uses regular expressions to match and extract relevant data, then formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed IAB OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (IAB).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MasOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A concrete implementation of the OUITxtFileParserHandler class, designed specifically to parse OUI data
    in text (.txt) format for the MA-S (MAC Address Block Small) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-S-related
    OUI entries in text files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUITxtFileParserHandler: Base class for handling text-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to the MA-S ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-S.
    """

    def __init__(self):
        """
        Initializes the MasOuiTxtFileParserHandler with a predefined OUI mask for MA-S ranges.

        The mask is tailored to handle the specific MAC address blocks for MA-S, which include 4 fully masked
        octets, 1 partially masked octet, and 1 unmasked octet.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-S OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-S.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc_path: str):

        """
        Handles the processing of the OUI text file to determine if it contains MA-S OUI entries.

        This method checks whether the OUI file is a valid text file and contains specific patterns that identify MA-S OUI ranges.
        If the file matches, it parses the document; otherwise, it passes the handling to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-S-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI-36/MA-S Range\s+Organization', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-S OUI document, extracting details such as MAC address ranges, company names,
        and physical addresses. The method uses regular expressions to match and extract relevant data, then formats
        it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-S OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-S).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MamOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A concrete implementation of the OUITxtFileParserHandler class, specifically designed to parse OUI data
    in text (.txt) format related to the MA-M (MAC Address Block Medium) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-M-related
    OUI entries found in text files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUITxtFileParserHandler: Base class for handling text-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to MA-M ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-M.
    """

    def __init__(self):
        """
        Initializes the MamOuiTxtFileParserHandler with a predefined OUI mask and OUI type for MA-M ranges.

        The mask is specifically tailored for MA-M OUI ranges, with 3 fully masked octets, 1 partially masked octet,
        and 2 unmasked octets, which corresponds to the structure of MA-M MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-M OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-M.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 2
        )
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI text file to check for MA-M OUI entries.

        The method determines if the OUI file contains MA-M-specific information by checking the file type and
        searching for relevant patterns in the file. If the file matches the expected format, it proceeds with parsing;
        otherwise, it passes the request to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-M-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI-28/MA-M Range\s+Organization', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-M OUI document, extracting key information such as MAC address ranges, company names,
        and physical addresses. The method uses regular expressions to locate and extract this data from the document,
        and formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-M OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-M).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = mac_range[:mac_range.find('-')]
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class MalOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A concrete implementation of the OUITxtFileParserHandler class, specifically designed to parse OUI data
    in text (.txt) format related to the MA-L (MAC Address Block Large) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-L-related
    OUI entries found in text files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUITxtFileParserHandler: Base class for handling text-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to MA-L ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-L.
    """

    def __init__(self):
        """
        Initializes the MalOuiTxtFileParserHandler with a predefined OUI mask and OUI type for MA-L ranges.

        The mask is specifically tailored for MA-L OUI ranges, consisting of 3 fully masked octets and 3 unmasked octets,
        which matches the structure of MA-L MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-L OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-L.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.MA_L

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI text file to determine if it contains MA-L OUI entries.

        The method checks whether the file is a valid text file and contains patterns related to MA-L OUI ranges.
        If the file matches the expected format, it proceeds to parse the document; otherwise, it passes the request
        to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-L-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'OUI/MA-L\s+Organization', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-L OUI document, extracting details such as MAC address ranges, company names,
        and physical addresses. The method uses regular expressions to match and extract relevant data, then formats
        it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-L OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-L).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


class CidOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    A concrete implementation of the OUITxtFileParserHandler class, designed specifically to parse OUI data
    in text (.txt) format related to CID (Company Identifier) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from CID-related
    OUI entries found in text files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUITxtFileParserHandler: Base class for handling text-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to CID ranges.
        _oui_type (OUIType): Specifies the OUI type as CID.
    """

    def __init__(self):
        """
        Initializes the CidOuiTxtFileParserHandler with a predefined OUI mask and OUI type for CID ranges.

        The mask is specifically tailored for CID OUI ranges, with 3 fully masked octets and 3 unmasked octets,
        corresponding to the structure of CID MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for CID OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as CID.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.CID

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI text file to determine if it contains CID OUI entries.

        The method checks whether the file is a valid text file and contains specific patterns related to CID OUI ranges.
        If the file matches the expected CID format, it proceeds to parse the document; otherwise, it passes the request
        to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed CID-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.TXT and re.search(r'CID\s+Organization', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the CID OUI document, extracting key information such as MAC address ranges, company names,
        and physical addresses. The method uses regular expressions to locate and extract this data from the document,
        and formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed CID OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (CID).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s+(.*)?"  # Optional line 1 of address
            r"\s+(.*)?"  # Optional line 2 of address
            r"\s+(.*)?",  # Optional country
            re.MULTILINE
        )
        segments = [segment for segment in oui_doc.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(octet) for octet in oui_hex.split('-')]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company1.strip(),
                    f"{first_address}-{last_address}",
                    oui_hex,
                    address
                ))
        return result


#
class IabOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    A concrete implementation of the OUICsvFileParserHandler class, designed specifically to parse OUI data
    in CSV (.csv) format related to IAB (Individual Address Block) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from IAB-related
    OUI entries found in CSV files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUICsvFileParserHandler: Base class for handling CSV-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to IAB ranges.
        _oui_type (OUIType): Specifies the OUI type as IAB.
    """
    def __init__(self):
        """
        Initializes the IabOuiCsvFileParserHandler with a predefined OUI mask and OUI type for IAB ranges.

        The mask is tailored to handle IAB-specific MAC address blocks, which include 4 fully masked octets,
        1 partially masked octet, and 1 unmasked octet.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for IAB OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as IAB.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI CSV file to determine if it contains IAB OUI entries.

        This method checks whether the OUI file is a valid CSV file and contains IAB-specific information. If the file
        matches the expected IAB format, the method proceeds to parse the document; otherwise, it passes the request
        to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed IAB-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'IAB,[0-9A-F]{9}', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the IAB OUI CSV document, extracting details such as MAC address ranges, company names,
        and physical addresses. The method uses regular expressions to match and extract relevant data, then formats
        it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI CSV file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed IAB OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (IAB).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'IAB,([0-9A-F]{6})([0-9A-F]{3}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MasOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    A concrete implementation of the OUICsvFileParserHandler class, designed specifically to parse OUI data
    in CSV (.csv) format related to the MA-S (MAC Address Block Small) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-S-related
    OUI entries found in CSV files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUICsvFileParserHandler: Base class for handling CSV-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to MA-S ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-S.
    """
    def __init__(self):
        """
        Initializes the MasOuiCsvFileParserHandler with a predefined OUI mask and OUI type for MA-S ranges.

        The mask is specifically tailored to handle the MA-S (MAC Address Block Small) ranges, consisting of 4 fully masked
        octets, 1 partially masked octet, and 1 unmasked octet.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-S OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-S.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 4 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))]
        )
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI CSV file to determine if it contains MA-S OUI entries.

        This method checks whether the OUI file is a valid CSV file and contains specific patterns related to MA-S ranges.
        If the file matches the expected format for MA-S, it proceeds to parse the document; otherwise, it passes the
        request to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-S-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-S,[0-9A-F]{9}', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-S OUI CSV document, extracting key information such as MAC address ranges,
        company names, and physical addresses. The method uses regular expressions to match and extract relevant data,
        then formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI CSV file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-S OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-S).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-S,([0-9A-F]{6})([0-9A-F]{3}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MamOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    A concrete implementation of the OUICsvFileParserHandler class, specifically designed to parse OUI data
    in CSV (.csv) format related to the MA-M (MAC Address Block Medium) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-M-related
    OUI entries found in CSV files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUICsvFileParserHandler: Base class for handling CSV-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to MA-M ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-M.
    """
    def __init__(self):
        """
        Initializes the MamOuiCsvFileParserHandler with a predefined OUI mask and OUI type for MA-M ranges.

        The mask is specifically tailored to handle the MA-M (MAC Address Block Medium) ranges, consisting of 3 fully masked
        octets, 1 partially masked octet, and 2 unmasked octets, matching the structure of MA-M MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-M OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-M.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('F0'))] +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 2
        )
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI CSV file to determine if it contains MA-M OUI entries.

        This method checks whether the OUI file is a valid CSV file and contains specific patterns related to MA-M ranges.
        If the file matches the expected format for MA-M, it proceeds to parse the document; otherwise, it passes the
        request to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-M-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-M,[0-9A-F]{7}', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-M OUI CSV document, extracting key information such as MAC address ranges,
        company names, and physical addresses. The method uses regular expressions to match and extract relevant data,
        then formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI CSV file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-M OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-M).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-M,([0-9A-F]{6})([0-9A-F]{1}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, range_octets, company, address_line = match
                oui_hex = oui_hex.strip()
                range_octets = range_octets.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = range_octets.strip() + '00000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class MalOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    A concrete implementation of the OUICsvFileParserHandler class, designed specifically to parse OUI data
    in CSV (.csv) format related to the MA-L (MAC Address Block Large) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from MA-L-related
    OUI entries found in CSV files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUICsvFileParserHandler: Base class for handling CSV-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to MA-L ranges.
        _oui_type (OUIType): Specifies the OUI type as MA-L.
    """
    def __init__(self):
        """
        Initializes the MalOuiCsvFileParserHandler with a predefined OUI mask and OUI type for MA-L ranges.

        The mask is specifically tailored to handle the MA-L (MAC Address Block Large) ranges, consisting of 3 fully masked
        octets and 3 unmasked octets, matching the structure of MA-L MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for MA-L OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as MA-L.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.MA_L

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI CSV file to determine if it contains MA-L OUI entries.

        This method checks whether the OUI file is a valid CSV file and contains specific patterns related to MA-L ranges.
        If the file matches the expected format for MA-L, it proceeds to parse the document; otherwise, it passes the
        request to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed MA-L-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'MA-L,[0-9A-F]{6}', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the MA-L OUI CSV document, extracting key information such as MAC address ranges,
        company names, and physical addresses. The method uses regular expressions to match and extract relevant data,
        then formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI CSV file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed MA-L OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (MA-L).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'MA-L,([0-9A-F]{6}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company, address_line = match
                oui_hex = oui_hex.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))

        return result


class CidOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    A concrete implementation of the OUICsvFileParserHandler class, designed specifically to parse OUI data
    in CSV (.csv) format related to CID (Company Identifier) ranges.

    This class defines methods for handling, parsing, and extracting relevant information from CID-related
    OUI entries found in CSV files, such as MAC address ranges, company names, and physical addresses.

    Inherits from:
        OUICsvFileParserHandler: Base class for handling CSV-based OUI files.

    Properties:
        _mask (List[Octet]): Predefined OUI mask specific to CID ranges.
        _oui_type (OUIType): Specifies the OUI type as CID.
    """
    def __init__(self):
        """
        Initializes the CidOuiCsvFileParserHandler with a predefined OUI mask and OUI type for CID ranges.

        The mask is specifically tailored to handle the CID (Company Identifier) ranges, consisting of 3 fully masked
        octets and 3 unmasked octets, matching the structure of CID MAC address blocks.

        Properties:
            _mask (List[Octet]): A list of octets representing the mask for CID OUI ranges.
            _oui_type (OUIType): Specifies the OUI type as CID.
        """
        self._mask: List[Octet] = (
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('FF'))] * 3 +
                [OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary('00'))] * 3
        )
        self._oui_type = OUIType.CID

    def handle(self, oui_doc_path: str):
        """
        Handles the processing of the OUI CSV file to determine if it contains CID OUI entries.

        This method checks whether the OUI file is a valid CSV file and contains specific patterns related to CID ranges.
        If the file matches the expected format for CID, it proceeds to parse the document; otherwise, it passes the
        request to the next handler in the chain.

        Parameters:
            oui_doc_path (str): The file path of the OUI document to be processed.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing parsed CID-related OUI data if the document matches,
                                      otherwise passes the request to the next handler.
        """
        self._generate_file_information(oui_doc_path)
        if self._file.file_type == FileType.CSV and re.search(r'CID,[0-9A-F]{6}', self._file.file_content):
            return self._parse(self._file.file_content)
        else:
            return super().handle(oui_doc_path)

    def _parse(self, oui_doc: str) -> Dict[str, List[OUIUnit]]:
        """
        Parses the contents of the CID OUI CSV document, extracting key information such as MAC address ranges,
        company names, and physical addresses. The method uses regular expressions to match and extract relevant data,
        then formats it into a structured output.

        Parameters:
            oui_doc (str): The content of the OUI CSV file as a string.

        Returns:
            Dict[str, List[OUIUnit]]: A dictionary containing the parsed CID OUI data, including:
                                      - MD5 hash of the document.
                                      - Type of OUI (CID).
                                      - List of OUIUnit objects, each representing a parsed OUI entry.
        """
        hash_object = hashlib.md5()
        hash_object.update(oui_doc.encode('utf-8'))
        md5_hash = hash_object.hexdigest()
        result = {'md5': md5_hash, 'type': self._oui_type, 'oui_units': []}
        pattern = re.compile(r'CID,([0-9A-F]{6}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*)')
        segments = [segment for segment in oui_doc.split('\n') if segment.strip()]
        for segment in segments:
            matches = pattern.findall(segment)
            for match in matches:
                oui_hex, company, address_line = match
                oui_hex = oui_hex.strip()
                company = company.replace('"', '').strip()
                address_line = address_line.strip()
                start_hex = '000000'
                oui_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(oui_hex[octet_i: octet_i + 2]) for octet_i in range(0, len(oui_hex), 2)]
                start_hex_in_binaries = [NumeralConverter.hexadecimal_to_binary(start_hex[index: index + 2]) for index in range(0, len(start_hex), 2)]
                full_mac_binaries = [OctetFlyWeightFactory.get_octet(mac_octet) for mac_octet in oui_hex_in_binaries + start_hex_in_binaries]
                first_address, last_address = self._parse_mac_range(full_mac_binaries, self._mask)
                address = self._parse_physical_address(address_line)
                result['oui_units'].append(OUIUnit(
                    full_mac_binaries,
                    self._mask,
                    self._oui_type,
                    company.strip(),
                    f"{first_address}-{last_address}",
                    '-'.join(oui_hex[octet_i: octet_i + 2] for octet_i in range(0, len(oui_hex), 2)),
                    address
                ))
        return result


class OuiFileParser:
    """
    A parser class designed to facilitate the parsing of OUI files, supporting both .csv and .txt file formats.
    It uses a chain of responsibility pattern to delegate the parsing task to the appropriate handler based on the
    file type and content. The handlers are arranged to prioritize smaller OUI ranges first, ensuring that the masks
    are applied in the most specific order possible.

    Methods:
        parse_oui_file: Static method to parse the OUI file based on its extension and delegate to the correct parser handler.
    """

    @staticmethod
    def parse_oui_file(oui_file_path: str, parsers: List[OUIFileParserHandler] = None) -> Union[Dict, None]:
        """
        Parses the OUI file at the given path using an appropriate handler based on the file extension and the list of parser handlers provided.
        The parsing handlers are configured to check for smaller OUI ranges first, ensuring specificity in mask application.

        Parameters:
            oui_file_path (str): The file path of the OUI file to be parsed.
            parsers (list): A list of initialized parser handler objects that will be used to attempt parsing the OUI file.
                            This list should be ordered from the most specific to the least specific handler
                            in terms of the OUI range size they handle.

        Returns:
            Dict or None: Returns the parsing result if successful; otherwise, passes through exceptions for unsupported formats.

        Raises:
            ValueError: If the file extension is neither .csv nor .txt, indicating unsupported file format.
        """
        _, ext = os.path.splitext(oui_file_path)
        if ext.lower() not in ['.csv', '.txt']:
            raise ValueError(f"Only .csv and .txt files are supported by OUI file parsers.")
        if parsers is None:
            parsers = [
                IabOuiTxtFileParserHandler(),
                IabOuiCsvFileParserHandler(),
                MasOuiTxtFileParserHandler(),
                MasOuiCsvFileParserHandler(),
                MamOuiTxtFileParserHandler(),
                MamOuiCsvFileParserHandler(),
                MalOuiTxtFileParserHandler(),
                MalOuiCsvFileParserHandler(),
                CidOuiTxtFileParserHandler(),
                CidOuiCsvFileParserHandler(),
            ]
        parser_handler = parsers[0]
        for next_handler in parsers[1:]:
            parser_handler.set_next(next_handler)
            parser_handler = next_handler
        return parsers[0].handle(oui_file_path)


if __name__ == '__main__':
    # handler = IabOuiTxtFileParserHandler()
    # result = handler.handle('./resources/test_iab.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MasOuiTxtFileParserHandler()
    # result = handler.handle('./resources/test_mas.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MamOuiTxtFileParserHandler()
    # result = handler.handle('./resources/test_mam.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MalOuiTxtFileParserHandler()
    # result = handler.handle('./resources/test_mal.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = CidOuiTxtFileParserHandler()
    # result = handler.handle('./resources/test_cid.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = IabOuiCsvFileParserHandler()
    # result = handler.handle('./resources/test_iab.csv')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MasOuiCsvFileParserHandler()
    # result = handler.handle('./resources/test_mas.csv')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MamOuiCsvFileParserHandler()
    # result = handler.handle('./resources/test_mam.csv')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break
    #
    # handler = MalOuiCsvFileParserHandler()
    # result = handler.handle('./resources/test_mal.csv')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break

    # handler = CidOuiCsvFileParserHandler()
    # result = handler.handle('./resources/test_cid.csv')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break

    # result = OuiFileParser.parse_oui_file('./resources/default_mal.txt')
    # index = 0
    # if result is not None:
    #     for oui_unit in result['oui_units']:
    #         print(oui_unit.record)
    #         index += 1
    #         if index == 5:
    #             break

    print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_resources/'))
#
#
#
#
#
#
#
#
#
#
#
