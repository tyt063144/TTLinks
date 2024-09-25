# `binary.py` Module Documentation

## Overview

This module provides an abstract class `Binary` and a concrete subclass `Octet`. These classes handle binary data representations, offering various methods to convert between binary, decimal, and hexadecimal formats. The `Binary` class defines the core behavior and abstract methods for validation, while the `Octet` class provides a concrete implementation specifically for 8-bit binary strings.

---

## Classes

### 1. `Binary`

#### Description
`Binary` is an abstract base class (ABC) designed for handling binary data representations. It provides fundamental operations such as binary-to-decimal and binary-to-hexadecimal conversions and includes an abstract method for validating binary strings.

#### Constructor
```python
def __init__(self, binary_string: str):
```
- **binary_string**: A string of binary digits ('0' and '1') to be processed.

#### Properties

- **`binary_digits`**:
    ```python
    @property
    def binary_digits() -> List[int]
    ```
    - Converts the binary string into a list of integers representing each binary digit.
    - **Returns**: A list of integers `[int]` representing the binary digits.

- **`binary_string`**:
    ```python
    @property
    def binary_string() -> str
    ```
    - Returns the binary string stored in the object.
    - **Returns**: A `str` containing the binary string.

- **`decimal`**:
    ```python
    @property
    def decimal() -> int
    ```
    - Converts the binary string to its decimal equivalent using the `NumeralConverter`.
    - **Returns**: An `int` representing the decimal value of the binary string.

- **`hex`**:
    ```python
    @property
    def hex() -> str
    ```
    - Converts the binary string to its hexadecimal equivalent using the `NumeralConverter`.
    - **Returns**: A `str` representing the hexadecimal value of the binary string.

#### Methods

- **`_initialization(binary_string: str)`**:
    Initializes the binary string after validating it.
    - **Args**: 
        - `binary_string` (`str`): The binary string to be validated and initialized.

- **`_validate(binary_string: str)`**:
    Abstract method that validates the binary string to ensure it contains only '0' or '1'. This method must be implemented by subclasses.
    - **Args**: 
        - `binary_string` (`str`): The binary string to validate.
    - **Raises**: 
        - `ValueError`: If the string contains invalid characters other than '0' or '1'.

- **`__str__()`**:
    Returns the binary string as a `str`.
    - **Returns**: A `str` representing the binary string.

- **`__repr__()`**:
    Returns a machine-readable string representation of the `Binary` instance.
    - **Returns**: A `str` showing the class name and the binary string.

---

### 2. `Octet` (Subclass of `Binary`)

#### Description
The `Octet` class represents an 8-bit binary string. It inherits from `Binary` and enforces additional validation to ensure that the binary string is exactly 8 bits long.

#### Methods

- **`_validate(binary_string: str)`**:
    Overrides the `_validate` method from the `Binary` class to ensure the binary string is exactly 8 bits long.
    - **Args**: 
        - `binary_string` (`str`): The binary string to validate.
    - **Raises**: 
        - `ValueError`: If the string is not exactly 8 characters long or contains invalid characters.

#### Example Usage

```python
from ttlinks.common.binary_utils.binary import Octet

# Create an Octet instance with a valid 8-bit binary string
octet = Octet("10101010")

# Access binary digits as a list of integers
print(octet.binary_digits)  # Output: [1, 0, 1, 0, 1, 0, 1, 0]

# Convert to decimal
print(octet.decimal)  # Output: 170

# Convert to hexadecimal
print(octet.hex)  # Output: 'AA'

# Attempt to create an Octet with an invalid length
try:
    invalid_octet = Octet("10101")  # Raises ValueError: An octet must be of length 8.
except ValueError as e:
    print(e)
```

---

## Dependencies

- **`NumeralConverter`**: A utility class for converting between binary, decimal, and hexadecimal representations. Make sure that it is imported from `ttlinks.common.tools.converters`.

---
