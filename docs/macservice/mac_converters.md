# `mac_converters.py` Module Documentation

### Overview

The `mac_converters.py` module provides a comprehensive solution for converting and handling MAC addresses and OUI (Organizationally Unique Identifier) ranges. Using a Chain of Responsibility (CoR) pattern, it delegates the conversion of MAC addresses based on different formats (e.g., binary digits, dashed hexadecimal, colon-separated hexadecimal). The module supports conversions for both 48-bit MAC addresses and 24-bit OUI, along with an extension to convert MAC addresses into EUI-64 format.

### Key Components

1. **`MACConverterHandler` class**:  
   - The base handler class for MAC address conversion, employing the CoR pattern to pass requests along a chain of handlers.
   - Each subclass defines its specific method to convert different MAC address formats into octets.

2. **Subclasses of `MACConverterHandler`**:
   - **`OctetMAC48ConverterHandler`**: Converts MAC addresses represented as 6 octets.
   - **`BinaryDigitsMAC48ConverterHandler`**: Converts binary digits (48-bit) representing a MAC address into octets.
   - **`DashedHexMAC48ConverterHandler`**: Converts MAC addresses in a dashed hexadecimal format (e.g., `AA-BB-CC-DD-EE-FF`).
   - **`ColonHexMAC48ConverterHandler`**: Converts MAC addresses in colon-separated hexadecimal format (e.g., `AA:BB:CC:DD:EE:FF`).
   - **`DotHexMAC48ConverterHandler`**: Converts MAC addresses in dotted hexadecimal format (e.g., `AABB.CCDD.EEFF`).
   
   - **`OctetOUI24ConverterHandler`**: Converts OUI addresses represented as 3 octets and pads them to 48 bits if necessary.
   - **`BinaryDigitsOUI24ConverterHandler`**: Converts binary digits (24-bit) representing an OUI into octets, with optional padding to 48 bits.
   - **`DashedHexOUI24ConverterHandler`**: Converts OUI addresses in dashed hexadecimal format (e.g., `AA-BB-CC`) and pads them to 48 bits.
   - **`ColonHexOUI24ConverterHandler`**: Converts OUI addresses in colon-separated hexadecimal format (e.g., `AA:BB:CC`) and pads them to 48 bits.
   - **`DotHexOUI24ConverterHandler`**: Converts OUI addresses in dotted hexadecimal format (e.g., `AABB.CC`) and pads them to 48 bits.

   - **`OctetEUI64ConverterHandler`**: Converts MAC addresses into EUI-64 format by adding the `ff:fe` extension and flipping the universal/local bit.

3. **`MACConverter` class**:  
   - Provides static methods to convert MAC addresses and OUI ranges using a chain of handler classes.
   - **Key Methods**:
     - `convert_mac()`: Converts a MAC address based on a list of handlers.
     - `convert_oui()`: Converts OUI ranges into 48-bit MAC addresses.
     - `convert_to_eui64()`: Converts MAC addresses to EUI-64 format.

### Example Usage
This section demonstrates how to use the `mac_converters.py` module to convert MAC addresses and OUI ranges in various formats. Not all possible use cases are covered here, but these examples illustrate the flexibility and utility of the module.

### Example 1: Convert a MAC Address in Dashed Hexadecimal Format
```python
from ttlinks.macservice.mac_converters import MACConverter

# Dashed hexadecimal MAC address (e.g., AA-BB-CC-DD-EE-FF)
mac_address = "AA-BB-CC-DD-EE-FF"
converted_mac = MACConverter.convert_mac(mac_address)
print(':'.join([octet.hex for octet in converted_mac]))
```
Expected Output:
```
AA:BB:CC:DD:EE:FF
```

### Example 2: Convert a MAC Address in Colon Hexadecimal Format
```python
from ttlinks.macservice.mac_converters import MACConverter

# Colon-separated hexadecimal MAC address (e.g., AA:BB:CC:DD:EE:FF)
mac_address = "AA:BB:CC:DD:EE:FF"
converted_mac = MACConverter.convert_mac(mac_address)
print(':'.join([octet.hex for octet in converted_mac]))
```
Expected Output:
```
AA:BB:CC:DD:EE:FF
```

### Example 3: Convert a MAC Address in Dot Hexadecimal Format
```python
from ttlinks.macservice.mac_converters import MACConverter

# Dot-separated hexadecimal MAC address (e.g., AABB.CCDD.EEFF or AA.BB.CC.DD.EE.FF)
mac_address = "AABB.CCDD.EEFF"
converted_mac = MACConverter.convert_mac(mac_address)
print(':'.join([octet.hex for octet in converted_mac]))
```
Expected Output:
```
AA:BB:CC:DD:EE:FF
```

### Example 4: Convert a MAC Address from Binary Digits
```python
from ttlinks.macservice.mac_converters import MACConverter

# Binary MAC address (48-bit binary sequence representing the MAC)
binary_mac = [1, 0, 1, 0, 1, 0, 1, 0] * 6  # Example 48-bit binary MAC address
converted_mac = MACConverter.convert_mac(binary_mac)
print(':'.join([octet.hex for octet in converted_mac]))
```
Expected Output:
```
AA:AA:AA:AA:AA:AA
```

### Example 5: Convert a 24-bit OUI Address in Dashed Hexadecimal Format and Pad to 48 bits
```python
from ttlinks.macservice.mac_converters import MACConverter

# Dashed hexadecimal OUI address (e.g., AA-BB-CC)
oui_address = "AA-BB-CC"
converted_oui = MACConverter.convert_oui(oui_address)
print(':'.join([octet.hex for octet in converted_oui]))
```
Expected Output:
```
AA:BB:CC:00:00:00
```

### Example 6: Convert a 24-bit OUI Address from Binary Digits and Pad to 48 bits
```python
from ttlinks.macservice.mac_converters import MACConverter

# Binary OUI address (24-bit binary sequence representing the OUI)
binary_oui = [1, 0, 1, 0, 1, 0, 1, 0] * 3  # Example 24-bit binary OUI
converted_oui = MACConverter.convert_oui(binary_oui)
print(':'.join([octet.hex for octet in converted_oui]))
```
Expected Output:
```
AA:AA:AA:00:00:00
```

### Example 7: Convert a MAC Address to EUI-64 Format
```python
from ttlinks.macservice.mac_converters import MACConverter

# Example MAC address (e.g., AA-BB-CC-DD-EE-FF)
mac_address = "AA-BB-CC-DD-EE-FF"
eui64_mac = MACConverter.convert_to_eui64(mac_address)
print(':'.join([octet.hex for octet in eui64_mac]))
```
Expected Output:
```
A8:BB:CC:FF:FE:DD:EE:FF
```


### Dependencies

The module relies on several key components from the `ttlinks` package:
- **`ttlinks.common.binary_utils.binary`**: Provides the `Octet` class to handle individual octets of a MAC address.
- **`ttlinks.common.binary_utils.binary_factory`**: Manages `Octet` instances using the `OctetFlyWeightFactory`.
- **`ttlinks.common.design_template.cor`**: Implements the Chain of Responsibility pattern via the `SimpleCoRHandler` class.
- **`ttlinks.common.tools.converters`**: Contains the `NumeralConverter` class, which facilitates binary-to-hexadecimal conversions.

### Conclusion

The `mac_converters.py` module offers a flexible and extensible solution for handling MAC address and OUI range conversions using a well-structured Chain of Responsibility pattern. With its handler-based approach, the module can easily be extended to support additional MAC address formats, ensuring robust and dynamic MAC-to-octet conversion for a variety of use cases.