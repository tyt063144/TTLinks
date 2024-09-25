# `ip_converters.py` Module Documentation

## Overview

The `ip_converters.py` module serves as a utility for converting IP address data between various formats (e.g., binary, dotted decimal, CIDR notation). It leverages the Chain of Responsibility design pattern to handle conversion requests efficiently and extendibly, making it suitable for both IPv4 and IPv6 addresses.

## Features

- **Flexible Conversion**: Handles various formats of IP addresses using a chain of handler classes.
- **Extensible Design**: Easily extendable to accommodate new IP address formats or custom conversion logic.
- **Comprehensive Handling**: Each handler is responsible for a specific format, ensuring precise and isolated handling of conversions.

---

## `IPConverter` Class

### Description

The `IPConverter` class provides static methods to convert IP addresses from various input formats (like binary digits, dotted decimal, or CIDR notation) into a list of octet objects. This conversion uses a chain of responsibility pattern, utilizing a series of `IPConverterHandler` instances to handle different formats for both IPv4 and IPv6 addresses. This setup allows for easy extension and customization of the conversion process.

### Methods

#### `convert_to_ipv4_octets`

- **Description**: Converts an IPv4 address from various formats into a list of octets using a predefined or custom sequence of converter handlers.
- **Parameters**:
  - `request_format (Any)`: The input representing an IPv4 address, which can be in different formats.
  - `converters (List[IPConverterHandler], optional)`: A list of converter handlers to apply during the conversion. If not provided, a default list is used.
- **Returns**:
  - `List[Octet]`: A list of octet objects representing the converted IPv4 address.
- **Example**:
```python
from ttlinks.ipservice.ip_converters import IPConverter
ip_address = '192.168.1.1'
octets = IPConverter.convert_to_ipv4_octets(ip_address)
print(octets)  # Output the list of octets
```

#### `convert_to_ipv6_octets`

- **Description**: Converts an IPv6 address from various formats into a list of octets, using a series of converter handlers.
- **Parameters**:
  - `request_format (Any)`: The input representing an IPv6 address, in different possible formats.
  - `converters (List[IPConverterHandler], optional)`: A list of converter handlers specific to IPv6 format handling. A default set is used if none provided.
- **Returns**:
  - `List[Octet]`: A list representing the IPv6 address in octet format.
- **Example**:
```python
from ttlinks.ipservice.ip_converters import IPConverter
ipv6_address = 'fe80::1'
octets = IPConverter.convert_to_ipv6_octets(ipv6_address)
print(octets)  # Display the list of octets
```

#### `convert_to_ip_octets`

- **Description**: Converts either an IPv4 or IPv6 address from various input formats to octets. It uses the appropriate handlers based on the IP type and format.
- **Parameters**:
  - `request_format (Any)`: The input representing either an IPv4 or IPv6 address in various formats.
  - `converters (List[IPConverterHandler], optional)`: A combined list of handlers for both IPv4 and IPv6 formats.
- **Returns**:
  - `List[Octet]`: A list of octets representing the converted IP address.
- **Example**:
```python
from ttlinks.ipservice.ip_converters import IPConverter
ip_address = '192.168.1.1'  # IPv4 example
# You could also try an IPv6 example like 'fe80::1'
octets = IPConverter.convert_to_ip_octets(ip_address)
print(octets)  # Print the resulting list of octets
```
---
## Abstract Classes

### 1. `IPConverterHandler`
#### Description

This abstract base class handles IP conversion requests within a chain-of-responsibility pattern. It provides a structured mechanism to pass requests down a chain of handlers, each designed to convert IP components into octets. If a handler cannot process the request, it passes the request to the next handler in the chain, if such a handler exists.

#### Inherits: `SimpleCoRHandler` from `ttlinks.common.design_template.cor`

This approach ensures that conversion responsibilities are modular and extendible, enabling precise and adaptable conversion processes for various IP formats in network applications.

---

