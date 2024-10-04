import pytest

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.macservice.mac_converters import OctetMAC48ConverterHandler, BinaryDigitsMAC48ConverterHandler, DashedHexMAC48ConverterHandler, \
    ColonHexMAC48ConverterHandler, DotHexMAC48ConverterHandler, OctetEUI64ConverterHandler, OctetOUI24ConverterHandler, \
    BinaryDigitsOUI24ConverterHandler, DashedHexOUI24ConverterHandler, ColonHexOUI24ConverterHandler, DotHexOUI24ConverterHandler, MACConverter, \
    DecimalMAC48ConverterHandler


# Test valid input case
def test_octet_mac48_valid_input():
    binary_string_list = ['11111111', '00000000', '11111111', '00000000', '11111111', '00000000']
    valid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetMAC48ConverterHandler()
    result = handler.handle(valid_octets)
    assert result == valid_octets


# Test input with more than 6 octets
def test_octet_mac48_too_many_octets():
    binary_string_list = ['11111111'] * 7  # 7 octets, which is invalid for MAC48
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetMAC48ConverterHandler()

    # Handle the invalid case (expect None or the next handler)
    result = handler.handle(invalid_octets)
    assert result is None  # Assuming that the handler passes if the request is invalid


# Test input with fewer than 6 octets
def test_octet_mac48_too_few_octets():
    binary_string_list = ['11111111', '00000000', '11111111', '00000000']  # 4 octets
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetMAC48ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Modify this based on how the handler processes it


# Test with an empty list
def test_octet_mac48_empty_list():
    empty_octets = []
    handler = OctetMAC48ConverterHandler()

    result = handler.handle(empty_octets)
    assert result is None


# Test with invalid types (e.g., passing strings instead of Octet objects)
def test_octet_mac48_invalid_types():
    invalid_octets = ['invalid_string', 'another_string', '11111111', '00000000']  # Strings instead of Octet
    handler = OctetMAC48ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Adjust based on expected behavior


# Test mixed valid and invalid octets
def test_octet_mac48_mixed_octets():
    binary_string_list = ['11111111', '00000000', '11111111']  # 3 valid octets
    mixed_input = [
                      OctetFlyWeightFactory.get_octet(binary_string) for binary_string in binary_string_list
                  ] + ['invalid_string', 42, None]  # Adding invalid entries

    handler = OctetMAC48ConverterHandler()

    result = handler.handle(mixed_input)
    assert result is None  # Adjust depending on the desired behavior


# Test valid binary digit input (48 bits representing 6 octets)
def test_binary_digits_mac48_valid_input():
    valid_binary_digits = [1, 0, 1, 0, 1, 0, 1, 0] * 6  # 48 bits total, representing 6 octets
    handler = BinaryDigitsMAC48ConverterHandler()
    result = handler.handle(valid_binary_digits)

    # Expected result would be 6 octets generated from the binary input
    assert len(result) == 6
    assert all(isinstance(octet, type(OctetFlyWeightFactory.get_octet('10101010'))) for octet in result)


# Test input with less than 48 bits
def test_binary_digits_mac48_too_few_bits():
    invalid_binary_digits = [1, 0, 1, 0] * 10  # Only 40 bits
    handler = BinaryDigitsMAC48ConverterHandler()
    result = handler.handle(invalid_binary_digits)

    assert result is None  # Adjust depending on the desired behavior when handling invalid inputs


# Test input with more than 48 bits
def test_binary_digits_mac48_too_many_bits():
    invalid_binary_digits = [1, 0] * 25  # 50 bits
    handler = BinaryDigitsMAC48ConverterHandler()
    result = handler.handle(invalid_binary_digits)

    assert result is None  # Modify based on expected behavior for invalid inputs


# Test with an empty list
def test_binary_digits_mac48_empty_list():
    empty_binary_digits = []
    handler = BinaryDigitsMAC48ConverterHandler()

    result = handler.handle(empty_binary_digits)
    assert result is None


# Test with mixed invalid types (e.g., strings or non-binary values)
def test_binary_digits_mac48_invalid_types():
    invalid_binary_digits = ['1', 0, 'invalid', 1] * 12  # Strings and non-binary values
    handler = BinaryDigitsMAC48ConverterHandler()

    result = handler.handle(invalid_binary_digits)
    assert result is None  # Adjust depending on how the handler should behave


