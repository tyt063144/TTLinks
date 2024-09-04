# TTLLinks IP and MAC Address Management and Conversion Toolkit
## Overview
This project provides a comprehensive toolkit for managing, validating, and converting IP addresses in both IPv4 and IPv6 formats, with planned support for MAC address management. Leveraging design patterns such as Chain of Responsibility and Flyweight, this toolkit ensures efficient and flexible handling of IP and MAC-related operations. The modular design allows for easy integration and extension within larger networking and automation systems.

## Installation
This project is available on PyPI and can be installed using pip:
```bash
pip install ttlinks
```

## Usage
After installation, you can import the necessary classes and utilities from the ttlinks package, for examples:
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr, IPv4NetMask, IPv6NetMask
from ttlinks.ipservice.converters import NumeralConverter
from ttlinks.ipservice.ip_utils import NetToolsSuite, IPType
# ...more
```

## Features

---

### 1. COMMON
- [Common](docs/common.md)
Here’s a concise description for `common.py`:

#### 1.1. Overview of `common.py`

The `common.py` module is a foundational part of the IP and MAC address management toolkit, providing essential utilities for handling binary data and enabling flexible request processing.

#### 1.2. Key Components

 - 1.2.1. **`BinaryClass`**:
   - Manages and validates binary strings, ensuring they contain only '0's and '1's.
   - Converts binary strings into lists of integers for easier manipulation.
   - Used as a foundational element across IP and MAC address operations.

 - 1.2.2. **`CoRHandler`**:
   - Implements the Chain of Responsibility pattern, allowing requests to be processed sequentially by multiple handlers.
   - Facilitates the validation and conversion of IP addresses in various formats without manual intervention.

 - 1.2.3. **`BinaryFlyWeightFactory`**:
   - Applies the Flyweight pattern to manage `BinaryClass` instances efficiently.
   - Reduces memory usage by reusing instances of identical binary strings.

#### 1.3. Usage

- **Binary Validation**: Use `BinaryClass` to ensure binary strings are valid and to convert them into structured formats.
- **Request Handling**: Leverage `CoRHandler` to create flexible, chained validation processes for IP and MAC addresses.
- **Memory Optimization**: Utilize `BinaryFlyWeightFactory` to minimize memory consumption when dealing with large sets of binary data.
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.common.base_utils import BinaryFlyWeightFactory
```
---

### 2. IPSERVICE
The ipservice module in the IP address management toolkit provides specialized classes and utilities for handling IPv4 and IPv6 addresses. It includes features for validating, converting, and manipulating IP addresses in various formats (such as dot-decimal, CIDR, and binary). The module leverages design patterns like Chain of Responsibility and Flyweight to ensure efficient processing and memory management. It is essential for tasks such as network configuration, IP address validation, and IP range calculations.<br>
### 2.1. IP_CONVERTERS

- [ip_converters](docs/ipservice/ip_converters.md)
Here’s a concise description for `ip_converters.py`:

#### 2.1.1. Overview of `ip_converters.py`
The `ip_converters` module is an integral part of the IP address management toolkit, providing classes and methods for converting IP addresses between various formats such as binary, decimal, hexadecimal, and CIDR notation. By leveraging the Chain of Responsibility pattern, this module allows for flexible and efficient processing of IP addresses, enabling seamless conversion across multiple formats.

#### 2.1.2. Key Components
- **Conversion Handlers**:
  - **`DotDecimalIPv4ConverterHandler`**: Converts IPv4 addresses from dot-decimal notation (e.g., `192.168.1.1`) into binary format using `BinaryClass`.
  - **`CIDRIPv4ConverterHandler`**: Converts IPv4 addresses in CIDR notation (e.g., `/24`) into a binary network mask.
  - **`BinaryIPv4ConverterHandler`**: Processes IPv4 addresses already represented as lists of `BinaryClass` instances, facilitating further conversion or validation.
  - **`BinaryDigitsIPv4ConverterHandler`**: Converts a list of binary digits (0s and 1s) into grouped `BinaryClass` instances representing an IPv4 address.
  - **`ColonHexIPv6ConverterHandler`**: Converts IPv6 addresses in colon-separated hexadecimal format (e.g., `2001:db8::1`) into binary format using `BinaryClass`.
  - **`CIDRIPv6ConverterHandler`**: Converts IPv6 addresses in CIDR notation (e.g., `/64`) into a binary network mask.
  - **`BinaryIPv6ConverterHandler`**: Processes IPv6 addresses already represented as lists of `BinaryClass` instances, enabling further conversion or validation.
  - **`BinaryDigitsIPv6ConverterHandler`**: Converts a list of binary digits (0s and 1s) into grouped `BinaryClass` instances representing an IPv6 address.

