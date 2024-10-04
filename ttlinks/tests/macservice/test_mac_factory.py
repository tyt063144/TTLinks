import pytest
from ttlinks.macservice.mac_factory import MACFactory, MACRandomizer
from ttlinks.macservice.mac_address import InterfaceMACAddr, MACType

# Initialize the MACFactory for the test cases
factory = MACFactory()
randomizer = MACRandomizer()

def test_single_mac_creation():
    # Test creation of a single MAC address
    mac_address = "12:34:56:78:90:AB"
    mac_obj = factory.mac(mac_address)
    assert isinstance(mac_obj, InterfaceMACAddr)
    assert str(mac_obj) == mac_address

def test_batch_mac_creation():
    # Test batch creation of MAC addresses
    mac_addresses = ["12:34:56:78:90:AB", "AB:CD:EF:12:34:56"]
    mac_objs = factory.batch_macs(mac_addresses)
    assert len(mac_objs) == 2
    assert str(mac_objs[0]) == mac_addresses[0]
    assert str(mac_objs[1]) == mac_addresses[1]

def test_duplicate_removal_in_batch():
    # Test that duplicate MAC addresses are removed in batch processing
    mac_addresses = ["12:34:56:78:90:AB", "12:34:56:78:90:AB"]
    mac_objs = factory.batch_macs(mac_addresses, keep_dup=False)
    assert len(mac_objs) == 1  # Duplicate should be removed

def test_random_mac_generation():
    # Test generation of a random MAC address
    mac_obj = factory.random_mac()
    assert isinstance(mac_obj, InterfaceMACAddr)
    assert len(str(mac_obj).split(":")) == 6  # Check valid MAC format

def test_random_mac_unicast_generation():
    # Test generation of a random unicast MAC address
    mac_obj = factory.random_mac(MACType.UNICAST)
    assert isinstance(mac_obj, InterfaceMACAddr)
    first_octet = int(str(mac_obj).split(":")[0], 16)
    assert not (first_octet & 0x01)  # Check LSB of first octet is 0 (unicast)

def test_random_mac_multicast_generation():
    # Test generation of a random multicast MAC address
    mac_obj = factory.random_mac(MACType.MULTICAST)
    assert isinstance(mac_obj, InterfaceMACAddr)
    first_octet = int(str(mac_obj).split(":")[0], 16)
    assert first_octet & 0x01  # Check LSB of first octet is 1 (multicast)

def test_random_macs_batch():
    # Test generation of a batch of random MAC addresses
    num_macs = 5
    mac_objs = factory.random_macs_batch(num_macs=num_macs)
    assert len(mac_objs) == num_macs
    for mac in mac_objs:
        assert len(str(mac).split(":")) == 6  # Check valid MAC format

def test_random_mac_unicast():
    # Test random unicast MAC address generation
    mac_int = randomizer.randomize(MACType.UNICAST)
    assert mac_int & (1 << 40) == 0  # Check LSB of first octet is 0 (unicast)

def test_random_mac_multicast():
    # Test random multicast MAC address generation
    mac_int = randomizer.randomize(MACType.MULTICAST)
    assert mac_int & (1 << 40) == (1 << 40)  # Check LSB of first octet is 1 (multicast)

def test_random_mac_broadcast():
    # Test broadcast MAC address generation
    mac_int = randomizer.randomize(MACType.BROADCAST)
    assert mac_int == 0xFFFFFFFFFFFF  # Check that all bits are set for broadcast