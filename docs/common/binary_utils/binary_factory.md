# `binary_factory.py` Module Documentation

## Overview

The `binary_factory.py` module provides an efficient mechanism for managing and reusing instances of binary data representations. It utilizes design patterns such as Singleton and Flyweight to optimize resource use by ensuring that each binary string (represented as an `Octet`) is created only once and reused when needed. Currently, the module contains the `OctetFlyWeightFactory` class, which is responsible for managing and caching these binary instances.

The primary focus of this module is to reduce memory overhead and improve performance when working with binary data by reusing objects rather than creating new ones for identical binary strings.

---

## Class

### 1. `OctetFlyWeightFactory`

#### Description
The `OctetFlyWeightFactory` class is responsible for creating and managing `Octet` instances. It ensures that only one instance of the factory exists (Singleton pattern) and that `Octet` instances are reused (Flyweight pattern). The factory maintains a pool of `Octet` instances, allowing for efficient handling of binary strings.

#### Methods

- **`__new__(cls)`**:
    - Ensures that only one instance of the factory exists.
    - **Returns**: The singleton instance of `OctetFlyWeightFactory`.

- **`get_octet(cls, binary_string: str) -> Octet`**:
    - Retrieves or creates an `Octet` for the given binary string. If the string is already cached, the existing instance is reused.
    - **Args**:
        - `binary_string` (`str`): The binary string to fetch or create.
    - **Returns**: The `Octet` instance corresponding to the binary string.

- **`get_flyweights(cls) -> Dict[str, Octet]`**:
    - Returns the current dictionary of `Octet` flyweights managed by the factory.
    - **Returns**: A `Dict[str, Octet]` containing binary strings as keys and `Octet` instances as values.

#### Example Usage

```python
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory

# Retrieve the factory instance
factory = OctetFlyWeightFactory()

# Get or create Octet instances
octet1 = factory.get_octet("11001010")
octet2 = factory.get_octet("10101010")
octet3 = factory.get_octet("11001010")  # Reuses the instance for "11001010"
print("Is octet1 is octet2: ", octet1 is octet2)
print("Is octet1 is octet3: ", octet1 is octet3)

# Access flyweights
flyweights = factory.get_flyweights()
print('flyweights', flyweights)  
```
Expected Output:
```
Is octet1 is octet2:  False
Is octet1 is octet3:  True
flyweights {'11001010': Octet(_binary_string=11001010), '10101010': Octet(_binary_string=10101010)}
```

---

## Design Patterns

- **Singleton**: Ensures that only one instance of the `OctetFlyWeightFactory` exists, promoting a single point of object management.
- **Flyweight**: Efficiently manages a pool of `Octet` instances to minimize memory usage by reusing instances for identical binary strings.

---

## Dependencies

- **`Octet`**: The factory relies on the `Octet` class (defined in the `binary_utils` module) to represent 8-bit binary strings.

---