## Concrete Classes
### 1. `OctetIPv4ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv4 addresses represented by exactly 4 octets. It inherits from `IPConverterHandler` and is a specific implementation within the chain of responsibility, designed to validate and convert IPv4 addresses into a standardized octet format.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it consists of exactly 4 octets representing an IPv4 address. If it does, it proceeds to convert the address. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list of octets representing an IP address.
  - **Returns**:
    - `List[Octet]`: A list of octets representing the IPv4 address if the request is valid, otherwise the result from the next handler.
  
- **_to_octets(request: List[Octet]) -> List[Octet]**: Converts the provided list of 4 octets into their desired octet format.
  - **Parameters**:
    - `request (List[Octet])`: A list of 4 octets representing the IPv4 address.
  - **Returns**:
    - `List[Octet]`: The same list of octets, assuming it is already in the correct format.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the OctetIPv4ConverterHandler
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_converters import OctetIPv4ConverterHandler

# Create an instance of the handler
ipv4_converter = OctetIPv4ConverterHandler()

# Define a request with exactly 4 octets
request_ipv4 = [
    OctetFlyWeightFactory.get_octet('11000000'),
    OctetFlyWeightFactory.get_octet('10101000'),
    OctetFlyWeightFactory.get_octet('00000001'),
    OctetFlyWeightFactory.get_octet('00000001')
]

# Convert the request
result = ipv4_converter.handle(request_ipv4)
print("Raw output:", result)
print("Converted octets:", '.'.join([str(octet.decimal) for octet in result]))
```
Expected Output:
```
Raw output: [Octet(_binary_string=11000000), Octet(_binary_string=10101000), Octet(_binary_string=00000001), Octet(_binary_string=00000001)]
Converted octets: 192.168.1.1
```


### 2. `BinaryDigitsIPv4ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv4 addresses represented by a list of 32 binary digits into octets. It inherits from `IPConverterHandler` and is part of the chain of responsibility, designed to handle and convert binary digit representations of IPv4 addresses.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it consists of a list of 32 binary digits representing an IPv4 address. If it does, it proceeds to convert these binary digits into octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list of 32 integers (0s and 1s) representing binary digits of an IPv4 address.
  - **Returns**:
    - `List[Octet]`: A list of octets if the request is valid; otherwise, the result from the next handler.
  
- **_to_octets(request: list[int]) -> List[Octet]**: Converts a list of 32 binary digits into a list of 4 octets by grouping every 8 bits. Each group of 8 bits is treated as a binary string and converted into an octet.
  - **Parameters**:
    - `request (list[int])`: A list of 32 integers representing binary digits of an IPv4 address.
  - **Returns**:
    - `List[Octet]`: A list of octet objects created from the binary digits.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the BinaryDigitsIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler

# Create an instance of the handler
binary_converter = BinaryDigitsIPv4ConverterHandler()

# Define a request with a list of 32 binary digits representing an IPv4 address
request_binary_ipv4 = [
    1, 1, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 0, 0, 0,
    1, 1, 1, 0, 0, 1, 0, 0,
    1, 1, 1, 0, 1, 0, 0, 1
]

# Convert the request
result = binary_converter.handle(request_binary_ipv4)
print("Raw output:", result)
print("Converted octets:", '.'.join([str(octet.decimal) for octet in result]))
```
Expected Output:
```
Raw output: [Octet(_binary_string=11000000), Octet(_binary_string=11001000), Octet(_binary_string=11100100), Octet(_binary_string=11101001)]
Converted octets: 192.200.228.233
```

### 3. `CIDRIPv4ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv4 addresses from CIDR notation into a subnet mask represented as octets. It inherits from `IPConverterHandler` and is an essential part of the chain of responsibility, designed to handle and convert CIDR formatted IPv4 addresses.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it is a CIDR string representing a subnet mask length for an IPv4 address. If it matches the CIDR format, it proceeds to convert this information into a subnet mask represented by octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a string in CIDR format (e.g., `/24`).
  - **Returns**:
    - `List[Octet]`: A list of octets representing the subnet mask if the request is valid; otherwise, the result from the next handler.
  
