import pytest
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPv4WildCard, IPv6Addr, IPv6NetMask, IPv6WildCard
from ttlinks.ipservice.ip_format_standardizer import CIDRInterfaceIPv4StandardizerHandler, DotInterfaceIPv4StandardizerHandler, \
    IPAddrInterfaceIPv4StandardizerHandler, DotWildcardIPv4StandardizerHandler, IPAddrWildcardIPv4StandardizerHandler, \
    CIDRInterfaceIPv6StandardizerHandler, IPAddrInterfaceIPv6StandardizerHandler, ColonWildcardIPv6StandardizerHandler, \
    IPAddrWildcardIPv6StandardizerHandler, IPStandardizer


def test_cidr_ipv4_standardizer_valid_input():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1/24'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('/24')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv4_standardizer_invalid_format():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1-24'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid format"


def test_cidr_ipv4_standardizer_non_numeric_octet():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.one.1/24'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric octet"


def test_cidr_ipv4_standardizer_leading_spaces():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '   10.0.0.1/8'
    result = handler.handle(test_input)
    assert result is None, "Should return None"


def test_cidr_ipv4_standardizer_trailing_spaces():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '172.16.0.1/16   '
    result = handler.handle(test_input)
    assert result is None, "Result should be None"


def test_cidr_ipv4_standardizer_full_netmask():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '255.255.255.255/32'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('255.255.255.255')
    expected_netmask = IPv4NetMask('/32')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv4_standardizer_out_of_range_octet():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '256.100.50.25/24'
    result = handler.handle(test_input)
    assert result is None, "Result should be None"


def test_cidr_ipv4_standardizer_invalid_netmask_number():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1/33'
    result = handler.handle(test_input)
    assert result is None, "Result should be None"


def test_cidr_ipv4_standardizer_non_numeric_netmask():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1/abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric netmask"


def test_cidr_ipv4_standardizer_leading_zeros():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.001.001/24'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('/24')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv4_standardizer_empty_string():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = ''
    result = handler.handle(test_input)
    assert result is None, "Should return None for empty string"


def test_cidr_ipv4_standardizer_none_input():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = None
    result = handler.handle(test_input)
    assert result is None, "Should return None for None input"


def test_cidr_ipv4_standardizer_netmask_zero():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '10.0.0.1/0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_netmask = IPv4NetMask('/0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv4_standardizer_netmask_one():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '10.0.0.1/1'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_netmask = IPv4NetMask('/1')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv4_standardizer_extra_characters_in_netmask():
    handler = CIDRInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1/24abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for extra characters in netmask"


