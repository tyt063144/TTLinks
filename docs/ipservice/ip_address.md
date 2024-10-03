Based on the content of the `ip_address.py` module you uploaded, here's a Markdown documentation template:

# `ip_address.py` Module Documentation

## Overview
The `ip_address.py` module provides a comprehensive framework for representing and handling IP addresses, including IPv4 and IPv6, along with their associated netmasks and wildcard masks. This module utilizes abstract and concrete classes to enforce structure and ensure that all IP address types adhere to valid formats and operations.

## Features

- **IP Address Validation**: Ensures that the input strings or other formats are valid IP addresses, raising exceptions for invalid inputs.
- **Binary Conversion**: Converts IP addresses to binary octet formats, providing both string and digit representations.
- **String Representation**: Supports user-friendly string outputs for IP addresses in conventional notations (dotted decimal for IPv4 and colon-hexadecimal for IPv6).
- **Mask Size Calculation**: Calculates the size of network masks and wildcard masks to determine the scope of networks or ranges.

---

## Abstract Classes

### 1. `IPAddr`
#### Description

The `IPAddr` class is an abstract base class designed to outline the fundamental structure and functionality for IP address representations. It enforces the implementation of essential methods such as validation, binary conversion, and user-friendly string representations across derived classes.

#### Inherits: None

This class serves as a template for creating specific IP address types (e.g., IPv4, IPv6), ensuring that all derived classes adhere to a consistent interface and behavior, crucial for reliable IP address manipulation in networking applications.

### 2. `IPNetMask`
#### Description

`IPNetMask` is an abstract base class that extends `IPAddr` to specifically handle network masks associated with IP addresses. It adds the requirement for methods that manage and calculate the size of network masks, thus differentiating the handling of full IP addresses from their subnet mask components.

#### Inherits: `IPAddr`

This abstraction allows for the specialized handling of network masks, segregating it from general IP address functionalities and focusing on aspects relevant to subnetting and network design.

---

## Concrete Classes
### 1. `IPv4Addr`
#### Description

The `IPv4Addr` class is a concrete implementation of the `IPAddr` abstract base class, specifically tailored for handling IPv4 addresses. It includes functionality for validating IPv4 addresses, converting them to binary formats, and representing them in both human-readable and official string forms.

#### Inherits: `IPAddr`

#### Methods

- **_validate(address: Any) -> None**:
  Ensures that the provided address is a valid IPv4 address by checking its format and converting it into a list of octets. If the address is invalid, it raises a `ValueError`.
  - **Parameters**:
    - `address (Any)`: The IPv4 address to be validated, in string or other format.
  - **Raises**:
    - `ValueError`: If the provided address is not a valid IPv4 address.

- **binary_digits -> Iterable[int]**:
  Returns the binary digits of the IPv4 address by converting each octet to binary and yielding the individual bits.
  - **Returns**:
    - `Iterable[int]`: A generator yielding the binary digits of the IPv4 address.

- **binary_string -> str**:
  Constructs and returns the binary representation of the IPv4 address as a string by concatenating the binary strings of each octet.
  - **Returns**:
    - `str`: A string representation of the IPv4 address in binary form.
    
- **decimal -> int**:
    Returns the decimal representation of the IPv4 address as an integer.
    - **Returns**:
        - `int`: The IPv4 address as an integer.
    
- **__str__() -> str**:
  Provides a human-readable string representation of the IPv4 address using the standard dotted decimal notation.
  - **Returns**:
    - `str`: The IPv4 address as a string in dotted decimal format.

- **__repr__() -> str**:
  Provides the official string representation of the IPv4 address, used primarily for debugging purposes.
  - **Returns**:
    - `str`: The internal representation of the IPv4 address.

#### Example Usage

