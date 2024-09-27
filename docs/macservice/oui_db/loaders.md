# `loaders.py` Module Documentation

## Overview

This module provides a set of loaders for handling OUI (Organizationally Unique Identifier) data, supporting both simple iteration and trie-based strategies for data storage and retrieval. The loaders can be configured to load data from local files, including default and custom databases, in various formats such as `.txt` and `.csv`. The module also introduces a strategy pattern, allowing different data loading strategies to be selected based on the use case.

## Classes

### OUIDBLoader (Abstract Class)

**Description**:  
The base abstract class for OUI loaders. This class defines the interface for connecting to and loading OUI data. The `OUIDBLoader` follows a strategy pattern, allowing different loading strategies to be set (e.g., simple iteration or trie-based loading).

- **Methods**:
  - `connect(*args)`: Abstract method for establishing a connection to the data source.
  - `load(*args)`: Abstract method for loading OUI data.
  - `_set_strategy(strategy: OUIDBStrategy) -> LoaderStrategy`: Abstract method to set the loading strategy.

### LoaderStrategy (Abstract Class)

**Description**:  
Defines the strategy interface for loading OUI data. Subclasses of this class implement different data loading strategies.

- **Methods**:
  - `load(*args)`: Abstract method for loading OUI units.

### SimpleLoaderStrategy

**Description**:  
A concrete strategy that loads OUI data into a simple list. This strategy is ideal for smaller datasets or cases where trie-based management is unnecessary.

- **Methods**:
  - `load(oui_units: List[Dict])`: Loads OUI units into a list and returns them as products.

### TrieLoaderStrategy

**Description**:  
A strategy that organizes OUI data in a trie structure for efficient prefix-based lookup. This strategy is ideal for larger datasets where trie-based management is more efficient.

- **Methods**:
  - `load(oui_units: List[Dict])`: Loads OUI units into a trie structure, where each OUI is stored based on its prefix.

### TrieOUIUnit

**Description**:  
Extends `TrieNode` to store OUI units. This class is used in conjunction with the `TrieLoaderStrategy` to store data in a trie structure.

- **Attributes**:
  - `oui_unit`: Stores specific OUI-related data.

---

## Local OUI Loaders

These are concrete implementations of `OUIDBLoader` that load OUI data from local databases. They support both default and custom databases, and handle various file formats like `.txt` and `.csv`.

### LocalOUIDBLoader

**Description**:  
A base class for local OUI loaders. It manages OUI data from local databases and supports both `SimpleLoaderStrategy` and `TrieLoaderStrategy`. It handles default and custom database loading, and includes methods for file integrity checks using MD5 hashes.

- **Attributes**:
  - `_base_dir`: The base directory for data files.
  - `_default_db`: The default database file name.
  - `_custom_db`: The custom database file name.
  - `_loader_type`: The type of loader (e.g., IAB, MA-S, CID).
  - `_official_docs`: Paths to the official document files.
  - `_file_parsers`: Handlers for parsing `.txt` and `.csv` file formats.
  - `_strategy`: The current strategy used for loading OUI data.

- **Methods**:
  - `_set_strategy()`: Sets the data loading strategy (either `SimpleLoaderStrategy` or `TrieLoaderStrategy`).
  - `_initialization()`: Ensures the local database is set up, creates a new database if necessary.
  - `_compare_hash()`: Compares MD5 hashes of official documentation files.
  - `_create_default_db()`: Creates the default database by parsing official documents.

### LocalIabLoader

**Description**:  
A loader specialized for loading IAB (Internet Architecture Board) OUI data. It supports both trie and simple iteration strategies for loading data from default or custom databases.

- **Attributes**:
  - `_default_db`: `default_iab.json`
  - `_custom_db`: `custom_iab.json`
  - `_loader_type`: `OUIType.IAB`
  - `_official_docs`: Paths to official IAB documents (`.txt` and `.csv` formats).
  - `_file_parsers`: Handlers for parsing IAB `.txt` and `.csv` files.

---

### LocalMasLoader

**Description**:  
A loader specialized for loading MA-S (MAC Address Small) OUI data. It supports trie-based and simple iteration strategies for loading data from default or custom databases.

- **Attributes**:
  - `_default_db`: `default_mas.json`
  - `_custom_db`: `custom_mas.json`
  - `_loader_type`: `OUIType.MA_S`
  - `_official_docs`: Paths to official MA-S documents (`.txt` and `.csv` formats).
  - `_file_parsers`: Handlers for parsing MA-S `.txt` and `.csv` files.

---

### LocalMamLoader

**Description**:  
A loader specialized for loading MA-M (MAC Address Medium) OUI data. It supports trie-based and simple iteration strategies for loading data from default or custom databases.

- **Attributes**:
  - `_default_db`: `default_mam.json`
  - `_custom_db`: `custom_mam.json`
  - `_loader_type`: `OUIType.MA_M`
  - `_official_docs`: Paths to official MA-M documents (`.txt` and `.csv` formats).
  - `_file_parsers`: Handlers for parsing MA-M `.txt` and `.csv` files.

---

### LocalMalLoader

**Description**:  
A loader specialized for loading MA-L (MAC Address Large) OUI data. It supports trie-based and simple iteration strategies for loading data from default or custom databases.

- **Attributes**:
  - `_default_db`: `default_mal.json`
  - `_custom_db`: `custom_mal.json`
  - `_loader_type`: `OUIType.MA_L`
  - `_official_docs`: Paths to official MA-L documents (`.txt` and `.csv` formats).
  - `_file_parsers`: Handlers for parsing MA-L `.txt` and `.csv` files.

---

### LocalCidLoader

**Description**:  
A loader specialized for loading CID (Company ID) OUI data. It supports trie-based and simple iteration strategies for loading data from default or custom databases.

- **Attributes**:
  - `_default_db`: `default_cid.json`
  - `_custom_db`: `custom_cid.json`
  - `_loader_type`: `OUIType.CID`
  - `_official_docs`: Paths to official CID documents (`.txt` and `.csv` formats).
  - `_file_parsers`: Handlers for parsing CID `.txt` and `.csv` files.

---

## Example Usage

```python
from ttlinks.macservice.oui_db.loaders import LocalIabLoader, OUIDBStrategy

# Instantiate a loader using the Trie strategy
loader = LocalIabLoader(OUIDBStrategy.TRIE)

# Connect to the local database
loader.connect()

# Load the data
loader.load()

# Access the loaded data
print(loader.data)
```

---

This updated `loaders.md` reflects the changes made in the new `loaders.py` file, incorporating the strategy pattern, new file parsers, and trie-based data management strategies.