def test_dot_ipv4_standardizer_valid_input():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1 255.255.255.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('255.255.255.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_invalid_format():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1/255.255.255.0'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid format"


def test_dot_ipv4_standardizer_non_numeric_octet():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.one.1 255.255.255.0'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric octet"


def test_dot_ipv4_standardizer_invalid_netmask():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1 255.255.255.256'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid netmask"


def test_dot_ipv4_standardizer_leading_spaces():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '   10.0.0.1 255.0.0.0'
    result = handler.handle(test_input)
    assert result is None, "Should return None"


def test_dot_ipv4_standardizer_trailing_spaces():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '172.16.0.1 255.255.0.0   '
    result = handler.handle(test_input)
    assert result is None, "Should return None"


def test_dot_ipv4_standardizer_full_netmask():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '255.255.255.255 255.255.255.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('255.255.255.255')
    expected_netmask = IPv4NetMask('255.255.255.255')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_out_of_range_octet():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '256.100.50.25 255.255.255.0'
    result = handler.handle(test_input)
    assert result is None, "Result should not be None"


def test_dot_ipv4_standardizer_invalid_netmask_number():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1 255.255.255.256'
    result = handler.handle(test_input)
    assert result is None, "Result should not be None"


def test_dot_ipv4_standardizer_non_numeric_netmask():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1 abc.def.ghi.jkl'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric netmask"


def test_dot_ipv4_standardizer_leading_zeros():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.001.001 255.255.255.000'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('255.255.255.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_empty_string():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = ''
    result = handler.handle(test_input)
    assert result is None, "Should return None for empty string"


def test_dot_ipv4_standardizer_none_input():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = None
    result = handler.handle(test_input)
    assert result is None, "Should return None for None input"


def test_dot_ipv4_standardizer_netmask_zero():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '10.0.0.1 0.0.0.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_netmask = IPv4NetMask('0.0.0.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_netmask_one():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '10.0.0.1 128.0.0.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_netmask = IPv4NetMask('128.0.0.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_extra_characters_in_netmask():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1 255.255.255.0abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for extra characters in netmask"


def test_dot_ipv4_standardizer_missing_netmask():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1'
    result = handler.handle(test_input)
    assert result is None, "Should return None when netmask is missing"


def test_dot_ipv4_standardizer_additional_spaces():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1    255.255.255.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('255.255.255.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_dot_ipv4_standardizer_tab_separator():
    handler = DotInterfaceIPv4StandardizerHandler()
    test_input = '192.168.1.1\t255.255.255.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('255.255.255.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_ipaddr_interface_ipv4_standardizer_valid_input():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('255.255.255.0')
    result = handler.handle(ip_addr, netmask)
    assert result is not None, "Result should not be None"
    assert result == (ip_addr, netmask), "Handler should return the IP and netmask as a tuple"


def test_ipaddr_interface_ipv4_standardizer_invalid_ip_type():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = '192.168.1.1'  # Not an IPv4Addr object
    netmask = IPv4NetMask('255.255.255.0')
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for invalid IP type"


def test_ipaddr_interface_ipv4_standardizer_invalid_netmask_type():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = '255.255.255.0'  # Not an IPv4NetMask object
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for invalid netmask type"


def test_ipaddr_interface_ipv4_standardizer_wrong_number_of_args():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('255.255.255.0')
    # Missing netmask argument
    result = handler.handle(ip_addr)
    assert result is None, "Should return None when missing arguments"
    # Extra argument
    result = handler.handle(ip_addr, netmask, 'extra')
    assert result is None, "Should return None when extra arguments are provided"


def test_ipaddr_interface_ipv4_standardizer_none_arguments():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    result = handler.handle(None, None)
    assert result is None, "Should return None when arguments are None"


def test_ipaddr_interface_ipv4_standardizer_incorrect_argument_types():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    result = handler.handle(123, 456)
    assert result is None, "Should return None for incorrect argument types"


def test_ipaddr_interface_ipv4_standardizer_ipv6addr_ipv4netmask():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6Addr
    ip_addr = IPv6Addr('::1')  # IPv6Addr instead of IPv4Addr
    netmask = IPv4NetMask('255.255.255.0')
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when IP is not IPv4Addr"


def test_ipaddr_interface_ipv4_standardizer_ipv4addr_ipv6netmask():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6NetMask
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv6NetMask('/64')  # IPv6NetMask instead of IPv4NetMask
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when netmask is not IPv4NetMask"


def test_ipaddr_interface_ipv4_standardizer_ipv4addr_ipv4wildcard():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4WildCard
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')  # Wildcard instead of netmask
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when netmask is not IPv4NetMask"


def test_ipaddr_interface_ipv4_standardizer_valid_cidr_netmask():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = IPv4Addr('10.0.0.1')
    netmask = IPv4NetMask('/8')  # CIDR notation
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should accept CIDR notation netmask"


def test_ipaddr_interface_ipv4_standardizer_edge_case_ips():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    # Test with '0.0.0.0'
    ip_addr = IPv4Addr('0.0.0.0')
    netmask = IPv4NetMask('0.0.0.0')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should handle '0.0.0.0' IP and netmask"
    # Test with '255.255.255.255'
    ip_addr = IPv4Addr('255.255.255.255')
    netmask = IPv4NetMask('255.255.255.255')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should handle '255.255.255.255' IP and netmask"


def test_ipaddr_interface_ipv4_standardizer_invalid_ip_value():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    # Cannot create an invalid IPv4Addr, so test is not applicable
    pass


def test_ipaddr_interface_ipv4_standardizer_invalid_netmask_value():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    # Cannot create an invalid IPv4NetMask, so test is not applicable
    pass


def test_ipaddr_interface_ipv4_standardizer_mixed_argument_types():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = '192.168.1.1'  # String instead of IPv4Addr
    netmask = 24  # Integer instead of IPv4NetMask
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for mixed incorrect argument types"


def test_ipaddr_interface_ipv4_standardizer_correct_types_but_invalid_data():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    # Since invalid IPv4Addr or IPv4NetMask cannot be instantiated (they raise ValueError), we cannot pass them to handle
    # Therefore, this test is not applicable
    pass


def test_ipaddr_interface_ipv4_standardizer_empty_arguments():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    result = handler.handle()
    assert result is None, "Should return None when no arguments are provided"


def test_ipaddr_interface_ipv4_standardizer_additional_arguments():
    handler = IPAddrInterfaceIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('255.255.255.0')
    extra_arg1 = 'extra1'
    extra_arg2 = 'extra2'
    result = handler.handle(ip_addr, netmask, extra_arg1, extra_arg2)
    assert result is None, "Should return None when too many arguments are provided"


def test_dot_wildcard_ipv4_standardizer_valid_input():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0.0.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None"
    assert isinstance(result, tuple), "Result should be a tuple"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_invalid_format():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1/0.0.0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid format"


def test_dot_wildcard_ipv4_standardizer_non_numeric_octet():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.one.1 0.0.0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric IP octet"


def test_dot_wildcard_ipv4_standardizer_invalid_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0.0.256'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid wildcard"


def test_dot_wildcard_ipv4_standardizer_leading_spaces():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '   10.0.0.1 0.255.255.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None for input with leading spaces"


def test_dot_wildcard_ipv4_standardizer_trailing_spaces():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '172.16.0.1 0.0.255.255   '
    result = handler.handle(test_input)
    assert result is None, "Should return None for input with trailing spaces"


def test_dot_wildcard_ipv4_standardizer_full_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 255.255.255.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('255.255.255.255')
    assert result is not None, "Result should not be None"
    assert isinstance(result, tuple), "Result should be a tuple"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_out_of_range_octet():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '256.100.50.25 0.0.0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None for out-of-range IP octet"


def test_dot_wildcard_ipv4_standardizer_non_numeric_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 abc.def.ghi.jkl'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric wildcard"


def test_dot_wildcard_ipv4_standardizer_leading_zeros():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.001.001 000.000.000.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_empty_string():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = ''
    result = handler.handle(test_input)
    assert result is None, "Should return None for empty string input"


def test_dot_wildcard_ipv4_standardizer_none_input():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = None
    result = handler.handle(test_input)
    assert result is None, "Should return None for None input"


def test_dot_wildcard_ipv4_standardizer_wildcard_zero():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '10.0.0.1 0.0.0.0'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_wildcard = IPv4WildCard('0.0.0.0')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_wildcard_all_ones():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '10.0.0.1 255.255.255.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('10.0.0.1')
    expected_wildcard = IPv4WildCard('255.255.255.255')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_extra_characters_in_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0.0.255abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for extra characters in wildcard"


def test_dot_wildcard_ipv4_standardizer_missing_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1'
    result = handler.handle(test_input)
    assert result is None, "Should return None when wildcard is missing"


def test_dot_wildcard_ipv4_standardizer_additional_spaces():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1    0.0.0.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_tab_separator():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1\t0.0.0.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_invalid_ip_and_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '999.999.999.999 999.999.999.999'
    result = handler.handle(test_input)
    assert result is None, "Should return None for completely invalid IP and wildcard"


def test_dot_wildcard_ipv4_standardizer_ipv4addr_wildcard_objects():
    handler = DotWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when inputs are not in string format"


def test_dot_wildcard_ipv4_standardizer_wildcard_with_non_zero_bits():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0.0.254'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.254')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_mixed_case():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0.0.255'
    result = handler.handle(test_input.lower())
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None even with lowercase input"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_multiple_spaces():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1      0.0.0.255'
    result = handler.handle(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None, "Result should not be None with multiple spaces"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_wildcard), f"Expected Wildcard {expected_wildcard}, got {result[1]}"


def test_dot_wildcard_ipv4_standardizer_ipv6_address():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = 'fe80::1 0.0.0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None when IP is not IPv4 address"


def test_dot_wildcard_ipv4_standardizer_ipv4_address_ipv6_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 ::ff'
    result = handler.handle(test_input)
    assert result is None, "Should return None when wildcard is not IPv4 format"


def test_dot_wildcard_ipv4_standardizer_no_space_separator():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.10.0.0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None when separator is missing"


def test_dot_wildcard_ipv4_standardizer_space_in_wildcard():
    handler = DotWildcardIPv4StandardizerHandler()
    test_input = '192.168.1.1 0.0 .0.255'
    result = handler.handle(test_input)
    assert result is None, "Should return None when wildcard has spaces within"


def test_ipaddr_wildcard_ipv4_standardizer_valid_input():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard)
    assert result == (ip_addr, wildcard), "Handler should return the IP address and wildcard as a tuple"


