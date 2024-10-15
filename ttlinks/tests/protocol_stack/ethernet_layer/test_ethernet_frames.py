import pytest

from ttlinks.macservice.mac_address import MACAddr
from ttlinks.protocol_stack.ethernet_layer.ethernet_parsers import EthernetFrameParser
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import IEEE8023 ,EthernetII, EthernetUnitFactory
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import LSAP, EthernetTypes, EthernetPayloadProtocolTypes


# Assuming EthernetFrameParser, Ethernet8023, and related classes are already defined or imported

def test_ieee8023_frame_parser1():
    # Example IEEE 802.3 frame
    ieee8023_frame = bytes.fromhex('0180c2000000042ae2da41050027424203000002023c7000089bb93afe82000000048028042ae2da4100800501001400020002000000000000000000')

    # Expected parsed result
    expected_result = {
        'dst': b'\x01\x80\xc2\x00\x00\x00',
        'src': b'\x04*\xe2\xdaA\x05',
        'length': b"\x00'",
        'llc': b'BB\x03',
        'snap': b'',
        'payload': b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    }

    frame_parser = EthernetFrameParser()
    ieee8023_frame_result = frame_parser.parse(ieee8023_frame)
    # Assert that the parsed result matches the expected result
    assert ieee8023_frame_result == expected_result
    # Now build the Ethernet8023 frame from the parsed result
    ethernet8023 = IEEE8023(**ieee8023_frame_result)
    # Validate frame attributes
    assert str(ethernet8023.dst) == str(MACAddr(b'\x01\x80\xc2\x00\x00\x00'))
    assert str(ethernet8023.src) == str(MACAddr(b'\x04*\xe2\xdaA\x05'))
    assert ethernet8023.length == 39
    assert ethernet8023.payload == b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ethernet8023.padding == b'\x00\x00\x00\x00\x00\x00\x00'
    assert ethernet8023.dsap == LSAP.BRIDGE_SPANNING_TREE
    assert ethernet8023.ssap == LSAP.BRIDGE_SPANNING_TREE
    assert ethernet8023.pid is None
    assert ethernet8023.frame_type == EthernetTypes.IEEE802_3


def test_ieee8023_frame_parser2():
    ieee8023_frame = bytes.fromhex('01000ccccccc042ae2da410501e7aaaa0300000c200002b469cd000100204333353630582d43726f73736e65742e63726f73736e65742e636f6d000500fc436973636f20494f5320536f6674776172652c204333353630435820536f6674776172652028433335363043582d554e4956455253414c4b392d4d292c2056657273696f6e2031352e3228332945332c2052454c4541534520534f4654574152452028666333290a546563686e6963616c20537570706f72743a20687474703a2f2f7777772e636973636f2e636f6d2f74656368737570706f72740a436f707972696768742028632920313938362d3230313620627920436973636f2053797374656d732c20496e632e0a436f6d70696c6564205765642031332d4a616e2d31362032333a30382062792070726f645f72656c5f7465616d0006001a636973636f2057532d433335363043582d3850542d5300020011000000010101cc0004c0a8011e000300164769676162697445746865726e6574302f3500040008000000290008002400000c011200000000ffffffff010221ff000000000000042ae2da4100ff000000090004000a00060028000b0005010012000500001300050000160011000000010101cc0004c0a8011e001a00100000000100000000ffffffff10040013303432612e653264612e34313030001003000531')

    frame_parser = EthernetFrameParser()
    ieee8023_frame_result = frame_parser.parse(ieee8023_frame)

    ethernet8023 = IEEE8023(**ieee8023_frame_result)

    assert str(ethernet8023.dst) == str(MACAddr(b'\x01\x00\x0C\xCC\xCC\xCC'))
    assert str(ethernet8023.src) == str(MACAddr(b'\x04\x2A\xE2\xDA\x41\x05'))
    assert ethernet8023.length == 487
    assert ethernet8023.oui.record['organization'] == 'Cisco Systems, Inc'  # Example OUI record for '00:00:0C'
    assert ethernet8023.dsap == LSAP.SNAP_EXTENSION
    assert ethernet8023.ssap == LSAP.SNAP_EXTENSION
    assert ethernet8023.pid.value == 0x2000
    assert ethernet8023.frame_type == EthernetTypes.IEEE802_3

def test_ethernet2_frame_parser():
    ethernet2_frame = bytes.fromhex('08bfb834c6a40011329426af08004500005a76f040007f060103c0a80114c0a80146dc000d3d0755b88ee04cc1f35018040345510000170303002d000000000000daa631749a3c2157acf2925f09de6cc22e0df260149becce9e269aff6ee27f688142b596148c24')
    frame_parser = EthernetFrameParser()
    ethernet2_frame_result = frame_parser.parse(ethernet2_frame)
    ethernet2 = EthernetII(**ethernet2_frame_result)
    assert str(ethernet2.dst) == str(MACAddr(b'\x08\xbf\xb8\x34\xc6\xa4'))
    assert str(ethernet2.src) == str(MACAddr(b'\x00\x11\x32\x94\x26\xaf'))
    assert ethernet2.frame_type == EthernetTypes.Ethernet_II
    assert ethernet2.type == EthernetPayloadProtocolTypes.IPv4