- **_to_octets(request: str) -> List[Octet]**: Converts a CIDR string into a subnet mask represented by octets. The method constructs a binary string with a number of '1's equal to the subnet part specified in the CIDR, followed by '0's to complete a set of 32 bits.
  - **Parameters**:
    - `request (str)`: A string in CIDR format (e.g., `/24`) representing the subnet mask length.
  - **Returns**:
    - `List[Octet]`: A list of octet objects representing the subnet mask.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the CIDRIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import CIDRIPv4ConverterHandler

# Create an instance of the handler
cidr_converter = CIDRIPv4ConverterHandler()

# Define a CIDR formatted request
request_cidr_ipv4 = '/24'

# Convert the request
result = cidr_converter.handle(request_cidr_ipv4)
print("Raw output:", result)
print("Converted subnet mask:", '.'.join([str(octet.decimal) for octet in result]))
```
Expected Output:
```
Raw output: [Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=00000000)]
Converted subnet mask: 255.255.255.0
```

### 4. `DotIPv4ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv4 addresses in dotted decimal notation into a list of octets. It inherits from `IPConverterHandler` and is a crucial component of the chain of responsibility, designed to handle and convert IPv4 addresses that are presented in the standard four-part dotted format.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it consists of a valid IPv4 address in dotted decimal format. If it does, it proceeds to convert the address into octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a string representing an IPv4 address in dotted decimal notation (e.g., `192.168.1.1`).
  - **Returns**:
    - `List[Octet]`: A list of octets representing the IPv4 address if the request is valid, otherwise the result from the next handler.
  
- **_to_octets(request: str) -> List[Octet]**: Converts an IPv4 address in dotted decimal notation into a list of octets. Each segment of the address is converted from its decimal form to binary, and then each binary string is converted into an octet.
  - **Parameters**:
    - `request (str)`: A string representing the IPv4 address in dotted decimal format.
  - **Returns**:
    - `List[Octet]`: The list of octets that represent the binary form of the IPv4 address.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the DotIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import DotIPv4ConverterHandler

# Create an instance of the handler
dot_ipv4_converter = DotIPv4ConverterHandler()

# Define a request with an IPv4 address in dotted decimal format
request_dot_ipv4 = '192.168.1.1'

# Convert the request
result = dot_ipv4_converter.handle(request_dot_ipv4)
print("Raw output:", result)
print("Converted octets:", '.'.join([octet.binary_string for octet in result]))
```
Expected Output:
```
Raw output: [Octet(_binary_string=11000000), Octet(_binary_string=10101000), Octet(_binary_string=00000001), Octet(_binary_string=00000001)]
Converted octets: 11000000.10101000.00000001.00000001
```

### 5. `OctetIPv6ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv6 addresses represented by exactly 16 octets. It inherits from `IPConverterHandler` and is an integral part of the chain of responsibility, designed to handle and convert IPv6 addresses that are presented in octet format. This handler verifies and directly returns the list of 16 octets as the output, assuming the input is already in the correct format.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it consists of exactly 16 octets representing an IPv6 address. If it does, it directly returns the list of octets without any further conversion. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list representing an IPv6 address in octet format.
  - **Returns**:
    - `List[Octet]`: The list of octets representing the IPv6 address if the request is valid, otherwise the result from the next handler.

- **_to_octets(request: Any) -> List[Octet]**: This method assumes the provided list of 16 octets is already formatted correctly for IPv6 and returns it directly. This is a straightforward operation as the conversion complexity is presumed to be handled prior to this stage.
  - **Parameters**:
    - `request (Any)`: A list of 16 octets representing the IPv6 address.
  - **Returns**:
    - `List[Octet]`: The same list of octets that was passed in.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the classification process to continue if this handler cannot definitively confirm the request as an IPv6 address.

#### Example Usage

