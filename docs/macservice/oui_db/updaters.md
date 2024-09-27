### `updaters.py` Module Documentation

## Overview

The `updaters.py` module provides classes for managing updates to various types of Organizationally Unique Identifier (OUI) databases. It defines an abstract base class `OUIDBUpdater` and several concrete implementations that handle the updating and reverting of custom OUI databases, such as **IAB (Industrial Automation and Building)**, **MA-S (Manufacturer Assigned - Small)**, **MA-M (Medium)**, **MA-L (Large)**, and **CID (Company Identifier)** databases. The classes allow users to update databases with new official documents and revert to default databases when necessary.

## Classes

### 1. `OUIDBUpdater`
- **Description**: 
    An abstract base class for updating OUI databases. Subclasses must implement the `update` and `revert` methods to handle custom databases.

- **Key Methods**:
    - `update(new_official_doc: str) -> None`: Updates the OUI database with a new official document.
    - `revert() -> None`: Reverts to the default OUI database by removing the custom database.

---

### 2. `LocalOUIDBUpdater`
- **Description**: 
    A concrete class that implements `OUIDBUpdater`, handling local OUI databases. This class allows users to update custom databases and revert to default ones.

- **Attributes**:
    - `_base_dir`: Directory path where the OUI databases are stored.
    - `_custom_db`: The name of the custom database file that can be updated or reverted.
    - `_updater_type`: The type of OUI updater (e.g., IAB, MA-S, MA-M, MA-L, CID).
    - `_file_parsers`: A list of file parsers for handling official documentation in `.txt` and `.csv` formats.

- **Key Methods**:
    - `update(new_official_doc: str) -> None`: Updates the custom database by parsing new official documents and saving the data.
    - `revert() -> None`: Removes the custom database, allowing the system to revert to the default database.

---

### Derived Updater Classes

#### 2.1 `LocalIabUpdater`
- **Description**: 
    Handles updates to the **IAB (Industrial Automation and Building)** OUI database. It allows users to update or revert the custom IAB OUI database with new official `.txt` or `.csv` documents.
  
- **Attributes**:
    - `_custom_db`: Name of the custom IAB database file (`custom_iab.json`).
    - `_updater_type`: The type of the updater (`OUIType.IAB`).
    - `_file_parsers`: Parsers for handling IAB documents in `.txt` and `.csv` formats.

#### 2.2 `LocalMasUpdater`
- **Description**: 
    Manages updates to the **MA-S (Manufacturer Assigned - Small)** OUI database, allowing users to update or revert the custom MA-S database with new official `.txt` or `.csv` documents.
  
- **Attributes**:
    - `_custom_db`: Name of the custom MA-S database file (`custom_mas.json`).
    - `_updater_type`: The type of the updater (`OUIType.MA_S`).
    - `_file_parsers`: Parsers for handling MA-S documents in `.txt` and `.csv` formats.

#### 2.3 `LocalMamUpdater`
- **Description**: 
    Manages updates to the **MA-M (Manufacturer Assigned - Medium)** OUI database. This class allows users to update or revert the custom MA-M OUI database using `.txt` or `.csv` documents.
  
- **Attributes**:
    - `_custom_db`: Name of the custom MA-M database file (`custom_mam.json`).
    - `_updater_type`: The type of the updater (`OUIType.MA_M`).
    - `_file_parsers`: Parsers for handling MA-M documents in `.txt` and `.csv` formats.

#### 2.4 `LocalMalUpdater`
- **Description**: 
    Handles updates to the **MA-L (Manufacturer Assigned - Large)** OUI database. Users can update or revert the custom MA-L OUI database using new `.txt` or `.csv` documents.
  
- **Attributes**:
    - `_custom_db`: Name of the custom MA-L database file (`custom_mal.json`).
    - `_updater_type`: The type of the updater (`OUIType.MA_L`).
    - `_file_parsers`: Parsers for handling MA-L documents in `.txt` and `.csv` formats.

#### 2.5 `LocalCidUpdater`
- **Description**: 
    Manages updates to the **CID (Company Identifier)** OUI database. Users can update or revert the custom CID database using official `.txt` or `.csv` documents.
  
- **Attributes**:
    - `_custom_db`: Name of the custom CID database file (`custom_cid.json`).
    - `_updater_type`: The type of the updater (`OUIType.CID`).
    - `_file_parsers`: Parsers for handling CID documents in `.txt` and `.csv` formats.

---

## Example Usage

```python
from ttlinks.macservice.oui_db.updaters import LocalIabUpdater, LocalMasUpdater, LocalMamUpdater, LocalMalUpdater, LocalCidUpdater

# Example usage of the OUIDBUpdater classes
iab_updater = LocalIabUpdater()
mas_updater = LocalMasUpdater()
mam_updater = LocalMamUpdater()
mal_updater = LocalMalUpdater()
cid_updater = LocalCidUpdater()

# Update the custom databases with new official documents
iab_updater.update('new_iab.txt')
mas_updater.update('new_mas.csv')
mam_updater.update('new_mam.txt')
mal_updater.update('new_mal.csv')
cid_updater.update('new_cid.txt')

# Revert the custom databases to the default versions
iab_updater.revert()
mas_updater.revert()
mam_updater.revert()
mal_updater.revert()
cid_updater.revert()
```
Expected Output:
```
New custom database: custom_iab.json is created or updated. Future lookups will use this database.
New custom database: custom_mas.json is created or updated. Future lookups will use this database.
New custom database: custom_mam.json is created or updated. Future lookups will use this database.
New custom database: custom_mal.json is created or updated. Future lookups will use this database.
New custom database: custom_cid.json is created or updated. Future lookups will use this database.
Custom database: custom_iab.json is removed.
Custom database: custom_mas.json is removed.
Custom database: custom_mam.json is removed.
Custom database: custom_mal.json is removed.
Custom database: custom_cid.json is removed.
```

---

## Conclusion

The `updaters.py` module provides an efficient mechanism for managing custom updates to OUI databases. By utilizing specific classes for IAB, MA-S, MA-M, MA-L, and CID OUI databases, it allows users to update custom databases using official documentation or revert to default databases as needed. The module simplifies database management through a unified interface, making it easy to update or restore default behavior for OUI lookups.