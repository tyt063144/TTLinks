from __future__ import annotations

import re


class NumeralConverter:

    @staticmethod
    def binary_to_decimal(binary_string: str) -> int:
        """
        Converts a binary string to its decimal (base-10) equivalent.

        Parameters:
        binary_string (str): A binary string to be converted.

        Returns:
        int: The decimal equivalent of the binary string.

        Raises:
        TypeError: If the input is not a string.
        """
        if type(binary_string) is not str:
            raise TypeError("Binary must be a string.")
        return int(binary_string, 2)

    @staticmethod
    def decimal_to_binary(decimal: int, r_just: int = 8) -> str:
        """
        Converts a decimal (base-10) number to its binary string equivalent,
        with optional right-justified padding.

        Parameters:
        decimal (int): The decimal number to convert.
        r_just (int): The number of digits to right-justify the binary output (default is 8).

        Returns:
        str: The binary string equivalent of the decimal number.

        Raises:
        TypeError: If the input types are not as expected (int for both parameters).
        """
        if type(decimal) is not int:
            raise TypeError("decimal must be an int.")
        if type(r_just) is not int:
            raise TypeError("r_just must be an int.")
        return bin(decimal)[2:].rjust(r_just, '0')

    @staticmethod
    def binary_to_hexadecimal(binary_string: str) -> str:
        """
        Converts a binary string to its hexadecimal string equivalent.

        Parameters:
        binary (str): A binary string to be converted.

        Returns:
        str: The hexadecimal string equivalent of the binary number.

        Raises:
        TypeError: If the input is not a string.
        """
        if type(binary_string) is not str:
            raise TypeError("binary must be a string.")
        decimal_value = int(binary_string, 2)
        hexadecimal_string = hex(decimal_value)[2:]
        return hexadecimal_string.upper()

    @staticmethod
    def hexadecimal_to_binary(hexadecimal: str, r_just: int = 8) -> str:
        """
        Converts a hexadecimal string to its binary string equivalent, with optional right-justified padding.

        Parameters:
        hexadecimal (str): A hexadecimal string to be converted.
        r_just (int): The number of digits to right-justify the binary output (default is 8).

        Returns:
        str: The binary string equivalent of the hexadecimal number.

        Raises:
        TypeError: If the input types are not as expected (string for hexadecimal, int for r_just).
        """
        if type(hexadecimal) is not str:
            raise TypeError("hexadecimal is not a string.")
        if not re.match(r"^[0-9A-F]+$", hexadecimal.upper()):
            raise TypeError("wrong hexadecimal format.")
        if type(r_just) is not int:
            raise TypeError("r_just is not a int.")
        decimal_value = int(hexadecimal, 16)
        binary_string = bin(decimal_value)[2:].rjust(r_just, '0')
        return binary_string

    @staticmethod
    def hexadecimal_to_decimal(hexadecimal: str) -> int:
        """
        Converts a hexadecimal string to its decimal (base-10) equivalent.

        Parameters:
        hexadecimal (str): A hexadecimal string to be converted.

        Returns:
        int: The decimal equivalent of the hexadecimal number.

        Raises:
        TypeError: If the input is not a string.
        """
        if type(hexadecimal) is not str:
            raise TypeError("hexadecimal must be a string.")
        if not re.match(r"^[0-9A-F]+$", hexadecimal.upper()):
            raise TypeError("wrong hexadecimal format.")
        return int(hexadecimal, 16)

    @staticmethod
    def decimal_to_hexadecimal(decimal: int, r_just: int = 2) -> str:
        """
        Converts a decimal (base-10) number to its hexadecimal string equivalent,
        with optional right-justified padding.

        Parameters:
        decimal (int): The decimal number to convert.
        r_just (int): The number of digits to right-justify the hexadecimal output (default is 2).

        Returns:
        str: The hexadecimal string equivalent of the decimal number.

        Raises:
        TypeError: If the input types are not as expected (int for both parameters).
        """
        if type(decimal) is not int:
            raise TypeError("decimal must be an int.")
        return hex(decimal)[2:].upper().rjust(r_just, '0')

    @staticmethod
    def bytes_to_decimal(byte_string: bytes) -> int:
        """
        Converts a bytes object to its decimal (base-10) equivalent.

        Parameters:
        byte_string (bytes): A bytes object to be converted.

        Returns:
        int: The decimal equivalent of the bytes object.

        Raises:
        TypeError: If the input is not a bytes object.
        """
        if type(byte_string) is not bytes:
            raise TypeError("byte_string must be a bytes object.")
        return int.from_bytes(byte_string, byteorder='big')

    @staticmethod
    def decimal_to_bytes(decimal: int, length: int) -> bytes:
        """
        Converts a decimal (base-10) number to a bytes object of a specified length.

        Parameters:
        decimal (int): The decimal number to convert.
        length (int): The number of bytes in the output.

        Returns:
        bytes: The bytes object representing the decimal number.

        Raises:
        TypeError: If the input types are not as expected (int for both parameters).
        """
        if type(decimal) is not int:
            raise TypeError("decimal must be an int.")
        if type(length) is not int:
            raise TypeError("length must be an int.")
        return decimal.to_bytes(length, byteorder='big')

    @staticmethod
    def binary_to_bytes(binary_string: str, length: int) -> bytes:
        """
        Converts a binary string to a bytes object of a specified length.

        Parameters:
        binary_string (str): A binary string to be converted.
        length (int): The number of bytes in the output.

        Returns:
        bytes: The bytes object representing the binary string.

        Raises:
        TypeError: If the input types are not as expected (str for binary_string, int for length).
        """
        if type(binary_string) is not str:
            raise TypeError("binary_string must be a string.")
        if type(length) is not int:
            raise TypeError("length must be an int.")
        return int(binary_string, 2).to_bytes(length, byteorder='big')

    @staticmethod
    def hexadecimal_to_bytes(hex_string: str, length: int) -> bytes:
        """
        Converts a hexadecimal string to a bytes object of a specified length.

        Parameters:
        hex_string (str): A hexadecimal string to be converted.
        length (int): The number of bytes in the output.

        Returns:
        bytes: The bytes object representing the hexadecimal string.

        Raises:
        TypeError: If the input types are not as expected (str for hex_string, int for length).
        """
        if type(hex_string) is not str:
            raise TypeError("hex_string must be a string.")
        if type(length) is not int:
            raise TypeError("length must be an int.")
        return bytes.fromhex(hex_string.rjust(length * 2, '0'))

    @staticmethod
    def bytes_to_binary(byte_string: bytes, r_just: int = 8) -> str:
        """
        Converts a bytes object to its binary string equivalent, with optional right-justified padding.

        Parameters:
        byte_string (bytes): A bytes object to be converted.
        r_just (int): The number of digits to right-justify the binary output (default is 8).

        Returns:
        str: The binary string equivalent of the bytes object.

        Raises:
        TypeError: If the input types are not as expected (bytes for byte_string, int for r_just).
        """
        if type(byte_string) is not bytes:
            raise TypeError("byte_string must be a bytes object.")
        if type(r_just) is not int:
            raise TypeError("r_just must be an int.")
        return bin(int.from_bytes(byte_string, byteorder='big'))[2:].rjust(r_just, '0')

    @staticmethod
    def bytes_to_hexadecimal(byte_string: bytes, r_just: int = 2) -> str:
        """
        Converts a bytes object to its hexadecimal string equivalent, with optional right-justified padding.

        Parameters:
        byte_string (bytes): A bytes object to be converted.
        r_just (int): The number of digits to right-justify the hexadecimal output (default is 2).

        Returns:
        str: The hexadecimal string equivalent of the bytes object.

        Raises:
        TypeError: If the input types are not as expected (bytes for byte_string, int for r_just).
        """
        if type(byte_string) is not bytes:
            raise TypeError("byte_string must be a bytes object.")
        if type(r_just) is not int:
            raise TypeError("r_just must be an int.")
        return byte_string.hex().upper().rjust(r_just * 2, '0')