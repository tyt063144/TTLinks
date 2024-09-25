
# `oui_file_parsers.py` Module Documentation

## Overview

The `oui_file_parsers.py` module handles the parsing of OUI (Organizationally Unique Identifier) files. It uses the Chain of Responsibility (CoR) pattern to delegate tasks to different handlers depending on the type and format of the OUI file. The module provides support for both text and CSV formats.
OUI files can be obtained from the official IEEE Standards <a href='https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries'>website</a>, where organizational information is published.

## Classes

### 1. `IEEEOuiFile`
- **Description**: A concrete implementation of the `File` abstract class, specifically designed to handle IEEE OUI files. This class reads and validates the content of an OUI file.
- **Key Methods**:
  - `_read`: Reads the file content.
  - `_validate`: Validates the OUI file.

### 2. `OUIFileParserHandler`
- Abstract base class for parsing OUI files.
- Key attributes: `_file`, `_mask`, `_oui_type`
- Implements Chain of Responsibility pattern with `handle()` and `parse()` methods.

#### Derived Handler Classes
- `IabOuiTxtFileParserHandler`
- `IabOuiCsvFileParserHandler`
- `MasOuiTxtFileParserHandler`
- `MasOuiCsvFileParserHandler`
- `MamOuiTxtFileParserHandler`
- `MamOuiCsvFileParserHandler`
- `MalOuiTxtFileParserHandler`
- `MalOuiCsvFileParserHandler`
- `CidOuiTxtFileParserHandler`
- `CidOuiCsvFileParserHandler`

These classes are specialized handlers for different OUI file types and ranges (IAB, CID, MA-S, MA-M, MA-L) in either text or CSV formats. They parse OUI data, including MAC address ranges and vendor information.

### 3. `OuiFileParser`
- **Description**: The main utility class designed to manage the parsing of OUI files by selecting the appropriate handler based on the file type (text or CSV). The class allows the parsing of different OUI formats in a unified interface.
  
- **Key Methods**:
  - `parse_oui_file(oui_file_path: str, parsers: List[OUIFileParserHandler] = None) -> Union[Dict, None]`: 
    - This static method parses the OUI file at the given path using a list of handler classes. The method determines the file type and selects the appropriate handler from the list.
    - **Parameters**:
      - `oui_file_path`: The path to the OUI file to be parsed.
      - `parsers`: A list of initialized parser handler objects.
    - **Returns**: A dictionary containing the parsed OUI data or `None` if the file format is unsupported.
  
- **Usage Example**:
```python
from ttlinks.macservice.oui_file_parsers import OuiFileParser
# Parse an OUI file (either .txt or .csv)
result = OuiFileParser.parse_oui_file('./path_to_oui_file.csv')
print(result['oui_units'][0])
```
Example output:
```
{'oui_id': '08:EA:44:00:00:00', 'oui_mask': 'FF:FF:FF:00:00:00', 'oui_type': 'MA_L', 'organization': 'Extreme Networks Headquarters', 'mac_range': '08:EA:44:00:00:00-08:EA:44:FF:FF:FF', 'oui_hex': '08-EA-44', 'address': '2121 RDU Center Drive, Morrisville, NC 27560, US'}
```

## Dependencies

- **ttlinks.Files.file_classifiers**: Used for determining the file type.
- **ttlinks.common.binary_utils.binary**: Provides binary handling through the `Octet` class.
- **ttlinks.common.binary_utils.binary_factory**: Manages `Octet` instances with `OctetFlyWeightFactory`.
- **ttlinks.common.tools.converters**: Contains utilities like `NumeralConverter` for handling binary-to-hexadecimal conversions.

## Conclusion

The `oui_file_parsers.py` module provides a robust solution for parsing OUI files in both text and CSV formats, supporting various MAC address blocks (IAB, MA-S, MA-M, MA-L, CID). The `OuiFileParser` class simplifies the usage by dynamically selecting the correct handler for each file type.

---
