# `mac_classifiers` Module  

The **`mac_classifiers`** module provides functionality to classify **MAC addresses** into three categories:  
- **Unicast**  
- **Multicast**  
- **Broadcast**  

This classification follows the **IEEE 802 MAC addressing standard** and is implemented using the **Chain of Responsibility** design pattern.  

## 1. Classify a MAC Address  

The `MACAddrClassifier` class provides a method to classify a given MAC address by processing it through a chain of classifiers.  

```python
from ttlinks.macservice.mac_classifiers import MACAddrClassifier
from ttlinks.macservice import MACType

mac1 = b'\xff\xff\xff\xff\xff\xff'  # Broadcast MAC
mac2 = b'\x02\x11\x22\x33\x44\x55'  # Unicast MAC
mac3 = b'\x01\x11\x22\x33\x44\x55'  # Multicast MAC

print(MACAddrClassifier.classify_mac(mac1))  # Expected Output: MACType.BROADCAST
print(MACAddrClassifier.classify_mac(mac2))  # Expected Output: MACType.UNICAST
print(MACAddrClassifier.classify_mac(mac3))  # Expected Output: MACType.MULTICAST
```

### Example Output:
```
MACType.BROADCAST
MACType.UNICAST
MACType.MULTICAST
```

## 2. Broadcast MAC Address Classification  

A **broadcast MAC address** consists of all `FF` bytes (`0xFF:FF:FF:FF:FF:FF`). The `BroadcastMACAddrClassifierHandler` identifies whether a given MAC address matches this pattern.  

```python
from ttlinks.macservice.mac_classifiers import BroadcastMACAddrClassifierHandler
from ttlinks.macservice import MACType

handler = BroadcastMACAddrClassifierHandler()
print(handler.handle(b'\xff\xff\xff\xff\xff\xff'))  # Expected Output: MACType.BROADCAST
```

### Example Output:
```
MACType.BROADCAST
```

## 3. Unicast MAC Address Classification  

A **unicast MAC address** is identified by checking the **least significant bit (LSB) of the first byte**. If the **LSB is 0**, it is an unicast address.  

```python
from ttlinks.macservice.mac_classifiers import UnicastMACAddrClassifierHandler
from ttlinks.macservice import MACType

handler = UnicastMACAddrClassifierHandler()
print(handler.handle(b'\x02\x11\x22\x33\x44\x55'))  # Expected Output: MACType.UNICAST
```

### Example Output:
```
MACType.UNICAST
```

## 4. Multicast MAC Address Classification  

A **multicast MAC address** is identified by checking the **least significant bit (LSB) of the first byte**. If the **LSB is 1**, it is a multicast address.  

```python
from ttlinks.macservice.mac_classifiers import MulticastMACAddrClassifierHandler
from ttlinks.macservice import MACType

handler = MulticastMACAddrClassifierHandler()
print(handler.handle(b'\x01\x11\x22\x33\x44\x55'))  # Expected Output: MACType.MULTICAST
```

### Example Output:
```
MACType.MULTICAST
```