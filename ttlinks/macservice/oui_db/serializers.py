from enum import Enum
from typing import Any

from ttlinks.macservice.oui_utils import OUIUnit


def oui_serializer(obj: Any) -> Any:
    """
    A custom serializer function that serializes `Enum` and `OUIUnit` objects into a JSON-compatible format.

    This function is used when converting Python objects (like `Enum` or `OUIUnit` instances) to JSON.
    If the object is an instance of `Enum`, it returns the name of the enum.
    If the object is an instance of `OUIUnit`, it returns its `record` attribute.

    Parameters:
    - obj (Any): The object to be serialized. It could be an instance of `Enum`, `OUIUnit`, or any other type.

    Returns:
    - Any: A JSON-serializable representation of the input object.
           - If the object is an `Enum`, it returns the enum's name.
           - If the object is an `OUIUnit`, it returns its `record` attribute.
           - For all other types, the function returns `None`, leaving the object to be handled by other serializers.

    Example:
    - If `obj` is an instance of an enum `OUIType.IAB`, this function will return `'IAB'`.
    - If `obj` is an instance of `OUIUnit`, this function will return its `record`.

    """
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, OUIUnit):
        return obj.record
