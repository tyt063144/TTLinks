import pytest

from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_type_classifiers import OctetIPv4IPTypeClassifierHandler, DotIPv4IPTypeClassifierHandler, OctetIPv4NetmaskClassifierHandler, \
    DotIPv4NetmaskClassifierHandler, CIDRIPv4NetmaskClassifierHandler, OctetIPv6IPTypeClassifierHandler, ColonIPv6IPTypeClassifierHandler, \
    OctetIPv6NetmaskClassifierHandler, ColonIPv6NetmaskClassifierHandler, CIDRIPv6NetmaskClassifierHandler, IPType


def test_octet_ipv4_ip_type_classifier_valid_ipv4_address():
    handler = OctetIPv4IPTypeClassifierHandler()
    request_ipv4 = [
        OctetFlyWeightFactory.get_octet('11000000'),  # 192
        OctetFlyWeightFactory.get_octet('10101000'),  # 168
        OctetFlyWeightFactory.get_octet('00000001'),  # 1
        OctetFlyWeightFactory.get_octet('00000001')  # 1
    ]
    result = handler.handle(request_ipv4)
    assert result == IPType.IPv4, "The IP should be classified as IPv4."


def test_octet_ipv4_ip_type_classifier_invalid_fewer_octets():
    handler = OctetIPv4IPTypeClassifierHandler()
    request_ipv4 = [
        OctetFlyWeightFactory.get_octet('11000000'),  # 192
        OctetFlyWeightFactory.get_octet('10101000'),  # 168
        OctetFlyWeightFactory.get_octet('00000001')  # 1
    ]
    result = handler.handle(request_ipv4)
    assert result != IPType.IPv4, "The IP should not be classified as IPv4 due to insufficient octets."


def test_octet_ipv4_ip_type_classifier_invalid_more_octets():
    handler = OctetIPv4IPTypeClassifierHandler()
    request_ipv4 = [
        OctetFlyWeightFactory.get_octet('11000000'),  # 192
        OctetFlyWeightFactory.get_octet('10101000'),  # 168
        OctetFlyWeightFactory.get_octet('00000001'),  # 1
        OctetFlyWeightFactory.get_octet('00000001'),  # 1
        OctetFlyWeightFactory.get_octet('00000001')  # Extra octet
    ]
    result = handler.handle(request_ipv4)
    assert result != IPType.IPv4, "The IP should not be classified as IPv4 due to excess octets."


def test_dot_ipv4_ip_type_classifier_valid_dotted_decimal_address():
    handler = DotIPv4IPTypeClassifierHandler()
    request_ipv4 = "192.168.1.1"
    result = handler.handle(request_ipv4)
    assert result == IPType.IPv4, "The IP should be classified as IPv4."


def test_dot_ipv4_ip_type_classifier_invalid_extra_octets():
    handler = DotIPv4IPTypeClassifierHandler()
    request_ipv4 = "192.168.1.1.2"
    result = handler.handle(request_ipv4)
    assert result != IPType.IPv4, "The IP should not be classified as IPv4 due to extra octets."


def test_dot_ipv4_ip_type_classifier_invalid_non_numeric():
    handler = DotIPv4IPTypeClassifierHandler()
    request_ipv4 = "192.168.abc.1"
    result = handler.handle(request_ipv4)
    assert result != IPType.IPv4, "The IP should not be classified as IPv4 due to non-numeric characters."


def test_dot_ipv4_ip_type_classifier_invalid_characters():
    handler = DotIPv4IPTypeClassifierHandler()
    request_ipv4 = "192.168.1.a"
    result = handler.handle(request_ipv4)
    assert result != IPType.IPv4, "The IP with invalid characters should not be classified as IPv4."


def test_dot_ipv4_ip_type_classifier_leading_zeros():
    handler = DotIPv4IPTypeClassifierHandler()
    request_ipv4 = "192.168.001.001"
    result = handler.handle(request_ipv4)
    assert result == IPType.IPv4, "The IP with leading zeros should be classified as IPv4."


