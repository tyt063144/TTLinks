import pytest

from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPCustomOptionHeaderBuilder, TCPOptionHeader, TCPOption4HeaderBuilder, \
    TCPOption3HeaderBuilder, TCPOption2HeaderBuilder, TCPOption5HeaderBuilder, TCPOptionSACKValue


def test_builder_custom_tcp_timestamp_option():
    option_header = TCPOptionHeader()
    tcp_op_builder = TCPCustomOptionHeaderBuilder(option_header)
    tcp_op_builder.set_kind(8)
    ## When a length is variable, the length will be set under the set_value method. For example: option 5 (SACK) and Custom Options
    # tcp_op_builder.set_length()
    value = 1328420247
    echo_reply = 3557171634
    tcp_op_builder.set_value(value.to_bytes(4, byteorder='big')+echo_reply.to_bytes(4, byteorder='big'))

    result = tcp_op_builder.build()
    unit = result.unit
    assert unit.get_field('kind') == 'Timestamp'
    assert unit.get_field('length') == 10
    assert unit.get_field('value') == {'timestamp': 1328420247, 'echo_reply': 3557171634}
    assert unit.as_bytes == b'\x08\nO.\x15\x97\xd4\x06!\xb2'
    assert unit.attributes == {'kind': b'\x08', 'length': b'\n', 'value': b'O.\x15\x97\xd4\x06!\xb2'}

def test_builder_tcp_SACK_permitted_option():
    option_header = TCPOptionHeader()
    tcp_op_builder = TCPOption4HeaderBuilder(option_header)
    tcp_op_builder.set_kind()
    tcp_op_builder.set_length()
    tcp_op_builder.set_value()

    result = tcp_op_builder.build()
    unit = result.unit
    assert unit.get_field('kind') == 'SACK Permitted'
    assert unit.get_field('length') == 2
    assert unit.get_field('value') == b''
    assert unit.as_bytes == b'\x04\x02'
    assert unit.attributes == {'kind': b'\x04', 'length': b'\x02', 'value': b''}

def test_builder_tcp_mss_option():
    option_header = TCPOptionHeader()
    tcp_op_builder = TCPOption2HeaderBuilder(option_header)
    tcp_op_builder.set_kind()
    tcp_op_builder.set_length()
    tcp_op_builder.set_value(1360)
    #
    result = tcp_op_builder.build()
    unit = result.unit
    assert unit.get_field('kind') == 'Maximum Segment Size'
    assert unit.get_field('length') == 4
    assert unit.get_field('value') == 1360
    assert unit.as_bytes == b'\x02\x04\x05P'
    assert unit.attributes == {'kind': b'\x02', 'length': b'\x04', 'value': b'\x05P'}

def test_builder_tcp_window_scale_option():
    option_header = TCPOptionHeader()
    tcp_op_builder = TCPOption3HeaderBuilder(option_header)
    tcp_op_builder.set_kind()
    tcp_op_builder.set_length()
    tcp_op_builder.set_value(8)
    #
    result = tcp_op_builder.build()
    unit = result.unit
    assert unit.get_field('kind') == 'Window Scale'
    assert unit.get_field('length') == 3
    assert unit.get_field('value') == 8
    assert unit.as_bytes == b'\x03\x03\x08'
    assert unit.attributes == {'kind': b'\x03', 'length': b'\x03', 'value': b'\x08'}

def test_builder_tcp_SACK_option():
    option_header = TCPOptionHeader()
    tcp_op_builder = TCPOption5HeaderBuilder(option_header)
    tcp_op_builder.set_kind()
    tcp_op_builder.set_value([TCPOptionSACKValue(100, 200), TCPOptionSACKValue(300, 400)])
    #
    result = tcp_op_builder.build()
    unit = result.unit
    assert unit.get_field('kind') == 'SACK'
    assert unit.get_field('length') == 18
    assert unit.as_bytes == b'\x05\x12\x00\x00\x00d\x00\x00\x00\xc8\x00\x00\x01,\x00\x00\x01\x90'
    assert unit.attributes == {'kind': b'\x05', 'length': b'\x12', 'value': b'\x00\x00\x00d\x00\x00\x00\xc8\x00\x00\x01,\x00\x00\x01\x90'}