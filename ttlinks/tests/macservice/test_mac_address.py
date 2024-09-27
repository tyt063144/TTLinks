import pytest

from ttlinks.macservice.mac_address import MACAddr
from ttlinks.macservice import MACType


def test_mac_initialization_unicast():
    """Test the initialization and classification of a unicast MAC address."""
    mac_addr = MACAddr("b0-fc-0d-60-51-f8")
    assert str(mac_addr) == "B0:FC:0D:60:51:F8", "MAC address string conversion failed."
    assert mac_addr.mac_type == MACType.UNICAST, "Failed to classify unicast MAC address."


def test_mac_initialization_multicast():
    """Test the initialization and classification of a multicast MAC address."""
    mac_addr = MACAddr("01-00-5e-00-00-fb")
    assert str(mac_addr) == "01:00:5E:00:00:FB", "MAC address string conversion failed."
    assert mac_addr.mac_type == MACType.MULTICAST, "Failed to classify multicast MAC address."


def test_mac_initialization_broadcast():
    """Test the initialization and classification of a broadcast MAC address."""
    mac_addr = MACAddr("ff:ff:ff:ff:ff:ff")
    assert str(mac_addr) == "FF:FF:FF:FF:FF:FF", "MAC address string conversion failed."
    assert mac_addr.mac_type == MACType.BROADCAST, "Failed to classify broadcast MAC address."


def test_invalid_mac_initialization():
    """Test that invalid MAC addresses raise an error during initialization."""
    with pytest.raises(ValueError, match=r"MAC address .* is not valid"):
        MACAddr("ZZ:ZZ:ZZ:ZZ:ZZ:ZZ")


def test_mac_binary_digits():
    """Test that the MAC address is correctly converted into its binary representation as digits."""
    mac_addr = MACAddr("b0-fc-0d-60-51-f8")
    expected_binary_digits = [
        1, 0, 1, 1, 0, 0, 0, 0,  # B0
        1, 1, 1, 1, 1, 1, 0, 0,  # FC
        0, 0, 0, 0, 1, 1, 0, 1,  # 0D
        0, 1, 1, 0, 0, 0, 0, 0,  # 60
        0, 1, 0, 1, 0, 0, 0, 1,  # 51
        1, 1, 1, 1, 1, 0, 0, 0   # F8
    ]
    assert mac_addr.binary_digits == expected_binary_digits, "Binary digits conversion failed."


def test_mac_binary_string():
    """Test that the MAC address is correctly converted into its binary string representation."""
    mac_addr = MACAddr("60-57-c8-98-43-13")
    expected_binary_string = "011000000101011111001000100110000100001100010011"
    assert mac_addr.binary_string == expected_binary_string, "Binary string conversion failed."


def test_mac_search_oui():
    """Test that the OUI database correctly identifies the organization associated with a MAC address."""
    mac_addr = MACAddr("b0-fc-0d-60-51-f8")
    assert mac_addr.oui is not None, "OUI search failed, OUI should not be None."
    assert "B0FC0D" in mac_addr.oui.record['oui_id'].replace(':', ''), "OUI record does not match the MAC address."


def test_mac_type_property():
    """Test that the mac_type property returns the correct MACType."""
    mac_addr = MACAddr("b0-fc-0d-60-51-f8")
    assert mac_addr.mac_type == MACType.UNICAST, "Failed to return correct mac_type property."

