import pytest

from ttlinks.ipservice import ip_utils
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig, IPv6SubnetConfig
from ttlinks.ipservice.ip_subnet_type_classifiers import IPSubnetTypeClassifier


def test_ipv4_private_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("192.168.1.0/15")))
    expected = {ip_utils.IPv4AddrType.PRIVATE, ip_utils.IPv4AddrType.PUBLIC}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_unspecified_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("0.0.0.0/32")))
    expected = {ip_utils.IPv4AddrType.UNSPECIFIED, ip_utils.IPv4AddrType.CURRENT_NETWORK}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_loopback_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("127.0.0.1/8")))
    expected = {ip_utils.IPv4AddrType.LOOPBACK}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_multicast_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("224.0.0.1/4")))
    expected = {ip_utils.IPv4AddrType.MULTICAST, ip_utils.IPv4AddrType.DOCUMENTATION}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_documentation_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("198.51.100.0/24")))
    expected = {ip_utils.IPv4AddrType.DOCUMENTATION}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_loopback_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::1/128")))
    expected = {ip_utils.IPv6AddrType.LOOPBACK}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_global_unicast_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("2001:db8::/32")))
    expected = {ip_utils.IPv6AddrType.DOCUMENTATION, ip_utils.IPv6AddrType.GLOBAL_UNICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_multicast_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("ff00::/8")))
    expected = {ip_utils.IPv6AddrType.MULTICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_unique_local_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("fc00::/7")))
    expected = {ip_utils.IPv6AddrType.UNIQUE_LOCAL}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_teredo_tunneling_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("2001::/32")))
    expected = {ip_utils.IPv6AddrType.TEREDO_TUNNELING, ip_utils.IPv6AddrType.GLOBAL_UNICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_carrier_nat_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("100.64.0.0/10")))
    expected = {ip_utils.IPv4AddrType.CARRIER_GRADE_NAT}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_benchmark_testing_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("198.18.0.0/15")))
    expected = {ip_utils.IPv4AddrType.BENCHMARK_TESTING}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_reserved_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("240.0.0.0/4")))
    expected = {ip_utils.IPv4AddrType.RESERVED, ip_utils.IPv4AddrType.LIMITED_BROADCAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_unspecified_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::/128")))
    expected = {ip_utils.IPv6AddrType.UNSPECIFIED}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_discard_prefix_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("100::/64")))
    expected = {ip_utils.IPv6AddrType.DISCARD_PREFIX}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_ipv4_mapped_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::ffff:192.0.2.128/96")))
    expected = {ip_utils.IPv6AddrType.IPV4_MAPPED}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_ipv4_translated_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::ffff:0:192.0.2.128/96")))
    expected = {ip_utils.IPv6AddrType.IPV4_TRANSLATED}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_orchidv2_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("2001:20::/28")))
    expected = {ip_utils.IPv6AddrType.ORCHIDV2, ip_utils.IPv6AddrType.GLOBAL_UNICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_srv6_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("5f00::/16")))
    expected = {ip_utils.IPv6AddrType.SRV6}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_6to4_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("2002::/16")))
    expected = {ip_utils.IPv6AddrType.IP6_TO4, ip_utils.IPv6AddrType.GLOBAL_UNICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_limited_broadcast_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("255.255.255.255/32")))
    expected = {ip_utils.IPv4AddrType.LIMITED_BROADCAST, ip_utils.IPv4AddrType.RESERVED}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_public_and_private_overlap():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("192.168.0.0/16")))
    expected = {ip_utils.IPv4AddrType.PRIVATE}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_entire_space():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("0.0.0.0/0")))
    expected = {
        ip_utils.IPv4AddrType.PUBLIC,
        ip_utils.IPv4AddrType.UNSPECIFIED,
        ip_utils.IPv4AddrType.CURRENT_NETWORK,
        ip_utils.IPv4AddrType.PRIVATE,
        ip_utils.IPv4AddrType.MULTICAST,
        ip_utils.IPv4AddrType.LINK_LOCAL,
        ip_utils.IPv4AddrType.LOOPBACK,
        ip_utils.IPv4AddrType.DOCUMENTATION,
        ip_utils.IPv4AddrType.RESERVED,
        ip_utils.IPv4AddrType.LIMITED_BROADCAST,
        ip_utils.IPv4AddrType.CARRIER_GRADE_NAT,
        ip_utils.IPv4AddrType.BENCHMARK_TESTING,
        ip_utils.IPv4AddrType.IPV6_TO_IPV4_RELAY,
        ip_utils.IPv4AddrType.DS_LITE
    }
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_entire_space():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::/0")))
    expected = {
        ip_utils.IPv6AddrType.UNSPECIFIED,
        ip_utils.IPv6AddrType.SRV6,
        ip_utils.IPv6AddrType.GLOBAL_UNICAST,
        ip_utils.IPv6AddrType.UNIQUE_LOCAL,
        ip_utils.IPv6AddrType.MULTICAST,
        ip_utils.IPv6AddrType.LINK_LOCAL,
        ip_utils.IPv6AddrType.LOOPBACK,
        ip_utils.IPv6AddrType.DOCUMENTATION,
        ip_utils.IPv6AddrType.IPV4_MAPPED,
        ip_utils.IPv6AddrType.IPV4_TRANSLATED,
        ip_utils.IPv6AddrType.IPV4_IPV6_TRANSLATION,
        ip_utils.IPv6AddrType.DISCARD_PREFIX,
        ip_utils.IPv6AddrType.IP6_TO4,
        ip_utils.IPv6AddrType.TEREDO_TUNNELING,
        ip_utils.IPv6AddrType.ORCHIDV2,
    }
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_point_to_point():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("192.168.1.0/31")))
    expected = {ip_utils.IPv4AddrType.PRIVATE}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_point_to_point():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("2001:db8::/127")))
    expected = {ip_utils.IPv6AddrType.DOCUMENTATION, ip_utils.IPv6AddrType.GLOBAL_UNICAST}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv4_overlap_boundary():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("224.0.0.0/4")))
    expected = {ip_utils.IPv4AddrType.MULTICAST, ip_utils.IPv4AddrType.DOCUMENTATION}
    assert result == expected, f"expected {expected}, but got {result}"


def test_ipv6_unspecified_and_loopback():
    subnet_classifier = IPSubnetTypeClassifier()
    result = set(subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::/128")))
    expected = {ip_utils.IPv6AddrType.UNSPECIFIED}
    assert result == expected, f"expected {expected}, but got {result}"


def test_invalid_ipv4_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    with pytest.raises(ValueError):
        subnet_classifier.classify_ipv4_subnet_types(IPv4SubnetConfig("192.168.1.0/33"))


def test_invalid_ipv6_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    with pytest.raises(ValueError):
        subnet_classifier.classify_ipv6_subnet_types(IPv6SubnetConfig("::/129"))


def test_empty_ipv4_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    with pytest.raises(AttributeError):
        subnet_classifier.classify_ipv4_subnet_types(None)


def test_empty_ipv6_subnet():
    subnet_classifier = IPSubnetTypeClassifier()
    with pytest.raises(AttributeError):
        subnet_classifier.classify_ipv6_subnet_types(None)
