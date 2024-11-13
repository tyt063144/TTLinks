import pytest

from ttlinks.protocol_stack.ip_packets.tcp import IPv4TCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


def test_ipv4_tcp():
    tcp = IPv4TCP(
        ipv4_flags=IPv4Flags.DONT_FRAGMENT,
        ttl=32,
        destination_address='192.168.1.30',
        source_port=54156,
        destination_port=22,
        sequence_number=1370412840,
        tcp_flags=[TCPFlags.SYN],
    )
    assert tcp.ip_unit.ttl == 32
    assert tcp.ip_unit.flags == IPv4Flags.DONT_FRAGMENT
    assert tcp.tcp_unit.source_port == 54156
    assert tcp.tcp_unit.destination_port == 22
    assert tcp.tcp_unit.sequence_number == 1370412840
    assert tcp.tcp_unit.flags == [TCPFlags.SYN]