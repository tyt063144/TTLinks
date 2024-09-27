### `database.py` Module Documentation

## Overview

The `database.py` module provides the `LocalOUIDatabase` class, a singleton class designed to manage the loading, updating, and searching of Organizationally Unique Identifier (OUI) databases. This class supports searching for OUI units using MAC addresses, updating the OUI database with new official documents, and reverting custom OUI databases to their default versions.

---

## Classes

### 1. `LocalOUIDatabase`

- **Description**:  
    `LocalOUIDatabase` is a singleton class responsible for managing the lifecycle of local OUI databases. It ensures that the OUI databases for multiple OUI types (IAB, MA-S, MA-M, MA-L, CID) are loaded once into memory. The class provides methods to search for OUI units based on MAC addresses, update OUI data with new official documents, and revert custom OUI databases to their default versions.

- **Attributes**:
    - `__instance (LocalOUIDatabase)`: The single instance of the class (singleton pattern).
    - `_loaders (List)`: A list of OUI loaders for each OUI type (IAB, MA-S, MA-M, MA-L, CID).
    - `_updaters (List)`: A list of OUI updaters for each OUI type.
    - `_searchers (List)`: A list of OUI searchers for each OUI type.
    - `_data (List)`: Stores the data loaded from the OUI databases.

- **Key Methods**:

    - `__new__(cls, **kwargs) -> LocalOUIDatabase`:  
      Ensures that only one instance of `LocalOUIDatabase` is created (Singleton pattern). Returns the instance if it already exists or creates a new one.

    - `__init__(self, **kwargs)`:  
      Initializes the `LocalOUIDatabase` with loaders, updaters, and searchers for various OUI types. Loads OUI data upon initialization. Optional parameters such as search strategy can be passed.

    - `load() -> None`:  
      Loads the OUI data into memory using the defined loaders for each OUI type. The data is stored in the `_data` attribute.

    - `update(file_path: str) -> None`:  
      Updates the OUI databases using a new official document. The file path points to the document containing OUI updates that are applied by the updaters.

    - `revert(updater_type: OUIType) -> None`:  
      Reverts a custom OUI database to its default version based on the specified updater type (IAB, MA-S, MA-M, MA-L, CID).

    - `search(mac: Any) -> OUIUnit`:  
      Searches the loaded OUI databases for a matching OUI unit based on the given MAC address. The MAC address is first converted to a binary format using `MACConverter`, and searchers for each OUI type attempt to find a match.

    - `bulk_search(macs: List[Any]) -> dict`:  
      Performs a bulk search for multiple MAC addresses. This method uses multi-threading to search concurrently, improving performance for large sets of MAC addresses. Returns a dictionary mapping MAC addresses to their corresponding OUI units.

---

## Example Usage

```python
from ttlinks.macservice.oui_db.database import LocalOUIDatabase


# Initialize the database with Trie-based searching (default)
oui_db = LocalOUIDatabase()

# Alternatively, initialize with Simple Iteration strategy
# oui_db = LocalOUIDatabase(strategy=OUIDBStrategy.SIMPLE_ITERATION)

# Example MAC addresses to search for
macs = [
    "08-BF-B8",
    "00-09-0F-FE-00-01",
    "b2:3c:4d:5e:6f:7a",
    "c3:4d:5e:6f:7a:8b",
    "00:50:C2:1F:5a:bb",
]

# Perform bulk search
results = oui_db.bulk_search(macs)

# Print the results
for mac, result in results.items():
    if result:
        print(f"MAC: {mac} - OUI: {result.record}")
    else:
        print(f"MAC: {mac} - No match found")
```
Example Output:
```
MAC: 00-09-0F-FE-00-01 - OUI: {
    'oui_id': '00:09:0F:00:00:00', 
    'oui_mask': 'FF:FF:FF:00:00:00', 
    'oui_type': 'MA_L', 
    'organization': 
    'Fortinet, Inc.', 
    'mac_range': '00:09:0F:00:00:00-00:09:0F:FF:FF:FF', 
    'oui_hex': '00-09-0F', 
    'address': '1090 Kifer Road, Sunnyvale, CA 94086, US'
}
MAC: 00:50:C2:1F:5a:bb - OUI: {
    'oui_id': '00:50:C2:1F:50:00', 
    'oui_mask': 'FF:FF:FF:FF:F0:00', 
    'oui_type': 'IAB', 
    'organization': 
    'Abest Communication Corp.', 
    'mac_range': '00:50:C2:1F:50:00-00:50:C2:1F:5F:FF', 
    'oui_hex': '00-50-C2', 
    'address': '19-7 Ting-Tien-Liao, Hsien-Jenli Tamshui, Taipei 251, TW'
}
MAC: 08-BF-B8 - OUI: {
'oui_id': '08:BF:B8:00:00:00', 
'oui_mask': 'FF:FF:FF:00:00:00', 
'oui_type': 'MA_L', 
'organization': 'ASUSTek COMPUTER INC.', 
'mac_range': '08:BF:B8:00:00:00-08:BF:B8:FF:FF:FF', 
'oui_hex': '08-BF-B8', 
'address': 'No.15,Lide Rd., Beitou, Dist.,Taipei 112,Taiwan, Taipei, Taiwan 112, TW'
}
MAC: b2:3c:4d:5e:6f:7a - No match found
MAC: c3:4d:5e:6f:7a:8b - No match found
```


---

## Key Components

- **`OUIUnit`**:  
  Represents the OUI data for an organization, including details such as `oui_id`, `oui_mask`, `organization`, `mac_range`, and `address`. The search function returns this object when a MAC address is found within the OUI database.

- **`MACConverter.convert_oui`**:  
  A utility that converts MAC addresses into a format that can be processed by the search function. It handles various MAC address formats (e.g., `00:60:9F`, `70-1A-B8`, `00.09.0F`).

---

## Dependencies

- **ttlinks.macservice.oui_utils.OUIUnit**:  
  The class representing the OUI unit in the database.

- **ttlinks.macservice.binary_tools.BinaryTools**:  
  Utilities for comparing binary digits to check if a MAC address falls within a given range.

- **MACConverter**:  
  A utility for converting MAC addresses into a list of `Octet` objects to facilitate searching within the OUI database.

---

This document follows the format you provided and reflects the new structure and features of the `LocalOUIDatabase` class.