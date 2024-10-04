# `mac_factory.py` Module Documentation

## Overview

The `mac_factory.py` module provides a concrete implementation for managing MAC (Media Access Control) addresses. It supports the generation of individual and batch MAC addresses, including the ability to create random MAC addresses of various types such as unicast, multicast, and broadcast. The module utilizes an abstract factory design pattern to offer a flexible and extensible interface for MAC address generation and management. Additionally, the module includes functionality for parallel batch processing of MAC addresses using multithreading.

## Features

- **Abstract Factory Pattern**: Implements the `InterfaceMACFactory`, which defines a flexible and extensible interface for generating and managing MAC addresses.
- **Single and Batch Processing**: Capable of processing individual MAC addresses or handling large batches, with optional parallel processing to improve performance.
- **Random MAC Generation**: Provides methods to generate random MAC addresses, with support for specific types such as unicast, multicast, and broadcast.
- **Multithreaded Batch Processing**: Efficiently processes large batches of MAC addresses using multithreading for improved performance and scalability.
- **Custom MAC Type Handling**: Supports different MAC address types, including unicast, multicast, and broadcast, allowing for customization based on network requirements.

---

## `MACFactory` Class

### Description

The `MACFactory` class is a concrete implementation of the `InterfaceMACFactory` abstract base class. It provides methods for generating and managing single and batch MAC addresses. Additionally, it offers random MAC address generation, with the ability to specify the type of MAC address (unicast, multicast, broadcast). It also supports multithreaded batch processing to efficiently handle large numbers of MAC addresses.

### Methods

#### `mac`

- **Description**: Converts a given string into an `InterfaceMACAddr` object representing the MAC address.
- **Parameters**:
  - `mac (str)`: The MAC address in string format.
- **Returns**:
  - `InterfaceMACAddr`: An object representing the processed MAC address.
```python
from ttlinks.macservice.mac_factory import MACFactory
mac_factory = MACFactory()
mac_address = mac_factory.mac("08:BF:B8:78:90:AB")
print(mac_address)
print(mac_address.oui.record)
```
Example Output:
```
{
  'oui_id': '08:BF:B8:00:00:00', 
  'oui_mask': 'FF:FF:FF:00:00:00', 
  'oui_type': 'MA_L', 
  'organization': 'ASUSTek COMPUTER INC.', 
  'mac_range': '08:BF:B8:00:00:00-08:BF:B8:FF:FF:FF', 
  'oui_hex': '08-BF-B8', 
  'address': 'No.15,Lide Rd., Beitou, Dist.,Taipei 112,Taiwan, Taipei, Taiwan 112, TW'
}
```

#### `batch_macs`

- **Description**: Processes a batch of MAC addresses and returns a list of `InterfaceMACAddr` objects. The method optionally supports parallel processing and allows duplicate removal based on user preference.
- **Parameters**:
  - `macs (list[str])`: A list of MAC addresses in string format to process.
  - `max_workers (int, optional)`: The maximum number of worker threads to use for parallel processing. Defaults to 10.
  - `keep_dup (bool, optional)`: Whether to retain duplicate MAC addresses in the batch. Defaults to `True`.
- **Returns**:
  - `List[InterfaceMACAddr]`: A list of objects representing the processed MAC addresses.
```python
from ttlinks.macservice.mac_factory import MACFactory

mac_factory = MACFactory()
batch_mac_addresses = mac_factory.batch_macs(["12:34:56:78:90:AB", "AB:CD:EF:12:34:56"], max_workers=5, keep_dup=False)
for mac in batch_mac_addresses:
    print(mac)
```
Example Output:
```
AB:CD:EF:12:34:56
12:34:56:78:90:AB
```

#### `random_mac`

- **Description**: Generates a single random MAC address. The method allows specifying the type of MAC address (unicast, multicast, broadcast).
- **Parameters**:
  - `mac_type (MACType, optional)`: The type of MAC address to generate. If not specified, a generic random MAC address is generated.
- **Returns**:
  - `InterfaceMACAddr`: An object representing the generated MAC address.
