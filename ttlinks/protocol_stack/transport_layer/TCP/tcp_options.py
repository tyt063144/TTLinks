import struct
from abc import abstractmethod, ABC
from typing import List, Dict, Any

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.protocol_stack.base_classes.header_builder import Header, HeaderBuilder
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit

# -------------------TCP Option Value Object-------------------
class TCPOptionSACKValue:
    """
    Represents a TCP Selective Acknowledgment (SACK) option value, which specifies a range of bytes
    acknowledged by the sender as received.

    Attributes:
    - left_edge (int): The left (starting) edge of the acknowledged range.
    - right_edge (int): The right (ending) edge of the acknowledged range.

    Methods:
    - _validate: Ensures that left and right edges are valid, non-negative integers within the 32-bit range.
    - __repr__: Provides a string representation of the SACK range.

    Exceptions:
    - Raises ValueError if the edges do not meet the specified constraints.
    """
    def __init__(self, left_edge: int, right_edge: int):
        """
        Initializes the TCPOptionSACKValue with left and right edges, validating them.

        Parameters:
        - left_edge (int): The starting edge of the SACK range.
        - right_edge (int): The ending edge of the SACK range.
        """
        self._validate(left_edge, right_edge)
        self._left_edge = left_edge
        self._right_edge = right_edge

    @staticmethod
    def _validate(left_edge: int, right_edge: int):
        """
        Validates that left and right edges are within acceptable ranges.

        Parameters:
        - left_edge (int): The starting edge to validate.
        - right_edge (int): The ending edge to validate.

        Raises:
        - ValueError: If edges are invalid.
        """
        if left_edge > right_edge:
            raise ValueError('Left edge must be less than or equal to right edge')
        if left_edge < 0 or right_edge < 0:
            raise ValueError('Left and right edges must be greater than or equal to 0')
        if left_edge > 0xFFFFFFFF or right_edge > 0xFFFFFFFF:
            raise ValueError('Left and right edges must be less than or equal to 4294967295')

    @property
    def left_edge(self) -> int:
        """
        Returns the left edge of the SACK range.

        Returns:
        - int: Left edge of the range.
        """
        return self._left_edge

    @property
    def right_edge(self) -> int:
        """
        Returns the right edge of the SACK range.

        Returns:
        - int: Right edge of the range.
        """
        return self._right_edge

    def __repr__(self):
        """
        Provides a string representation of the SACK range.

        Returns:
        - str: Formatted string of the SACK range.
        """
        return f'SACKRange(left_edge={self._left_edge}, right_edge={self._right_edge})'

class TCPOptionTimestampValue:
    """
    Represents a TCP Timestamp option value, including a timestamp and an echo reply for
    round-trip time measurements.

    Attributes:
    - timestamp (int): The current timestamp value.
    - echo_reply (int): Echoed timestamp from the receiving host.

    Methods:
    - __repr__: Provides a string representation of the timestamp and echo reply values.
    """
    def __init__(self, timestamp: int, echo_reply: int):
        """
        Initializes the TCPOptionTimestampValue with a timestamp and echo reply.

        Parameters:
        - timestamp (int): The timestamp value.
        - echo_reply (int): The echoed timestamp value.
        """
        self._timestamp = timestamp
        self._echo_reply = echo_reply

    @property
    def timestamp(self) -> int:
        """
        Returns the timestamp value.

        Returns:
        - int: The timestamp value.
        """
        return self._timestamp

    @property
    def echo_reply(self) -> int:
        """
        Returns the echoed timestamp value.

        Returns:
        - int: The echoed timestamp value.
        """
        return self._echo_reply

    def __repr__(self):
        """
        Provides a string representation of the timestamp and echo reply values.

        Returns:
        - str: Formatted string with timestamp and echo reply.
        """
        return f'Timestamp(timestamp={self._timestamp}, echo_reply={self._echo_reply})'