# Test with mixed valid and invalid binary values
def test_binary_digits_mac48_mixed_values():
    mixed_binary_digits = [1, 0, 1, 0] * 6 + ['invalid', None]  # Partially valid, partially invalid
    handler = BinaryDigitsMAC48ConverterHandler()

    result = handler.handle(mixed_binary_digits)
    assert result is None  # Depending on how the handler should behave with mixed input


# Test valid dashed hex MAC48 input (e.g., "AA-BB-CC-DD-EE-FF")
def test_dashed_hex_mac48_valid_input():
    valid_mac = "AA-BB-CC-DD-EE-FF"
    handler = DashedHexMAC48ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, type(OctetFlyWeightFactory.get_octet('10101010'))) for octet in result)


# Test input with an invalid dashed hex format (e.g., wrong characters)
def test_dashed_hex_mac48_invalid_characters():
    invalid_mac = "GG-HH-II-JJ-KK-LL"  # Invalid hex characters
    handler = DashedHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should result in None or an error


# Test input with less than 12 hex digits
def test_dashed_hex_mac48_too_few_digits():
    invalid_mac = "AA-BB-CC-DD"  # Too few digits
    handler = DashedHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Not enough digits should result in None


# Test input with more than 12 hex digits
def test_dashed_hex_mac48_too_many_digits():
    invalid_mac = "AA-BB-CC-DD-EE-FF-GG"  # Too many digits
    handler = DashedHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Too many digits should result in None


# Test with empty string
def test_dashed_hex_mac48_empty_string():
    empty_mac = ""
    handler = DashedHexMAC48ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty string should return None


# Test with invalid separator (e.g., using colons instead of dashes)
def test_dashed_hex_mac48_invalid_separator():
    invalid_mac = "AA:BB:CC:DD:EE:FF"  # Colons instead of dashes
    handler = DashedHexMAC48ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Should not accept colons in this handler


# Test valid colon hex MAC48 input (e.g., "AA:BB:CC:DD:EE:FF")
def test_colon_hex_mac48_valid_input():
    valid_mac = "AA:BB:CC:DD:EE:FF"
    handler = ColonHexMAC48ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, type(OctetFlyWeightFactory.get_octet('10101010'))) for octet in result)


# Test input with an invalid colon hex format (e.g., wrong characters)
def test_colon_hex_mac48_invalid_characters():
    invalid_mac = "GG:HH:II:JJ:KK:LL"  # Invalid hex characters
    handler = ColonHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should result in None or an error


# Test input with less than 12 hex digits
def test_colon_hex_mac48_too_few_digits():
    invalid_mac = "AA:BB:CC:DD"  # Too few digits
    handler = ColonHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Not enough digits should result in None


# Test input with more than 12 hex digits
def test_colon_hex_mac48_too_many_digits():
    invalid_mac = "AA:BB:CC:DD:EE:FF:GG"  # Too many digits
    handler = ColonHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Too many digits should result in None


# Test with empty string
def test_colon_hex_mac48_empty_string():
    empty_mac = ""
    handler = ColonHexMAC48ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty string should return None


# Test with invalid separator (e.g., using dashes instead of colons)
def test_colon_hex_mac48_invalid_separator():
    invalid_mac = "AA-BB-CC-DD-EE-FF"  # Dashes instead of colons
    handler = ColonHexMAC48ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Should not accept dashes in this handler


# Test valid dot hex MAC48 input (e.g., "AAAA.BBBB.CCCC")
def test_dot_hex_mac48_valid_input():
    valid_mac = "AAAA.BBBB.CCCC"
    handler = DotHexMAC48ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, type(OctetFlyWeightFactory.get_octet('10101010'))) for octet in result)


# Test input with an invalid dot hex format (e.g., wrong characters)
def test_dot_hex_mac48_invalid_characters():
    invalid_mac = "GGGG.HHHH.IIII"  # Invalid hex characters
    handler = DotHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should result in None or an error


# Test input with less than 12 hex digits
def test_dot_hex_mac48_too_few_digits():
    invalid_mac = "AAAA.BBBB"  # Too few digits
    handler = DotHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Not enough digits should result in None


# Test input with more than 12 hex digits
def test_dot_hex_mac48_too_many_digits():
    invalid_mac = "AAAA.BBBB.CCCC.DDDD"  # Too many digits
    handler = DotHexMAC48ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Too many digits should result in None


# Test with empty string
def test_dot_hex_mac48_empty_string():
    empty_mac = ""
    handler = DotHexMAC48ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty string should return None


