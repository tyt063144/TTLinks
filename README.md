# TTLLinks IP and MAC Address Management and Conversion Toolkit
## Overview
This project provides a comprehensive toolkit for managing, validating, and converting IP addresses in both IPv4 and IPv6 formats, with planned support for MAC address management. Leveraging design patterns such as Chain of Responsibility and Flyweight, this toolkit ensures efficient and flexible handling of IP and MAC-related operations. The modular design allows for easy integration and extension within larger networking and automation systems.

## Installation
This project is available on PyPI and can be installed using pip:
```bash
pip install ttlinks
```

## Usage
After installation, you can import the necessary classes and utilities from the ttlinks package:
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

---

### 2. IPSERVICE
The ipservice module in the IP address management toolkit provides specialized classes and utilities for handling IPv4 and IPv6 addresses. It includes features for validating, converting, and manipulating IP addresses in various formats (such as dot-decimal, CIDR, and binary). The module leverages design patterns like Chain of Responsibility and Flyweight to ensure efficient processing and memory management. It is essential for tasks such as network configuration, IP address validation, and IP range calculations.<br>
[Read more](docs/ipservice.md)


## Contributing
Contributions to this project are welcome! Please feel free to submit issues or pull requests on <a href='https://github.com/tyt063144/TTLinks'>GitHub</a>. Ensure your code follows the established style and passes all tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For further information, please contact Yantao at tyt063144@gmail.com.