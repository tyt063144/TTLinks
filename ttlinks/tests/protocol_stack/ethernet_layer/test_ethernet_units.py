import pytest

from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory


def test_parse_ethernet8023_frame1():
    # Example Ethernet frame in hexadecimal
    ethernet_frame = bytes.fromhex('0180c2000000042ae2da41050027424203000002023c7000089bb93afe82000000048028042ae2da4100800501001400020002000000000000000000')
    ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
    frame_type = ethernet_unit.frame_type.name
    destination_mac = str(ethernet_unit.dst)
    source_mac = str(ethernet_unit.src)
    dsap = ethernet_unit.dsap.name
    ssap = ethernet_unit.ssap.name
    control = ethernet_unit.control
    assert frame_type == 'IEEE802_3'
    assert destination_mac == '01:80:C2:00:00:00'
    assert source_mac == '04:2A:E2:DA:41:05'
    assert dsap == 'BRIDGE_SPANNING_TREE'
    assert ssap == 'BRIDGE_SPANNING_TREE'
    assert control == b'\x03'


def test_parse_ethernet8023_frame2():
    # Example Ethernet frame in hexadecimal
    ethernet_frame = bytes.fromhex('01000ccccccc042ae2da410501e7aaaa0300000c200002b469cd000100204333353630582d43726f73736e65742e63726f73736e65742e636f6d000500fc436973636f20494f5320536f6674776172652c204333353630435820536f6674776172652028433335363043582d554e4956455253414c4b392d4d292c2056657273696f6e2031352e3228332945332c2052454c4541534520534f4654574152452028666333290a546563686e6963616c20537570706f72743a20687474703a2f2f7777772e636973636f2e636f6d2f74656368737570706f72740a436f707972696768742028632920313938362d3230313620627920436973636f2053797374656d732c20496e632e0a436f6d70696c6564205765642031332d4a616e2d31362032333a30382062792070726f645f72656c5f7465616d0006001a636973636f2057532d433335363043582d3850542d5300020011000000010101cc0004c0a8011e000300164769676162697445746865726e6574302f3500040008000000290008002400000c011200000000ffffffff010221ff000000000000042ae2da4100ff000000090004000a00060028000b0005010012000500001300050000160011000000010101cc0004c0a8011e001a00100000000100000000ffffffff10040013303432612e653264612e34313030001003000531')
    ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
    frame_type = ethernet_unit.frame_type.name
    destination_mac = str(ethernet_unit.dst)
    source_mac = str(ethernet_unit.src)
    dsap = ethernet_unit.dsap.name
    ssap = ethernet_unit.ssap.name
    control = ethernet_unit.control
    next_layer = ethernet_unit.pid.name
    oui_organization = ethernet_unit.oui.record['organization']
    assert frame_type == 'IEEE802_3'
    assert destination_mac == '01:00:0C:CC:CC:CC'
    assert source_mac == '04:2A:E2:DA:41:05'
    assert dsap == 'SNAP_EXTENSION'
    assert ssap == 'SNAP_EXTENSION'
    assert control == b'\x03'
    assert next_layer == 'CDP'
    assert oui_organization == 'Cisco Systems, Inc'

def test_parse_arp_frame():
    # Example Ethernet frame in hexadecimal
    ethernet_frame = bytes.fromhex(
        'ffffffffffff40234323be730806000108000604000140234323be73c0a801d0000000000000c0a80101000000000000000000000000000000000000')
    ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
    frame_type = ethernet_unit.frame_type.name
    destination_mac = str(ethernet_unit.dst)
    source_mac = str(ethernet_unit.src)
    next_layer = ethernet_unit.type.name
    assert frame_type == 'Ethernet_II'
    assert destination_mac == 'FF:FF:FF:FF:FF:FF'
    assert source_mac == '40:23:43:23:BE:73'
    assert next_layer == 'ARP'

def test_parse_echo_reply_packet():
    ethernet_frame = bytes.fromhex(
        '08bfb834c6a4089bb93afe8208004540003c000000007601728308080808c0a8014600005473000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869')
    ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
    frame_type = ethernet_unit.frame_type.name
    destination_mac = str(ethernet_unit.dst)
    source_mac = str(ethernet_unit.src)
    next_layer = ethernet_unit.type.name
    ethernet_payload = ethernet_unit.payload
    ip_version = ethernet_payload.version.name
    ip_header_length = ethernet_payload.header_length
    ip_ttl = ethernet_payload.ttl
    ip_dscp = ethernet_payload.dscp.value
    ip_ecn = ethernet_payload.ecn
    ip_total_length = ethernet_payload.total_length
    ip_identification = ethernet_payload.identification
    ip_flags = ethernet_payload.flags.value
    ip_fragment_offset = ethernet_payload.fragment_offset
    ip_protocol = ethernet_payload.protocol.name
    ip_checksum = ethernet_payload.header_checksum
    ip_src = str(ethernet_payload.source_address)
    ip_dst = str(ethernet_payload.destination_address)
    assert frame_type == 'Ethernet_II'
    assert destination_mac == '08:BF:B8:34:C6:A4'
    assert source_mac == '08:9B:B9:3A:FE:82'
    assert next_layer == 'IPv4'
    assert ip_version == 'IPv4'
    assert ip_header_length == 20
    assert ip_ttl == 118
    assert ip_dscp == 16
    assert ip_ecn == 0
    assert ip_total_length == 60
    assert ip_identification == 0
    assert ip_flags == 0
    assert ip_fragment_offset == 0
    assert ip_protocol == 'ICMP'
    assert ip_checksum == '0x7283'
    assert ip_src == '8.8.8.8'
    assert ip_dst == '192.168.1.70'