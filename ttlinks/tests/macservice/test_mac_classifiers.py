from ttlinks.macservice import MACType
from ttlinks.macservice.mac_classifiers import MACAddrClassifier, UnicastMACAddrClassifierHandler, MulticastMACAddrClassifierHandler
from ttlinks.macservice.mac_converters import MACConverter


# Test case for classifying a broadcast MAC address
def test_classify_broadcast_mac():
    broadcast_mac = "FF:FF:FF:FF:FF:FF"
    mac_octets = MACConverter.convert_mac(broadcast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.BROADCAST, "Failed to classify Broadcast MAC"


# Test case for classifying a unicast MAC address
def test_classify_unicast_mac():
    unicast_mac = "00:00:00:00:00:00"
    mac_octets = MACConverter.convert_mac(unicast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.UNICAST, "Failed to classify Unicast MAC"


# Test case for classifying a multicast MAC address
def test_classify_multicast_mac():
    multicast_mac = "01:00:5E:00:00:00"
    mac_octets = MACConverter.convert_mac(multicast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.MULTICAST, "Failed to classify Multicast MAC"


# Test case for invalid MAC address conversion
def test_invalid_mac_conversion():
    invalid_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
    result = MACConverter.convert_mac(invalid_mac)
    assert result is None

# Test that chain of responsibility handles classification correctly
def test_chain_of_responsibility_order():
    # Test broadcast classification
    broadcast_mac = "FF:FF:FF:FF:FF:FF"
    mac_octets = MACConverter.convert_mac(broadcast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.BROADCAST, "Chain failed to classify Broadcast MAC"

    # Test unicast classification
    unicast_mac = "00:00:00:00:00:00"
    mac_octets = MACConverter.convert_mac(unicast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.UNICAST, "Chain failed to classify Unicast MAC"

    # Test multicast classification
    multicast_mac = "01:00:5E:00:00:00"
    mac_octets = MACConverter.convert_mac(multicast_mac)
    mac_type = MACAddrClassifier.classify_mac(mac_octets)
    assert mac_type == MACType.MULTICAST, "Chain failed to classify Multicast MAC"


# Test case for custom chain of responsibility with only Unicast and Multicast classifiers
def test_custom_classifier_chain():

    unicast_handler = UnicastMACAddrClassifierHandler()
    multicast_handler = MulticastMACAddrClassifierHandler()

    # Chain only includes Unicast and Multicast handlers
    unicast_handler.set_next(multicast_handler)

    # Test unicast classification
    unicast_mac = "00:00:00:00:00:00"
    mac_octets = MACConverter.convert_mac(unicast_mac)
    mac_type = unicast_handler.handle(mac_octets)
    assert mac_type == MACType.UNICAST, "Custom chain failed to classify Unicast MAC"

    # Test multicast classification
    multicast_mac = "01:00:5E:00:00:00"
    mac_octets = MACConverter.convert_mac(multicast_mac)
    mac_type = unicast_handler.handle(mac_octets)
    assert mac_type == MACType.MULTICAST, "Custom chain failed to classify Multicast MAC"