# -------------------TCP Option Unit-------------------
class TCPOptionUnit(ProtocolUnit, ABC):
    """
    Abstract base class for TCP options, supporting a variety of TCP options with unique identifiers.

    Supported TCP Options:
    - End of Option List
    - No-Operation
    - Maximum Segment Size
    - Window Scale
    - SACK Permitted
    - SACK
    - Timestamp
    - Unknown Option

    Attributes:
    - kind (bytes): Option type identifier.
    - length (bytes): Length of the option in bytes.
    - value (bytes): The option's data payload.

    Properties:
    - as_bytes: Returns the complete option as a byte sequence.
    - attributes: Provides a dictionary of the option’s raw kind, length, and value.
    - summary: Provides a human-readable dictionary of option attributes.

    Methods:
    - kind: Abstract property for the option type.
    - length: Abstract property for the option length.
    - value: Abstract property for the option value.
    """
    def __init__(self, kind: bytes, length: bytes=b'', value: bytes=b''):
        """
        Initializes the TCP option with its kind, length, and value.

        Parameters:
        - kind (bytes): The kind of the TCP option.
        - length (bytes): The length of the option, defaults to an empty byte string.
        - value (bytes): The option's value or data, defaults to an empty byte string.
        """
        self._kind = kind
        self._length = length
        self._value = value

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the TCP option as a concatenated byte sequence.

        Returns:
        - bytes: The TCP option as bytes.
        """
        return self._kind + self._length + self._value
    @property
    def attributes(self)-> dict:
        """
        Returns a dictionary of the TCP option's raw attributes.

        Returns:
        - dict: Dictionary containing the 'kind', 'length', and 'value' attributes.
        """
        return {
            "kind": self._kind,
            "length": self._length,
            "value": self._value,
        }
    @property
    def summary(self) -> dict:
        """
        Returns a human-readable dictionary of the TCP option's attributes.

        Returns:
        - dict: Dictionary with descriptive keys for 'kind', 'length', and 'value'.
        """
        return {
            "kind": self.kind,
            "length": self.length,
            "value": self.value,
        }
    @property
    @abstractmethod
    def kind(self):
        pass
    @property
    @abstractmethod
    def length(self):
        pass
    @property
    @abstractmethod
    def value(self):
        pass
    def __repr__(self):
        """
        Returns a string representation of the TCP option.

        Returns:
        - str: Formatted string of the TCP option kind, length, and value.
        """
        return f'{self.kind}(length={self.length}, value={self.value})'

class TCPOption0Unit(TCPOptionUnit):
    """
    Represents the "End of Option List" TCP option (kind 0).

    Properties:
    - kind: Returns 'End of Option List'.
    - length: Returns the length attribute (empty by default for this option).
    - value: Returns the value attribute (empty by default for this option).
    """
    @property
    def kind(self) -> str:
        return 'End of Option List'
    @property
    def length(self) -> bytes:
        return self._length
    @property
    def value(self) -> bytes:
        return self._value

class TCPOption1Unit(TCPOptionUnit):
    """
    Represents the "No-Operation" TCP option (kind 1).

    Properties:
    - kind: Returns 'No-Operation'.
    - length: Returns the length attribute (empty by default for this option).
    - value: Returns the value attribute (empty by default for this option).
    """
    @property
    def kind(self) -> str:
        return 'No-Operation'
    @property
    def length(self) -> bytes:
        return self._length
    @property
    def value(self) -> bytes:
        return self._value

class TCPOption2Unit(TCPOptionUnit):
    """
    Represents the "Maximum Segment Size" TCP option (kind 2).

    Properties:
    - kind: Returns 'Maximum Segment Size'.
    - length: Interprets the length attribute as an integer.
    - value: Interprets the value as an integer representing the maximum segment size.
    """
    @property
    def kind(self) -> str:
        return 'Maximum Segment Size'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> int:
        return int.from_bytes(self._value, byteorder='big')

class TCPOption3Unit(TCPOptionUnit):
    """
    Represents the "Window Scale" TCP option (kind 3).

    Properties:
    - kind: Returns 'Window Scale'.
    - length: Interprets the length attribute as an integer.
    - value: Interprets the value as an integer representing the window scale factor.
    """
    @property
    def kind(self) -> str:
        return 'Window Scale'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> int:
        return int.from_bytes(self._value, byteorder='big')

class TCPOption4Unit(TCPOptionUnit):
    """
    Represents the "SACK Permitted" TCP option (kind 4).

    Properties:
    - kind: Returns 'SACK Permitted'.
    - length: Interprets the length attribute as an integer.
    - value: Returns the value attribute as bytes (typically unused for this option).
    """
    @property
    def kind(self) -> str:
        return 'SACK Permitted'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> bytes:
        return self._value

class TCPOption5Unit(TCPOptionUnit):
    """
    Represents the "SACK" (Selective Acknowledgment) TCP option (kind 5), which includes multiple
    acknowledgment ranges.

    Properties:
    - kind: Returns 'SACK'.
    - length: Interprets the length attribute as an integer.
    - value: Interprets the value as a list of TCPOptionSACKValue, representing SACK ranges.
    """
    @property
    def kind(self) -> str:
        return 'SACK'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> List[TCPOptionSACKValue]:
        sacks = []
        for i in range(0, len(self._value), 8):
            sack = {
                'left_edge': int.from_bytes(self._value[i:i+4], byteorder='big'),
                'right_edge': int.from_bytes(self._value[i+4:i+8], byteorder='big')
            }
            sacks.append(TCPOptionSACKValue(**sack))
        return sacks

class TCPOption8Unit(TCPOptionUnit):
    """
    Represents the "Timestamp" TCP option (kind 8), used for measuring round-trip time.

    Properties:
    - kind: Returns 'Timestamp'.
    - length: Interprets the length attribute as an integer.
    - value: Interprets the value as a dictionary containing timestamp and echo reply values.
    """
    @property
    def kind(self) -> str:
        return 'Timestamp'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> Dict[str, int]:
        values = {'timestamp': int.from_bytes(self._value[:4], byteorder='big'), 'echo_reply': int.from_bytes(self._value[4:], byteorder='big')}
        return values

class TCPUnknownOptionUnit(TCPOptionUnit):
    """
    Represents an unknown TCP option, allowing it to be stored and passed through without interpretation.

    Properties:
    - kind: Returns 'Unknown Option'.
    - length: Interprets the length attribute as an integer.
    - value: Returns the raw byte sequence of the unknown option.
    """
    @property
    def kind(self) -> str:
        return 'Unknown Option'
    @property
    def length(self) -> int:
        return int.from_bytes(self._length, byteorder='big')
    @property
    def value(self) -> bytes:
        return self._value


# -------------------TCP Option Unit Selector-------------------
class TCPOptionUnitSelectorHandler(SimpleCoRHandler):
    """
    Base handler class for selecting the appropriate TCP option unit class based on the option kind.
    Implements the **Chain of Responsibility** pattern, where each subclass handles a specific option kind.

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Attempts to handle the given option kind, returning the
      corresponding TCPOption unit class or passing the request to the next handler.

    Returns:
    - The matching TCPOption unit class if handled, otherwise `TCPUnknownOptionUnit`.
    """
    @abstractmethod
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if self._next_handler:
            return self._next_handler.handle(kind)
        return TCPUnknownOptionUnit

class TCPOption0UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption0Unit class for option kind 0 (End of Option List).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption0Unit` if the kind is 0; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 0:
            return TCPOption0Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption1UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption1Unit class for option kind 1 (No-Operation).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption1Unit` if the kind is 1; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 1:
            return TCPOption1Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption2UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption2Unit class for option kind 2 (Maximum Segment Size).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption2Unit` if the kind is 2; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 2:
            return TCPOption2Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption3UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption3Unit class for option kind 3 (Window Scale).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption3Unit` if the kind is 3; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 3:
            return TCPOption3Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption4UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption4Unit class for option kind 4 (SACK Permitted).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption4Unit` if the kind is 4; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 4:
            return TCPOption4Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption5UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption5Unit class for option kind 5 (SACK).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption5Unit` if the kind is 5; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 5:
            return TCPOption5Unit
        return super().handle(kind, *args, **kwargs)

class TCPOption8UnitSelectorHandler(TCPOptionUnitSelectorHandler):
    """
    Handler to select the TCPOption8Unit class for option kind 8 (Timestamp).

    Methods:
    - handle(kind: Any, *args, **kwargs) -> Any: Returns `TCPOption8Unit` if the kind is 8; otherwise,
      passes to the next handler.
    """
    def handle(self, kind: Any, *args, **kwargs) -> Any:
        if kind == 8:
            return TCPOption8Unit
        return super().handle(kind, *args, **kwargs)

class TCPOptionUnitSelector:
    """
    Utility class for selecting the appropriate TCP option unit class based on the option kind.
    Uses a chain of handlers to evaluate each option kind and return the corresponding TCPOption unit class.

    Methods:
    - select_tcp_option_unit(kind: int) -> type(TCPOptionUnit): Static method that initializes the handler
      chain and returns the appropriate TCPOption unit class based on the provided kind.
    """
    @staticmethod
    def select_tcp_option_unit(kind: int) -> type(TCPOptionUnit):
        """
        Selects the appropriate TCP option unit class based on the provided option kind.

        Parameters:
        - kind (int): The integer identifier for the TCP option kind.

        Returns:
        - type(TCPOptionUnit): The TCP option unit class corresponding to the specified kind, or `TCPUnknownOptionUnit`
          if the kind is unrecognized.
        """
        selectors = [
            TCPOption0UnitSelectorHandler(),
            TCPOption1UnitSelectorHandler(),
            TCPOption2UnitSelectorHandler(),
            TCPOption3UnitSelectorHandler(),
            TCPOption4UnitSelectorHandler(),
            TCPOption5UnitSelectorHandler(),
            TCPOption8UnitSelectorHandler(),
        ]
        selector_handler = selectors[0]
        for next_handler in selectors[1:]:
            selector_handler.set_next(next_handler)
            selector_handler = next_handler
        return selectors[0].handle(kind)

# -------------------TCP Option Header-------------------
class TCPOptionHeader(Header):
    """
    Represents the header of a TCP option and provides methods for constructing and retrieving
    the appropriate TCPOption unit based on the option kind.

    Methods:
    - _tcp_option_unit: Determines the correct TCPOption unit class using `TCPOptionUnitSelector`.
    - _construct: Constructs the option fields as a dictionary, packaging kind, length, and value as bytes.
    - unit: Returns an instance of the TCPOption unit, built from the constructed fields.

    Attributes:
    - _fields (dict): A dictionary holding 'kind', 'length', and 'value' for the TCP option.
    """
    def _tcp_option_unit(self) -> type(TCPOptionUnit):
        """
        Selects the appropriate TCPOption unit class based on the 'kind' field.

        Returns:
        - type(TCPOptionUnit): The TCPOption unit class determined by the option kind.
        """
        tcp_option_unit = TCPOptionUnitSelector.select_tcp_option_unit(self._fields['kind'])
        return tcp_option_unit

    def _construct(self) -> dict:
        """
        Constructs the fields of the TCP option header as a dictionary of packed bytes.

        Returns:
        - dict: Dictionary containing 'kind', 'length', and 'value' in byte format.
        """
        kind = struct.pack('!B', self._fields['kind'])
        length = struct.pack('!B', self._fields['length']) if self._fields.get('length') else b''
        value = self._fields['value'] if self._fields.get('value') else b''

        return {
            'kind': kind,
            'length': length,
            'value': value,
        }

    @property
    def unit(self) -> ProtocolUnit:
        """
        Returns an instance of the selected TCPOption unit, constructed from the header fields.

        Returns:
        - ProtocolUnit: The TCPOption unit instance initialized with the header's constructed fields.
        """
        tcp_option_unit = self._tcp_option_unit()
        return tcp_option_unit(**self._construct())


# -------------------TCP Option Header Builder-------------------
class TCPOptionHeaderBuilderInterface(HeaderBuilder, ABC):
    """
    Abstract builder interface for constructing TCP option headers, using the Builder pattern.

    Methods:
    - set_kind(kind: int): Abstract method to set the 'kind' field for a TCP option header.
    - set_length(length: int): Abstract method to set the 'length' field for a TCP option header.
    - set_value(value: int): Abstract method to set the 'value' field for a TCP option header.
    """
    @abstractmethod
    def set_kind(self, kind: int):
        pass
        # self._header.add_field('kind', kind)
    @abstractmethod
    def set_length(self, length: int):
        pass
        # self._header.add_field('length', length)
    @abstractmethod
    def set_value(self, value: int):
        pass
        # self._header.add_field('value', value)

class TCPOption0HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "End of Option List" TCP option (kind 0). This option does not have length or value fields.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 0.
    - set_length(length: int): Raises a ValueError if a length is provided, as this option has no length.
    - set_value(value: int): Raises a ValueError if a value is provided, as this option has no value.
    """
    def set_kind(self, kind: int = 0):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = None):
        if length is not None:
            raise ValueError('End of Option List option does not have a length')
        self._header.add_field('length', None)
    def set_value(self, value: int = None):
        if value is not None:
            raise ValueError('End of Option List option does not have a value')
        self._header.add_field('value', None)