def test_ipaddr_wildcard_ipv4_standardizer_invalid_ip_type():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = '192.168.1.1'  # Should be an IPv4Addr object
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None for invalid IP address type"


def test_ipaddr_wildcard_ipv4_standardizer_invalid_wildcard_type():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = '0.0.0.255'  # Should be an IPv4WildCard object
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None for invalid wildcard type"


def test_ipaddr_wildcard_ipv4_standardizer_wrong_number_of_args():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr)  # Missing wildcard
    assert result is None, "Should return None when arguments are missing"

    result = handler.handle(ip_addr, wildcard, 'extra_arg')
    assert result is None, "Should return None when too many arguments are provided"


def test_ipaddr_wildcard_ipv4_standardizer_none_arguments():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    result = handler.handle(None, None)
    assert result is None, "Should return None when arguments are None"


def test_ipaddr_wildcard_ipv4_standardizer_invalid_ip_value():
    # Cannot create invalid IPv4Addr object; invalid IP would raise an exception during object creation
    pass


def test_ipaddr_wildcard_ipv4_standardizer_invalid_wildcard_value():
    # Cannot create invalid IPv4WildCard object; invalid wildcard would raise an exception during object creation
    pass


def test_ipaddr_wildcard_ipv4_standardizer_ipv6addr_ipv4wildcard():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6Addr
    ip_addr = IPv6Addr('::1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when IP address is not IPv4Addr"


def test_ipaddr_wildcard_ipv4_standardizer_ipv4addr_ipv6wildcard():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6WildCard
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv6WildCard('::ff')
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when wildcard is not IPv4WildCard"


def test_ipaddr_wildcard_ipv4_standardizer_mixed_argument_types():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = '192.168.1.1'  # Should be IPv4Addr object
    wildcard = '0.0.0.255'  # Should be IPv4WildCard object
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when arguments are of incorrect types"


def test_ipaddr_wildcard_ipv4_standardizer_empty_arguments():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    result = handler.handle()
    assert result is None, "Should return None when no arguments are provided"


def test_ipaddr_wildcard_ipv4_standardizer_additional_arguments():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard, 'extra_arg')
    assert result is None, "Should return None when extra arguments are provided"