def test_octet_ipv4_netmask_classifier_valid_netmask():
    handler = OctetIPv4NetmaskClassifierHandler()
    request_netmask = [
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('00000000')  # 0
    ]
    result = handler.handle(request_netmask)
    assert result == IPType.IPv4, "The netmask should be classified as IPv4."


def test_octet_ipv4_netmask_classifier_invalid_non_contiguous():
    handler = OctetIPv4NetmaskClassifierHandler()
    request_netmask = [
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('00000000'),  # 0
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('00000000')  # 0
    ]
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The netmask with non-contiguous bits should not be classified as IPv4."


def test_octet_ipv4_netmask_classifier_valid_full_netmask():
    handler = OctetIPv4NetmaskClassifierHandler()
    request_netmask = [
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111')  # 255
    ]
    result = handler.handle(request_netmask)
    assert result == IPType.IPv4, "The full netmask should be classified as IPv4."


def test_octet_ipv4_netmask_classifier_invalid_short_netmask():
    handler = OctetIPv4NetmaskClassifierHandler()
    request_netmask = [
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111'),  # 255
        OctetFlyWeightFactory.get_octet('11111111')  # 255
    ]
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The short netmask should not be classified as IPv4."


def test_dot_ipv4_netmask_classifier_valid_dotted_decimal_netmask():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = "255.255.255.0"
    result = handler.handle(request_netmask)
    assert result == IPType.IPv4, "The netmask should be classified as IPv4."


def test_dot_ipv4_netmask_classifier_invalid_non_contiguous():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = "255.0.255.0"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The netmask with non-contiguous bits should not be classified as IPv4."


def test_dot_ipv4_netmask_classifier_invalid_format_extra_dots():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = "255.255.255.0.0"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The netmask with extra dots should not be classified as IPv4."


def test_dot_ipv4_netmask_classifier_invalid_empty_string():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = ""
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "An empty string should not be classified as an IPv4 netmask."


def test_dot_ipv4_netmask_classifier_valid_full_netmask():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = "255.255.255.255"
    result = handler.handle(request_netmask)
    assert result == IPType.IPv4, "The full netmask should be classified as IPv4."


def test_dot_ipv4_netmask_classifier_invalid_characters():
    handler = DotIPv4NetmaskClassifierHandler()
    request_netmask = "255.255.255.a"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The netmask with invalid characters should not be classified as IPv4."


def test_cidr_ipv4_netmask_classifier_valid_cidr_notation():
    handler = CIDRIPv4NetmaskClassifierHandler()
    request_netmask = "/24"
    result = handler.handle(request_netmask)
    assert result == IPType.IPv4, "The CIDR notation netmask '/24' should be classified as IPv4."


def test_cidr_ipv4_netmask_classifier_invalid_out_of_range():
    handler = CIDRIPv4NetmaskClassifierHandler()
    request_netmask = "/33"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The CIDR notation '/33' should not be classified as IPv4 because it is out of range."


def test_cidr_ipv4_netmask_classifier_edge_cases():
    handler = CIDRIPv4NetmaskClassifierHandler()
    edge_cases = ["/0", "/32"]
    results = [handler.handle(case) for case in edge_cases]
    assert all(result == IPType.IPv4 for result in results), "Edge CIDR notations '/0' and '/32' should be classified as IPv4."


def test_cidr_ipv4_netmask_classifier_invalid_format():
    handler = CIDRIPv4NetmaskClassifierHandler()
    request_netmask = "24"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The string '24' should not be classified as IPv4 since it lacks the '/' prefix."


def test_cidr_ipv4_netmask_classifier_invalid_non_numeric():
    handler = CIDRIPv4NetmaskClassifierHandler()
    request_netmask = "/abc"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv4, "The CIDR notation '/abc' should not be classified as IPv4 because it is non-numeric."


def test_octet_ipv6_ip_type_classifier_valid_ipv6_address():
    handler = OctetIPv6IPTypeClassifierHandler()
    request_ipv6 = [OctetFlyWeightFactory.get_octet('00000000') for _ in range(16)]  # 16 octets representing zeros
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "The IPv6 address should be classified as IPv6."