# Test with invalid separator (e.g., using dashes instead of dots)
def test_dot_hex_mac48_invalid_separator():
    invalid_mac = "AAAA-BBBB-CCCC"  # Dashes instead of dots
    handler = DotHexMAC48ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Should not accept dashes in this handler


# Test valid input for converting 6 octets to EUI-64
def test_octet_eui64_valid_input():
    binary_string_list = ['11111111', '00000000', '11111111', '00000000', '11111111', '00000000']
    valid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetEUI64ConverterHandler()
    result = handler.handle(valid_octets)

    # Expecting 8 octets in the result (EUI-64 is 64-bit, 8 octets)
    assert len(result) == 8
    assert all(isinstance(octet, type(OctetFlyWeightFactory.get_octet('10101010'))) for octet in result)


# Test input with more than 6 octets (which is invalid for conversion to EUI-64)
def test_octet_eui64_too_many_octets():
    binary_string_list = ['11111111'] * 7  # 7 octets, which is invalid for EUI-64 conversion
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetEUI64ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Handler should return None or pass to the next in the chain


# Test input with fewer than 6 octets
def test_octet_eui64_too_few_octets():
    binary_string_list = ['11111111', '00000000']  # Only 2 octets, not enough for EUI-64
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetEUI64ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Handler should return None for too few octets


# Test empty input list
def test_octet_eui64_empty_input():
    empty_octets = []
    handler = OctetEUI64ConverterHandler()

    result = handler.handle(empty_octets)
    assert result is None  # Empty input should result in None


# Test mixed valid and invalid octets
def test_octet_eui64_mixed_input():
    valid_octets = [
        OctetFlyWeightFactory.get_octet('11111111'),
        OctetFlyWeightFactory.get_octet('00000000'),
    ]
    mixed_input = valid_octets + ['invalid_octet', 42, None]  # Some invalid entries

    handler = OctetEUI64ConverterHandler()
    result = handler.handle(mixed_input)

    assert result is None  # Invalid input should result in None


# Test valid input for 3 octets with padding to 6 octets
def test_octet_oui24_valid_input_with_padding():
    binary_string_list = ['11111111', '00000000', '11111111']  # 3 octets
    valid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetOUI24ConverterHandler()
    result = handler.handle(valid_octets)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3


# Test input with more than 3 octets (should return None)
def test_octet_oui24_too_many_octets():
    binary_string_list = ['11111111'] * 4  # 4 octets, which is invalid for OUI-24
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetOUI24ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Too many octets should return None


# Test input with fewer than 3 octets (should return None)
def test_octet_oui24_too_few_octets():
    binary_string_list = ['11111111'] * 2  # Only 2 octets, not enough for OUI-24
    invalid_octets = [
        OctetFlyWeightFactory.get_octet(binary_string)
        for binary_string in binary_string_list
    ]
    handler = OctetOUI24ConverterHandler()

    result = handler.handle(invalid_octets)
    assert result is None  # Too few octets should return None


# Test empty input list (should return None)
def test_octet_oui24_empty_input():
    empty_octets = []
    handler = OctetOUI24ConverterHandler()

    result = handler.handle(empty_octets)
    assert result is None  # Empty input should return None


# Test mixed valid and invalid octets (should return None)
def test_octet_oui24_mixed_input():
    valid_octets = [
        OctetFlyWeightFactory.get_octet('11111111'),
        OctetFlyWeightFactory.get_octet('00000000'),
    ]
    mixed_input = valid_octets + ['invalid_octet', 42, None]  # Some invalid entries

    handler = OctetOUI24ConverterHandler()
    result = handler.handle(mixed_input)

    assert result is None  # Invalid input should return None


# Test valid input of 24 binary digits (OUI-24 format with padding to 6 octets)
def test_binary_digits_oui24_valid_input_with_padding():
    valid_binary_digits = [1, 0, 1, 0, 1, 0, 1, 0] * 3  # 24 bits representing 3 octets
    handler = BinaryDigitsOUI24ConverterHandler()
    result = handler.handle(valid_binary_digits)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3


# Test input with more than 24 binary digits (should return None)
def test_binary_digits_oui24_too_many_bits():
    invalid_binary_digits = [1, 0] * 13  # 26 bits
    handler = BinaryDigitsOUI24ConverterHandler()
    result = handler.handle(invalid_binary_digits)

    assert result is None  # Too many bits should return None