```python
# Example showing how to use the IPv4Addr class
from ttlinks.ipservice.ip_address import IPv4Addr
ipv4 = IPv4Addr("192.168.1.1")
print(ipv4)
print(repr(ipv4))
print(ipv4.binary_string)
print(list(ipv4.binary_digits))
print(ipv4.decimal)
```
Expected Output:
```
192.168.1.1
IPv4Addr('_address=[Octet(_binary_string=11000000), Octet(_binary_string=10101000), Octet(_binary_string=00000001), Octet(_binary_string=00000001)])
11000000101010000000000100000001
[1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
3232235777
```

### 2. `IPv6Addr`
#### Description

The `IPv6Addr` class implements the `IPAddr` abstract base class, focusing on the management and manipulation of IPv6 addresses. This class handles the validation, binary conversion, and representation of IPv6 addresses, ensuring compliance with IPv6 standards and providing tools for effective networking operations.

#### Inherits: `IPAddr`

#### Methods

- **_validate(address: Any) -> None**:
  Validates a given IPv6 address to check its correctness and formats it into a structured octet list. If the input is not a valid IPv6 address, it throws a `ValueError`.
  - **Parameters**:
    - `address (Any)`: The IPv6 address to be validated, typically in a string format.
  - **Raises**:
    - `ValueError`: If the address fails validation checks, indicating it is not a valid IPv6 address.

- **binary_digits -> Iterable[int]**:
  Generates the binary digits of the IPv6 address. This method iterates through each octet, converting it to binary, and yields individual bits.
  - **Returns**:
    - `Iterable[int]`: A sequence of integers representing the binary digits of the IPv6 address.

- **binary_string -> str**:
  Constructs a binary string representation of the IPv6 address by concatenating the binary forms of each octet.
  - **Returns**:
    - `str`: The binary string representation of the IPv6 address.

- **decimal -> int**:
    Returns the decimal representation of the IPv6 address as an integer.
    - **Returns**:
        - `int`: The IPv6 address as an integer.

- **__str__() -> str**:
  Converts the IPv6 address into a human-readable string using the standard colon-separated hexadecimal format.
  - **Returns**:
    - `str`: The IPv6 address in colon-separated hexadecimal format.

- **__repr__() -> str**:
  Provides a detailed string representation of the IPv6 address for debugging purposes.
  - **Returns**:
    - `str`: An internal representation detailing the IPv6 address.

#### Example Usage

```python
# Demonstrating the use of the IPv6Addr class
from ttlinks.ipservice.ip_address import IPv6Addr
ipv6 = IPv6Addr("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
print(ipv6)
print(repr(ipv6))
print(ipv6.binary_string)
print(list(ipv6.binary_digits))
print(ipv6.decimal)
```
Expected Output:
```
2001:db8:85a3::8a2e:370:7334
IPv6Addr('_address=[Octet(_binary_string=00100000), Octet(_binary_string=00000001), Octet(_binary_string=00001101), Octet(_binary_string=10111000), Octet(_binary_string=10000101), Octet(_binary_string=10100011), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=10001010), Octet(_binary_string=00101110), Octet(_binary_string=00000011), Octet(_binary_string=01110000), Octet(_binary_string=01110011), Octet(_binary_string=00110100)])
00100000000000010000110110111000100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110100
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
42540766452641154071740215577757643572
```

### 3. `IPv4NetMask`
#### Description

The `IPv4NetMask` class extends both the `IPNetMask` and `IPv4Addr` classes, specializing in handling network masks specifically for IPv4 addresses. This class is crucial for managing network boundaries in IPv4-based networks, providing functionalities for validating network masks and calculating their sizes.

#### Inherits: `IPNetMask`, `IPv4Addr`

#### Methods

- **_validate(address: Any) -> None**:
  Validates the given IPv4 network mask to ensure it adheres to acceptable standards. If the mask is invalid, a `ValueError` is raised.
  - **Parameters**:
    - `address (Any)`: The IPv4 network mask to validate, which can be in CIDR notation or dotted decimal format.
  - **Raises**:
    - `ValueError`: Triggered if the network mask is not a valid IPv4 mask.

