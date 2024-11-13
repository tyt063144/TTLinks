import copy
from abc import ABC, abstractmethod
from typing import Union, Any

from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit


class Header(ABC):
    """
    Base abstract class representing a protocol header.

    This class follows the **Template Method** design pattern, where certain steps
    of the algorithm (header construction) are defined by the abstract methods,
    leaving the implementation details to the subclasses.

    The `Header` class is designed to manage and store various fields associated with
    a protocol header. It supports adding and retrieving fields by name.

    Methods:
    - add_field: Adds a field to the header.
    - get_field: Retrieves the value of a specified field.
    - _construct (abstract): To be implemented by subclasses to handle header construction.
    - unit (abstract property): Represents a ProtocolUnit related to the header.

    Parameters:
    None

    Attributes:
    _fields: Dictionary to store header fields and their corresponding values.

    Returns:
    None
    """
    def __init__(self):
        self._fields = {}

    def add_field(self, name:str, value: Any):
        """
        Adds a field to the header with a specified name and value.

        Parameters:
        name (str): The name of the field.
        value (Union[bytes, int]): The value of the field, which can be either bytes or an integer.

        Returns:
        None
        """
        self._fields[name] = value

    def get_field(self, name:str) -> Any:
        """
        Retrieves the value of the specified field.

        Parameters:
        name (str): The name of the field to retrieve.

        Returns:
        Union[bytes, int]: The value of the specified field or None if the field does not exist.
        """
        return self._fields.get(name)

    @abstractmethod
    def _construct(self):
        """
        Abstract method to construct the header. Must be implemented by subclasses.
        """
        pass

    @property
    @abstractmethod
    def unit(self) -> ProtocolUnit:
        """
        Abstract property representing a ProtocolUnit object associated with the header.
        Must be implemented by subclasses.
        """
        pass


class HeaderBuilder(ABC):
    """
    Abstract builder class for constructing a `Header` object.

    This class follows the **Builder** design pattern, which allows for the step-by-step
    construction of complex objects (in this case, the `Header`). The builder facilitates
    constructing the header and resetting its state to its original (backup) form.

    The **Builder Pattern** is useful when constructing a complex object requires multiple
    steps or when you want to control the creation process. This `HeaderBuilder` class is
    designed to manage the construction of a `Header` object and reset it if necessary.

    Methods:
    - reset: Restores the header to its backup state.
    - build: Returns the current header and resets it.

    Parameters:
    header (Header, optional): An instance of a Header object. Defaults to None.

    Attributes:
    _header: Stores the current header object being built.
    _backup_header: Stores a deep copy of the initial header for reset purposes.

    Returns:
    None
    """
    def __init__(self, header:Header=None):
        self._header = header
        self._backup_header = copy.deepcopy(self._header)

    def reset(self):
        """
        Restores the header to its backup state.

        If the current header differs from the backup, it replaces the current header
        with a deep copy of the original backup header.

        Parameters:
        None

        Returns:
        None
        """
        if self._header != self._backup_header:
            self._header = copy.deepcopy(self._backup_header)

    def build(self) -> Header:
        """
        Returns the current header and resets it to the backup state.

        This method finalizes the header being built and then resets the builder
        so that it can be reused to build a new header.

        Parameters:
        None

        Returns:
        Header: The finalized header object.
        """
        header = self._header
        self.reset()
        return header