# Test input with fewer than 24 binary digits (should return None)
def test_binary_digits_oui24_too_few_bits():
    invalid_binary_digits = [1, 0, 1, 0] * 5  # Only 20 bits
    handler = BinaryDigitsOUI24ConverterHandler()
    result = handler.handle(invalid_binary_digits)

    assert result is None  # Too few bits should return None


# Test empty input list (should return None)
def test_binary_digits_oui24_empty_input():
    empty_binary_digits = []
    handler = BinaryDigitsOUI24ConverterHandler()

    result = handler.handle(empty_binary_digits)
    assert result is None  # Empty input should return None


# Test mixed valid and invalid binary values (should return None)
def test_binary_digits_oui24_mixed_input():
    mixed_binary_digits = [1, 0, 1, 0] * 3 + ['invalid', 42, None]  # 24 valid bits and some invalid entries
    handler = BinaryDigitsOUI24ConverterHandler()
    result = handler.handle(mixed_binary_digits)

    assert result is None  # Invalid input should return None


# Test valid dashed hex OUI-24 input with padding (e.g., "AA-BB-CC")
def test_dashed_hex_oui24_valid_input_with_padding():
    valid_mac = "AA-BB-CC"
    handler = DashedHexOUI24ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3


# Test input with an invalid dashed hex format (e.g., wrong characters)
def test_dashed_hex_oui24_invalid_characters():
    invalid_mac = "GG-HH-II"  # Invalid hex characters
    handler = DashedHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should return None


# Test input with fewer than 6 hex digits (too few octets)
def test_dashed_hex_oui24_too_few_digits():
    invalid_mac = "AA-BB"  # Not enough digits
    handler = DashedHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too few digits


# Test input with more than 6 hex digits (too many octets)
def test_dashed_hex_oui24_too_many_digits():
    invalid_mac = "AA-BB-CC-DD"  # Too many digits
    handler = DashedHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too many digits


# Test empty string input (should return None)
def test_dashed_hex_oui24_empty_input():
    empty_mac = ""
    handler = DashedHexOUI24ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty input should return None


# Test with invalid separator (e.g., using colons instead of dashes)
def test_dashed_hex_oui24_invalid_separator():
    invalid_mac = "AA:BB:CC"  # Colons instead of dashes
    handler = DashedHexOUI24ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Invalid separator should return None


# Test valid colon hex OUI-24 input with padding (e.g., "AA:BB:CC")
def test_colon_hex_oui24_valid_input_with_padding():
    valid_mac = "AA:BB:CC"
    handler = ColonHexOUI24ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3


# Test input with an invalid colon hex format (e.g., wrong characters)
def test_colon_hex_oui24_invalid_characters():
    invalid_mac = "GG:HH:II"  # Invalid hex characters
    handler = ColonHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should return None


# Test input with fewer than 6 hex digits (too few octets)
def test_colon_hex_oui24_too_few_digits():
    invalid_mac = "AA:BB"  # Not enough digits
    handler = ColonHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too few digits


# Test input with more than 6 hex digits (too many octets)
def test_colon_hex_oui24_too_many_digits():
    invalid_mac = "AA:BB:CC:DD"  # Too many digits
    handler = ColonHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too many digits


# Test empty string input (should return None)
def test_colon_hex_oui24_empty_input():
    empty_mac = ""
    handler = ColonHexOUI24ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty input should return None


# Test with invalid separator (e.g., using dashes instead of colons)
def test_colon_hex_oui24_invalid_separator():
    invalid_mac = "AA-BB-CC"  # Dashes instead of colons
    handler = ColonHexOUI24ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Invalid separator should return None


def test_dot_hex_oui24_invalid_input_with_padding():
    valid_mac = "AAAA.BBBB.CCCC"
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(valid_mac)

    assert result is None

def test_dot_hex_oui24_valid_input1():
    valid_mac = "AAAA.BB"
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3

def test_dot_hex_oui24_valid_input2():
    valid_mac = "AA.AA.BB"
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(valid_mac)

    # Expecting 6 octets in the result (3 valid + 3 padding '00' octets)
    assert len(result) == 6
    assert result[3:] == [OctetFlyWeightFactory.get_octet('00000000')] * 3


# Test input with an invalid dot hex format (e.g., wrong characters)
def test_dot_hex_oui24_invalid_characters():
    invalid_mac = "GGGG.HHHH.IIII"  # Invalid hex characters
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Invalid characters should return None