class TCPOption1HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "No-Operation" TCP option (kind 1). This option does not have length or value fields.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 1.
    - set_length(length: int): Raises a ValueError if a length is provided, as this option has no length.
    - set_value(value: int): Raises a ValueError if a value is provided, as this option has no value.
    """
    def set_kind(self, kind: int = 1):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = None):
        if length is not None:
            raise ValueError('No-Operation option does not have a length')
        self._header.add_field('length', None)
    def set_value(self, value: int = None):
        if value is not None:
            raise ValueError('No-Operation option does not have a value')
        self._header.add_field('value', None)

class TCPOption2HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "Maximum Segment Size" TCP option (kind 2). This option has a default length of 4 bytes and a default
    value of 1460 (typical MSS value), but both can be customized.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 2 or uses a provided custom kind.
    - set_length(length: int): Sets the 'length' field to 4 by default or a custom length if provided.
    - set_value(value: int): Sets the 'value' field to 1460 (typical MSS) or a provided value in bytes.
    """
    def set_kind(self, kind: int = None):
        if kind is not None:
            self._header.add_field('kind', kind)
        else:
            self._header.add_field('kind', 2)
    def set_length(self, length: int = None):
        if length is not None:
            self._header.add_field('length', length)
        else:
            self._header.add_field('length', 4)
    def set_value(self, value: int = None):
        if value is not None:
            value_as_bytes = struct.pack('!H', value)
        else:
            value_as_bytes = struct.pack('!H', 1460)
        self._header.add_field('value', value_as_bytes)

