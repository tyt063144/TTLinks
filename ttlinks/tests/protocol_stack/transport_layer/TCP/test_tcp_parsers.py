import pytest

from ttlinks.protocol_stack.transport_layer.TCP.tcp_parsers import TCPParser
from ttlinks.protocol_stack.transport_layer.TCP.tcp_units import TCPUnit


class TCPPayload:
    @staticmethod
    def tcp_option_2_4_8_1_3():
        return bytes.fromhex('b2fe005076ee585300000000a002faf03c690000020405b40402080aa254b24a0000000001030307')


def test_tcp_parser_1():
    tcp_parser = TCPParser()
    parsed_tcp = tcp_parser.parse(TCPPayload.tcp_option_2_4_8_1_3())
    tcp_unit = TCPUnit(**parsed_tcp)
    assert tcp_unit.as_bytes == b'\xb2\xfe\x00Pv\xeeXS\x00\x00\x00\x00\xa0\x02\xfa\xf0<i\x00\x00\x02\x04\x05\xb4\x04\x02\x08\n\xa2T\xb2J\x00\x00\x00\x00\x01\x03\x03\x07'
    assert tcp_unit.options[0].as_bytes == b'\x02\x04\x05\xb4'
    assert tcp_unit.options[1].as_bytes == b'\x04\x02'
    assert tcp_unit.options[2].as_bytes == b'\x08\n\xa2T\xb2J\x00\x00\x00\x00'
    assert tcp_unit.options[3].as_bytes == b'\x01'
    assert tcp_unit.options[4].as_bytes == b'\x03\x03\x07'