import pytest
from ttlinks.macservice.mac_converters import (
    BinaryDigitsMAC48ConverterHandler,
    DashedHexMAC48ConverterHandler,
    ColonHexMAC48ConverterHandler,
    DotHexMAC48ConverterHandler,
    DecimalMAC48ConverterHandler,
    BytesMAC48ConverterHandler,
    BinaryDigitsOUI24ConverterHandler,
    DashedHexOUI24ConverterHandler,
    ColonHexOUI24ConverterHandler,
    DotHexOUI24ConverterHandler,
    BytesMAC24ConverterHandler,
    OctetEUI64ConverterHandler,
    MACConverter
)

@pytest.mark.parametrize("binary_mac, expected", [
    ([0, 1] * 24, b'\x55\x55\x55\x55\x55\x55'),  # 01010101 01010101 01010101 01010101 01010101 01010101
    ([1, 0] * 24, b'\xAA\xAA\xAA\xAA\xAA\xAA')   # 10101010 10101010 10101010 10101010 10101010 10101010
])
def test_binary_digits_mac48_converter(binary_mac, expected):
    handler = BinaryDigitsMAC48ConverterHandler()
    assert handler.handle(binary_mac) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AA-BB-CC-DD-EE-FF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),
    ("00-11-22-33-44-55", b'\x00\x11\x22\x33\x44\x55')
])
def test_dashed_hex_mac48_converter(mac_str, expected):
    handler = DashedHexMAC48ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AA:BB:CC:DD:EE:FF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),
    ("00:11:22:33:44:55", b'\x00\x11\x22\x33\x44\x55')
])
def test_colon_hex_mac48_converter(mac_str, expected):
    handler = ColonHexMAC48ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AABB.CCDD.EEFF", b'\xAA\xBB\xCC\xDD\xEE\xFF'),
    ("0011.2233.4455", b'\x00\x11\x22\x33\x44\x55')
])
def test_dot_hex_mac48_converter(mac_str, expected):
    handler = DotHexMAC48ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("decimal_mac, expected", [
    (281474976710655, b'\xFF\xFF\xFF\xFF\xFF\xFF'),  # Maximum MAC address (0xFFFFFFFFFFFF)
    (1250999896491, b'\x01\x23\x45\x67\x89\xAB')    # 0x0123456789AB
])
def test_decimal_mac48_converter(decimal_mac, expected):
    handler = DecimalMAC48ConverterHandler()
    assert handler.handle(decimal_mac) == expected


@pytest.mark.parametrize("byte_mac, expected", [
    (b'\xAA\xBB\xCC\xDD\xEE\xFF', b'\xAA\xBB\xCC\xDD\xEE\xFF'),
    (b'\x00\x11\x22\x33\x44\x55', b'\x00\x11\x22\x33\x44\x55')
])
def test_bytes_mac48_converter(byte_mac, expected):
    handler = BytesMAC48ConverterHandler()
    assert handler.handle(byte_mac) == expected


@pytest.mark.parametrize("binary_oui, expected", [
    ([0, 1] * 12, b'\x55\x55\x55\x00\x00\x00'),
    ([1, 0] * 12, b'\xAA\xAA\xAA\x00\x00\x00')
])
def test_binary_digits_oui24_converter(binary_oui, expected):
    handler = BinaryDigitsOUI24ConverterHandler()
    assert handler.handle(binary_oui) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AA-BB-CC", b'\xAA\xBB\xCC\x00\x00\x00'),
    ("00-11-22", b'\x00\x11\x22\x00\x00\x00')
])
def test_dashed_hex_oui24_converter(mac_str, expected):
    handler = DashedHexOUI24ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AA:BB:CC", b'\xAA\xBB\xCC\x00\x00\x00'),
    ("00:11:22", b'\x00\x11\x22\x00\x00\x00')
])
def test_colon_hex_oui24_converter(mac_str, expected):
    handler = ColonHexOUI24ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("mac_str, expected", [
    ("AABB.CC", b'\xAA\xBB\xCC\x00\x00\x00'),
    ("0011.22", b'\x00\x11\x22\x00\x00\x00')
])
def test_dot_hex_oui24_converter(mac_str, expected):
    handler = DotHexOUI24ConverterHandler()
    assert handler.handle(mac_str) == expected


