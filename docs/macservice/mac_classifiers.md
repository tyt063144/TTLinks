### `mac_classifiers.py` Module Documentation

### Overview

The `mac_classifiers.py` module provides functionality for classifying MAC (Media Access Control) addresses based on their type: Unicast, Multicast, or Broadcast. Using the Chain of Responsibility (CoR) design pattern, the module supports flexible classification by delegating requests through a chain of handlers. The handlers classify MAC addresses based on their binary representation and the properties of the first octet.

The module allows users to classify MAC addresses into three types:
- **Unicast**: A point-to-point communication where the least significant bit (LSB) of the first octet is 0.
- **Multicast**: A communication where the least significant bit (LSB) of the first octet is 1.
- **Broadcast**: A communication to all devices in a network, where all bits of the MAC address are set to 1.

### Key Components

1. **`MACAddrClassifierHandler` Class**:
   - Abstract base class for MAC address classification, following the Chain of Responsibility pattern.
   - Provides the `handle()` method to process the MAC address and `_verify_type()` method to check if a MAC address matches a specific type.

2. **Subclasses of `MACAddrClassifierHandler`**:
   - **`BroadcastMACAddrClassifierHandler`**: Classifies a MAC address as `MACType.BROADCAST` if all bits in the address are set to 1.
   - **`UnicastMACAddrClassifierHandler`**: Classifies a MAC address as `MACType.UNICAST` if the least significant bit (LSB) of the first octet is 0.
   - **`MulticastMACAddrClassifierHandler`**: Classifies a MAC address as `MACType.MULTICAST` if the least significant bit (LSB) of the first octet is 1.

3. **`MACAddrClassifier` Class**:
   - Static class that classifies MAC addresses using a chain of `MACAddrClassifierHandler` objects.
   - Provides the `classify_mac()` method that takes a MAC address and processes it through the chain of handlers to determine its type.

### Example Usage

This section demonstrates how to use the `mac_classifiers.py` module to classify MAC addresses as Unicast, Multicast, or Broadcast.

#### Example 1: Classifying a Broadcast MAC Address
```python
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter

# Broadcast MAC address (all bits set to 1)
mac_address = "FF:FF:FF:FF:FF:FF"
mac_type = MACAddrClassifier.classify_mac(MACConverter.convert_mac(mac_address))
print(mac_type)
```
**Expected Output**:
```
MACType.BROADCAST
```

#### Example 2: Classifying a Unicast MAC Address
```python
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter

# Unicast MAC address (LSB of first octet is 0)
mac_address = "00:00:00:00:00:00"
mac_type = MACAddrClassifier.classify_mac(MACConverter.convert_mac(mac_address))
print(mac_type)
```
**Expected Output**:
```
MACType.UNICAST
```

#### Example 3: Classifying a Multicast MAC Address
```python
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice.mac_converters import MACConverter

# Multicast MAC address (LSB of first octet is 1)
mac_address = "01:00:AA:cb:00:00"
mac_type = MACAddrClassifier.classify_mac(MACConverter.convert_mac(mac_address))
print(mac_type)
```
**Expected Output**:
```
MACType.MULTICAST
```

### Dependencies

The module relies on several key components:
- **`ttlinks.common.binary_utils.binary.Octet`**: Represents an octet of a MAC address.
- **`ttlinks.common.design_template.cor.SimpleCoRHandler`**: Implements the Chain of Responsibility pattern.
- **`ttlinks.macservice.mac_converters.MACConverter`**: Converts MAC addresses from various formats (e.g., hexadecimal) into a list of `Octet` objects.

### Conclusion

The `mac_classifiers.py` module provides a flexible and extensible solution for classifying MAC addresses as Unicast, Multicast, or Broadcast using a Chain of Responsibility pattern. The module can be easily extended by adding more classifier handlers if additional classification logic is needed.