def test_octet_ipv6_ip_type_classifier_invalid_fewer_octets():
    handler = OctetIPv6IPTypeClassifierHandler()
    request_ipv6 = [OctetFlyWeightFactory.get_octet('00000000') for _ in range(15)]  # 15 octets
    result = handler.handle(request_ipv6)
    assert result != IPType.IPv6, "The address with fewer than 16 octets should not be classified as IPv6."


def test_octet_ipv6_ip_type_classifier_invalid_more_octets():
    handler = OctetIPv6IPTypeClassifierHandler()
    request_ipv6 = [OctetFlyWeightFactory.get_octet('00000000') for _ in range(17)]  # 17 octets
    result = handler.handle(request_ipv6)
    assert result != IPType.IPv6, "The address with more than 16 octets should not be classified as IPv6."


def test_octet_ipv6_ip_type_classifier_all_zero_address():
    handler = OctetIPv6IPTypeClassifierHandler()
    request_ipv6 = [OctetFlyWeightFactory.get_octet('00000000') for _ in range(16)]  # All zeros
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "An all-zero IPv6 address should be classified as IPv6."


def test_octet_ipv6_ip_type_classifier_all_ones_address():
    handler = OctetIPv6IPTypeClassifierHandler()
    request_ipv6 = [OctetFlyWeightFactory.get_octet('11111111') for _ in range(16)]  # All ones
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "An all-ones IPv6 address should be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_valid_address():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "2001:0db8::1"
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "The IPv6 address should be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_invalid_extra_characters():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "2001:0db8::1::"
    result = handler.handle(request_ipv6)
    assert result != IPType.IPv6, "The IPv6 address with extra characters should not be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_invalid_blocks():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "2001:0db8:zzzz::"
    result = handler.handle(request_ipv6)
    assert result != IPType.IPv6, "The IPv6 address with invalid blocks should not be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_full_format_address():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "2001:0db8:0000:0000:0000:0000:0000:0001"
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "The full format IPv6 address should be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_loopback_address():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "::1"
    result = handler.handle(request_ipv6)
    assert result == IPType.IPv6, "The loopback IPv6 address should be classified as IPv6."


def test_colon_ipv6_ip_type_classifier_embedded_ipv4():
    handler = ColonIPv6IPTypeClassifierHandler()
    request_ipv6 = "::ffff:192.168.1.1"
    result = handler.handle(request_ipv6)
    print('result', result)
    assert result == IPType.IPv6, "The IPv6 address with embedded IPv4 should be classified as IPv6."


def test_octet_ipv6_netmask_classifier_valid_netmask():
    handler = OctetIPv6NetmaskClassifierHandler()
    request_netmask = [
                          OctetFlyWeightFactory.get_octet('11111111') for _ in range(8)  # 8 leading octets as 255 (full bits)
                      ] + [
                          OctetFlyWeightFactory.get_octet('00000000') for _ in range(8)  # 8 trailing octets as 0
                      ]
    result = handler.handle(request_netmask)
    assert result == IPType.IPv6, "The valid IPv6 netmask should be classified as IPv6."


def test_octet_ipv6_netmask_classifier_invalid_non_contiguous():
    handler = OctetIPv6NetmaskClassifierHandler()
    request_netmask = [
                          OctetFlyWeightFactory.get_octet('11111111'),  # 255
                          OctetFlyWeightFactory.get_octet('00000000'),  # 0
                          OctetFlyWeightFactory.get_octet('11111111'),  # 255
                          OctetFlyWeightFactory.get_octet('00000000')  # 0
                      ] * 4  # Repeated to make up 16 octets
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The netmask with non-contiguous bits should not be classified as IPv6."