- **get_mask_size() -> int**:
  Calculates the size of the network mask by counting the number of '1' bits in its binary representation. This size corresponds to the number of bits used for the network part of an address in CIDR notation.
  - **Returns**:
    - `int`: The size of the network mask, indicating the number of bits that define the network portion of an address.

- **binary_string -> str**:
  Returns a string representation of the binary format of the network mask, allowing for easy interpretation of network boundaries.
  - **Returns**:
    - `str`: The binary representation of the IPv4 network mask.

#### Example Usage

```python
# Example demonstrating how to use the IPv4NetMask class
from ttlinks.ipservice.ip_address import IPv4NetMask
ipv4_netmask = IPv4NetMask("/24")  # Also works with 255.255.255.0
print(ipv4_netmask)
print(repr(ipv4_netmask))
print(ipv4_netmask.get_mask_size())
print(ipv4_netmask.binary_string)
print(list(ipv4_netmask.binary_digits))
```
Expected Output:
```
255.255.255.0
IPv4NetMask('_address=[Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=00000000)])
24
11111111111111111111111100000000
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
```

### 4. `IPv4WildCard`
#### Description

The `IPv4WildCard` class is a specialized version of the `IPv4NetMask` class, designed to handle IPv4 wildcard masks. Wildcard masks are used in networking to specify ranges of IP addresses, particularly for access control lists and routing protocols. This class provides functionality for validating wildcard masks and calculating the number of possible IP addresses they can represent based on their binary structure.

#### Inherits: `IPv4NetMask`

#### Methods

- **_validate(address: Any) -> None**:
  Ensures that the provided address is a valid IPv4 wildcard mask. If the mask is not valid, it raises a `ValueError`.
  - **Parameters**:
    - `address (Any)`: The wildcard mask to be validated, typically provided in dotted decimal format.
  - **Raises**:
    - `ValueError`: If the address is not a valid IPv4 wildcard mask.

- **get_mask_size() -> int**:
  Calculates the potential size of the IP address range that the wildcard mask can cover. This is determined by counting the number of '1' bits in the binary representation of the mask, which are considered "don't care" bits allowing flexibility in the IP addresses.
  - **Returns**:
    - `int`: The number of possible IP addresses that can be represented by the wildcard mask.

- **binary_string -> str**:
  Generates the binary string representation of the wildcard mask, which is useful for understanding the mask's impact on IP address filtering and matching.
  - **Returns**:
    - `str`: The binary representation of the IPv4 wildcard mask.

#### Example Usage

```python
# Example demonstrating how to use the IPv4WildCard class
from ttlinks.ipservice.ip_address import IPv4WildCard
ipv4_wildcard = IPv4WildCard("0.255.0.255")
print(ipv4_wildcard)
print(repr(ipv4_wildcard))
print(ipv4_wildcard.get_mask_size())
print(ipv4_wildcard.binary_string)
print(ipv4_wildcard.binary_digits)
```
Expected Output:
```
0.255.0.255
IPv4WildCard('_address=[Octet(_binary_string=00000000), Octet(_binary_string=11111111), Octet(_binary_string=00000000), Octet(_binary_string=11111111)])
65536
00000000111111110000000011111111
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
```

### 5. `IPv6NetMask`
#### Description

The `IPv6NetMask` class extends both the `IPNetMask` and `IPv6Addr` classes to specifically handle network masks for IPv6 addresses. This class is crucial for managing network boundaries in IPv6-based networks, offering functionalities to validate network masks and compute their sizes in terms of the number of network bits.

#### Inherits: `IPNetMask`, `IPv6Addr`

#### Methods