@pytest.mark.parametrize("byte_oui, expected", [
    (b'\xAA\xBB\xCC', b'\xAA\xBB\xCC\x00\x00\x00'),
    (b'\x00\x11\x22', b'\x00\x11\x22\x00\x00\x00')
])
def test_bytes_oui24_converter(byte_oui, expected):
    handler = BytesMAC24ConverterHandler()
    assert handler.handle(byte_oui) == expected


@pytest.mark.parametrize("mac_bytes, expected", [
    (b'\x00\x11\x22\x33\x44\x55', b'\x00\x11\x22\xFF\xFE\x33\x44\x55'),
    (b'\xAA\xBB\xCC\xDD\xEE\xFF', b'\xAA\xBB\xCC\xFF\xFE\xDD\xEE\xFF')
])
def test_octet_eui64_converter(mac_bytes, expected):
    handler = OctetEUI64ConverterHandler()
    assert handler.handle(mac_bytes) == expected


def test_mac_converter():
    assert MACConverter.convert_mac("AA-BB-CC-DD-EE-FF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac("AA:BB:CC:DD:EE:FF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac("AABB.CCDD.EEFF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac(281474976710655) == b'\xFF\xFF\xFF\xFF\xFF\xFF'
    assert MACConverter.convert_mac(b'\xAA\xBB\xCC\xDD\xEE\xFF') == b'\xAA\xBB\xCC\xDD\xEE\xFF'


def test_invalid_mac_formats():
    handler = DashedHexMAC48ConverterHandler()
    assert handler.handle("AA-BB-CC-DD-EE") is None  # Invalid length
    assert handler.handle("ZZ-BB-CC-DD-EE-FF") is None  # Invalid characters

def test_mac_converter_valid_cases():
    assert MACConverter.convert_mac("AA-BB-CC-DD-EE-FF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac("AA:BB:CC:DD:EE:FF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac("AABB.CCDD.EEFF") == b'\xAA\xBB\xCC\xDD\xEE\xFF'
    assert MACConverter.convert_mac(281474976710655) == b'\xFF\xFF\xFF\xFF\xFF\xFF'
    assert MACConverter.convert_mac(b'\xAA\xBB\xCC\xDD\xEE\xFF') == b'\xAA\xBB\xCC\xDD\xEE\xFF'

def test_mac_converter_invalid_cases():
    assert MACConverter.convert_mac("AA-BB-CC-DD-EE") is None  # Too short
    assert MACConverter.convert_mac("ZZ-BB-CC-DD-EE-FF") is None  # Invalid hex
    assert MACConverter.convert_mac("AA:BB:CC:DD:EE:FF:11") is None  # Too long
    assert MACConverter.convert_mac("00.11.22.33.44") is None  # Not enough bytes
    assert MACConverter.convert_mac(-1) is None  # Negative number
    assert MACConverter.convert_mac(281474976710656) is None  # Too large for MAC
    assert MACConverter.convert_mac("") is None  # Empty input

def test_mac_converter_to_eui64():
    assert MACConverter.convert_to_eui64("00-11-22-33-44-55") == b'\x00\x11\x22\xFF\xFE\x33\x44\x55'
    assert MACConverter.convert_to_eui64("AA:BB:CC:DD:EE:FF") == b'\xAA\xBB\xCC\xFF\xFE\xDD\xEE\xFF'
    assert MACConverter.convert_to_eui64("AABB.CCDD.EEFF") == b'\xAA\xBB\xCC\xFF\xFE\xDD\xEE\xFF'
    assert MACConverter.convert_to_eui64(b'\x00\x11\x22\x33\x44\x55') == b'\x00\x11\x22\xFF\xFE\x33\x44\x55'
    assert MACConverter.convert_to_eui64("AA-BB") is None  # Too short
    assert MACConverter.convert_to_eui64("ZZ-BB-CC-DD-EE-FF") is None  # Invalid hex
