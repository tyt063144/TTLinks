import pytest

from ttlinks.protocol_stack.transport_layer.TCP.tcp_builder import TCPBuilderDirector, TCPHeaderBuilder, TCPHeader
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionBuilderDirector, TCPOption2HeaderBuilder, TCPOption3HeaderBuilder, \
    TCPOption4HeaderBuilder
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


def test_tcp_builder():
    tcp_option_director = TCPOptionBuilderDirector(TCPOption2HeaderBuilder)
    tcp_option2 = tcp_option_director.build(kind=2)
    tcp_option_director.set_builder(TCPOption3HeaderBuilder)
    tcp_option3 = tcp_option_director.build(kind=3, length=3, value=8)
    tcp_option_director.set_builder(TCPOption4HeaderBuilder)
    tcp_option4 = tcp_option_director.build(kind=4, length=2)


    director = TCPBuilderDirector(TCPHeaderBuilder(TCPHeader()))
    tcp_unit = director.construct(
        source_ip='192.168.1.70',
        destination_ip='18.220.182.65',
        source_port=54156,
        destination_port=443,
        sequence_number=1370412840,
        acknowledgment_number=0,
        reserved=0,
        flags=[TCPFlags.SYN],
        window_size=64240,
        option_units=[tcp_option2, tcp_option3, tcp_option4],
    )
    assert tcp_unit.as_bytes == b'\xd3\x8c\x01\xbbQ\xae\xd7(\x00\x00\x00\x00\x80\x02\xfa\xf0\xea\xf4\x00\x00\x02\x04\x05\xb4\x01\x03\x03\x08\x01\x01\x04\x02'
    assert tcp_unit.attributes == {'source_port': b'\xd3\x8c', 'destination_port': b'\x01\xbb', 'sequence_number': b'Q\xae\xd7(', 'acknowledgment_number': b'\x00\x00\x00\x00', 'offset_reserved_flags': b'\x80\x02', 'window_size': b'\xfa\xf0', 'checksum': b'\xea\xf4', 'urgent_pointer': b'\x00\x00', 'options': b'\x02\x04\x05\xb4\x01\x03\x03\x08\x01\x01\x04\x02'}