# Test input with fewer than 6 hex digits (too few octets)
def test_dot_hex_oui24_too_many_digits1():
    invalid_mac = "AAAA.BBBB"  # Not enough digits
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too few digits


# Test input with more than 6 hex digits (too many octets)
def test_dot_hex_oui24_too_many_digits2():
    invalid_mac = "AAAA.BBBB.CCCC.DDDD"  # Too many digits
    handler = DotHexOUI24ConverterHandler()
    result = handler.handle(invalid_mac)

    assert result is None  # Should return None for too many digits


# Test empty string input (should return None)
def test_dot_hex_oui24_empty_input():
    empty_mac = ""
    handler = DotHexOUI24ConverterHandler()

    result = handler.handle(empty_mac)
    assert result is None  # Empty input should return None


# Test with invalid separator (e.g., using colons instead of dots)
def test_dot_hex_oui24_invalid_separator():
    invalid_mac = "AAAA:BBBB:CCCC"  # Colons instead of dots
    handler = DotHexOUI24ConverterHandler()

    result = handler.handle(invalid_mac)
    assert result is None  # Invalid separator should return None


# Test for convert_mac with valid MAC48 input (e.g., 6 octets)
def test_mac_converter_convert_mac_valid_input():
    valid_mac = "AA-BB-CC-DD-EE-FF"  # Dashed hex format
    result = MACConverter.convert_mac(valid_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, Octet) for octet in result)


# Test for convert_mac with invalid MAC48 input
def test_mac_converter_convert_mac_invalid_input():
    invalid_mac = "ZZ-YY-XX-WW-VV-UU"  # Invalid hex characters
    result = MACConverter.convert_mac(invalid_mac)

    assert result is None  # Should return None for invalid input

# Test for convert_oui with invalid OUI-24 input
def test_mac_converter_convert_oui_invalid_input():
    invalid_oui = "GGGG.HHHH.IIII"  # Invalid hex characters
    result = MACConverter.convert_oui(invalid_oui)

    assert result is None  # Should return None for invalid input


# Test for convert_to_eui64 with valid MAC48 input, converting to EUI-64
def test_mac_converter_convert_to_eui64_valid_input():
    valid_mac = "AA-BB-CC-DD-EE-FF"  # Dashed hex format
    result = MACConverter.convert_to_eui64(valid_mac)

    # Expecting 8 octets in the result (EUI-64 format)
    assert len(result) == 8
    assert all(isinstance(octet, Octet) for octet in result)


# Test for convert_to_eui64 with invalid MAC48 input
def test_mac_converter_convert_to_eui64_invalid_input():
    invalid_mac = "ZZ-YY-XX-WW-VV-UU"  # Invalid hex characters
    result = MACConverter.convert_to_eui64(invalid_mac)

    assert result is None  # Should return None for invalid input


# Test valid decimal MAC48 input (e.g., 48-bit decimal)
def test_decimal_mac48_valid_input():
    valid_decimal_mac = 281474976710655  # Decimal representation of FF:FF:FF:FF:FF:FF
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(valid_decimal_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, Octet) for octet in result)
    assert result[0].hex == 'FF' and result[-1].hex == 'FF'


# Test decimal input with more than 48 bits
def test_decimal_mac48_too_large():
    invalid_decimal_mac = 2**50  # Larger than 48 bits
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(invalid_decimal_mac)

    assert result is None  # Should return None for too large input


# Test decimal input with fewer than 48 bits (e.g., a valid smaller number)
def test_decimal_mac48_valid_small_input():
    valid_decimal_mac = 123456789  # A smaller valid decimal MAC (up to 48 bits)
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(valid_decimal_mac)

    # Expecting 6 octets in the result
    assert len(result) == 6
    assert all(isinstance(octet, Octet) for octet in result)


# Test decimal input with invalid type (e.g., string instead of integer)
def test_decimal_mac48_invalid_type():
    invalid_decimal_mac = "123456789"  # String instead of integer
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(invalid_decimal_mac)

    assert result is None  # Should return None for invalid type


# Test empty input
def test_decimal_mac48_empty_input():
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(None)

    assert result is None  # Should return None for empty input


# Test negative decimal input (which is invalid for MAC addresses)
def test_decimal_mac48_negative_input():
    invalid_decimal_mac = -123456  # Negative numbers are invalid
    handler = DecimalMAC48ConverterHandler()
    result = handler.handle(invalid_decimal_mac)

    assert result is None  # Should return None for negative input