- **_validate(address: Any) -> None**:
  Validates the provided IPv6 network mask to ensure it adheres to acceptable IPv6 netmask standards. If the mask is invalid, a `ValueError` is raised.
  - **Parameters**:
    - `address (Any)`: The IPv6 network mask to validate, which can be in CIDR notation or full IPv6 format.
  - **Raises**:
    - `ValueError`: Triggered if the network mask is not a valid IPv6 mask.

- **get_mask_size() -> int**:
  Calculates the size of the IPv6 network mask by counting the number of '1' bits in its binary representation. This measurement is crucial for determining the network portion of an IPv6 address.
  - **Returns**:
    - `int`: The size of the network mask, indicating the number of bits that define the network portion of an address in CIDR notation.

- **binary_string -> str**:
  Provides a binary string representation of the IPv6 network mask, facilitating a clear understanding of network segmentation and boundary definition.
  - **Returns**:
    - `str`: The binary string representation of the IPv6 network mask.

#### Example Usage

```python
# Example showing how to use the IPv6NetMask class
from ttlinks.ipservice.ip_address import IPv6NetMask
ipv6_netmask = IPv6NetMask("ffff:f000::")  # Also works with CIDR notation
print(ipv6_netmask)
print(ipv6_netmask.get_mask_size())
print(repr(ipv6_netmask))
print(ipv6_netmask.binary_string)
print(list(ipv6_netmask.binary_digits))
```
Expected Output:
```
ffff:f000::
20
IPv6NetMask('_address=[Octet(_binary_string=11111111), Octet(_binary_string=11111111), ...])
11111111111111111111000000000000000...
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, ...]
```

### 6. `IPv6WildCard`
#### Description

The `IPv6WildCard` class is an extension of the `IPv6NetMask` class, designed specifically to handle wildcard masks for IPv6 addresses. Wildcard masks are used in networking to specify ranges of IP addresses, particularly for matching purposes in network configurations such as routing and security. This class facilitates the validation of wildcard masks and calculates the potential size of the address range they cover.

#### Inherits: `IPv6NetMask`

#### Methods

- **_validate(address: Any) -> None**:
  Validates the given IPv6 wildcard mask to ensure it adheres to expected formats. If the mask is not valid, it raises a `ValueError`.
  - **Parameters**:
    - `address (Any)`: The IPv6 wildcard mask to be validated, typically provided in colon-separated hexadecimal format.
  - **Raises**:
    - `ValueError`: If the address is not a valid IPv6 wildcard mask.

- **get_mask_size() -> int**:
  Calculates the size of the IP address range that the wildcard mask can potentially cover by counting the number of '1' bits in its binary representation, which represent "don't care" positions.
  - **Returns**:
    - `int`: The number of possible IP addresses that can be represented by the wildcard mask.

- **binary_string -> str**:
  Generates the binary string representation of the wildcard mask, which is essential for understanding the flexibility and range of IP address matching it allows.
  - **Returns**:
    - `str`: The binary representation of the IPv6 wildcard mask.

#### Example Usage

```python
# Demonstrating how to use the IPv6WildCard class
from ttlinks.ipservice.ip_address import IPv6WildCard
ipv6_wildcard = IPv6WildCard("ffff:f000::AB")
print(ipv6_wildcard)
print(repr(ipv6_wildcard))
print(ipv6_wildcard.get_mask_size())
print(ipv6_wildcard.binary_string)
print(list(ipv6_wildcard.binary_digits))
```
Expected Output:
```
ffff:f000::ab
IPv6WildCard('_address=[Octet(_binary_string=11111111), Octet(_binary_string=11111111), ...])
33554432
11111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010101011
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
```

---
## Dependencies

The module depends on several external libraries and modules:
- `ipaddress`: Used for IP address manipulation and validation.
- `ttlinks.common.binary_utils.binary`: Provides utilities for binary operations.
- `ttlinks.ipservice.ip_converters`: Converts IP addresses into binary and other formats.
- `ttlinks.ipservice.ip_type_classifiers`: Classifies strings and other inputs as specific IP address types.
