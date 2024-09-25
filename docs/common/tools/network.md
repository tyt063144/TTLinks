# `network.py` Module Documentation

## Overview

The `network.py` module under `common/tools` contains the `BinaryTools` class, which provides utility methods for working with binary data. Currently, the class includes the method `is_binary_in_range`, which determines whether a set of binary digits falls within a specific range based on a given mask and ID.

This module is useful for networking and data analysis scenarios where binary operations are required to check if certain binary patterns match within a specified range.

---

## Class

### 1. `BinaryTools`

#### Description

The `BinaryTools` class offers static methods for performing operations on binary data. It provides tools to evaluate whether one set of binary digits is within a specific range defined by another set of binary digits and a mask.

#### Methods

##### 1. `expand_by_mask(digits: List[int], mask: List[int]) -> List[tuple[int]]`
```python
@staticmethod
def expand_by_mask(digits: List[int], mask: List[int]) -> List[tuple[int]]:
```

- **Description**:
    - This method expands a given set of `digits` based on the `mask` to generate all possible combinations. For each position in the `digits`, if the corresponding bit in the `mask` is `1`, the digit remains fixed. If the `mask` bit is `0`, the digit can take multiple values (by default, `0` or `1`).
    
    - The method is useful for generating all possible combinations of an address (IP, MAC, etc.) where certain bits can vary, and others are fixed according to the mask.

- **Arguments**:
    - `digits` (`List[int]`): A list of digits representing an address (e.g., an IP or MAC address). These digits can be expanded based on the `mask`.
    - `mask` (`List[int]`): A list of binary digits acting as a mask. Positions set to `1` in the mask will keep the corresponding digits fixed, while positions set to `0` will allow the corresponding digits to vary.

- **Returns**:
    - `List[tuple[int]]`: A list of tuples, where each tuple represents a possible combination of the `digits` based on the `mask`.

- **Example Usage**:
    ```python
    from ttlinks.common.tools.network import BinaryTools
  
    digits = [0, 1, 0]
    mask = [1, 1, 0]
    result = BinaryTools.expand_by_mask(digits, mask)
    # result will be [(0, 1, 0), (0, 1, 1)]
    ```
  
##### 2. `is_binary_in_range(id_digits: List[int], mask_digits: List[int], compared_digits: List[int]) -> bool`
```python
@staticmethod
def is_binary_in_range(id_digits: List[int], mask_digits: List[int], compared_digits: List[int]) -> bool:
```

- **Description**:
    - This method checks if a set of `compared_digits` falls within a range defined by `id_digits` and `mask_digits`. It compares the digits from the `id_digits` and `compared_digits` up to the number of positions where the `mask_digits` are set to 1.
    
    - The `mask_digits` determine how many of the bits in the `id_digits` and `compared_digits` should be compared. A 1 in `mask_digits` indicates that the corresponding bit in `id_digits` and `compared_digits` should be compared, while a 0 allows that position to differ.

- **Arguments**:
    - `id_digits` (`List[int]`): A list of binary digits representing the ID. These digits define the reference point for the comparison.
    - `mask_digits` (`List[int]`): A list of binary digits acting as a mask. Positions set to 1 in the mask will be compared between `id_digits` and `compared_digits`.
    - `compared_digits` (`List[int]`): A list of binary digits representing the values to compare against the `id_digits`.

- **Returns**:
    - `bool`: Returns `True` if the `compared_digits` are within the range defined by `id_digits` and `mask_digits`. Returns `False` if they fall outside that range.

- **Raises**:
    - `ValueError`: Raised if the lengths of `id_digits`, `mask_digits`, and `compared_digits` are not the same.

- **Example Usage**: 
    ```python
    from ttlinks.common.tools.network import BinaryTools

    id_digits = [1, 0, 1, 0, 1, 1]
    mask_digits = [1, 1, 1, 0, 0, 0]
    compared_digits = [1, 0, 1, 1, 0, 0]

    result = BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits)
    # Output: True
    ```

In this example:
- The `id_digits` and `compared_digits` are compared up to the number of bits where `mask_digits` has 1s.
- The method returns `True` if the compared digits match the ID within the masked range.

---