- **Numeral Converters**:
  - **`NumeralConverter`**: Facilitates the conversion between binary, decimal, and hexadecimal formats. This utility class is essential for handling IP addresses at a low level, enabling accurate and efficient transformation of IP data.

### 2.2. IP_UTILS
- [ip_utils](docs/ipservice/ip_utils.md)

#### 2.2.1. Overview of `ip_utils.py`
The `ip_utils` module is a core component of the IP address management toolkit. It provides essential utilities and enumerations for handling and analyzing both IPv4 and IPv6 addresses. This module includes functionality for classifying different types of IP addresses, generating all possible IP combinations based on a given netmask, and determining whether an IP address falls within a specified network range.


#### 2.2.2. Key Components
- **IP Type Enumerations**:
  - **`IPType`**: Defines whether an IP address is IPv4 or IPv6 and includes methods to validate and retrieve IP types.
  - **`IPv4AddrType`**: Enumerates various categories of IPv4 addresses, such as public, private, multicast, loopback, and more.
  - **`IPv6AddrType`**: Enumerates various categories of IPv6 addresses, including global unicast, unique local addresses, multicast, and others.

- **Network Utility Tools**:
  - **`netmask_expand`**: Expands a given IP address based on a netmask to generate all possible IP address combinations. This is useful for generating subnets or understanding the range of addresses covered by a netmask.
  - **`ip_within_range`**: Determines if a given IP address falls within a specified network range. This method is essential for network validation, routing decisions, and ensuring that addresses conform to specified network boundaries.

### 2.3. IP_VALIDATORS
- [ip_validators](docs/ipservice/ip_validators.md)

#### 2.3.1. Overview of `ip_validators.py`
The `ip_validators` module is a critical part of the IP address management toolkit, offering robust validation mechanisms for both IPv4 and IPv6 addresses. By employing the Chain of Responsibility pattern, this module ensures that IP addresses are thoroughly validated according to different criteria, including format, range, and type. This validation process is essential for maintaining the integrity and correctness of network configurations.

#### 2.3.2. Key Components
- **Validation Handlers**:
  - **`IPValidatorHandler`**: Abstract base class for all IP address validation handlers, setting up the framework for the Chain of Responsibility pattern.<br>
  
  **IPv4**
    - **`IPv4IPBinaryValidator`**: Validates IPv4 addresses provided as lists of binary class instances, ensuring that each octet is within the valid range (0-255).
    - **`IPv4IPStringValidator`**: Validates IPv4 addresses provided in dot-decimal notation, converting them to binary class instances for validation.
    - **`IPv4NetmaskBinaryValidator`**: Validates IPv4 netmasks provided as binary class instances, ensuring that they represent valid contiguous masks.
    - **`IPv4NetmaskDotDecimalValidator`**: Validates IPv4 netmasks in dot-decimal format, converting them to binary class instances for validation.
    - **`IPv4NetmaskCIDRValidator`**: Validates IPv4 netmasks provided in CIDR notation, ensuring they represent valid network masks.<br>

  **IPv6**
    - **`IPv6IPBinaryValidator`**: Validates IPv6 addresses provided as lists of binary class instances, ensuring that each segment is within the valid range.
    - **`IPv6IPColonHexValidator`**: Validates IPv6 addresses provided in colon-separated hexadecimal notation, converting them to binary class instances for validation.
    - **`IPv6NetmaskBinaryValidator`**: Validates IPv6 netmasks provided as binary class instances, ensuring they represent valid contiguous masks.
    - **`IPv6NetmaskColonHexValidator`**: Validates IPv6 netmasks in colon-separated hexadecimal format, converting them to binary class instances for validation.
    - **`IPv6NetmaskCIDRValidator`**: Validates IPv6 netmasks provided in CIDR notation, ensuring they represent valid network masks.

## Contributing
Contributions to this project are welcome! Please feel free to submit issues or pull requests on <a href='https://github.com/tyt063144/TTLinks'>GitHub</a>. Ensure your code follows the established style and passes all tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For further information, please contact Yantao at tyt063144@gmail.com.