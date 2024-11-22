from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.ipservice.ip_converters import (
    BinaryDigitsIPv4ConverterHandler, CIDRIPv4ConverterHandler,
    DotIPv4ConverterHandler, BinaryDigitsIPv6ConverterHandler,
    CIDRIPv6ConverterHandler, ColonIPv6ConverterHandler
)


# IPv4 Binary Digits Handler Tests
def test_binary_digits_ipv4_handler_valid_address():
    request = [
        1, 1, 0, 0, 0, 0, 0, 0,  # 192
        1, 0, 1, 0, 1, 0, 0, 0,  # 168
        0, 0, 0, 0, 0, 0, 0, 1,  # 1
        0, 0, 0, 0, 0, 0, 0, 1  # 1
    ]
    expected_bytes = b'\xc0\xa8\x01\x01'
    converter = BinaryDigitsIPv4ConverterHandler()
    result = converter.handle(request)
    assert result == expected_bytes, "Should correctly convert binary digits to octets for a valid IPv4 address."


def test_binary_digits_ipv4_handler_incorrect_number_of_digits():
    request_short = [1, 1, 0, 0]  # Too few digits
    request_long = [1] * 33  # Too many digits
    converter = BinaryDigitsIPv4ConverterHandler()
    assert converter.handle(request_short) is None, "Should return None for too few binary digits."
    assert converter.handle(request_long) is None, "Should return None for too many binary digits."


def test_binary_digits_ipv4_handler_invalid_digit_values():
    request = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 1, 0, 1, 0, 1, 1, 0, 2, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0]
    converter = BinaryDigitsIPv4ConverterHandler()
    result = converter.handle(request)
    assert result is None, "Should return None for invalid binary values."


def test_binary_digits_ipv4_handler_empty_list():
    request = []
    converter = BinaryDigitsIPv4ConverterHandler()
    result = converter.handle(request)
    assert result is None, "Should return None for an empty list of binary digits."


def test_binary_digits_ipv4_handler_none_input():
    converter = BinaryDigitsIPv4ConverterHandler()
    result = converter.handle(None)
    assert result is None, "Should return None when None is passed as input."


# IPv4 CIDR Handler Tests
def test_cidr_ipv4_handler_valid_notation():
    converter = CIDRIPv4ConverterHandler()
    test_cases = [
        ("/24", [255, 255, 255, 0]),
        ("/16", [255, 255, 0, 0]),
        ("/8", [255, 0, 0, 0]),
        ("/32", [255, 255, 255, 255]),
        ("/0", [0, 0, 0, 0])
    ]
    for cidr, expected in test_cases:
        result = [x for x in converter.handle(cidr)]
        assert result == expected, f"Failed for CIDR {cidr}. Expected {expected}, got {result}"


def test_cidr_ipv4_handler_invalid_notation():
    invalid_cidrs = ["/33", "/-1", "/abc", "192.168.1.0/24", "/"]
    converter = CIDRIPv4ConverterHandler()
    for cidr in invalid_cidrs:
        result = converter.handle(cidr)
        assert result is None, f"Should return None for invalid CIDR {cidr}"


def test_cidr_ipv4_handler_non_string_input():
    non_strings = [None, 24, [], {}, 192168010]
    converter = CIDRIPv4ConverterHandler()
    for input_val in non_strings:
        result = converter.handle(input_val)
        assert result is None, f"Should return None for non-string input {input_val}"


def test_cidr_ipv4_handler_empty_string():
    converter = CIDRIPv4ConverterHandler()
    result = converter.handle("")
    assert result is None, "Should return None for an empty string input"


# IPv4 Dot Handler Tests
def test_dot_ipv4_handler_valid_address():
    converter = DotIPv4ConverterHandler()
    ipv4_address = "192.168.1.1"
    expected = b'\xc0\xa8\x01\x01'
    result = converter.handle(ipv4_address)
    assert result == expected, f"Should correctly convert {ipv4_address} to octets."


def test_dot_ipv4_handler_invalid_address():
    converter = DotIPv4ConverterHandler()
    invalid_addresses = ["192.168.256.1", "10.10.10", "10.10", "300.300.300.300", "192.168.1.1.1"]
    for address in invalid_addresses:
        result = converter.handle(address)
        assert result is None, f"Should return None for invalid IPv4 address {address}"


