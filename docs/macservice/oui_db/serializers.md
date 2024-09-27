### `serializers.py` Module Documentation

## Overview

The `serializers.py` module provides a custom serialization function, `oui_enum_serializer`, designed to handle the serialization of specific objects into JSON-compatible formats. The module handles Python `Enum` types and custom `OUIUnit` objects from the `ttlinks.macservice.oui_utils` package, converting them into formats that can be easily stored or transferred as JSON.

## Functions

### 1. `oui_enum_serializer`

- **Description**: 
    A custom serializer function that serializes instances of `Enum` and `OUIUnit` into JSON-compatible formats. This function is essential when dealing with OUI data that needs to be serialized for storage, logging, or data transmission purposes.

- **Parameters**:
    - `obj (Any)`: The object to be serialized. It can be any Python object, but the function specifically handles `Enum` and `OUIUnit` objects.

- **Returns**:
    - **str**: If `obj` is an instance of `Enum`, the function returns the enum’s name as a string.
    - **dict**: If `obj` is an instance of `OUIUnit`, the function returns the `record` attribute of the `OUIUnit`.
    - **None**: For objects that are neither `Enum` nor `OUIUnit`, the function returns `None`, allowing other serializers to handle those objects.

- **Usage Example**:
```python
from ttlinks.macservice.oui_utils import OUIUnitCreator
from ttlinks.macservice.oui_utils import OUIType
from ttlinks.macservice.oui_db.serializers import oui_enum_serializer
obj1 = OUIType.IAB
oui_creator = OUIUnitCreator()
obj2 = oui_creator.create_product(**{
    'oui_id': 'E8:0A:B9:00:00:00',
    'oui_mask': 'FF:FF:FF:00:00:00',
    'oui_type': 'MA_L',
    'organization': 'Cisco Systems, Inc',
    'mac_range': 'E8:0A:B9:00:00:00-E8:0A:B9:FF:FF:FF',
    'oui_hex': 'E8-0A-B9',
    'address': '80 West Tasman Drive San Jose CA US 94568'
})
# Serialize Enum
print(oui_enum_serializer(obj1))

# Serialize OUIUnit
print(oui_enum_serializer(obj2))
```
Expected Output:
```
IAB
{'oui_id': 'E8:0A:B9:00:00:00', 'oui_mask': 'FF:FF:FF:00:00:00', 'oui_type': 'MA_L', 'organization': 'Cisco Systems, Inc', 'mac_range': 'E8:0A:B9:00:00:00-E8:0A:B9:FF:FF:FF', 'oui_hex': 'E8-0A-B9', 'address': '80 West Tasman Drive San Jose CA US 94568'}
```

### Example Use Cases

1. **Serializing Enum Values**:
    When dealing with enums, this function can convert an enum object into a string for logging or storing it in JSON format. For example:
    ```python
    OUIType.IAB -> "IAB"
    ```

2. **Serializing OUIUnit Objects**:
    The function extracts the `record` attribute of `OUIUnit` objects, making them easily serializable:
    ```python
    OUIUnit({'id': '00:1A:79', 'organization': 'Company A'}) -> {'id': '00:1A:79', 'organization': 'Company A'}
    ```
