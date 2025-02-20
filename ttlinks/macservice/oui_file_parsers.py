import csv
import io
import os
import re
from abc import abstractmethod, ABC
from typing import List, Dict, Union

from ttlinks.common.design_template.cor import BidirectionalCoRHandler
from ttlinks.files.file_classifiers import FileType
from ttlinks.files.file_utils import File
from ttlinks.macservice.oui_utils import OUIType, OUIUnit


class IEEEOuiTxtFile(File):
    """
    Represents an IEEE OUI text file.

    This class extends the File class and provides methods for validating
    and reading the content of a text-based OUI file.
    """
    def _validate(self):
        """Validates the file using the parent class's validation method."""
        super()._validate()

    def _read(self):
        """Reads the entire content of the text file and stores it."""
        self._file_content = open(self._file_path, self._read_method).read()


class IEEEOuiCsvFile(File):
    """
    Represents an IEEE OUI CSV file.

    This class extends the File class and provides methods for validating
    and reading the content of a CSV-based OUI file.
    """
    def _validate(self):
        """Validates the file using the parent class's validation method."""
        super()._validate()

    def _read(self):
        """Reads the entire content of the CSV file and stores it."""
        self._file_content = open(self._file_path, self._read_method).read()


class OUIFileParserHandler(BidirectionalCoRHandler):
    """
    Abstract handler class for parsing OUI files.

    Implements the Chain of Responsibility (CoR) pattern for handling
    different file formats and parsing strategies.
    """
    _oui_type: OUIType = OUIType.UNKNOWN

    @abstractmethod
    def __init__(self):
        """Abstract constructor."""
        pass

    @abstractmethod
    def handle(self, oui_doc: File, *args, **kwargs):
        """
        Handles the parsing of an OUI document.

        If the current handler cannot process the document, it passes it to the next handler in the chain.

        :param oui_doc: The OUI file object to be handled.
        :return: The result of the next handler or None.
        """
        if self._next_handler:
            return self._next_handler.handle(oui_doc, *args, **kwargs)
        return self._next_handler

    @abstractmethod
    def _parse(self, oui_doc: File):
        """
        Abstract method for parsing the OUI document.

        :param oui_doc: The OUI file to be parsed.
        """
        pass


class OUITxtFileParserHandler(OUIFileParserHandler, ABC):
    """
    Handles parsing of IEEE OUI text files.

    Extracts OUI, company details, and addresses using regex patterns.
    """
    def __init__(self):
        """
        Initializes the OUI text file parser with a predefined regex pattern
        for extracting OUI-related data.
        """
        self._oui_pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6}-\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s*(.*)?"  # Optional line 1 of address
            r"\s*(.*)?"  # Optional line 2 of address
            r"\s*(.*)?",  # Optional country
            re.MULTILINE
        )

    def _parse(self, oui_doc: IEEEOuiTxtFile) -> Dict[str, List[OUIUnit]]:
        """
        Parses an IEEE OUI text file and extracts relevant information.

        :param oui_doc: The IEEE OUI text file to parse.
        :return: A dictionary containing the parsed OUI data.
        """
        oui_type = self._oui_type
        result = {'md5': oui_doc.md5, 'type': oui_type, 'oui_units': []}
        segments = [segment for segment in oui_doc.file_content.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = self._oui_pattern.findall(segment)
            for match in matches:
                oui_hex, company1, mac_range, company2, address_line1, address_line2, country = match
                oui_id = oui_hex.replace('-', '')
                start_hex = mac_range[:mac_range.find('-')]
                end_hex = mac_range[mac_range.find('-') + 1:]
                block_size = self._oui_type.value['block_size']
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    oui_id,
                    start_hex,
                    end_hex,
                    block_size,
                    oui_type,
                    company1.strip() if company1 else '',
                    address
                ))
        return result

    def _parse_physical_address(self, address_line1: str, address_line2: str, country: str) -> str:
        """
        Formats a physical address from multiple address lines.

        :param address_line1: First line of the address.
        :param address_line2: Second line of the address.
        :param country: Country of the company.
        :return: A formatted string representing the full address.
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
    Handles parsing of IEEE OUI CSV files.

    Extracts OUI, company details, and addresses from structured CSV files.
    """
    def _parse(self, oui_doc: IEEEOuiCsvFile) -> Dict[str, List[OUIUnit]]:
        oui_type = self._oui_type
        block_size = self._oui_type.value['block_size']
        result = {'md5': oui_doc.md5, 'type': oui_type, 'oui_units': []}
        file_io = io.StringIO(oui_doc.file_content)
        reader = csv.reader(file_io)
        next(reader)
        for row in reader:
            assignment = row[1]
            oui_id = assignment[:6]
            start_hex = assignment[6:].ljust(6, '0')
            end_hex = assignment[6:].ljust(6, 'F')
            company = row[2]
            address = row[3]

            result['oui_units'].append(OUIUnit(
                oui_id,
                start_hex,
                end_hex,
                block_size,
                oui_type,
                company.strip(),
                address.strip()
            ))
        return result

    def _parse_physical_address(self, address_line: str) -> str:
        """
        Parses and formats a physical address from a single address line.

        :param address_line: The raw address line.
        :return: A formatted address string.
        """
        pass


class IabOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles parsing of IEEE IAB (Individual Address Block) OUI text files.

    Identifies the IAB range and extracts relevant OUI data.
    """
    def __init__(self):
        """Initializes the handler with the IAB OUI type."""
        super().__init__()
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc: IEEEOuiTxtFile, *args, **kwargs):
        """
        Processes an OUI text file to determine if it belongs to the IAB type.

        :param oui_doc: The IEEE OUI text file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.TXT and re.search(r'IAB Range\s+Organization', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MasOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles parsing of IEEE MA-S (Small MAC Address Block) OUI text files.

    Extracts OUI-36/MA-S range data from the text file.
    """
    def __init__(self):
        """Initializes the handler with the MA-S OUI type."""
        super().__init__()
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc: IEEEOuiTxtFile, *args, **kwargs):
        """
        Processes an OUI text file to determine if it belongs to the MA-S type.

        :param oui_doc: The IEEE OUI text file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.TXT and re.search(r'OUI-36/MA-S Range\s+Organization', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MamOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles parsing of IEEE MA-M (Medium MAC Address Block) OUI text files.

    Extracts OUI-28/MA-M range data from the text file.
    """

    def __init__(self):
        """Initializes the handler with the MA-M OUI type."""
        super().__init__()
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc: IEEEOuiTxtFile, *args, **kwargs):
        """
        Processes an OUI text file to determine if it belongs to the MA-M type.

        :param oui_doc: The IEEE OUI text file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.TXT and re.search(r'OUI-28/MA-M Range\s+Organization', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MalOuiTxtFileParserHandler(OUITxtFileParserHandler):
    """
    Handles parsing of IEEE MA-L (Large MAC Address Block) OUI text files.

    Extracts OUI/MA-L range data from the text file.
    """

    def __init__(self):
        """Initializes the handler with the MA-L OUI type and defines the regex pattern."""
        super().__init__()
        self._oui_type = OUIType.MA_L
        self._oui_pattern = re.compile(
            r"^(\S{2}-\S{2}-\S{2})\s+\(hex\)\s+(.*?)\s*\n"
            r"(\S{6})\s+\(base 16\)(.*)\n?"  # OUI and company name
            r"\s*(.*)?"  # Optional line 1 of address
            r"\s*(.*)?"  # Optional line 2 of address
            r"\s*(.*)?",  # Optional country
            re.MULTILINE
        )

    def handle(self, oui_doc: IEEEOuiTxtFile, *args, **kwargs):
        """
        Processes an OUI text file to determine if it belongs to the MA-L type.

        :param oui_doc: The IEEE OUI text file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.TXT and re.search(r'OUI/MA-L\s+Organization', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)

    def _parse(self, oui_doc: IEEEOuiTxtFile) -> Dict[str, List[OUIUnit]]:
        """
        Parses the MA-L OUI text file and extracts relevant information.

        :param oui_doc: The IEEE OUI text file.
        :return: A dictionary containing the parsed OUI data.
        """
        oui_type = self._oui_type
        result = {'md5': oui_doc.md5, 'type': oui_type, 'oui_units': []}
        segments = [segment for segment in oui_doc.file_content.split('\n\n') if segment.strip()]

        for segment in segments:
            matches = self._oui_pattern.findall(segment)
            for match in matches:
                oui_hex, company1, _, company2, address_line1, address_line2, country = match
                oui_id = oui_hex.replace('-', '')
                start_hex = '000000'
                end_hex = 'FFFFFF'
                block_size = self._oui_type.value['block_size']
                address = self._parse_physical_address(address_line1.strip(), address_line2.strip(), country.strip())
                result['oui_units'].append(OUIUnit(
                    oui_id,
                    start_hex,
                    end_hex,
                    block_size,
                    oui_type,
                    company1.strip() if company1 else '',
                    address
                ))
        return result


class CidOuiTxtFileParserHandler(MalOuiTxtFileParserHandler):
    """
    Handles parsing of CID (Company ID) OUI text files.

    CID is a special type of OUI assignment, handled similarly to MA-L.
    """

    def __init__(self):
        """Initializes the handler with the CID OUI type."""
        super().__init__()
        self._oui_type = OUIType.CID

    def handle(self, oui_doc: IEEEOuiTxtFile, *args, **kwargs):
        """
        Processes an OUI text file to determine if it belongs to the CID type.

        :param oui_doc: The IEEE OUI text file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.TXT and re.search(r'CID\s+Organization', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class IabOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles parsing of IEEE IAB (Individual Address Block) OUI CSV files.

    Identifies the IAB format and extracts relevant OUI data.
    """

    def __init__(self):
        """Initializes the handler with the IAB OUI type."""
        self._oui_type = OUIType.IAB

    def handle(self, oui_doc: IEEEOuiCsvFile, *args, **kwargs):
        """
        Processes an OUI CSV file to determine if it belongs to the IAB type.

        :param oui_doc: The IEEE OUI CSV file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.CSV and re.search(r'IAB,[0-9A-F]{9}', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MasOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles parsing of IEEE MA-S (Small MAC Address Block) OUI CSV files.

    Extracts OUI-36/MA-S range data from the CSV file.
    """
    def __init__(self):
        """Initializes the handler with the MA-S OUI type."""
        self._oui_type = OUIType.MA_S

    def handle(self, oui_doc: IEEEOuiCsvFile, *args, **kwargs):
        """
        Processes an OUI CSV file to determine if it belongs to the MA-S type.

        :param oui_doc: The IEEE OUI CSV file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.CSV and re.search(r'MA-S,[0-9A-F]{9}', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MamOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles parsing of IEEE MA-M (Medium MAC Address Block) OUI CSV files.

    Extracts OUI-28/MA-M range data from the CSV file.
    """

    def __init__(self):
        """Initializes the handler with the MA-M OUI type."""
        self._oui_type = OUIType.MA_M

    def handle(self, oui_doc: IEEEOuiCsvFile, *args, **kwargs):
        """
        Processes an OUI CSV file to determine if it belongs to the MA-M type.

        :param oui_doc: The IEEE OUI CSV file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.CSV and re.search(r'MA-M,[0-9A-F]{7}', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class MalOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles parsing of IEEE MA-L (Large MAC Address Block) OUI CSV files.

    Extracts OUI/MA-L range data from the CSV file.
    """
    def __init__(self):
        """Initializes the handler with the MA-L OUI type."""
        self._oui_type = OUIType.MA_L

    def handle(self, oui_doc: IEEEOuiCsvFile, *args, **kwargs):
        """
        Processes an OUI CSV file to determine if it belongs to the MA-L type.

        :param oui_doc: The IEEE OUI CSV file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.CSV and re.search(r'MA-L,[0-9A-F]{6}', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class CidOuiCsvFileParserHandler(OUICsvFileParserHandler):
    """
    Handles parsing of CID (Company ID) OUI CSV files.

    Extracts CID OUI range data from the CSV file.
    """

    def __init__(self):
        """Initializes the handler with the CID OUI type."""
        self._oui_type = OUIType.CID

    def handle(self, oui_doc: IEEEOuiCsvFile, *args, **kwargs):
        """
        Processes an OUI CSV file to determine if it belongs to the CID type.

        :param oui_doc: The IEEE OUI CSV file.
        :return: Parsed OUI data if the document matches, otherwise passes to the next handler.
        """
        if oui_doc.file_type == FileType.CSV and re.search(r'CID,[0-9A-F]{6}', oui_doc.file_content):
            return self._parse(oui_doc)
        else:
            return super().handle(oui_doc, *args, **kwargs)


class OuiFileParser:
    """
    OUI File Parser class that manages the parsing of IEEE OUI files.

    Uses a Chain of Responsibility pattern to apply different handlers
    based on the file type and format.
    """

    @staticmethod
    def parse_oui_file(oui_file: Union[IEEEOuiTxtFile, IEEEOuiCsvFile], parsers: List[OUIFileParserHandler] = None) -> Union[Dict, None]:
        """
        Parses an OUI file (TXT or CSV) using the appropriate parser handlers.

        :param oui_file: The IEEE OUI file to parse.
        :param parsers: Optional list of custom parser handlers.
        :return: Parsed OUI data as a dictionary, or None if parsing fails.
        :raises ValueError: If the file format is not supported.
        """
        _, ext = os.path.splitext(oui_file.file_path)
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
        return parsers[0].handle(oui_file)