class TCPOption3HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "Window Scale" TCP option (kind 3). This option has a default length of 3 bytes and a
    default value of 7 for the scaling factor, but both can be customized.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 3 by default.
    - set_length(length: int): Sets the 'length' field to 3 by default.
    - set_value(value: int): Sets the 'value' field to 7 by default, or a provided scaling factor in bytes.
    """
    def set_kind(self, kind: int = 3):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = 3):
        self._header.add_field('length', length)
    def set_value(self, value: int = 7):
        value_as_bytes = struct.pack('!B', value)
        self._header.add_field('value', value_as_bytes)

class TCPOption4HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "SACK Permitted" TCP option (kind 4). This option has a fixed length of 2 bytes
    and does not include a value.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 4 by default.
    - set_length(length: int): Sets the 'length' field to 2 by default.
    - set_value(value: int): Raises a ValueError if a value is provided, as this option does not have a value.
    """
    def set_kind(self, kind: int = 4):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = 2):
        self._header.add_field('length', length)
    def set_value(self, value: int = None):
        if value is not None:
            raise ValueError('SACK Permitted option does not have a value')
        self._header.add_field('value', None)

class TCPOption5HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "SACK" (Selective Acknowledgment) TCP option (kind 5). This option requires a length
    and includes multiple SACK ranges.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 5 by default.
    - set_length(length: int): Sets the 'length' field; raises an error if not provided.
    - set_value(value: List[TCPOptionSACKValue]): Constructs the value from provided SACK ranges.
    """
    def set_kind(self, kind: int = 5):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = None):
        """
        It's not necessary to set the length of the SACK option directly, as it is calculated based on the number of SACK ranges.
        """
        if length is None:
            raise ValueError('Length must be specified for SACK option')
        self._header.add_field('length', length)
    def set_value(self, value:List[TCPOptionSACKValue]):
        value_as_bytes = b''
        for sack in value:
            value_as_bytes += struct.pack('!I', sack.left_edge) + struct.pack('!I', sack.right_edge)
        self.set_length(len(value_as_bytes) + 2)
        self._header.add_field('value', value_as_bytes)

class TCPOption8HeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for the "Timestamp" TCP option (kind 8). This option has a default length of 10 bytes and
    includes a timestamp and an echo reply.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to 8 by default.
    - set_length(length: int): Sets the 'length' field to 10 by default.
    - set_value(value: TCPOptionTimestampValue): Constructs the value from a timestamp and echo reply.
    """
    def set_kind(self, kind: int = 8):
        self._header.add_field('kind', kind)
    def set_length(self, length: int = 10):
        self._header.add_field('length', length)
    def set_value(self, value: TCPOptionTimestampValue):
        value_as_bytes = struct.pack('!I', value.timestamp) + struct.pack('!I', value.echo_reply)
        self._header.add_field('value', value_as_bytes)