def test_ipaddr_wildcard_ipv4_standardizer_correct_types_but_invalid_data():
    # Since invalid IPv4Addr or IPv4WildCard cannot be instantiated (they raise ValueError), we cannot pass them to the handler
    pass


def test_ipaddr_wildcard_ipv4_standardizer_none_ip():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(None, wildcard)
    assert result is None, "Should return None when IP address is None"


def test_ipaddr_wildcard_ipv4_standardizer_none_wildcard():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('192.168.1.1')
    result = handler.handle(ip_addr, None)
    assert result is None, "Should return None when wildcard is None"


def test_ipaddr_wildcard_ipv4_standardizer_valid_edge_case_ips():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('0.0.0.0')
    wildcard = IPv4WildCard('255.255.255.255')
    result = handler.handle(ip_addr, wildcard)
    assert result == (ip_addr, wildcard), "Handler should process edge case IP and wildcard"


def test_ipaddr_wildcard_ipv4_standardizer_ipv4addr_ipv4netmask():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4NetMask
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4NetMask('255.255.255.0')  # Should be IPv4WildCard
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when wildcard is not IPv4WildCard"


def test_ipaddr_wildcard_ipv4_standardizer_incorrect_types():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = 12345  # Incorrect type
    wildcard = ['0', '0', '0', '255']  # Incorrect type
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None for completely incorrect argument types"


def test_ipaddr_wildcard_ipv4_standardizer_edge_case_wildcards():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4Addr('255.255.255.255')
    wildcard = IPv4WildCard('0.0.0.0')
    result = handler.handle(ip_addr, wildcard)
    assert result == (ip_addr, wildcard), "Handler should process edge case wildcard mask"


def test_ipaddr_wildcard_ipv4_standardizer_ip_as_wildcard():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    ip_addr = IPv4WildCard('0.0.0.255')  # Wrong type
    wildcard = IPv4Addr('192.168.1.1')  # Wrong type
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when arguments are swapped types"


def test_ipaddr_wildcard_ipv4_standardizer_ipv6addr_and_ipv6wildcard():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6Addr, IPv6WildCard
    ip_addr = IPv6Addr('fe80::1')
    wildcard = IPv6WildCard('::ff')
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when both arguments are IPv6 types"


def test_ipaddr_wildcard_ipv4_standardizer_incorrect_argument_numbers():
    handler = IPAddrWildcardIPv4StandardizerHandler()
    result = handler.handle()
    assert result is None, "Should return None when no arguments are provided"
    ip_addr = IPv4Addr('192.168.1.1')
    result = handler.handle(ip_addr)
    assert result is None, "Should return None when only one argument is provided"
    wildcard = IPv4WildCard('0.0.0.255')
    result = handler.handle(ip_addr, wildcard, 'extra', 'arguments')
    assert result is None, "Should return None when too many arguments are provided"


def test_cidr_ipv6_standardizer_valid_input():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/64'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/64')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv6_standardizer_invalid_format():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1-64'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid format"


def test_cidr_ipv6_standardizer_non_hex_characters():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::g1/64'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-hexadecimal characters"


def test_cidr_ipv6_standardizer_leading_spaces():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '   2001:0db8::1/64'
    result = handler.handle(test_input)
    assert result is None, "Should return None for input with leading spaces"


def test_cidr_ipv6_standardizer_trailing_spaces():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/64   '
    result = handler.handle(test_input)
    assert result is None, "Should return None for input with trailing spaces"


def test_cidr_ipv6_standardizer_full_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    expected_netmask = IPv6NetMask('/128')
    assert result is not None, "Result should not be None"
    assert str(result[0]) == str(expected_ip), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv6_standardizer_out_of_range_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/129'
    result = handler.handle(test_input)
    assert result is None, "Should return None for netmask out of range"