```python
# Example showing how to use the OctetIPv6ConverterHandler
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_converters import OctetIPv6ConverterHandler

# Create an instance of the handler
ipv6_converter = OctetIPv6ConverterHandler()

# Define a request with exactly 16 octets representing an IPv6 address
request_ipv6 = [
    OctetFlyWeightFactory.get_octet('00000010'),  # Example octets
    OctetFlyWeightFactory.get_octet('01011110'),  # Placeholder values
    OctetFlyWeightFactory.get_octet('10011000'),  # for demonstration
] + [OctetFlyWeightFactory.get_octet('00000000')] * 13

# Convert the request
result = ipv6_converter.handle(request_ipv6)
print("Raw output:", result)
print("Converted octets:", [octet.hex for octet in result])
```
Expected Output:
```
Raw output: [Octet(_binary_string=00000010), Octet(_binary_string=01011110), Octet(_binary_string=10011000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000)]
Converted octets: ['02', '5E', '98', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
```

### 6. `BinaryDigitsIPv6ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv6 addresses represented by a list of 128 binary digits into octets. It inherits from `IPConverterHandler` and is an essential part of the chain of responsibility, designed to handle and convert binary digit representations of IPv6 addresses.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it consists of exactly 128 binary digits representing an IPv6 address. If it does, it proceeds to convert these binary digits into octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list of 128 integers (0s and 1s) representing binary digits of an IPv6 address.
  - **Returns**:
    - `List[Octet]`: A list of octets if the request is valid; otherwise, the result from the next handler.

- **_to_octets(request: list[int]) -> List[Octet]**: Converts a list of 128 binary digits into a list of 16 octets by grouping every 8 bits. Each group of 8 bits is treated as a binary string and converted into an octet using the `OctetFlyWeightFactory`.
  - **Parameters**:
    - `request (list[int])`: A list of 128 integers representing binary digits of an IPv6 address.
  - **Returns**:
    - `List[Octet]`: A list of octet objects created from the binary digits.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the BinaryDigitsIPv6ConverterHandler
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv6ConverterHandler

# Create an instance of the handler
binary_ipv6_converter = BinaryDigitsIPv6ConverterHandler()

# Define a request with a list of 128 binary digits representing an IPv6 address
request_binary_ipv6 = [
	1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
	1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0,
	1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0,
	1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1,
]

# Convert the request
result = binary_ipv6_converter.handle(request_binary_ipv6)
print("Raw output:", result)
print("Converted octets:", [octet.hex for octet in result])
```
Expected Output:
```
Raw output: [Octet(_binary_string=11000000), Octet(_binary_string=11000000), Octet(_binary_string=11000000), Octet(_binary_string=11000000), Octet(_binary_string=11001000), Octet(_binary_string=11001000), Octet(_binary_string=11001000), Octet(_binary_string=11001000), Octet(_binary_string=11100100), Octet(_binary_string=11100100), Octet(_binary_string=11100100), Octet(_binary_string=11100100), Octet(_binary_string=11101001), Octet(_binary_string=11101001), Octet(_binary_string=11101001), Octet(_binary_string=11101001)]
Converted octets: ['C0', 'C0', 'C0', 'C0', 'C8', 'C8', 'C8', 'C8', 'E4', 'E4', 'E4', 'E4', 'E9', 'E9', 'E9', 'E9']
```

### 7. `CIDRIPv6ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv6 addresses from CIDR notation into a subnet mask represented as octets. It inherits from `IPConverterHandler` and is crucial within the chain of responsibility, designed to handle and convert CIDR formatted IPv6 addresses.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it is a CIDR string representing a subnet mask length for an IPv6 address. If it matches the CIDR format, it proceeds to convert this information into a subnet mask represented by octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a string in CIDR format (e.g., `/64`).
  - **Returns**:
    - `List[Octet]`: A list of octets representing the subnet mask if the request is valid; otherwise, the result from the next handler.
  