class TCPCustomOptionHeaderBuilder(TCPOptionHeaderBuilderInterface):
    """
    Builder for custom TCP options. Allows specifying arbitrary kinds, lengths, and values for options
    that do not fit standard option types.

    Methods:
    - set_kind(kind: int): Sets the 'kind' field to the specified value.
    - set_length(length: int): Sets the 'length' field; raises an error if not provided.
    - set_value(value: bytes): Sets the 'value' field as raw bytes and adjusts the length accordingly.

    Examples:
    - Maximum Segment Size (MSS) option (kind 2):
        ```
        value = 1460
        .set_value(value.to_bytes(2, byteorder='big'))
        Expected output: b'\x05\xB4'
        ```

    - Timestamp option (kind 8):
        ```
        value = 1328420247
        echo_reply = 3557171634
        .set_value(value.to_bytes(4, byteorder='big') + echo_reply.to_bytes(4, byteorder='big'))
        ```
    """
    def set_kind(self, kind: int):
        """
        Sets the 'kind' field for the custom option.

        Parameters:
        - kind (int): The kind identifier for the option.
        """
        self._header.add_field('kind', kind)
    def set_length(self, length: int = None):
        """
        Sets the 'length' field for the custom option. Raises an error if not provided.

        Parameters:
        - length (int): The length of the custom option.

        Raises:
        - ValueError: If length is not specified.
        """
        if length is None:
            raise ValueError('Length must be specified for custom option')
        self._header.add_field('length', length)
    def set_value(self, value: bytes):
        """
        Sets the 'value' field for the custom option as raw bytes, calculates and sets the length.

        Parameters:
        - value (bytes): The custom option value in bytes.

        Examples:
        - For an MSS option (kind 2), with a value of 1460:
            ```
            set_value(1460.to_bytes(2, byteorder='big'))
            ```
        - For a Timestamp option (kind 8), with timestamp and echo_reply values:
            ```
            timestamp = 1328420247
            echo_reply = 3557171634
            set_value(timestamp.to_bytes(4, byteorder='big') + echo_reply.to_bytes(4, byteorder='big'))
            ```
        """
        self.set_length(len(value) + 2)
        self._header.add_field('value', value)


