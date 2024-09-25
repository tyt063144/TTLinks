# `converters.py` Module Documentation

## Overview

The `converters.py` module currently provides a utility class, `NumeralConverter`, for converting between binary, decimal, and hexadecimal numeral systems. This module is designed to offer efficient and reliable numeral system conversions, and while it currently contains only the `NumeralConverter` class, it is structured to accommodate additional converters in the future.

The `NumeralConverter` class methods are static, making them easily accessible for converting between numeral systems without instantiating the class.

---

## Class

### 1. `NumeralConverter`

#### Description

The `NumeralConverter` class offers static methods for converting between binary, decimal, and hexadecimal numeral systems. While it is the only class in the module at present, more converters may be introduced in the future to handle additional formats or numeral systems.

#### Methods

- **`binary_to_decimal(binary_string: str) -> int`**:
    - Converts a binary string to its decimal (base-10) equivalent.
    - **Parameters**:
        - `binary_string` (`str`): The binary string to convert (e.g., "1010").
    - **Returns**: The decimal equivalent as an `int`.
    - **Raises**: 
        - `TypeError`: If the input is not a string.

- **`decimal_to_binary(decimal: int, r_just: int = 8) -> str`**:
    - Converts a decimal number to its binary string equivalent, with optional right-justified padding.
    - **Parameters**:
        - `decimal` (`int`): The decimal number to convert.
        - `r_just` (`int`): Optional padding to the right (default is 8).
    - **Returns**: The binary string as a `str`.
    - **Raises**: 
        - `TypeError`: If the inputs are not of the expected type.

- **`binary_to_hexadecimal(binary_string: str) -> str`**:
    - Converts a binary string to its hexadecimal equivalent.
    - **Parameters**:
        - `binary_string` (`str`): The binary string to convert.
    - **Returns**: The hexadecimal string as a `str`.
    - **Raises**: 
        - `TypeError`: If the input is not a string.

- **`hexadecimal_to_binary(hexadecimal: str, r_just: int = 8) -> str`**:
    - Converts a hexadecimal string to its binary string equivalent, with optional right-justified padding.
    - **Parameters**:
        - `hexadecimal` (`str`): The hexadecimal string to convert.
        - `r_just` (`int`): Optional padding to the right (default is 8).
    - **Returns**: The binary string as a `str`.
    - **Raises**: 
        - `TypeError`: If the inputs are not of the expected type.

- **`hexadecimal_to_decimal(hexadecimal: str) -> int`**:
    - Converts a hexadecimal string to its decimal equivalent.
    - **Parameters**:
        - `hexadecimal` (`str`): The hexadecimal string to convert.
    - **Returns**: The decimal equivalent as an `int`.
    - **Raises**: 
        - `TypeError`: If the input is not a string.

- **`decimal_to_hexadecimal(decimal: int, r_just: int = 2) -> str`**:
    - Converts a decimal number to its hexadecimal equivalent, with optional right-justified padding.
    - **Parameters**:
        - `decimal` (`int`): The decimal number to convert.
        - `r_just` (`int`): Optional padding to the right (default is 2).
    - **Returns**: The hexadecimal string as a `str`.
    - **Raises**: 
        - `TypeError`: If the inputs are not of the expected type.

#### Example Usage

```python
from ttlinks.common.tools.converters import NumeralConverter

# Convert binary to decimal
output1 = NumeralConverter.binary_to_decimal("101010")
print(f"binary 101010 is `{output1}` in decimal")

# Convert decimal to binary
output2 = NumeralConverter.decimal_to_binary(42)
print(f"decimal 42 is `{output2}` in binary")

# Convert binary to hexadecimal
output3 = NumeralConverter.binary_to_hexadecimal("101010")
print(f"binary 101010 is `{output3}` in hexadecimal")

# Convert hexadecimal to binary
output4 = NumeralConverter.hexadecimal_to_binary("2A") 
print(f"hexadecimal 2A is `{output4}` in binary")

# Convert hexadecimal to decimal
output5 = NumeralConverter.hexadecimal_to_decimal("2A") 
print(f"hexadecimal 2A is `{output5}` in decimal")

# Convert decimal to hexadecimal
output6 = NumeralConverter.decimal_to_hexadecimal(42) 
print(f"decimal 42 is `{output6}` in hexadecimal")
```
Expected Output:
```
binary 101010 is `42` in decimal
decimal 42 is `00101010` in binary
binary 101010 is `2A` in hexadecimal
hexadecimal 2A is `00101010` in binary
hexadecimal 2A is `42` in decimal
decimal 42 is `2A` in hexadecimal
```

---

## Design Patterns
- **Static Methods**: All methods are static, making them accessible without creating an instance of the class.

---
