### `searchers.py` Module Documentation

## Overview

The `searchers` module provides various strategies and classes for searching Organizationally Unique Identifier (OUI) data. It supports both simple list-based searches and more efficient trie-based searches for faster lookup in large datasets. This module is designed to work with MAC addresses and search for the corresponding OUI records in local databases.

## Key Classes and Interfaces

### `SearcherStrategy` (Abstract Class)

**Description**:
- Defines the interface for search strategies.
- It allows the creation of different search mechanisms (e.g., Trie-based or list-based searching).

**Methods**:
- `search(*args)`: Abstract method to perform the search operation. Subclasses must implement this method to define the logic for searching through the OUI data.

---

### `SimpleSearcherStrategy`

**Description**:
- Implements a list-based search strategy. This strategy is suitable for smaller datasets where a simple iteration through the OUI units is sufficient.
- Checks if a given MAC address falls within the range of a particular OUI unit using binary comparison.

**Methods**:
- `_is_within(mac: List[Octet], oui: OUIUnit) -> bool`: Helper method that checks if the MAC address is within the range of the OUI unit.
- `search(mac: List[Octet], oui_data: list) -> OUIUnit`: Performs a search through the OUI data to find a matching OUI unit for the provided MAC address.

---

### `TrieSearcherStrategy`

**Description**:
- Implements a trie-based search strategy. This strategy is ideal for larger datasets, as it allows for efficient prefix-based lookup.
- Traverses a trie structure to find the OUI unit with the longest matching prefix for the provided MAC address.

**Methods**:
- `search(mac: List[Octet], oui_data: list) -> OUIUnit`: Searches through the trie structure to find the OUI unit that matches the longest prefix of the provided MAC address.

---

### `OUIDBSearcher` (Abstract Class)

**Description**:
- Defines the interface for OUI database searchers.
- Allows for the selection of different search strategies (Trie-based or Simple Iteration) and performing searches on OUI databases.

**Methods**:
- `_set_strategy(strategy: OUIDBStrategy) -> SearcherStrategy`: Abstract method to set the search strategy.
- `search(mac: List[Octet], database: any) -> OUIUnit`: Abstract method to perform a search for an OUI unit using the provided MAC address.

---

## Local OUI Searchers

These classes are concrete implementations of the `OUIDBSearcher` abstract class. They are designed to search through local OUI databases using different search strategies and applying appropriate MAC address masks.

### `LocalOUIDBSearcher`

**Description**:
- Implements a searcher for local OUI databases. It supports both Trie-based and list-based search strategies, allowing for flexible searching depending on the dataset size and complexity.
- Applies masks to MAC addresses before searching, ensuring that the correct parts of the address are used for matching.
- defaults to the Trie search strategy.

**Attributes**:
- `_searcher_type`: Defines the type of OUI data being searched (e.g., IAB, MA-S, MA-M, MA-L, CID).
- `_mask`: A list of octets representing the mask used to adjust the MAC address for searching.
- `_strategy`: The selected search strategy (Trie or Simple Iteration).

**Methods**:
- `_set_strategy()`: Sets the appropriate search strategy (Trie or Simple Iteration).
- `search()`: Searches for the corresponding OUI unit in the local database using the provided MAC address.

---

### Specific OUI Searchers

These searchers are specialized versions of `LocalOUIDBSearcher` and are designed for specific types of OUI databases (IAB, MA-S, MA-M, MA-L, CID). They apply different masks for adjusting the MAC address based on the type of OUI data being searched.

#### `LocalIabSearcher`

**Description**:
- A searcher for IAB (Internet Architecture Board) OUI data.
- Applies the IAB-specific mask to the MAC address before searching.

---

#### `LocalMasSearcher`

**Description**:
- A searcher for MA-S (Manufacturer Assigned - Small) OUI data.
- Applies the MA-S-specific mask to the MAC address before searching.

---

#### `LocalMamSearcher`

**Description**:
- A searcher for MA-M (Manufacturer Assigned - Medium) OUI data.
- Applies the MA-M-specific mask to the MAC address before searching.

---

#### `LocalMalSearcher`

**Description**:
- A searcher for MA-L (Manufacturer Assigned - Large) OUI data.
- Applies the MA-L-specific mask to the MAC address before searching.

---

#### `LocalCidSearcher`

**Description**:
- A searcher for CID (Company Identifier) OUI data.
- Applies the CID-specific mask to the MAC address before searching.

---

## Example Usage

```python
from ttlinks.macservice.oui_db.searchers import LocalMalSearcher, OUIDBStrategy
from ttlinks.macservice.oui_db.loaders import LocalMalLoader
from ttlinks.macservice.mac_converters import MACConverter

# Initialize the searcher with the desired strategy (Trie or Simple Iteration)
searcher = LocalMalSearcher(OUIDBStrategy.TRIE)

# Load the OUI database using the corresponding loader
loader = LocalMalLoader(OUIDBStrategy.TRIE)
loader.connect()
loader.load()

# Convert MAC address and search the database
mac_address = MACConverter.convert_oui('08-BF-B8-00-00-00')
oui_unit = searcher.search(mac_address, [loader.data])

# Print the matching OUI unit
if oui_unit:
    print(oui_unit.record)
```
Expected Output:
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