# MAC Services Documentation

## `macservice` - Module Overview

### 1. **`mac_address.py`**
This module defines abstract base classes for representing and processing MAC addresses, including validation, classification, and interaction with the OUI database. It follows the Chain of Responsibility pattern for MAC classification.
- [MAC Address Processing](docs/macservice/mac_address.md)

### 2. **`mac_converters.py`**
This module provides classes to convert MAC addresses between different formats such as binary, octet, dashed hex, and colon-separated formats. The `MACConverterHandler` chain of responsibility handles conversion requests.
- [MAC Address Converters](docs/macservice/mac_converters.md)

### 3. **`mac_classifiers.py`**
This module contains handlers for classifying MAC addresses, such as `BroadcastMACAddrClassifierHandler` and `UnicastMACAddrClassifierHandler`. It uses the Chain of Responsibility (CoR) pattern to allow multiple classifiers to handle the classification of MAC addresses.
- [MAC Address Classifiers](docs/macservice/mac_classifiers.md)

### Module Descriptions:

#### 1. **`mac_address.py`**
This module defines the core framework for representing and handling MAC addresses. It provides the foundation for validating, classifying, and searching MAC addresses within the OUI database. It includes abstract classes and base implementations that manage interactions between MAC addresses and the database, supporting seamless integration with other modules for advanced MAC-related operations.

#### 2. **`mac_classifiers.py`**
This module handles the classification of MAC addresses, determining whether a given address is unicast, multicast, or broadcast. By employing the Chain of Responsibility pattern, it allows different classifiers to process MAC addresses and identify their type based on predefined binary rules. This is essential for understanding how a MAC address functions within network communication.

#### 3. **`mac_converters.py`**
This module focuses on converting MAC addresses between various formats, including binary, octet, and hexadecimal representations. By utilizing a Chain of Responsibility pattern, the module can pass MAC address conversion requests through different handlers, each specializing in a particular format, ensuring flexible and accurate conversions for different use cases.