def test_cidr_ipv6_standardizer_non_numeric_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for non-numeric netmask"


def test_cidr_ipv6_standardizer_leading_zeros():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '02001:0db8::0001/64'
    result = handler.handle(test_input)
    assert result is None, "Result should be None"


def test_cidr_ipv6_standardizer_empty_string():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = ''
    result = handler.handle(test_input)
    assert result is None, "Should return None for empty string"


def test_cidr_ipv6_standardizer_none_input():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = None
    result = handler.handle(test_input)
    assert result is None, "Should return None for None input"


def test_cidr_ipv6_standardizer_netmask_zero():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/0'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/0')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv6_standardizer_netmask_one():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/1'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/1')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv6_standardizer_extra_characters_in_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/64abc'
    result = handler.handle(test_input)
    assert result is None, "Should return None for extra characters in netmask"


def test_cidr_ipv6_standardizer_abbreviated_address():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '::1/128'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('::1')
    expected_netmask = IPv6NetMask('/128')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"


def test_cidr_ipv6_standardizer_invalid_address():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::zzzz/64'
    result = handler.handle(test_input)
    assert result is None, "Should return None for invalid IPv6 address"


def test_cidr_ipv6_standardizer_mixed_case_address():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0Db8::1/64'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/64')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"


def test_cidr_ipv6_standardizer_ipv4_mapped_ipv6():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '::ffff:192.168.1.1/96'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('::ffff:c0a8:101')
    expected_netmask = IPv6NetMask('/96')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"


def test_cidr_ipv6_standardizer_too_many_segments():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8:0:0:0:0:0:1:1/64'
    result = handler.handle(test_input)
    assert result is None, "Should return None for address with too many segments"


def test_cidr_ipv6_standardizer_missing_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1'
    result = handler.handle(test_input)
    assert result is None, "Should return None when netmask is missing"


def test_cidr_ipv6_standardizer_additional_spaces():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1    /64'
    result = handler.handle(test_input)
    assert result is None, "Should return None when there are additional spaces"


def test_cidr_ipv6_standardizer_space_in_address():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1 1/64'
    result = handler.handle(test_input)
    assert result is None, "Should return None when address contains spaces"


def test_cidr_ipv6_standardizer_address_with_zone_id():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = 'fe80::1%eth0/64'
    result = handler.handle(test_input)
    assert result is None, "Result should not be None"


def test_cidr_ipv6_standardizer_negative_netmask():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/-1'
    result = handler.handle(test_input)
    assert result is None, "Should return None for negative netmask"


def test_cidr_ipv6_standardizer_netmask_with_leading_zeros():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '2001:0db8::1/064'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/64')
    assert result is not None, "Result should not be None"
    assert str(result[1]) == str(expected_netmask), f"Expected Netmask {expected_netmask}, got {result[1]}"


def test_cidr_ipv6_standardizer_ip_with_embedded_ipv4():
    handler = CIDRInterfaceIPv6StandardizerHandler()
    test_input = '::ffff:192.0.2.128/96'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('::ffff:c000:0280')
    expected_netmask = IPv6NetMask('/96')
    assert result is not None, "Result should not be None"
    assert str(result[0]).lower() == str(expected_ip).lower(), f"Expected IP {expected_ip}, got {result[0]}"


def test_ipaddr_interface_ipv6_standardizer_valid_input():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should return the IP address and netmask as a tuple"


def test_ipaddr_interface_ipv6_standardizer_invalid_ip_type():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = '2001:db8::1'  # Not an IPv6Addr object
    netmask = IPv6NetMask('/64')
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for invalid IP address type"


def test_ipaddr_interface_ipv6_standardizer_invalid_netmask_type():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = '/64'  # Not an IPv6NetMask object
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for invalid netmask type"


def test_ipaddr_interface_ipv6_standardizer_wrong_number_of_args():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    # Missing netmask argument
    result = handler.handle(ip_addr)
    assert result is None, "Should return None when missing arguments"
    # Extra argument
    result = handler.handle(ip_addr, netmask, 'extra')
    assert result is None, "Should return None when extra arguments are provided"


def test_ipaddr_interface_ipv6_standardizer_none_arguments():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    result = handler.handle(None, None)
    assert result is None, "Should return None when arguments are None"


def test_ipaddr_interface_ipv6_standardizer_incorrect_argument_types2():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    result = handler.handle(123, 456)
    assert result is None, "Should return None for incorrect argument types"


def test_ipaddr_interface_ipv6_standardizer_ipv4addr_ipv6netmask():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4Addr
    ip_addr = IPv4Addr('192.168.1.1')  # IPv4Addr instead of IPv6Addr
    netmask = IPv6NetMask('/64')
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when IP is not IPv6Addr"


