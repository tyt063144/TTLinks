import pytest
from ttlinks.macservice import MACType
from ttlinks.macservice.mac_classifiers import (
    BroadcastMACAddrClassifierHandler,
    UnicastMACAddrClassifierHandler,
    MulticastMACAddrClassifierHandler,
    MACAddrClassifier
)

@pytest.mark.parametrize("mac_bytes, expected", [
    (b'\xff\xff\xff\xff\xff\xff', MACType.BROADCAST),  # 全 0xFF 为广播地址
    (b'\x01\x00\x5e\x00\x00\xfb', MACType.MULTICAST),  # IPv4 组播地址
    (b'\x33\x33\x00\x00\x00\x01', MACType.MULTICAST),  # IPv6 组播地址
    (b'\x00\x11\x22\x33\x44\x55', MACType.UNICAST),  # 标准单播地址
    (b'\x02\xaa\xbb\xcc\xdd\xee', MACType.UNICAST),  # LSB 为 0，单播
])
def test_mac_classifiers(mac_bytes, expected):
    assert MACAddrClassifier.classify_mac(mac_bytes) == expected


@pytest.mark.parametrize("mac_bytes", [
    b'\xff\xff\xff\xff\xff\xff',  # 纯广播
])
def test_broadcast_classifier(mac_bytes):
    handler = BroadcastMACAddrClassifierHandler()
    assert handler.handle(mac_bytes) == MACType.BROADCAST


@pytest.mark.parametrize("mac_bytes", [
    b'\x00\x11\x22\x33\x44\x55',  # 典型单播
    b'\x02\xaa\xbb\xcc\xdd\xee',  # LSB 为 0
    b'\x04\xff\xaa\xbb\xcc\xdd',  # LSB 为 0
])
def test_unicast_classifier(mac_bytes):
    handler = UnicastMACAddrClassifierHandler()
    assert handler.handle(mac_bytes) == MACType.UNICAST


@pytest.mark.parametrize("mac_bytes", [
    b'\x01\x00\x5e\x00\x00\xfb',  # 组播地址（IPv4）
    b'\x33\x33\x00\x00\x00\x01',  # 组播地址（IPv6）
    b'\x09\x11\x22\x33\x44\x55',  # LSB 为 1
])
def test_multicast_classifier(mac_bytes):
    handler = MulticastMACAddrClassifierHandler()
    assert handler.handle(mac_bytes) == MACType.MULTICAST


@pytest.mark.parametrize("invalid_mac", [
    b'\xff\xff\xff\xff\xff',
    b'\x01\x02\x03\x04\x05\x06\x07',
    b'\x00\x11\x22\x33\x44',
])
def test_invalid_mac_addresses(invalid_mac):
    assert MACAddrClassifier.classify_mac(invalid_mac) is None


def test_mac_classifier_chain():
    classifiers = [
        BroadcastMACAddrClassifierHandler(),
        UnicastMACAddrClassifierHandler(),
        MulticastMACAddrClassifierHandler(),
    ]
    classifiers[0].set_next(classifiers[1])
    classifiers[1].set_next(classifiers[2])

    assert classifiers[0].handle(b'\xff\xff\xff\xff\xff\xff') == MACType.BROADCAST
    assert classifiers[0].handle(b'\x00\x11\x22\x33\x44\x55') == MACType.UNICAST
    assert classifiers[0].handle(b'\x01\x00\x5e\x00\x00\xfb') == MACType.MULTICAST
