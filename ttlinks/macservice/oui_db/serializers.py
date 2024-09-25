from enum import Enum
from typing import Any

from ttlinks.macservice.oui_utils import OUIUnit


def oui_enum_serializer(obj: Any) -> Any:
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, OUIUnit):
        return obj.record
