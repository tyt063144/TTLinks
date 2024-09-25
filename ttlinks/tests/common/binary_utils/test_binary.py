import pytest
from ttlinks.common.binary_utils import binary
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory


def test_octet_initialization():
    # Test valid octet initialization
    octet = OctetFlyWeightFactory().get_octet("10101010")
    assert octet.binary_string == '10101010'
    assert octet.binary_digits == [1, 0, 1, 0, 1, 0, 1, 0]
    assert octet.decimal == 170
    assert octet.hex == 'AA'


def test_octet_invalid_initialization():
    # Test invalid binary string (non-binary characters)
    with pytest.raises(ValueError, match="Invalid binary string. Must contain only 0s and 1s."):
        OctetFlyWeightFactory().get_octet("10102A10")

    # Test invalid length for octet (must be exactly 8 bits)
    with pytest.raises(ValueError, match="An octet must be of length 8."):
        OctetFlyWeightFactory().get_octet('10101')  # Less than 8 bits

    with pytest.raises(ValueError, match="An octet must be of length 8"):
        OctetFlyWeightFactory().get_octet('101010101010')  # More than 8 bits


def test_octet_str_and_repr():
    # Test __str__ and __repr__ methods
    octet = OctetFlyWeightFactory().get_octet('11001100')
    assert str(octet) == '11001100'
    assert repr(octet) == "Octet(_binary_string=11001100)"
