import pytest

from ttlinks.protocol_stack.ethernet_layer.ethernet_parsers import EthernetFrameParser


def test_parse_ethernet8023_frame():
    # Example Ethernet frame in hexadecimal
    ethernet_frame = bytes.fromhex('0180c2000000042ae2da41050027424203000002023c7000089bb93afe82000000048028042ae2da4100800501001400020002000000000000000000')

    # Expected parsed values
    expected_parsed_frame = {
        'dst': b'\x01\x80\xc2\x00\x00\x00',
        'src': b'\x04*\xe2\xdaA\x05',
        'length': b"\x00'",
        'llc': b'BB\x03',
        'snap': b'',
        'payload': b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    }
    # Initialize the EthernetFrameParser
    parser = EthernetFrameParser()
    # Parse the Ethernet frame
    parsed_frame = parser.parse(ethernet_frame)
    # Assert that the parsed frame matches the expected values
    assert parsed_frame == expected_parsed_frame

def test_parse_ethernet2_frame():
    ethernet_frame = bytes.fromhex('08bfb834c6a4089bb93afe8208060001080006040001089bb93afe82c0a801fe000000000000c0a80146000000000000000000000000000000000000')
    expected_parsed_frame = {
        'dst': b'\x08\xbf\xb84\xc6\xa4',
        'src': b'\x08\x9b\xb9:\xfe\x82',
        'type': b'\x08\x06',
        'payload': b'\x00\x01\x08\x00\x06\x04\x00\x01\x08\x9b\xb9:\xfe\x82\xc0\xa8\x01\xfe\x00\x00\x00\x00\x00\x00\xc0\xa8\x01F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    }
    # Initialize the EthernetFrameParser
    parser = EthernetFrameParser()
    # Parse the Ethernet frame
    parsed_frame = parser.parse(ethernet_frame)
    # Assert that the parsed frame matches the expected values
    assert parsed_frame == expected_parsed_frame