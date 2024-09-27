### `mac_address.py` Module Documentation

### Overview

The `mac_address.py` module provides a comprehensive solution for handling, validating, and classifying MAC (Media Access Control) addresses. It also provides functionalities to interact with the OUI (Organizationally Unique Identifier) database to determine the organization associated with the MAC address. This module implements the Chain of Responsibility (CoR) pattern for MAC address classification and offers utilities for MAC address conversion to binary formats and string representations.

### Key Components

1. **`InterfaceMACAddr` Class**:
   - An abstract base class defining the structure for handling MAC addresses, including validation, classification, and interaction with the OUI database.
   - **Key Methods**:
     - `_initialization(mac: List[Octet])`: Initializes and validates the MAC address.
     - `_validate(mac: List[Octet])`: Validates the MAC address and converts it into its binary form.
     - `_classify_mac_address()`: Classifies the MAC address as either unicast, multicast, or broadcast.
     - `_search_oui()`: Searches the local OUI database to find the OUI associated with the MAC address.
     - `binary_digits`: Returns the binary representation of the MAC address as a list of bits.
     - `binary_string`: Returns the binary representation of the MAC address as a binary string.
     - `__str__()`: Returns the MAC address in a human-readable hexadecimal format.

2. **`MACAddr` Class**:
   - A concrete implementation of the `InterfaceMACAddr` class, responsible for initializing, validating, classifying, and searching OUI information for a MAC address.
   - **Key Methods**:
     - `_initialization(mac: Any)`: Initializes the MAC address, classifies its type, and searches for OUI information.
     - `_validate(mac: Any)`: Converts the input MAC address to binary format and raises an error if invalid.
     - `_classify_mac_address()`: Classifies the MAC address using the `MACAddrClassifier`.
     - `_search_oui()`: Searches the OUI database for the organization associated with the MAC address.
     - `binary_digits`: Returns the binary representation of the MAC address as a list of bits.
     - `binary_string`: Returns the MAC address as a binary string.
     - `__str__()`: Returns the MAC address formatted as a colon-separated hexadecimal string (e.g., `AA:BB:CC:DD:EE:FF`).

### Example Usage

#### Example 1: Initialize and Classify a MAC Address
```python
from ttlinks.macservice.mac_address import MACAddr

mac_addr = MACAddr("b0-fc-0d-60-51-f8")
print(mac_addr)            # Human-readable format
print(mac_addr.mac_type)   # MAC Type (UNICAST, MULTICAST, or BROADCAST)
print(mac_addr.oui.record) # OUI record from the database
```

**Expected Output**:
```
B0:FC:0D:60:51:F8
MACType.UNICAST
[OUI Record Information]
```

#### Example 2: Convert MAC Address to Binary Formats
```python
from ttlinks.macservice.mac_address import MACAddr

mac_addr = MACAddr("60-57-c8-98-43-13")
print(mac_addr.binary_digits)  # List of binary digits
print(mac_addr.binary_string)  # Binary string representation
```

**Expected Output**:
```
[Binary Digits as List]
Binary String: "01100000010101111100100010011000010000110011"
```

### Dependencies

The module relies on several key components:
- **`ttlinks.common.binary_utils.binary.Octet`**: Represents an octet of a MAC address.
- **`ttlinks.common.tools.converters.NumeralConverter`**: Converts binary values into hexadecimal representations.
- **`ttlinks.macservice.mac_classifiers.MACAddrClassifier`**: Classifies MAC addresses as Unicast, Multicast, or Broadcast.
- **`ttlinks.macservice.mac_converters.MACConverter`**: Converts MAC addresses to and from different formats (e.g., hexadecimal, binary).
- **`ttlinks.macservice.oui_db.database.LocalOUIDatabase`**: Provides access to the local OUI database for retrieving OUI records.

### Conclusion

The `mac_address.py` module offers a robust solution for handling and processing MAC addresses, including classification and OUI lookup. With its clear structure and interface, the module is easily extendable and adaptable for various network applications, ensuring accurate MAC address handling and efficient lookups in the OUI database.