# -------------------TCP Option Builder Director-------------------
class TCPOptionBuilderDirector:
    """
    Director class for constructing TCP option headers using a specified builder.
    This class orchestrates the construction process, configuring the option's kind, length, and value
    through a builder interface.

    Methods:
    - set_builder(builder: type(TCPOptionHeaderBuilderInterface)): Sets the builder to be used for constructing TCP options.
    - build(kind: int, length: int = None, value: Any = None): Configures and builds the TCP option header based on the provided parameters.

    Attributes:
    - _builder (TCPOptionHeaderBuilderInterface): The builder instance used for constructing the TCP option.
    """
    def __init__(self, builder: type(TCPOptionHeaderBuilderInterface)):
        """
        Initializes the director with a builder instance for constructing a TCP option header.

        Parameters:
        - builder (type(TCPOptionHeaderBuilderInterface)): The builder class to use for constructing the option.
        """
        self._builder = builder(TCPOptionHeader())

    def set_builder(self, builder: type(TCPOptionHeaderBuilderInterface)):
        """
        Sets a new builder for constructing the TCP option header.

        Parameters:
        - builder (type(TCPOptionHeaderBuilderInterface)): The new builder class to use.
        """
        self._builder = builder(TCPOptionHeader())

    def build(self, kind: int, length: int = None, value: Any = None):
        """
        Constructs the TCP option header by setting the kind, length, and value using the builder.

        Parameters:
        - kind (int): The kind identifier for the TCP option.
        - length (int, optional): The length of the option. If None, uses the default length defined by the builder.
        - value (Any, optional): The value of the option. If None, uses the default value defined by the builder.

        Returns:
        - TCPOptionHeader: The constructed TCP option header instance.
        """
        self._builder.set_kind(kind)
        self._builder.set_length(length)
        self._builder.set_value(value)
        return self._builder.build()