- **_to_octets(request: str) -> List[Octet]**: Converts a CIDR string into a subnet mask represented by octets. The method constructs a binary string with a number of '1's equal to the subnet part specified in the CIDR, followed by '0's to complete a set of 128 bits.
  - **Parameters**:
    - `request (str)`: A string in CIDR format (e.g., `/64`) representing the subnet mask length.
  - **Returns**:
    - `List[Octet]`: A list of octet objects representing the subnet mask.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the CIDRIPv6ConverterHandler
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_converters import CIDRIPv6ConverterHandler

# Create an instance of the handler
cidr_ipv6_converter = CIDRIPv6ConverterHandler()

# Define a CIDR formatted request for an IPv6 address
request_cidr_ipv6 = '/64'

# Convert the request
result = cidr_ipv6_converter.handle(request_cidr_ipv6)
ipv6_hex_string = ''.join([octet.hex for octet in result])
print("Raw output:", result)
print("IPv6 hex string:", ipv6_hex_string)
print("Colon-hex format:", ':'.join([ipv6_hex_string[i:i + 4] for i in range(0, len(ipv6_hex_string), 4)]))
```
Expected Output:
```
Raw output: [Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=11111111), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000)]
IPv6 hex string: FFFFFFFFFFFFFFFF0000000000000000
Colon-hex format: FFFF:FFFF:FFFF:FFFF:0000:0000:0000:0000
```

### 8. `ColonIPv6ConverterHandler`
#### Description

This concrete handler class specializes in converting IPv6 addresses in colon-hexadecimal notation into a list of octets. It inherits from `IPConverterHandler` and is a critical component of the chain of responsibility, designed to handle and convert IPv6 addresses presented in the standard colon-separated format.

#### Inherits: `IPConverterHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it is a valid IPv6 address in colon-hexadecimal format. If valid, it proceeds to convert the address into octets. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a string representing an IPv6 address in colon-hexadecimal notation (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`).
  - **Returns**:
    - `List[Octet]`: A list of octets representing the IPv6 address if the request is valid, otherwise the result from the next handler.

- **_to_octets(request: str) -> List[Octet]**: Converts an IPv6 address in colon-hexadecimal notation into a list of octets. The method uses the `ipaddress` library to parse and expand the IPv6 address to ensure it is in full notation without abbreviations, and then converts each hexadecimal block into binary to form octets.
  - **Parameters**:
    - `request (str)`: A string representing the IPv6 address in colon-hexadecimal format.
  - **Returns**:
    - `List[Octet]`: The list of octets that represent the binary form of the IPv6 address.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the conversion process to continue if this handler cannot definitively convert the request.

#### Example Usage

```python
# Example showing how to use the ColonIPv6ConverterHandler
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_converters import ColonIPv6ConverterHandler

# Create an instance of the handler
colon_ipv6_converter = ColonIPv6ConverterHandler()

# Define a request with an IPv6 address in colon-hexadecimal format
request_colon_ipv6 = '2001:0db8:85a3::8a2e:0370:7334'

# Convert the request
result = colon_ipv6_converter.handle(request_colon_ipv6)
print("Raw output:", result)
print("Converted octets:", [octet.hex for octet in result])
```
Expected Output:
```
Raw output: [Octet(_binary_string=00100000), Octet(_binary_string=00000001), Octet(_binary_string=00001101), Octet(_binary_string=10111000), Octet(_binary_string=10000101), Octet(_binary_string=10100011), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=00000000), Octet(_binary_string=10001010), Octet(_binary_string=00101110), Octet(_binary_string=00000011), Octet(_binary_string=01110000), Octet(_binary_string=01110011), Octet(_binary_string=00110100)]
Converted octets: ['20', '01', '0D', 'B8', '85', 'A3', '00', '00', '00', '00', '8A', '2E', '03', '70', '73', '34']
```


---
## Dependencies

List and describe the external libraries and modules the `ip_converters.py` module depends on:
- `ipaddress`: For handling and validating IP addresses.
- `re`: For regular expression operations, particularly in validating and parsing IP formats.
- Other internal dependencies within the `ttlinks` package.
