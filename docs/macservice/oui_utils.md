# `oui_utils.py` Module Documentation

## Overview

The `oui_utils.py` module provides tools for managing and handling Organizationally Unique Identifiers (OUIs). It defines the types of OUIs and utilizes the flyweight design pattern to efficiently manage the creation of OUI instances. The module also provides a factory class for creating OUI objects, converting hexadecimal data to binary, and facilitating the creation of OUI units. The flyweight pattern ensures memory efficiency by sharing instances of the same OUI object.

## Classes

### 1. `OUIType`
- **Description**: An enumeration class that categorizes different types of OUIs.
  
- **Categories**:
  - `UNKNOWN`: Unidentified or unspecified OUI type.
  - `IAB`: Individual Address Block, typically used for smaller requirements.
  - `MA_S`: Standard MAC Address block size used by most organizations.
  - `MA_M`: Medium-sized MAC Address block for larger organizational needs.
  - `MA_L`: Large MAC Address block for extensive hardware requirements.
  - `CID`: Company ID, used for identifying specific organizations beyond the typical MAC address allocations.

---

### 2. `OUIUnit`
- **Description**: Represents an OUI unit used for identifying manufacturers or organizations by a unique MAC prefix. The `OUIUnit` class applies the flyweight design pattern to manage instances efficiently, ensuring identical OUIs are shared and not duplicated.

#### Key Attributes:
  - `_oui_units`: A class-level dictionary storing unique `OUIUnit` instances indexed by a tuple key.

#### Key Methods:

- **`__new__`**:
  - **Description**: Ensures that only one instance of `OUIUnit` is created for each unique combination of OUI ID, OUI mask, and OUI type. If an instance with the same key already exists, it returns the existing instance.
  - **Parameters**:
    - `oui_id (List[Octet])`: Binary representation of the OUI ID.
    - `oui_mask (List[Octet])`: Binary mask applied to the OUI.
    - `oui_type (OUIType)`: The type of the OUI.
    - `organization (Union[str, None])`: Organization associated with the OUI.
    - `mac_range (Union[str, None])`: MAC range associated with the OUI.
    - `oui_hex (Union[str, None])`: Hexadecimal representation of the OUI.
    - `address (Union[str, None])`: Organization's address.
  - **Returns**: 
    - `OUIUnit`: A new or existing instance of `OUIUnit`.

- **`oui_id_binary_digits`**:
  - **Description**: Returns the binary digits for the OUI's identifier.
  - **Returns**: A list of integers representing the binary digits of the OUI ID.

- **`oui_mask_binary_digits`**:
  - **Description**: Returns the binary digits for the OUI's mask.
  - **Returns**: A list of integers representing the binary digits of the OUI mask.

- **`record`**:
  - **Description**: Returns a dictionary containing the hexadecimal representation of the OUI details.
  - **Returns**: A dictionary with the following keys:
    - `oui_id`: Hexadecimal representation of the OUI ID.
    - `oui_mask`: Hexadecimal representation of the OUI mask.
    - `oui_type`: The type of OUI (`UNKNOWN`, `IAB`, `MA_S`, etc.).
    - `organization`: Name of the organization.
    - `mac_range`: The MAC range.
    - `oui_hex`: The hexadecimal OUI value.
    - `address`: The address of the organization.

---

### 3. `OUIUnitCreator`
- **Description**: A factory class for creating instances of `OUIUnit`. It processes the raw input, converts hexadecimal data to binary, and creates appropriate `OUIUnit` objects.

#### Key Methods:

- **`create_product`**:
  - **Description**: Creates a new instance of `OUIUnit` based on the provided arguments (e.g., OUI ID, OUI mask, OUI type, etc.).
  - **Parameters**:
    - `**kwargs`: Contains raw input such as `oui_id`, `oui_mask`, `oui_type`, etc., which are processed before creating the `OUIUnit`.
  - **Returns**:
    - `OUIUnit`: A new instance of `OUIUnit`.

#### Usage Example:
```python
from ttlinks.macservice.oui_utils import OUIUnitCreator

# Initialize the factory
oui_creator = OUIUnitCreator()

# Example input OUI data
input_data = {
    'oui_id': '00:1A:2B',
    'oui_mask': 'FF:FF:FF',
    'oui_type': 'MA_L',
    'organization': 'Example Corp',
    'mac_range': '00:1A:2B:00:00:00-00:1A:2B:FF:FF:FF',
    'oui_hex': '00-1A-2B',
    'address': '123 Example St, City, Country'
}

# Create OUIUnit instance
oui_unit = oui_creator.create_product(**input_data)

# Retrieve the OUIUnit's record
print(oui_unit.record)
```

Example output:
```json
{
  'oui_id': '00:1A:2B:00:00:00', 
  'oui_mask': 'FF:FF:FF:00:00:00', 
  'oui_type': 'MA_L', 
  'organization': 'Example Corp', 
  'mac_range': '00:1A:2B:00:00:00-00:1A:2B:FF:FF:FF', 
  'oui_hex': '00-1A-2B', 
  'address': '123 Example St, City, Country'
}
```

---

## Dependencies

- **ttlinks.common.binary_utils.binary**: Provides binary handling through the `Octet` class.
- **ttlinks.common.binary_utils.binary_factory**: Manages `Octet` instances with `OctetFlyWeightFactory`.
- **ttlinks.common.tools.converters**: Contains utilities like `NumeralConverter` for handling binary-to-hexadecimal conversions.
