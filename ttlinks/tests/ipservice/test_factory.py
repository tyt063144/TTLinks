import pytest

from ttlinks.ipservice.ip_configs import IPv4HostConfig, IPv4SubnetConfig, IPv4WildCardConfig, IPv6HostConfig, IPv6SubnetConfig, IPv6WildCardConfig
from ttlinks.ipservice.ip_factory import IPv4Factory, IPv6Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks, IPv6TypeAddrBlocks


@pytest.fixture
def ipv4_factory():
    return IPv4Factory()


def test_ipv4_host_creation(ipv4_factory):
    host = "192.168.1.10/24"
    ipv4_host = ipv4_factory.host(host)
    assert isinstance(ipv4_host, IPv4HostConfig)
    assert str(ipv4_host.addr) == "192.168.1.10"
    assert str(ipv4_host.mask) == "255.255.255.0"


def test_ipv4_subnet_creation(ipv4_factory):
    subnet = "192.168.1.0/24"
    ipv4_subnet = ipv4_factory.subnet(subnet)
    assert isinstance(ipv4_subnet, IPv4SubnetConfig)
    assert str(ipv4_subnet.addr) == "192.168.1.0"
    assert str(ipv4_subnet.mask) == "255.255.255.0"


def test_ipv4_wildcard_creation(ipv4_factory):
    wildcard = "192.168.1.10 0.0.0.255"
    ipv4_wildcard = ipv4_factory.wildcard(wildcard)
    assert isinstance(ipv4_wildcard, IPv4WildCardConfig)
    assert str(ipv4_wildcard.addr) == "192.168.1.0"
    assert str(ipv4_wildcard.mask) == "0.0.0.255"


def test_ipv4_random_host(ipv4_factory):
    ipv4_random_host = ipv4_factory.random_host(IPv4TypeAddrBlocks.PRIVATE)
    assert isinstance(ipv4_random_host, IPv4HostConfig)
    assert ipv4_random_host.addr is not None


def test_ipv4_random_subnet(ipv4_factory):
    ipv4_random_subnet = ipv4_factory.random_subnet(IPv4TypeAddrBlocks.PRIVATE)
    assert isinstance(ipv4_random_subnet, IPv4SubnetConfig)
    assert ipv4_random_subnet.addr is not None


def test_ipv4_batch_host_creation(ipv4_factory):
    hosts = ["192.168.1.10/24", "172.16.0.10/16", "10.0.0.10/8"]
    ipv4_hosts = ipv4_factory.batch_hosts(*hosts)
    assert len(ipv4_hosts) == 3
    for ipv4_host in ipv4_hosts:
        assert isinstance(ipv4_host, IPv4HostConfig)


def test_ipv4_batch_subnet_creation(ipv4_factory):
    subnets = ["192.168.1.0/24", "172.16.0.0/16", "10.0.0.0/8"]
    ipv4_subnets = ipv4_factory.batch_subnets(*subnets)
    assert len(ipv4_subnets) == 3
    for ipv4_subnet in ipv4_subnets:
        assert isinstance(ipv4_subnet, IPv4SubnetConfig)


@pytest.fixture
def ipv6_factory():
    return IPv6Factory()


def test_ipv6_host_creation(ipv6_factory):
    host = "2001:db8::1/64"
    ipv6_host = ipv6_factory.host(host)
    assert isinstance(ipv6_host, IPv6HostConfig)
    assert str(ipv6_host.addr) == "2001:db8::1".upper()
    assert str(ipv6_host.mask) == "ffff:ffff:ffff:ffff::".upper()


def test_ipv6_subnet_creation(ipv6_factory):
    subnet = "2001:db8::/64"
    ipv6_subnet = ipv6_factory.subnet(subnet)
    assert isinstance(ipv6_subnet, IPv6SubnetConfig)
    assert str(ipv6_subnet.addr) == "2001:db8::".upper()
    assert str(ipv6_subnet.mask) == "ffff:ffff:ffff:ffff::".upper()


def test_ipv6_wildcard_creation(ipv6_factory):
    wildcard = "2001:db8::1 ::ff"
    ipv6_wildcard = ipv6_factory.wildcard(wildcard)
    assert isinstance(ipv6_wildcard, IPv6WildCardConfig)
    assert str(ipv6_wildcard.addr) == "2001:db8::".upper()
    assert str(ipv6_wildcard.mask) == "::ff".upper()


def test_ipv6_random_host(ipv6_factory):
    ipv6_random_host = ipv6_factory.random_host(IPv6TypeAddrBlocks.LINK_LOCAL)
    assert isinstance(ipv6_random_host, IPv6HostConfig)
    assert ipv6_random_host.addr is not None


def test_ipv6_random_subnet(ipv6_factory):
    ipv6_random_subnet = ipv6_factory.random_subnet(IPv6TypeAddrBlocks.LINK_LOCAL)
    assert isinstance(ipv6_random_subnet, IPv6SubnetConfig)
    assert ipv6_random_subnet.addr is not None


def test_ipv6_batch_host_creation(ipv6_factory):
    hosts = ["2001:db8::1/64", "fe80::1/64", "::1/128"]
    ipv6_hosts = ipv6_factory.batch_hosts(hosts)
    assert len(ipv6_hosts) == 3
    for ipv6_host in ipv6_hosts:
        assert isinstance(ipv6_host, IPv6HostConfig)


def test_ipv6_batch_subnet_creation(ipv6_factory):
    subnets = ["2001:db8::/64", "fe80::/64", "::/128"]
    ipv6_subnets = ipv6_factory.batch_subnets(subnets)
    assert len(ipv6_subnets) == 3
    for ipv6_subnet in ipv6_subnets:
        assert isinstance(ipv6_subnet, IPv6SubnetConfig)
