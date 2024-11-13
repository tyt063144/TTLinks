import pytest

from ttlinks.ipservice.ip_type_classifiers import IPType
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.dscp_utils import DSCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_builder import IPv4HeaderBuilderDirector, IPv4HeaderBuilder, IPv4Header


def test_ipv4_builder_default():
    ipv4_director = IPv4HeaderBuilderDirector(IPv4HeaderBuilder(IPv4Header()))
    ipv4_unit = ipv4_director.construct()
    assert ipv4_unit.version == IPType.IPv4
    assert ipv4_unit.ihl == 5
    assert ipv4_unit.dscp == DSCP(0)
    assert ipv4_unit.ecn == 0
    assert ipv4_unit.header_length == 20
    assert ipv4_unit.total_length == 40
    assert ipv4_unit.identification == 0
    assert ipv4_unit.flags == IPv4Flags(0)
    assert ipv4_unit.fragment_offset == 0
    assert ipv4_unit.ttl == 64
    assert ipv4_unit.protocol == IPPayloadProtocolTypes.TCP