def test_ipaddr_interface_ipv6_standardizer_ipv6addr_ipv4netmask():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4NetMask
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv4NetMask('/24')  # IPv4NetMask instead of IPv6NetMask
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when netmask is not IPv6NetMask"


def test_ipaddr_interface_ipv6_standardizer_valid_input_with_full_netmask():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    netmask = IPv6NetMask('/128')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should process IP with /128 netmask"


def test_ipaddr_interface_ipv6_standardizer_edge_case_ips():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    # Test with '::' (unspecified address)
    ip_addr = IPv6Addr('::')
    netmask = IPv6NetMask('/0')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should handle '::' IP and /0 netmask"

    # Test with loopback address
    ip_addr = IPv6Addr('::1')
    netmask = IPv6NetMask('/128')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should handle loopback address"


def test_ipaddr_interface_ipv6_standardizer_invalid_ip_value():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    # Cannot create an invalid IPv6Addr, so test is not applicable
    pass


def test_ipaddr_interface_ipv6_standardizer_invalid_netmask_value():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    # Cannot create an invalid IPv6NetMask, so test is not applicable
    pass


def test_ipaddr_interface_ipv6_standardizer_mixed_argument_types():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = '2001:db8::1'  # String instead of IPv6Addr
    netmask = 64  # Integer instead of IPv6NetMask
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for mixed incorrect argument types"


def test_ipaddr_interface_ipv6_standardizer_empty_arguments():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    result = handler.handle()
    assert result is None, "Should return None when no arguments are provided"


def test_ipaddr_interface_ipv6_standardizer_additional_arguments():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    extra_arg1 = 'extra1'
    extra_arg2 = 'extra2'
    result = handler.handle(ip_addr, netmask, extra_arg1, extra_arg2)
    assert result is None, "Should return None when too many arguments are provided"


def test_ipaddr_interface_ipv6_standardizer_ipv6addr_ipv6netmask_objects():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should return the IP address and netmask as a tuple"


def test_ipaddr_interface_ipv6_standardizer_none_ip():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    netmask = IPv6NetMask('/64')
    result = handler.handle(None, netmask)
    assert result is None, "Should return None when IP address is None"


def test_ipaddr_interface_ipv6_standardizer_none_netmask():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    result = handler.handle(ip_addr, None)
    assert result is None, "Should return None when netmask is None"


def test_ipaddr_interface_ipv6_standardizer_incorrect_argument_types():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = 12345  # Incorrect type
    netmask = ['/', '64']  # Incorrect type
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None for completely incorrect argument types"


def test_ipaddr_interface_ipv6_standardizer_ipv6addr_ipv6wildcard():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6WildCard
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('::ff')  # Should be IPv6NetMask
    result = handler.handle(ip_addr, wildcard)
    assert result is None, "Should return None when netmask is not IPv6NetMask"


def test_ipaddr_interface_ipv6_standardizer_ip_as_netmask():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6NetMask('/64')  # Wrong type
    netmask = IPv6Addr('2001:db8::1')  # Wrong type
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when arguments are swapped types"


def test_ipaddr_interface_ipv6_standardizer_ipv4_objects():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('/24')
    result = handler.handle(ip_addr, netmask)
    assert result is None, "Should return None when IPv4 objects are provided"


def test_ipaddr_interface_ipv6_standardizer_ipv6addr_with_embedded_ipv4():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('::ffff:192.168.1.1')
    netmask = IPv6NetMask('/96')
    result = handler.handle(ip_addr, netmask)
    assert result == (ip_addr, netmask), "Handler should process IPv6 address with embedded IPv4"


def test_ipaddr_interface_ipv6_standardizer_extra_arguments():
    handler = IPAddrInterfaceIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    extra_arg = 'extra'
    result = handler.handle(ip_addr, netmask, extra_arg)
    assert result is None, "Should return None when extra arguments are provided"


def test_colon_wildcard_ipv6_standardizer_valid_input():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_invalid_format():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1/ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_non_hex_characters():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::g1 ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_invalid_wildcard():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff:gggg:gggg:gggg:gggg'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_leading_zeros():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '02001:0db8::0001 0fff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None  # Leading zeros are not allowed in IPv6 addresses


