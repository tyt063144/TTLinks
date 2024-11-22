import pytest

from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr, IPv4NetMask, IPv4WildCard, IPv6NetMask, IPv6WildCard


# IPv4 Address Tests
def test_ipv4_address_valid():
    ip = IPv4Addr("192.168.1.1")
    assert str(ip) == "192.168.1.1", "Should return the correct string representation"


def test_ipv4_address_invalid():
    with pytest.raises(ValueError):
        IPv4Addr("999.999.999.999")


def test_ipv4_address_binary_string():
    ip = IPv4Addr("192.168.1.1")
    expected_binary = '11000000101010000000000100000001'
    assert ip.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv4_address_binary_digits():
    ip = IPv4Addr("192.168.1.1")
    expected_digits = [int(x) for x in '11000000101010000000000100000001']
    assert list(ip.binary_digits) == expected_digits, "Should return the correct binary digits"


def test_ipv4_address_too_short():
    with pytest.raises(ValueError):
        IPv4Addr("192.168.1")


def test_ipv4_address_too_long():
    with pytest.raises(ValueError):
        IPv4Addr("192.168.1.1.1")


def test_ipv4_address_empty():
    with pytest.raises(ValueError):
        IPv4Addr("")


# IPv6 Address Tests
def test_ipv6_address_valid():
    ip = IPv6Addr("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert str(ip) == "2001:db8:85a3::8a2e:370:7334".upper(), "Should return the correct string representation"


def test_ipv6_address_invalid():
    with pytest.raises(ValueError):
        IPv6Addr("2001:0db8:85a3:0000:0000:8a2e:0370:7334:9876")


def test_ipv6_address_binary_string():
    ip = IPv6Addr("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    expected_binary = ('0010000000000001000011011011100010000101101000110000000000000000'
                       '0000000000000000100010100010111000000011011100000111001100110100')
    assert ip.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv6_address_binary_digits():
    ip = IPv6Addr("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    expected_digits = [int(x) for x in [
        0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,
        1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0
    ]]
    assert list(ip.binary_digits) == expected_digits, "Should return the correct binary digits"


def test_ipv6_address_compressed():
    ip = IPv6Addr("2001:db8::8a2e:370:7334")
    assert str(ip) == "2001:db8::8a2e:370:7334".upper(), "Should handle and return compressed IPv6 address correctly"


def test_ipv6_address_loopback():
    ip = IPv6Addr("::1")
    assert str(ip) == "::1", "Should correctly handle the loopback address"


def test_ipv6_address_empty():
    with pytest.raises(ValueError):
        IPv6Addr("")


# IPv4 Netmask Tests
def test_ipv4_netmask_valid():
    mask = IPv4NetMask("255.255.255.0")
    assert str(mask) == "255.255.255.0", "Should return the correct string representation"


def test_ipv4_netmask_invalid():
    with pytest.raises(ValueError):
        IPv4NetMask("255.255.255.256")


def test_ipv4_netmask_size():
    mask = IPv4NetMask("255.255.255.0")
    assert mask.mask_size == 24, "Should return the correct mask size"


def test_ipv4_netmask_binary_string():
    mask = IPv4NetMask("255.255.255.0")
    expected_binary = '11111111111111111111111100000000'
    assert mask.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv4_netmask_cidr_notation():
    mask = IPv4NetMask("/24")
    assert str(mask) == "255.255.255.0", "Should convert CIDR to dotted decimal"


def test_ipv4_netmask_all_zeros():
    mask = IPv4NetMask("0.0.0.0")
    assert mask.mask_size == 0, "Should handle zero netmask correctly"


def test_ipv4_netmask_all_ones():
    mask = IPv4NetMask("255.255.255.255")
    assert mask.mask_size == 32, "Should handle full netmask correctly"


# IPv4 Wildcard Tests
def test_ipv4_wildcard_valid():
    wildcard = IPv4WildCard("0.0.0.255")
    assert str(wildcard) == "0.0.0.255", "Should return the correct string representation"


def test_ipv4_wildcard_invalid():
    with pytest.raises(ValueError):
        IPv4WildCard("256.0.0.0")


def test_ipv4_wildcard_mask_size():
    wildcard = IPv4WildCard("0.0.0.255")
    assert wildcard.mask_size == 8, "Should return the correct range size based on the wildcard mask"


def test_ipv4_wildcard_binary_string():
    wildcard = IPv4WildCard("0.255.0.255")
    expected_binary = '00000000111111110000000011111111'
    assert wildcard.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv4_wildcard_all_ones():
    wildcard = IPv4WildCard("0.0.0.0")
    assert wildcard.mask_size == 0, "Should handle the wildcard that matches no IPs"


def test_ipv4_wildcard_all_zeros():
    wildcard = IPv4WildCard("255.255.255.255")
    assert wildcard.mask_size == 32, "Should handle the wildcard that matches all IPs"


# IPv6 Netmask Tests
def test_ipv6_netmask_valid():
    mask = IPv6NetMask("ffff:ffff:ffff:ffff::")
    assert str(mask) == "ffff:ffff:ffff:ffff::".upper(), "Should return the correct string representation"


def test_ipv6_netmask_invalid():
    with pytest.raises(ValueError):
        IPv6NetMask("gggg:gggg:gggg:gggg::")


def test_ipv6_netmask_size():
    mask = IPv6NetMask("ffff:ffff:ffff:ffff::")
    assert mask.mask_size == 64, "Should return the correct mask size"


def test_ipv6_netmask_binary_string():
    mask = IPv6NetMask("ffff:ffff:ffff:ffff::")
    expected_binary = ('1111111111111111111111111111111111111111111111111111111111111111'
                       '0000000000000000000000000000000000000000000000000000000000000000')
    assert mask.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv6_netmask_cidr_notation():
    mask = IPv6NetMask("/64")
    assert str(mask) == "ffff:ffff:ffff:ffff::".upper(), "Should convert CIDR to full IPv6 netmask"


def test_ipv6_netmask_all_zeros():
    mask = IPv6NetMask("::")
    assert mask.mask_size == 0, "Should handle zero netmask correctly"


def test_ipv6_netmask_all_ones():
    mask = IPv6NetMask("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    assert mask.mask_size == 128, "Should handle full netmask correctly"


# IPv6 Wildcard Tests
def test_ipv6_wildcard_valid():
    wildcard = IPv6WildCard("ffff:ffff::ffff")
    assert str(wildcard) == "ffff:ffff::ffff".upper(), "Should return the correct string representation"


def test_ipv6_wildcard_invalid():
    with pytest.raises(ValueError):
        IPv6WildCard("gggg:gggg::gggg")


def test_ipv6_wildcard_mask_size():
    wildcard = IPv6WildCard("ffff:ffff::")
    assert wildcard.mask_size == 32, "Should return the correct range size based on the wildcard mask"


def test_ipv6_wildcard_binary_string():
    wildcard = IPv6WildCard("ffff:ffff::ffff")
    expected_binary = ('1111111111111111111111111111111100000000000000000000000000000000'
                       '0000000000000000000000000000000000000000000000001111111111111111')
    assert wildcard.binary_string == expected_binary, "Should return the correct binary string"


def test_ipv6_wildcard_all_zeros():
    wildcard = IPv6WildCard("::")
    assert wildcard.mask_size == 0, "Should handle wildcard that matches only one address"


def test_ipv6_wildcard_all_ones():
    wildcard = IPv6WildCard("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    assert wildcard.mask_size == 128, "Should handle wildcard that matches all IPs"
