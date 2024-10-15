import pytest

from ttlinks.common.algorithm.checksum import ChecksumCalculator, InternetChecksum


@pytest.fixture
def internet_checksum_calculator():
    """
    A pytest fixture to create an instance of ChecksumCalculator using InternetChecksum algorithm.
    """
    return ChecksumCalculator(InternetChecksum())

def test_internet_checksum_basic(internet_checksum_calculator):
    """
    Test the InternetChecksum algorithm with a simple byte sequence.
    """
    data = b"\x01\x02\x03\x04"
    checksum = internet_checksum_calculator.calculate(data)
    assert isinstance(checksum, int), "Checksum should be an integer"
    assert checksum == 0xFBF9, f"Expected checksum to be 0xFBF9, but got {hex(checksum)}"

def test_internet_checksum_odd_length(internet_checksum_calculator):
    """
    Test the InternetChecksum algorithm with an odd-length byte sequence, which should be padded.
    """
    data = b"\x01\x02\x03"
    checksum = internet_checksum_calculator.calculate(data)
    assert isinstance(checksum, int), "Checksum should be an integer"
    assert checksum == 0xFBFD, f"Expected checksum to be 0xFBFD, but got {hex(checksum)}"

def test_internet_checksum_empty_data(internet_checksum_calculator):
    """
    Test the InternetChecksum algorithm with empty data.
    """
    data = b""
    checksum = internet_checksum_calculator.calculate(data)
    assert checksum == 0xFFFF, f"Expected checksum to be 0xFFFF, but got {hex(checksum)}"

def test_internet_checksum_large_data(internet_checksum_calculator):
    """
    Test the InternetChecksum algorithm with a large sequence of bytes.
    """
    data = b"\xff" * 1000  # A large byte sequence filled with 0xff
    checksum = internet_checksum_calculator.calculate(data)
    assert isinstance(checksum, int), "Checksum should be an integer"
    assert checksum == 0x0000, f"Expected checksum to be 0x0000, but got {hex(checksum)}"

def test_internet_checksum_boundary_case(internet_checksum_calculator):
    """
    Test the InternetChecksum algorithm with data length exactly on a 16-bit boundary.
    """
    data = b"\x12\x34" * 100
    checksum = internet_checksum_calculator.calculate(data)
    assert isinstance(checksum, int), "Checksum should be an integer"
    assert checksum == 0xE3A8, f"Expected checksum to be 0xE3A8, but got {hex(checksum)}"