def test_dot_ipv4_handler_non_string_input():
    converter = DotIPv4ConverterHandler()
    non_strings = [None, 12345, 19216801, ["192", "168", "1", "1"], {"ip": "192.168.1.1"}]
    for input_val in non_strings:
        result = converter.handle(input_val)
        assert result is None, f"Should return None for non-string input {input_val}"


def test_dot_ipv4_handler_empty_string():
    converter = DotIPv4ConverterHandler()
    result = converter.handle("")
    assert result is None, "Should return None for an empty string input"


# IPv6 Binary Digits Handler Tests
def test_binary_digits_ipv6_handler_valid_address():
    converter = BinaryDigitsIPv6ConverterHandler()
    request = [0] * 64 + [1] * 64  # Simplified example of ::FFFF:FFFF:FFFF:FFFF
    expected_octets = b'\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'
    result = converter.handle(request)
    assert result == expected_octets, "Should correctly convert 128 binary digits to octets for a valid IPv6 address."


def test_binary_digits_ipv6_handler_incorrect_number_of_digits():
    converter = BinaryDigitsIPv6ConverterHandler()
    request_short = [0] * 100  # Too few digits
    request_long = [0] * 140  # Too many digits
    assert converter.handle(request_short) is None, "Should return None for too few binary digits."
    assert converter.handle(request_long) is None, "Should return None for too many binary digits."


def test_binary_digits_ipv6_handler_invalid_digit_values():
    converter = BinaryDigitsIPv6ConverterHandler()
    request_invalid = [2] * 128  # Invalid binary digit values
    result = converter.handle(request_invalid)
    assert result is None, "Should return None for invalid binary values."


def test_binary_digits_ipv6_handler_empty_list():
    converter = BinaryDigitsIPv6ConverterHandler()
    result = converter.handle([])
    assert result is None, "Should return None for an empty list of binary digits."


def test_binary_digits_ipv6_handler_none_input():
    converter = BinaryDigitsIPv6ConverterHandler()
    result = converter.handle(None)
    assert result is None, "Should return None when None is passed as input."


def test_binary_digits_ipv6_handler_non_integer_list():
    converter = BinaryDigitsIPv6ConverterHandler()
    request = ['0', '1', '0', '1'] * 32  # Non-integer inputs
    result = converter.handle(request)
    assert result is None, "Should return None for non-integer input items."


# IPv6 CIDR Handler Tests
def test_cidr_ipv6_handler_valid_notation():
    converter = CIDRIPv6ConverterHandler()
    test_cases = [
        ("/64", ['11111111'] * 8 + ['00000000'] * 8),
        ("/128", ['11111111'] * 16),
        ("/0", ['00000000'] * 16),
        ("/32", ['11111111'] * 4 + ['00000000'] * 12),
        ("/114", ['11111111'] * 14 + ['11000000', '00000000'])
    ]
    for cidr, expected in test_cases:
        expected_octets = NumeralConverter.binary_to_bytes(''.join(expected), 16)
        result = converter.handle(cidr)
        assert result == expected_octets, f"Failed for CIDR {cidr}. Expected {expected_octets}, got {result}"


def test_cidr_ipv6_handler_invalid_notation():
    converter = CIDRIPv6ConverterHandler()
    invalid_cidrs = ["/129", "/-1", "192.168.1.0/24", "/abc", "", "/ "]
    for cidr in invalid_cidrs:
        result = converter.handle(cidr)
        assert result is None, f"Should return None for invalid CIDR {cidr}"


def test_cidr_ipv6_handler_non_string_input():
    converter = CIDRIPv6ConverterHandler()
    non_strings = [None, 24, [], {}, 19216801]
    for input_val in non_strings:
        result = converter.handle(input_val)
        assert result is None, f"Should return None for non-string input {input_val}"


def test_cidr_ipv6_handler_empty_string():
    converter = CIDRIPv6ConverterHandler()
    result = converter.handle("")
    assert result is None, "Should return None for an empty string input"


