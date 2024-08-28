from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


class CoRHandler(ABC):
    """Abstract base class for handlers in the Chain of Responsibility pattern."""

    @abstractmethod
    def set_next(self, h: CoRHandler) -> CoRHandler:
        """Set the next handler in the chain."""
        pass

    @abstractmethod
    def handle(self, request):
        """Handle the request. Concrete handlers must implement this method."""
        pass


class BinaryClass:
    def __init__(self, binary_strings: str) -> None:
        """
        Initializes a BinaryClass with a validated binary string.

        Args:
        binary_strings (str): A string that should only contain the characters '0' or '1'.

        Raises:
        ValueError: If the binary_strings contains any characters other than '0' or '1'.
        """
        self.__binary_strings = self._validate_binary(binary_strings)

    @staticmethod
    def _validate_binary(binary_to_validate: str) -> str:
        """
        Validates if the provided string is a binary string.

        Args:
        binary_to_validate (str): The binary string to validate.

        Returns:
        str: The validated binary string.

        Raises:
        ValueError: If binary_to_validate contains any characters other than '0' or '1'.
        """
        if not all(char in '01' for char in binary_to_validate):
            raise ValueError("Invalid binary string. Must contain only 0s and 1s.")
        return binary_to_validate

    def binary_digits(self) -> List[int]:
        """
        Converts the binary string to a list of integers.

        Returns:
        List[int]: A list of integers representing the binary digits.
        """
        return list(map(int, self.__binary_strings))

    def __str__(self):
        return self.__binary_strings

    def __repr__(self) -> str:
        """
        Returns a string representation of the BinaryClass instance.

        Returns:
        str: The formal string representation of the BinaryClass, suitable for debugging.
        """
        return f"BinaryClass(binary_string='{self.__binary_strings}')"


class BinaryFlyWeight:
    def __init__(self, binary_string: str) -> None:
        """
        Initializes a BinaryFlyWeight with a binary string.

        Args:
        binary_string (str): The binary string to store.
        """
        self.__binary_string = binary_string

    def get_binary_string(self) -> str:
        """
        Retrieves the stored binary string.

        Returns:
        str: The binary string.
        """
        return self.__binary_string


class BinaryFlyWeightFactory:
    __instance = None
    __flyweights: Dict[str, BinaryClass] = {}

    def __new__(cls):
        """
        Ensures that only one instance of BinaryFlyWeightFactory exists.
        """
        if cls.__instance is None:
            cls.__instance = super(BinaryFlyWeightFactory, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def get_binary_flyweight(cls):
        """
        Retrieves the dictionary of flyweight instances.

        Returns:
        Dict[str, BinaryClass]: The dictionary containing all the flyweights.
        """
        return cls.__flyweights

    @classmethod
    def get_binary_class(cls, binary_string) -> BinaryClass:
        """
        Retrieves or creates a BinaryClass instance for the given binary string.

        Args:
        binary_string (str): The binary string for which a BinaryClass is required.

        Returns:
        BinaryClass: The BinaryClass instance corresponding to the binary string.
        """
        binary_class = cls.__flyweights.get(binary_string)
        if binary_class is None:
            binary_class = BinaryClass(binary_string)
            cls.__flyweights[binary_string] = binary_class
        return binary_class
