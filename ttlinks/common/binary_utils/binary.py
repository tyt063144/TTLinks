from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from ttlinks.common.tools.converters import NumeralConverter


class Binary(ABC):
    """
    Abstract base class for handling binary data representations. This class provides fundamental
    operations for binary strings and defines an abstract method for validation which must be
    implemented by subclasses.
    """
    def __init__(self, binary_string: str):
        """
        Initializes the Binary object with a given binary string after validating it.

        Args:
            binary_string (str): A string containing binary digits to be processed.
        """
        self._binary_string = None
        self._initialization(binary_string)

    @property
    def binary_digits(self) -> List[int]:
        """
        Converts the binary string into a list of integers for individual digit access.

        Returns:
            List[int]: A list of integers representing each digit in the binary string.
        """
        return [int(char) for char in self._binary_string]

    @property
    def binary_string(self) -> str:
        """
        Returns the binary string stored in the object.

        Returns:
            str: The binary string.
        """
        return self._binary_string

    @property
    def decimal(self) -> int:
        return NumeralConverter.binary_to_decimal(self._binary_string)

    @property
    def hex(self):
        return NumeralConverter.binary_to_hexadecimal(self._binary_string)

    def _initialization(self, binary_string: str) -> None:
        """
        Validates and initializes the binary string.

        Args:
            binary_string (str): The binary string to be validated and initialized.
        """
        self._validate(binary_string)
        self._binary_string = binary_string

    @abstractmethod
    def _validate(self, binary_string: str) -> None:
        """
        Validates the input string to ensure it contains only binary digits ('0' or '1').
        This method must be implemented by subclasses to include additional validation if necessary.

        Args:
            binary_string (str): The binary string to validate.

        Raises:
            ValueError: If the string contains characters other than '0' or '1'.
        """
        if not all(char in '01' for char in binary_string):
            raise ValueError("Invalid binary string. Must contain only 0s and 1s.")

    def __str__(self):
        """
        Returns the string representation of the binary data.

        Returns:
            str: The binary string.
        """
        return self._binary_string

    def __repr__(self) -> str:
        """
        Provides a machine-readable representation of the Binary object.

        Returns:
            str: A string representation of the Binary instance that includes the class name and the binary string.
        """
        return f"{self.__class__.__name__}(_binary_string={self._binary_string})"


class Octet(Binary):
    """
    Represents an octet, which is a specific type of Binary that consists of exactly 8 bits. This class provides
    additional validation for the length of the binary string.
    """

    @property
    def hex(self):
        return NumeralConverter.binary_to_hexadecimal(self._binary_string).rjust(2, '0')

    def _validate(self, binary_string: str) -> None:
        """
        Validates the binary string to ensure it is exactly 8 bits long, in addition to ensuring
        it contains only '0' or '1'. Overrides the basic validation provided by the Binary class.

        Args:
            binary_string (str): The binary string to validate.

        Raises:
            ValueError: If the binary string is not exactly 8 characters long or contains invalid characters.
        """
        super()._validate(binary_string)
        if len(binary_string) != 8:
            raise ValueError("An octet must be of length 8.")