# IPv6 Colon Handler Tests
def test_colon_ipv6_handler_valid_address():
    converter = ColonIPv6ConverterHandler()
    test_cases = [
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334",
         ["00100000", "00000001", "00001101", "10111000", "10000101", "10100011", "00000000", "00000000",
          "00000000", "00000000", "10001010", "00101110", "00000011", "01110000", "01110011", "00110100"]),
        ("2001:db8::1",
         ["00100000", "00000001", "00001101", "10111000", "00000000", "00000000", "00000000", "00000000",
          "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000001"]),
        ("::1",
         ["00000000"] * 15 + ["00000001"]),
        ("::",
         ["00000000"] * 16)
    ]
    for ipv6, expected_binaries in test_cases:
        expected_octets = NumeralConverter.binary_to_bytes(''.join(expected_binaries), 16)
        result = converter.handle(ipv6)
        assert result == expected_octets, f"Failed for IPv6 {ipv6}. Expected {expected_octets}, got {result}"


def test_colon_ipv6_handler_invalid_address():
    converter = ColonIPv6ConverterHandler()
    invalid_addresses = ["2001:0db8:85a3:0000:0000:8a2e:0370:7334:8765",  # Too many segments
                         "2001:db8::85a3::7334",  # Double "::"
                         "2001:0dbg:85a3::7334",  # Invalid hex character
                         "2001:db8::85a3:"]  # Incomplete segment
    for address in invalid_addresses:
        result = converter.handle(address)
        assert result is None, f"Should return None for invalid IPv6 address {address}"


def test_colon_ipv6_handler_non_string_input():
    converter = ColonIPv6ConverterHandler()
    non_strings = [None, 12345, 19216801, ["2001", "0db8", "85a3"], {"ip": "2001:db8::1"}]
    for input_val in non_strings:
        result = converter.handle(input_val)
        assert result is None, f"Should return None for non-string input {input_val}"


def test_colon_ipv6_handler_empty_string():
    converter = ColonIPv6ConverterHandler()
    result = converter.handle("")
    assert result is None, "Should return None for an empty string input"


# IPv4 Binary Digits Handler Tests
def test_binary_digits_ipv4_handler_boundary_values():
    converter = BinaryDigitsIPv4ConverterHandler()
    # Test with exactly 32 binary digits
    request = [1] * 32
    result = converter.handle(request)
    assert result is not None, "Should handle exactly 32 binary digits."


# IPv4 CIDR Handler Tests
def test_cidr_ipv4_handler_boundary_values():
    converter = CIDRIPv4ConverterHandler()
    # Test with boundary CIDR values
    assert converter.handle("/0") is not None, "Should handle /0 CIDR."
    assert converter.handle("/32") is not None, "Should handle /32 CIDR."


# IPv6 Binary Digits Handler Tests
def test_binary_digits_ipv6_handler_boundary_values():
    converter = BinaryDigitsIPv6ConverterHandler()
    # Test with exactly 128 binary digits
    request = [1] * 128
    result = converter.handle(request)
    assert result is not None, "Should handle exactly 128 binary digits."


# IPv6 CIDR Handler Tests
def test_cidr_ipv6_handler_boundary_values():
    converter = CIDRIPv6ConverterHandler()
    # Test with boundary CIDR values
    assert converter.handle("/0") is not None, "Should handle /0 CIDR."
    assert converter.handle("/128") is not None, "Should handle /128 CIDR."


# IPv4 Dot Handler Tests
def test_dot_ipv4_handler_leading_zeros():
    converter = DotIPv4ConverterHandler()
    ipv4_address = "192.168.001.001"
    expected = b'\xc0\xa8\x01\x01'
    result = converter.handle(ipv4_address)
    assert result == expected, f"Should correctly convert {ipv4_address} to octets."


# IPv6 Colon Handler Tests
def test_colon_ipv6_handler_leading_zeros():
    converter = ColonIPv6ConverterHandler()
    ipv6_address = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    expected_binaries = [
        "00100000", "00000001", "00001101", "10111000", "10000101", "10100011", "00000000", "00000000",
        "00000000", "00000000", "10001010", "00101110", "00000011", "01110000", "01110011", "00110100"
    ]
    expected_octets = NumeralConverter.binary_to_bytes(''.join(expected_binaries), 16)
    result = converter.handle(ipv6_address)
    assert result == expected_octets, f"Failed for IPv6 {ipv6_address}. Expected {expected_octets}, got {result}"
