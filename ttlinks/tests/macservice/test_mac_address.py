import pytest

from ttlinks.macservice import MACType
from ttlinks.macservice.mac_address import MACAddr
# from ttlinks.common.tools.converters import NumeralConverter

@pytest.mark.parametrize("input_mac, expected_bytes", [
    ("AA-BB-CC-DD-EE-FF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),  # Dashed Hex
    ("AA:BB:CC:DD:EE:FF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),  # Colon Hex
    ("AABB.CCDD.EEFF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),  # Dotted Hex
    (281474976710655, b'\xFF\xFF\xFF\xFF\xFF\xFF'),  # Decimal
    (b'\x00\x11\x22\x33\x44\x55', b'\x00\x11\x22\x33\x44\x55'),  # Bytes
])
def test_mac_address_initialization(input_mac, expected_bytes):
    """
    Test valid MAC address inputs in different formats.
    """
    mac = MACAddr(input_mac)
    assert mac._address == expected_bytes


@pytest.mark.parametrize("invalid_mac", [
    "AA-BB-CC-DD-EE",  # Too short
    "AA:BB:CC:DD:EE:FF:00",  # Too long
    "GG-HH-II-JJ-KK-LL",  # Non-hex characters
    "01-23-45-67-89",  # Missing octet
    281474976710656,  # Exceeds 48-bit limit
    -1,  # Negative number
    "",  # Empty string
    None,  # NoneType
    1234567890123456,  # Too large integer
])
def test_invalid_mac_address_initialization(invalid_mac):
    """
    Test invalid MAC address inputs.
    """
    with pytest.raises(ValueError):
        MACAddr(invalid_mac)


@pytest.mark.parametrize("input_mac, expected_type", [
    (b'\xff\xff\xff\xff\xff\xff', MACType.BROADCAST),  # Broadcast Address
    (b'\x00\x11\x22\x33\x44\x55', MACType.UNICAST),  # Standard Unicast
    (b'\x02\xAA\xBB\xCC\xDD\xEE', MACType.UNICAST),  # LSB = 0 (Unicast)
    (b'\x01\x00\x5e\x00\x00\xfb', MACType.MULTICAST),  # IPv4 Multicast
    (b'\x33\x33\x00\x00\x00\x01', MACType.MULTICAST),  # IPv6 Multicast
])
def test_mac_address_classification(input_mac, expected_type):
    """
    Test MAC address classification (Unicast, Multicast, Broadcast).
    """
    mac = MACAddr(input_mac)
    assert mac.mac_type == expected_type


def test_mac_address_oui_lookup():
    """
    Test OUI lookup (mocked to return a test vendor).
    """
    mac = MACAddr("08-BF-B8-34-00-00")
    assert len(mac.oui) == 1
    assert mac.oui[0].record == {'oui_id': '08BFB8', 'start_hex': '000000', 'end_hex': 'FFFFFF', 'start_decimal': 9619518783488, 'end_decimal': 9619535560703, 'block_size': 16777215, 'oui_type': 'MA_L', 'organization': 'ASUSTek COMPUTER INC.', 'address': 'No.15,Lide Rd., Beitou, Dist.,Taipei 112,Taiwan Taipei Taiwan TW 112'}


@pytest.mark.parametrize("input_mac, expected_binary", [
    ("AA-BB-CC-DD-EE-FF", "101010101011101111001100110111011110111011111111"),
    ("00-11-22-33-44-55", "000000000001000100100010001100110100010001010101"),
    ("FF-FF-FF-FF-FF-FF", "111111111111111111111111111111111111111111111111"),
])
def test_mac_binary_string(input_mac, expected_binary):
    """
    Test binary string representation of MAC address.
    """
    mac = MACAddr(input_mac)
    assert mac.binary_string == expected_binary


@pytest.mark.parametrize("input_mac, expected_hex", [
    ("AA-BB-CC-DD-EE-FF", "AABBCCDDEEFF"),
    ("00-11-22-33-44-55", "001122334455"),
    ("FF-FF-FF-FF-FF-FF", "FFFFFFFFFFFF"),
])
def test_mac_hexadecimal_representation(input_mac, expected_hex):
    """
    Test hexadecimal string representation of MAC address.
    """
    mac = MACAddr(input_mac)
    assert mac.as_hexadecimal == expected_hex


@pytest.mark.parametrize("input_mac, expected_decimal", [
    ("AA-BB-CC-DD-EE-FF", 187723572702975),
    ("00-11-22-33-44-55", 73588229205),
    ("FF-FF-FF-FF-FF-FF", 281474976710655),
])
def test_mac_decimal_representation(input_mac, expected_decimal):
    """
    Test decimal representation of MAC address.
    """
    mac = MACAddr(input_mac)
    assert mac.as_decimal == expected_decimal


@pytest.mark.parametrize("input_mac, expected_string", [
    ("AA-BB-CC-DD-EE-FF", "AA:BB:CC:DD:EE:FF"),
    ("00-11-22-33-44-55", "00:11:22:33:44:55"),
    ("FF-FF-FF-FF-FF-FF", "FF:FF:FF:FF:FF:FF"),
])
def test_mac_string_representation(input_mac, expected_string):
    """
    Test human-readable string representation of MAC address.
    """
    mac = MACAddr(input_mac)
    assert str(mac) == expected_string


@pytest.mark.parametrize("invalid_mac", [
    "AA-BB-CC-DD-EE",  # Too short
    "GG-HH-II-JJ-KK-LL",  # Non-hex characters
    None,  # NoneType
    1234567890123456,  # Too large integer
])
def test_mac_address_validation_raises_exception(invalid_mac):
    """
    Ensure validation raises ValueError for invalid MAC inputs.
    """
    with pytest.raises(ValueError):
        MACAddr(invalid_mac)