```python
from ttlinks.macservice.mac_factory import MACFactory
from ttlinks.macservice.mac_address import MACType

mac_factory = MACFactory()
random_mac_address = mac_factory.random_mac(MACType.UNICAST)
print(random_mac_address)
print(random_mac_address.mac_type)
```
Example Output:
```
1E:37:68:8D:AD:FE
MACType.UNICAST
```

#### `random_macs_batch`

- **Description**: Generates a batch of random MAC addresses, with the option to specify the number and type of MAC addresses.
- **Parameters**:
  - `mac_type (MACType, optional)`: The type of MAC addresses to generate (unicast, multicast, broadcast). Defaults to `None`.
  - `num_macs (int, optional)`: The number of random MAC addresses to generate. Defaults to 10.
- **Returns**:
  - `List[InterfaceMACAddr]`: A list of randomly generated MAC addresses.
```python
from ttlinks.macservice.mac_factory import MACFactory
from ttlinks.macservice.mac_address import MACType

mac_factory = MACFactory()
random_batch_mac_multicast = mac_factory.random_macs_batch(MACType.MULTICAST, num_macs=5)
for mac_multicast in random_batch_mac_multicast:
    print(mac_multicast)
    print(mac_multicast.address[0])
print('-'*50)
random_batch_mac_unicast = mac_factory.random_macs_batch(MACType.UNICAST, num_macs=5)
for mac_unicast in random_batch_mac_unicast:
    print(mac_unicast)
    print(mac_unicast.address[0])
```
Example Output:
```
1F:39:53:35:C1:99
00011111
93:E2:D4:13:43:D0
10010011
87:FB:2B:63:2A:2D
10000111
13:ED:D3:75:91:71
00010011
31:67:DC:C7:AF:C9
00110001
--------------------------------------------------
8A:DE:6C:D4:36:9B
10001010
E2:B6:96:A5:B5:20
11100010
20:83:71:EC:F4:E8
00100000
5C:4D:C5:C3:50:76
01011100
56:D8:61:55:74:72
01010110
```

---

## `MACRandomizer` Class

### Description

The `MACRandomizer` class is responsible for generating random MAC addresses. It supports the generation of unicast, multicast, and broadcast MAC addresses by modifying the appropriate bits in the first octet of the MAC address to match the specified type. This class uses random bit generation to ensure that the addresses are valid 48-bit MAC addresses.

### Methods

#### `randomize`

- **Description**: Generates a random MAC address based on the specified MAC type. If no type is provided, a generic random MAC address is generated.
- **Parameters**:
  - `mac_type (MACType, optional)`: The type of MAC address to generate. Can be unicast, multicast, or broadcast. Defaults to `None` for a generic random MAC address.
- **Returns**:
  - `int`: A randomly generated MAC address represented as a 48-bit integer.

#### `_prepare`

- **Description**: A helper function that generates a random 48-bit integer and modifies the first octet to match the specified MAC type (unicast, multicast, broadcast).
- **Parameters**:
  - `mac_type (MACType, optional)`: The type of MAC address to generate. Can be unicast, multicast, or broadcast.
- **Returns**:
  - `int`: A 48-bit integer representing the generated MAC address.
```python
from ttlinks.macservice.mac_factory import MACRandomizer
from ttlinks.macservice.mac_address import MACType

mac_randomizer = MACRandomizer()
random_mac = mac_randomizer.randomize(MACType.BROADCAST)
print(hex(random_mac))
```
Example Output:
```
0xffffffffffff
```

---

## Dependencies

- **`concurrent.futures`**: Used for managing parallel execution in batch MAC address processing with `ThreadPoolExecutor`.
- **`random`**: Utilized for generating random 48-bit integers, which form the basis of random MAC addresses.
- **`abc`**: Provides the `ABC` and `abstractmethod` for defining abstract base classes and ensuring the factory interface methods are implemented.
- **`ttlinks.macservice.MACType`**: Enum class defining the different types of MAC addresses (unicast, multicast, broadcast).
- **`ttlinks.macservice.mac_address.InterfaceMACAddr` and `MACAddr`**: Classes that define the structure and behavior of MAC addresses.