def test_octet_ipv6_netmask_classifier_mixed_contiguous_non_contiguous():
    handler = OctetIPv6NetmaskClassifierHandler()
    request_netmask = [
                          OctetFlyWeightFactory.get_octet('11111111'),  # 255
                          OctetFlyWeightFactory.get_octet('11110000'),  # 240
                          OctetFlyWeightFactory.get_octet('11111111'),  # 255
                          OctetFlyWeightFactory.get_octet('00001111')  # 15
                      ] * 4  # Repeated to make up 16 octets
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The netmask with mixed contiguous and non-contiguous bits should not be classified as IPv6."


def test_octet_ipv6_netmask_classifier_valid_full_netmask():
    handler = OctetIPv6NetmaskClassifierHandler()
    request_netmask = [OctetFlyWeightFactory.get_octet('11111111') for _ in range(16)]  # All bits set
    result = handler.handle(request_netmask)
    assert result == IPType.IPv6, "The full netmask should be classified as IPv6."


def test_octet_ipv6_netmask_classifier_invalid_length():
    handler = OctetIPv6NetmaskClassifierHandler()
    short_netmask = [OctetFlyWeightFactory.get_octet('11111111') for _ in range(15)]
    long_netmask = [OctetFlyWeightFactory.get_octet('11111111') for _ in range(17)]
    assert handler.handle(short_netmask) != IPType.IPv6, "A netmask with fewer than 16 octets should not be classified as IPv6."
    assert handler.handle(long_netmask) != IPType.IPv6, "A netmask with more than 16 octets should not be classified as IPv6."


def test_colon_ipv6_netmask_classifier_valid_netmask():
    handler = ColonIPv6NetmaskClassifierHandler()
    request_netmask = "ffff:ffff:ffff:ffff::"
    result = handler.handle(request_netmask)
    assert result == IPType.IPv6, "The IPv6 netmask should be classified as IPv6."


def test_colon_ipv6_netmask_classifier_invalid_non_contiguous():
    handler = ColonIPv6NetmaskClassifierHandler()
    request_netmask = "ffff:0fff:ffff::"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The IPv6 netmask with non-contiguous bits should not be classified as IPv6."


def test_colon_ipv6_netmask_classifier_invalid_format():
    handler = ColonIPv6NetmaskClassifierHandler()
    request_netmask = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"  # Too many sections
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "An incorrectly formatted IPv6 netmask should not be classified as IPv6."


def test_colon_ipv6_netmask_classifier_edge_cases():
    handler = ColonIPv6NetmaskClassifierHandler()
    minimal_netmask = "::"
    full_netmask = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
    assert handler.handle(minimal_netmask) == IPType.IPv6, "The minimal netmask '::' should be classified as IPv6."
    assert handler.handle(full_netmask) == IPType.IPv6, "The full netmask should be classified as IPv6."


def test_cidr_ipv6_netmask_classifier_valid_cidr_notation():
    handler = CIDRIPv6NetmaskClassifierHandler()
    request_netmask = "/64"
    result = handler.handle(request_netmask)
    assert result == IPType.IPv6, "The CIDR notation '/64' should be classified as IPv6."


def test_cidr_ipv6_netmask_classifier_invalid_out_of_range():
    handler = CIDRIPv6NetmaskClassifierHandler()
    request_netmask = "/129"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The CIDR notation '/129' should not be classified as IPv6 because it is out of range."


def test_cidr_ipv6_netmask_classifier_edge_cases():
    handler = CIDRIPv6NetmaskClassifierHandler()
    edge_cases = ["/0", "/128"]
    results = [handler.handle(case) for case in edge_cases]
    assert all(result == IPType.IPv6 for result in results), "Edge CIDR notations '/0' and '/128' should be classified as IPv6."


def test_cidr_ipv6_netmask_classifier_invalid_format():
    handler = CIDRIPv6NetmaskClassifierHandler()
    request_netmask = "64"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The string '64' should not be classified as IPv6 since it lacks the '/' prefix."


def test_cidr_ipv6_netmask_classifier_invalid_non_numeric():
    handler = CIDRIPv6NetmaskClassifierHandler()
    request_netmask = "/abc"
    result = handler.handle(request_netmask)
    assert result != IPType.IPv6, "The CIDR notation '/abc' should not be classified as IPv6 because it is non-numeric."
