# MAC Services Documentation

## `macservice` - Module Overview

### 1. **`mac_address.py`**
This module defines abstract base classes for representing and processing MAC addresses, including validation, classification, and interaction with the OUI database. It follows the Chain of Responsibility pattern for MAC classification.
- [MAC Address Processing](/docs/macservice/mac_address.md)

### 2. **`mac_converters.py`**
This module provides classes to convert MAC addresses between different formats such as binary, octet, dashed hex, and colon-separated formats. The `MACConverterHandler` chain of responsibility handles conversion requests.
- [MAC Address Converters](/docs/macservice/mac_converters.md)

### 3. **`mac_classifiers.py`**
This module contains handlers for classifying MAC addresses, such as `BroadcastMACAddrClassifierHandler` and `UnicastMACAddrClassifierHandler`. It uses the Chain of Responsibility (CoR) pattern to allow multiple classifiers to handle the classification of MAC addresses.
- [MAC Address Classifiers](/docs/macservice/mac_classifiers.md)

### 4. **`mac_utils.py`**
This module defines enums related to MAC addresses, such as `MACType`, which categorizes MAC addresses as unicast, multicast, or broadcast.
- [MAC Utilities](/docs/macservice/mac_utils.md)

### 5. **`oui_file_parsers.py`**

This module provides parsers for handling OUI files in various formats such as `.txt` and `.csv`. It employs a Chain of Responsibility pattern to pass parsing tasks along different handler classes based on the file type and content. Specific handlers are responsible for parsing different OUI ranges such as MA-S, MA-M, and IAB, ensuring efficient parsing of MAC address ranges, company information, and physical addresses.

- [OUI File Parsers](/docs/macservice/oui_file_parsers.md)

### 6. **`oui_utils.py`**
This module contains utility classes related to OUI management, including the `OUIUnit` class, which represents an OUI entry, and the `OUIType` enum for categorizing different OUI types.
- [OUI Utilities](/docs/macservice/oui_utils.md)

---

## `oui_db` - Module Overview

### 1. **`database.py`**
This module provides an abstract base class (`OUIDatabase`) for loading, updating, and searching OUI data. It also includes the concrete implementation `LocalOUIDatabase` for managing OUI data from local sources.
- [OUI Database Management](/docs/macservice/oui_db/database.md)

### 2. **`loaders.py`**
This module defines the loading strategies for OUI data. The `SimpleLoaderStrategy` loads OUI units into a list, while the `TrieLoaderStrategy` loads OUI units into a trie structure.
- [OUI Data Loaders](/docs/macservice/oui_db/loaders.md)

### 3. **`searchers.py`**
This module implements strategies for searching through OUI databases using either simple iteration or a Trie-based search strategy. The `OUIDBSearcher` class handles MAC lookups within the OUI database.
- [OUI Data Searchers](/docs/macservice/oui_db/searchers.md)

### 4. **`updaters.py`**
This module handles updates and reverts to the local OUI database. Classes like `LocalIabUpdater` and `LocalMasUpdater` provide mechanisms to update specific OUI types (e.g., IAB, MA-S) from official documents.
- [OUI Data Updaters](/docs/macservice/oui_db/updaters.md)

### 5. **`serializers.py`**
This module provides custom serialization logic for OUI units and enums. It includes a serializer (`oui_serializer`) that serializes `Enum` and `OUIUnit` objects into a JSON-compatible format.
- [OUI Data Serializers](/docs/macservice/oui_db/serializers.md)
---


### Module Descriptions:

#### 1. **`mac_address.py`**
This module defines the core framework for representing and handling MAC addresses. It provides the foundation for validating, classifying, and searching MAC addresses within the OUI database. It includes abstract classes and base implementations that manage interactions between MAC addresses and the database, supporting seamless integration with other modules for advanced MAC-related operations.

#### 2. **`mac_classifiers.py`**
This module handles the classification of MAC addresses, determining whether a given address is unicast, multicast, or broadcast. By employing the Chain of Responsibility pattern, it allows different classifiers to process MAC addresses and identify their type based on predefined binary rules. This is essential for understanding how a MAC address functions within network communication.

#### 3. **`mac_converters.py`**
This module focuses on converting MAC addresses between various formats, including binary, octet, and hexadecimal representations. By utilizing a Chain of Responsibility pattern, the module can pass MAC address conversion requests through different handlers, each specializing in a particular format, ensuring flexible and accurate conversions for different use cases.

#### 4. **`mac_utils.py`**
This utility module defines the enumeration for MAC address types (e.g., unicast, multicast, and broadcast) and provides essential utilities for categorizing MAC addresses. It serves as a helper module, simplifying the management of MAC address types and supporting other modules in their classification and processing tasks.

#### 5. **`oui_utils.py`**
This utility module offers support for working with OUI data, including classes for categorizing OUI types and representing OUI units. It helps manage the relationships between MAC addresses and their corresponding organizational identifiers, ensuring that OUI data is processed and categorized correctly. It also includes various helper functions to assist with data manipulation and organization.

#### 6. **`oui_file_parsers.py`**
This module is responsible for parsing OUI files in both text and CSV formats. It uses a chain of handler classes to process different types of OUI ranges (such as IAB, MA-S, MA-M, and CID). By extracting MAC ranges, organizational information, and physical addresses from OUI documents, this module enables the system to ingest new OUI data and integrate it into the database.

#### 6. **`database.py`**
This module manages the OUI database, providing the core functionality for loading, updating, and searching OUI data. It defines the structure for interacting with OUI databases, both locally and through abstract interfaces. This module plays a critical role in maintaining the integrity and up-to-dateness of the OUI data, which is essential for identifying MAC address ownership and classifications.

#### 7. **`loaders.py`**
This module defines different strategies for loading OUI data into memory. It offers both simple and Trie-based loading approaches, allowing for flexible and efficient storage of OUI data depending on the scale and complexity of the data. This module ensures that the OUI data is structured in a way that optimizes searching and retrieval operations.

#### 8. **`searchers.py`**
This module provides search strategies for finding entries within the OUI database. It offers both simple iteration-based searches and more complex Trie-based searches, enabling faster lookups for large datasets. By using this module, the system can efficiently retrieve OUI data associated with MAC addresses, significantly improving lookup performance for network-related queries.

#### 9. **`updaters.py`**
This module manages the updating of OUI data, providing mechanisms to apply updates from new OUI records or documents. It also includes the capability to revert changes, ensuring that the database can be restored to a previous state if necessary. This module is crucial for maintaining the accuracy of OUI data, especially when new organizational identifiers are added or existing ones are modified.

#### 10. **`serializers.py`**
This module handles the serialization of OUI data, converting it into formats suitable for storage or transmission (e.g., JSON). It ensures that complex data structures, such as OUI entries and enumerations, can be easily shared or persisted across systems, making it essential for database exports and integrations with external systems.