def test_factory_for_ieee8023_1():
    # Example IEEE 802.3 frame
    ieee8023_frame = bytes.fromhex('0180c2000000042ae2da41050027424203000002023c7000089bb93afe82000000048028042ae2da4100800501001400020002000000000000000000')

    # Expected parsed result
    expected_result = {
        'dst': b'\x01\x80\xc2\x00\x00\x00',
        'src': b'\x04*\xe2\xdaA\x05',
        'length': b"\x00'",
        'llc': b'BB\x03',
        'snap': b'',
        'payload': b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    }

    ethernet_frame = EthernetUnitFactory.create_unit(ieee8023_frame)
    # Assert that the parsed result matches the expected result
    assert ethernet_frame.attributes == expected_result
    # Validate frame attributes
    assert str(ethernet_frame.dst) == str(MACAddr(b'\x01\x80\xc2\x00\x00\x00'))
    assert str(ethernet_frame.src) == str(MACAddr(b'\x04*\xe2\xdaA\x05'))
    assert ethernet_frame.length == 39
    assert ethernet_frame.payload == b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ethernet_frame.padding == b'\x00\x00\x00\x00\x00\x00\x00'
    assert ethernet_frame.dsap == LSAP.BRIDGE_SPANNING_TREE
    assert ethernet_frame.ssap == LSAP.BRIDGE_SPANNING_TREE
    assert ethernet_frame.pid is None
    assert ethernet_frame.frame_type == EthernetTypes.IEEE802_3


def test_factory_for_ieee8023_2():
    ieee8023_frame = bytes.fromhex('01000ccccccc042ae2da410501e7aaaa0300000c200002b469cd000100204333353630582d43726f73736e65742e63726f73736e65742e636f6d000500fc436973636f20494f5320536f6674776172652c204333353630435820536f6674776172652028433335363043582d554e4956455253414c4b392d4d292c2056657273696f6e2031352e3228332945332c2052454c4541534520534f4654574152452028666333290a546563686e6963616c20537570706f72743a20687474703a2f2f7777772e636973636f2e636f6d2f74656368737570706f72740a436f707972696768742028632920313938362d3230313620627920436973636f2053797374656d732c20496e632e0a436f6d70696c6564205765642031332d4a616e2d31362032333a30382062792070726f645f72656c5f7465616d0006001a636973636f2057532d433335363043582d3850542d5300020011000000010101cc0004c0a8011e000300164769676162697445746865726e6574302f3500040008000000290008002400000c011200000000ffffffff010221ff000000000000042ae2da4100ff000000090004000a00060028000b0005010012000500001300050000160011000000010101cc0004c0a8011e001a00100000000100000000ffffffff10040013303432612e653264612e34313030001003000531')

    ethernet_frame = EthernetUnitFactory.create_unit(ieee8023_frame)

    assert str(ethernet_frame.dst) == str(MACAddr(b'\x01\x00\x0C\xCC\xCC\xCC'))
    assert str(ethernet_frame.src) == str(MACAddr(b'\x04\x2A\xE2\xDA\x41\x05'))
    assert ethernet_frame.length == 487
    assert ethernet_frame.oui.record['organization'] == 'Cisco Systems, Inc'  # Example OUI record for '00:00:0C'
    assert ethernet_frame.dsap == LSAP.SNAP_EXTENSION
    assert ethernet_frame.ssap == LSAP.SNAP_EXTENSION
    assert ethernet_frame.pid.value == 0x2000
    assert ethernet_frame.frame_type == EthernetTypes.IEEE802_3

def test_factory_for_ethernet2():
    ethernet2_frame = bytes.fromhex('08bfb834c6a40011329426af08004500005a76f040007f060103c0a80114c0a80146dc000d3d0755b88ee04cc1f35018040345510000170303002d000000000000daa631749a3c2157acf2925f09de6cc22e0df260149becce9e269aff6ee27f688142b596148c24')
    ethernet_frame = EthernetUnitFactory.create_unit(ethernet2_frame)
    assert str(ethernet_frame.dst) == str(MACAddr(b'\x08\xbf\xb8\x34\xc6\xa4'))
    assert str(ethernet_frame.src) == str(MACAddr(b'\x00\x11\x32\x94\x26\xaf'))
    assert ethernet_frame.frame_type == EthernetTypes.Ethernet_II
    assert ethernet_frame.type == EthernetPayloadProtocolTypes.IPv4