def test_colon_wildcard_ipv6_standardizer_empty_string():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = ''
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_none_input():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = None
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_wildcard_zero():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = 'fe80::1 ::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('fe80::1')
    expected_wildcard = IPv6WildCard('::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_wildcard_all_ones():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = 'fe80::1 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('fe80::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_extra_characters_in_wildcard():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff::abc'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::abc')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_missing_wildcard():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_additional_spaces():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1    ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_tab_separator():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1\tffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_invalid_ip_and_wildcard():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = 'zzzz:zzzz::1 zzzz:zzzz::'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_mixed_case():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:Db8::1 fFFF:ffff:FFFF:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_multiple_spaces():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1      ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_ipv4_mapped_ipv6():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '::ffff:192.168.1.1 ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    expected_ip = IPv6Addr('::ffff:192.168.1.1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_colon_wildcard_ipv6_standardizer_no_space_separator():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_space_in_wildcard():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8::1 ffff:ffff :ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None


def test_colon_wildcard_ipv6_standardizer_too_many_segments():
    handler = ColonWildcardIPv6StandardizerHandler()
    test_input = '2001:db8:0:0:0:0:0:1:1 ffff:ffff:ffff:ffff::'
    result = handler.handle(test_input)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_valid_input():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_ipaddr_wildcard_ipv6_standardizer_invalid_ip_type():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = '2001:db8::1'  # Not an IPv6Addr object
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_invalid_wildcard_type():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = 'ffff:ffff:ffff:ffff::'  # Not an IPv6WildCard object
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_wrong_number_of_args():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr)
    assert result is None
    result = handler.handle(ip_addr, wildcard, 'extra')
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_none_arguments():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    result = handler.handle(None, None)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_incorrect_argument_types():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    result = handler.handle(12345, 67890)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_ipv4addr_ipv6wildcard():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4Addr
    ip_addr = IPv4Addr('192.168.1.1')  # IPv4Addr instead of IPv6Addr
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_ipv6addr_ipv4wildcard():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv4WildCard
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv4WildCard('0.0.0.255')  # IPv4WildCard instead of IPv6WildCard
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_valid_edge_case_ips():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('::')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard)
    expected_ip = IPv6Addr('::')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_ipaddr_wildcard_ipv6_standardizer_ip_as_wildcard():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6WildCard('ffff:ffff:ffff:ffff::')  # Wrong type
    wildcard = IPv6Addr('2001:db8::1')  # Wrong type
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_ipv6addr_ipv6netmask():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    from ttlinks.ipservice.ip_address import IPv6NetMask
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6NetMask('/64')  # Should be IPv6WildCard
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_extra_arguments():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard, 'extra')
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_none_ip():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(None, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_none_wildcard():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('2001:db8::1')
    result = handler.handle(ip_addr, None)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_ipv6addr_with_embedded_ipv4():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = IPv6Addr('::ffff:192.168.1.1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = handler.handle(ip_addr, wildcard)
    expected_ip = IPv6Addr('::ffff:192.168.1.1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_ipaddr_wildcard_ipv6_standardizer_mixed_argument_types():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    ip_addr = '2001:db8::1'  # Should be IPv6Addr object
    wildcard = 'ffff:ffff:ffff:ffff::'  # Should be IPv6WildCard object
    result = handler.handle(ip_addr, wildcard)
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_empty_arguments():
    handler = IPAddrWildcardIPv6StandardizerHandler()
    result = handler.handle()
    assert result is None


def test_ipaddr_wildcard_ipv6_standardizer_invalid_ip_value():
    # Cannot create invalid IPv6Addr; invalid IP would raise exception during object creation
    pass


def test_ipaddr_wildcard_ipv6_standardizer_invalid_wildcard_value():
    # Cannot create invalid IPv6WildCard; invalid wildcard would raise exception during object creation
    pass


def test_ipv4_interface_valid_cidr_input():
    test_input = '192.168.1.1/24'
    result = IPStandardizer.ipv4_interface(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('/24')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_netmask)


def test_ipv4_interface_valid_dot_input():
    test_input = '192.168.1.1 255.255.255.0'
    result = IPStandardizer.ipv4_interface(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_netmask = IPv4NetMask('255.255.255.0')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_netmask)


def test_ipv4_interface_ipaddr_netmask_objects():
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('/24')
    result = IPStandardizer.ipv4_interface(ip_addr, netmask)
    assert result is not None
    assert str(result[0]) == str(ip_addr)
    assert str(result[1]) == str(netmask)


def test_ipv4_interface_invalid_input():
    test_input = 'invalid input'
    result = IPStandardizer.ipv4_interface(test_input)
    assert result is None


def test_ipv4_interface_none_input():
    result = IPStandardizer.ipv4_interface(None)
    assert result is None


def test_ipv4_wildcard_valid_input():
    test_input = '192.168.1.1 0.0.0.255'
    result = IPStandardizer.ipv4_wildcard(test_input)
    expected_ip = IPv4Addr('192.168.1.1')
    expected_wildcard = IPv4WildCard('0.0.0.255')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_ipv4_wildcard_ipaddr_wildcard_objects():
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    result = IPStandardizer.ipv4_wildcard(ip_addr, wildcard)
    assert result is not None
    assert str(result[0]) == str(ip_addr)
    assert str(result[1]) == str(wildcard)


def test_ipv4_wildcard_invalid_input():
    test_input = 'invalid input'
    result = IPStandardizer.ipv4_wildcard(test_input)
    assert result is None


def test_ipv4_wildcard_none_input():
    result = IPStandardizer.ipv4_wildcard(None)
    assert result is None


def test_ipv6_interface_valid_cidr_input():
    test_input = '2001:db8::1/64'
    result = IPStandardizer.ipv6_interface(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('/64')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_netmask)


def test_ipv6_interface_valid_colon_input():
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff::'
    result = IPStandardizer.ipv6_interface(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_netmask = IPv6NetMask('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_netmask)


def test_ipv6_interface_ipaddr_netmask_objects():
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    result = IPStandardizer.ipv6_interface(ip_addr, netmask)
    assert result is not None
    assert str(result[0]) == str(ip_addr)
    assert str(result[1]) == str(netmask)


def test_ipv6_interface_invalid_input():
    test_input = 'invalid input'
    result = IPStandardizer.ipv6_interface(test_input)
    assert result is None


def test_ipv6_interface_none_input():
    result = IPStandardizer.ipv6_interface(None)
    assert result is None


def test_ipv6_wildcard_valid_input():
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff::'
    result = IPStandardizer.ipv6_wildcard(test_input)
    expected_ip = IPv6Addr('2001:db8::1')
    expected_wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_wildcard)


def test_ipv6_wildcard_ipaddr_wildcard_objects():
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    result = IPStandardizer.ipv6_wildcard(ip_addr, wildcard)
    assert result is not None
    assert str(result[0]) == str(ip_addr)
    assert str(result[1]) == str(wildcard)


def test_ipv6_wildcard_invalid_input():
    test_input = 'invalid input'
    result = IPStandardizer.ipv6_wildcard(test_input)
    assert result is None


def test_ipv6_wildcard_none_input():
    result = IPStandardizer.ipv6_wildcard(None)
    assert result is None


def test_ipv4_interface_ipv6_input():
    test_input = '2001:db8::1/64'
    result = IPStandardizer.ipv4_interface(test_input)
    assert result is None


def test_ipv6_interface_ipv4_input():
    test_input = '192.168.1.1/24'
    result = IPStandardizer.ipv6_interface(test_input)
    assert result is None


def test_ipv4_wildcard_ipv6_input():
    test_input = '2001:db8::1 ffff:ffff:ffff:ffff::'
    result = IPStandardizer.ipv4_wildcard(test_input)
    assert result is None


def test_ipv6_wildcard_ipv4_input():
    test_input = '192.168.1.1 0.0.0.255'
    result = IPStandardizer.ipv6_wildcard(test_input)
    assert result is None


def test_ipv4_interface_extra_arguments():
    ip_addr = IPv4Addr('192.168.1.1')
    netmask = IPv4NetMask('/24')
    extra_arg = 'extra'
    result = IPStandardizer.ipv4_interface(ip_addr, netmask, extra_arg)
    assert result is None


def test_ipv6_interface_extra_arguments():
    ip_addr = IPv6Addr('2001:db8::1')
    netmask = IPv6NetMask('/64')
    extra_arg = 'extra'
    result = IPStandardizer.ipv6_interface(ip_addr, netmask, extra_arg)
    assert result is None


def test_ipv4_wildcard_extra_arguments():
    ip_addr = IPv4Addr('192.168.1.1')
    wildcard = IPv4WildCard('0.0.0.255')
    extra_arg = 'extra'
    result = IPStandardizer.ipv4_wildcard(ip_addr, wildcard, extra_arg)
    assert result is None


def test_ipv6_wildcard_extra_arguments():
    ip_addr = IPv6Addr('2001:db8::1')
    wildcard = IPv6WildCard('ffff:ffff:ffff:ffff::')
    extra_arg = 'extra'
    result = IPStandardizer.ipv6_wildcard(ip_addr, wildcard, extra_arg)
    assert result is None


def test_ipv4_interface_ip_only():
    test_input = '192.168.1.1'
    result = IPStandardizer.ipv4_interface(test_input)
    assert result is None


def test_ipv6_interface_ip_only():
    test_input = '2001:db8::1'
    result = IPStandardizer.ipv6_interface(test_input)
    assert result is None


def test_ipv4_wildcard_ip_only():
    test_input = '192.168.1.1'
    result = IPStandardizer.ipv4_wildcard(test_input)
    assert result is None


def test_ipv6_wildcard_ip_only():
    test_input = '2001:db8::1'
    result = IPStandardizer.ipv6_wildcard(test_input)
    assert result is None


def test_ipv6_interface_ipv4_mapped_ipv6():
    test_input = '::ffff:192.168.1.1/96'
    result = IPStandardizer.ipv6_interface(test_input)
    expected_ip = IPv6Addr('::ffff:192.168.1.1')
    expected_netmask = IPv6NetMask('/96')
    assert result is not None
    assert str(result[0]) == str(expected_ip)
    assert str(result[1]) == str(expected_netmask)
