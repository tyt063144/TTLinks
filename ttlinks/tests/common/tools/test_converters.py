import pytest
from ttlinks.common.tools.converters import NumeralConverter

def test_binary_to_decimal():
    # Test converting binary to decimal
    assert NumeralConverter.binary_to_decimal("101010") == 42
    assert NumeralConverter.binary_to_decimal("1111") == 15

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.binary_to_decimal(101010)  # Not a string

def test_decimal_to_binary():
    # Test converting decimal to binary
    assert NumeralConverter.decimal_to_binary(42) == "00101010"
    assert NumeralConverter.decimal_to_binary(15, r_just=4) == "1111"

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.decimal_to_binary("42")  # Not an integer

def test_binary_to_hexadecimal():
    # Test converting binary to hexadecimal
    assert NumeralConverter.binary_to_hexadecimal("101010") == "2A"
    assert NumeralConverter.binary_to_hexadecimal("1111") == "F"

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.binary_to_hexadecimal(101010)  # Not a string

def test_hexadecimal_to_binary():
    # Test converting hexadecimal to binary
    assert NumeralConverter.hexadecimal_to_binary("2A") == "00101010"
    assert NumeralConverter.hexadecimal_to_binary("F", r_just=4) == "1111"

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.hexadecimal_to_binary(42)  # Not a string
    with pytest.raises(TypeError):
        NumeralConverter.hexadecimal_to_binary("G2")  # Invalid hexadecimal format

def test_hexadecimal_to_decimal():
    # Test converting hexadecimal to decimal
    assert NumeralConverter.hexadecimal_to_decimal("2A") == 42
    assert NumeralConverter.hexadecimal_to_decimal("F") == 15

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.hexadecimal_to_decimal(42)  # Not a string
    with pytest.raises(TypeError):
        NumeralConverter.hexadecimal_to_decimal("G2")  # Invalid hexadecimal format

def test_decimal_to_hexadecimal():
    # Test converting decimal to hexadecimal
    assert NumeralConverter.decimal_to_hexadecimal(42) == "2A"
    assert NumeralConverter.decimal_to_hexadecimal(15, r_just=2) == "0F"

    # Test invalid input
    with pytest.raises(TypeError):
        NumeralConverter.decimal_to_hexadecimal("42")  # Not an integer
