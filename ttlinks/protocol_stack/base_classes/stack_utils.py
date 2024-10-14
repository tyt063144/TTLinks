from abc import ABC, abstractmethod


class ProtocolUnit(ABC):
    """
    Abstract base class representing a unit of a network protocol.

    The `ProtocolUnit` class defines a common interface for all protocol units,
    providing methods for converting the unit to bytes, generating a summary of its data,
    and retrieving the protocol-specific attributes.

    This class is intended to be subclassed by concrete protocol unit implementations.

    Properties:
    - as_bytes (abstract): Must be implemented to return the protocol unit's data in bytes format.
    - summary (abstract): Must be implemented to return a summary of the protocol unit's information as a dictionary.
    - attributes (abstract): Must be implemented to return detailed attributes of the protocol unit as a dictionary.

    Methods:
    - as_bytes: Abstract property that represents the byte representation of the protocol unit.
    - summary: Abstract property that represents a summary of the protocol unit, typically used for logging or debugging.
    - attributes: Abstract property that represents specific protocol attributes (e.g., headers, payload).
    """
    @property
    @abstractmethod
    def as_bytes(self) -> bytes:
        """
        Abstract method to return the protocol unit's data as a sequence of bytes.

        This method must be implemented by subclasses to provide the protocol unit's byte-level representation.

        Returns:
        bytes: The byte representation of the protocol unit.
        """
        pass

    @property
    @abstractmethod
    def summary(self) -> dict:
        """
        Abstract method to return a summary of the protocol unit's information.

        This method must be implemented by subclasses to return a dictionary
        summarizing key details about the protocol unit (e.g., metadata, type, size).

        Returns:
        dict: A dictionary containing a summary of the protocol unit.
        """
        pass

    @property
    @abstractmethod
    def attributes(self) -> dict:
        """
        Abstract method to return the protocol unit's detailed attributes.

        This method must be implemented by subclasses to return a dictionary of the protocol's specific attributes,
        which may include headers, payloads, and other protocol-specific fields.

        Returns:
        dict: A dictionary containing the protocol unit's attributes.
        """
        pass