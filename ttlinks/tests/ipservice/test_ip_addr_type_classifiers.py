import pytest
from ttlinks.ipservice.ip_addr_type_classifiers import (
    IPv4AddrTypeLimitedBroadcastHandler,
    IPv4AddrTypeCurrentNetworkHandler,
    IPv4AddrClassifierPrivateHandler,
    IPv4AddrClassifierPublicHandler, IPv4AddrClassifierMulticastHandler, IPv4AddrClassifierLinkLocalHandler, IPv4AddrClassifierLoopbackHandler,
    IPv4AddrClassifierDSLiteHandler, IPv4AddrClassifierDocumentationHandler, IPv4AddrClassifierCarrierNATHandler,
    IPv4AddrClassifierBenchmarkTestingHandler, IPv4AddrClassifierIP6To4RelayHandler, IPv4AddrClassifierReservedHandler,
    IPv6AddrClassifierLoopbackHandler, IPv6AddrClassifierIPv4MappedHandler, IPv6AddrClassifierIPv4TranslatedHandler,
    IPv6AddrClassifierIPv4To6TranslationHandler, IPv6AddrClassifierDiscardPrefixHandler, IPv6AddrClassifierTeredoTunnelingHandler,
    IPv6AddrClassifierDocumentationHandler, IPv6AddrClassifierORCHIDV2Handler, IPv6AddrClassifier6To4SchemeHandler, IPv6AddrClassifierSRV6Handler,
    IPv6AddrClassifierLinkLocalHandler, IPv6AddrClassifierMulticastHandler, IPv6AddrClassifierUniqueLocalHandler,
    IPv6AddrClassifierGlobalUnicastHandler
)
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv6AddrType


def test_ipv4_limited_broadcast_handler():
    handler = IPv4AddrTypeLimitedBroadcastHandler()
    limited_broadcast_ip = IPv4Addr("255.255.255.255")
    result = handler.handle(limited_broadcast_ip)
    assert result == IPv4AddrType.LIMITED_BROADCAST, "Should classify as LIMITED_BROADCAST"


def test_ipv4_limited_broadcast_handler_boundary_lower():
    handler = IPv4AddrTypeLimitedBroadcastHandler()
    near_broadcast_ip = IPv4Addr("255.255.255.254")
    result = handler.handle(near_broadcast_ip)
    assert result != IPv4AddrType.LIMITED_BROADCAST, "Should not classify as LIMITED_BROADCAST"


def test_ipv4_limited_broadcast_handler_invalid_ip():
    handler = IPv4AddrTypeLimitedBroadcastHandler()
    normal_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(normal_ip)
    assert result != IPv4AddrType.LIMITED_BROADCAST, "Should not classify as LIMITED_BROADCAST"


def test_ipv4_current_network_handler():
    handler = IPv4AddrTypeCurrentNetworkHandler()
    current_network_ip = IPv4Addr("0.0.0.0")
    result = handler.handle(current_network_ip)
    assert result == IPv4AddrType.CURRENT_NETWORK, "Should classify as CURRENT_NETWORK"


def test_ipv4_current_network_handler_boundary_upper():
    handler = IPv4AddrTypeCurrentNetworkHandler()
    near_current_network_ip = IPv4Addr("0.255.255.255")
    result = handler.handle(near_current_network_ip)
    assert result == IPv4AddrType.CURRENT_NETWORK, "Should classify as CURRENT_NETWORK"


def test_ipv4_current_network_handler_boundary_outside():
    handler = IPv4AddrTypeCurrentNetworkHandler()
    outside_current_network_ip = IPv4Addr("1.0.0.0")
    result = handler.handle(outside_current_network_ip)
    assert result != IPv4AddrType.CURRENT_NETWORK, "Should not classify as CURRENT_NETWORK"


def test_ipv4_current_network_handler_invalid_ip():
    handler = IPv4AddrTypeCurrentNetworkHandler()
    normal_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(normal_ip)
    assert result != IPv4AddrType.CURRENT_NETWORK, "Should not classify as CURRENT_NETWORK"


def test_ipv4_private_handler():
    handler = IPv4AddrClassifierPrivateHandler()
    private_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(private_ip)
    assert result == IPv4AddrType.PRIVATE, "Should classify as PRIVATE"


def test_ipv4_private_handler_boundary_lower():
    handler = IPv4AddrClassifierPrivateHandler()
    private_ip = IPv4Addr("10.0.0.0")
    result = handler.handle(private_ip)
    assert result == IPv4AddrType.PRIVATE, "Should classify as PRIVATE"


def test_ipv4_private_handler_boundary_upper():
    handler = IPv4AddrClassifierPrivateHandler()
    private_ip = IPv4Addr("192.168.255.255")
    result = handler.handle(private_ip)
    assert result == IPv4AddrType.PRIVATE, "Should classify as PRIVATE"


def test_ipv4_private_handler_invalid_ip():
    handler = IPv4AddrClassifierPrivateHandler()
    public_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(public_ip)
    assert result != IPv4AddrType.PRIVATE, "Should not classify as PRIVATE"


def test_ipv4_public_handler():
    handler = IPv4AddrClassifierPublicHandler()
    public_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(public_ip)
    assert result == IPv4AddrType.PUBLIC, "Should classify as PUBLIC"


def test_ipv4_public_handler_boundary_lower():
    handler = IPv4AddrClassifierPublicHandler()
    public_ip = IPv4Addr("1.1.1.1")
    result = handler.handle(public_ip)
    assert result == IPv4AddrType.PUBLIC, "Should classify as PUBLIC"


def test_ipv4_public_handler_boundary_upper():
    handler = IPv4AddrClassifierPublicHandler()
    public_ip = IPv4Addr("223.255.255.255")
    result = handler.handle(public_ip)
    assert result == IPv4AddrType.PUBLIC, "Should classify as PUBLIC"


def test_ipv4_public_handler_invalid_ip_private():
    handler = IPv4AddrClassifierPublicHandler()
    private_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(private_ip)
    assert result != IPv4AddrType.PUBLIC, "Should not classify as PUBLIC"


def test_ipv4_public_handler_invalid_ip_reserved():
    handler = IPv4AddrClassifierPublicHandler()
    reserved_ip = IPv4Addr("240.0.0.1")
    result = handler.handle(reserved_ip)
    assert result != IPv4AddrType.PUBLIC, "Should not classify as PUBLIC"


def test_ipv4_multicast_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierMulticastHandler()

    # Test with a multicast IP address (e.g., 224.0.0.1)
    multicast_ip = IPv4Addr("224.0.0.1")
    result = handler.handle(multicast_ip)
    assert result == IPv4AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv4_multicast_handler_boundary_lower():
    # Test with the lower boundary of multicast IP range (e.g., 224.0.0.0)
    handler = IPv4AddrClassifierMulticastHandler()
    lower_boundary_ip = IPv4Addr("224.0.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv4_multicast_handler_boundary_upper():
    # Test with the upper boundary of multicast IP range (e.g., 239.255.255.255)
    handler = IPv4AddrClassifierMulticastHandler()
    upper_boundary_ip = IPv4Addr("239.255.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv4_multicast_handler_invalid_ip():
    # Test with an IP address that is not in the multicast range (e.g., 192.168.1.1)
    handler = IPv4AddrClassifierMulticastHandler()
    non_multicast_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(non_multicast_ip)
    assert result != IPv4AddrType.MULTICAST, "Should not classify as MULTICAST"


def test_ipv4_link_local_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierLinkLocalHandler()

    # Test with a link-local IP address (e.g., 169.254.1.1)
    link_local_ip = IPv4Addr("169.254.1.1")
    result = handler.handle(link_local_ip)
    assert result == IPv4AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv4_link_local_handler_boundary_lower():
    # Test with the lower boundary of the link-local IP range (e.g., 169.254.0.0)
    handler = IPv4AddrClassifierLinkLocalHandler()
    lower_boundary_ip = IPv4Addr("169.254.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv4_link_local_handler_boundary_upper():
    # Test with the upper boundary of the link-local IP range (e.g., 169.254.255.255)
    handler = IPv4AddrClassifierLinkLocalHandler()
    upper_boundary_ip = IPv4Addr("169.254.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv4_link_local_handler_invalid_ip():
    # Test with an IP address that is not in the link-local range (e.g., 192.168.1.1)
    handler = IPv4AddrClassifierLinkLocalHandler()
    non_link_local_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(non_link_local_ip)
    assert result != IPv4AddrType.LINK_LOCAL, "Should not classify as LINK_LOCAL"


def test_ipv4_loopback_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierLoopbackHandler()

    # Test with a loopback IP address (e.g., 127.0.0.1)
    loopback_ip = IPv4Addr("127.0.0.1")
    result = handler.handle(loopback_ip)
    assert result == IPv4AddrType.LOOPBACK, "Should classify as LOOPBACK"


def test_ipv4_loopback_handler_boundary_lower():
    # Test with the lower boundary of the loopback IP range (e.g., 127.0.0.0)
    handler = IPv4AddrClassifierLoopbackHandler()
    lower_boundary_ip = IPv4Addr("127.0.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.LOOPBACK, "Should classify as LOOPBACK"


def test_ipv4_loopback_handler_boundary_upper():
    # Test with the upper boundary of the loopback IP range (e.g., 127.255.255.255)
    handler = IPv4AddrClassifierLoopbackHandler()
    upper_boundary_ip = IPv4Addr("127.255.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.LOOPBACK, "Should classify as LOOPBACK"


def test_ipv4_loopback_handler_invalid_ip():
    # Test with an IP address that is not in the loopback range (e.g., 192.168.1.1)
    handler = IPv4AddrClassifierLoopbackHandler()
    non_loopback_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(non_loopback_ip)
    assert result != IPv4AddrType.LOOPBACK, "Should not classify as LOOPBACK"


def test_ipv4_dslite_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierDSLiteHandler()

    # Test with a DS-Lite IP address (e.g., 192.0.0.2)
    dslite_ip = IPv4Addr("192.0.0.2")
    result = handler.handle(dslite_ip)
    assert result == IPv4AddrType.DS_LITE, "Should classify as DS_LITE"


def test_ipv4_dslite_handler_boundary_lower():
    # Test with the lower boundary of the DS-Lite IP range (e.g., 192.0.0.0)
    handler = IPv4AddrClassifierDSLiteHandler()
    lower_boundary_ip = IPv4Addr("192.0.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.DS_LITE, "Should classify as DS_LITE"


def test_ipv4_dslite_handler_boundary_upper():
    # Test with the upper boundary of the DS-Lite IP range (e.g., 192.0.0.255)
    handler = IPv4AddrClassifierDSLiteHandler()
    upper_boundary_ip = IPv4Addr("192.0.0.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.DS_LITE, "Should classify as DS_LITE"


def test_ipv4_dslite_handler_invalid_ip():
    # Test with an IP address that is not in the DS-Lite range (e.g., 8.8.8.8)
    handler = IPv4AddrClassifierDSLiteHandler()
    non_dslite_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(non_dslite_ip)
    assert result != IPv4AddrType.DS_LITE, "Should not classify as DS_LITE"


def test_ipv4_documentation_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierDocumentationHandler()

    # Test with a documentation IP address (e.g., 192.0.2.1)
    documentation_ip = IPv4Addr("192.0.2.1")
    result = handler.handle(documentation_ip)
    assert result == IPv4AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv4_documentation_handler_boundary_lower():
    # Test with the lower boundary of a documentation IP range (e.g., 192.0.2.0)
    handler = IPv4AddrClassifierDocumentationHandler()
    lower_boundary_ip = IPv4Addr("192.0.2.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv4_documentation_handler_boundary_upper():
    # Test with the upper boundary of a documentation IP range (e.g., 203.0.113.255)
    handler = IPv4AddrClassifierDocumentationHandler()
    upper_boundary_ip = IPv4Addr("203.0.113.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv4_documentation_handler_invalid_ip():
    # Test with an IP address that is not in the documentation range (e.g., 8.8.8.8)
    handler = IPv4AddrClassifierDocumentationHandler()
    non_documentation_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(non_documentation_ip)
    assert result != IPv4AddrType.DOCUMENTATION, "Should not classify as DOCUMENTATION"


def test_ipv4_carriernat_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierCarrierNATHandler()

    # Test with a Carrier-Grade NAT (CGNAT) IP address (e.g., 100.64.0.1)
    carriernat_ip = IPv4Addr("100.64.0.1")
    result = handler.handle(carriernat_ip)
    assert result == IPv4AddrType.CARRIER_GRADE_NAT, "Should classify as CARRIER_GRADE_NAT"


def test_ipv4_carriernat_handler_boundary_lower():
    # Test with the lower boundary of the Carrier-Grade NAT range (e.g., 100.64.0.0)
    handler = IPv4AddrClassifierCarrierNATHandler()
    lower_boundary_ip = IPv4Addr("100.64.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.CARRIER_GRADE_NAT, "Should classify as CARRIER_GRADE_NAT"


def test_ipv4_carriernat_handler_boundary_upper():
    # Test with the upper boundary of the Carrier-Grade NAT range (e.g., 100.127.255.255)
    handler = IPv4AddrClassifierCarrierNATHandler()
    upper_boundary_ip = IPv4Addr("100.127.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.CARRIER_GRADE_NAT, "Should classify as CARRIER_GRADE_NAT"


def test_ipv4_carriernat_handler_invalid_ip():
    # Test with an IP address that is not in the Carrier-Grade NAT range (e.g., 8.8.8.8)
    handler = IPv4AddrClassifierCarrierNATHandler()
    non_carriernat_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(non_carriernat_ip)
    assert result != IPv4AddrType.CARRIER_GRADE_NAT, "Should not classify as CARRIER_GRADE_NAT"


def test_ipv4_benchmark_testing_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierBenchmarkTestingHandler()

    # Test with a Benchmark Testing IP address (e.g., 198.18.0.1)
    benchmark_testing_ip = IPv4Addr("198.18.0.1")
    result = handler.handle(benchmark_testing_ip)
    assert result == IPv4AddrType.BENCHMARK_TESTING, "Should classify as BENCHMARK_TESTING"


def test_ipv4_benchmark_testing_handler_boundary_lower():
    # Test with the lower boundary of the Benchmark Testing IP range (e.g., 198.18.0.0)
    handler = IPv4AddrClassifierBenchmarkTestingHandler()
    lower_boundary_ip = IPv4Addr("198.18.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.BENCHMARK_TESTING, "Should classify as BENCHMARK_TESTING"


def test_ipv4_benchmark_testing_handler_boundary_upper():
    # Test with the upper boundary of the Benchmark Testing IP range (e.g., 198.19.255.255)
    handler = IPv4AddrClassifierBenchmarkTestingHandler()
    upper_boundary_ip = IPv4Addr("198.19.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.BENCHMARK_TESTING, "Should classify as BENCHMARK_TESTING"


def test_ipv4_benchmark_testing_handler_invalid_ip():
    # Test with an IP address that is not in the Benchmark Testing range (e.g., 8.8.8.8)
    handler = IPv4AddrClassifierBenchmarkTestingHandler()
    non_benchmark_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(non_benchmark_ip)
    assert result != IPv4AddrType.BENCHMARK_TESTING, "Should not classify as BENCHMARK_TESTING"


def test_ipv4_ip6to4_relay_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierIP6To4RelayHandler()

    # Test with an IPv6-to-IPv4 relay IP address (e.g., 192.88.99.1)
    ip6to4_ip = IPv4Addr("192.88.99.1")
    result = handler.handle(ip6to4_ip)
    assert result == IPv4AddrType.IPV6_TO_IPV4_RELAY, "Should classify as IPV6_TO_IPV4_RELAY"


def test_ipv4_ip6to4_relay_handler_boundary_lower():
    # Test with the lower boundary of the IPv6-to-IPv4 relay range (e.g., 192.88.99.0)
    handler = IPv4AddrClassifierIP6To4RelayHandler()
    lower_boundary_ip = IPv4Addr("192.88.99.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.IPV6_TO_IPV4_RELAY, "Should classify as IPV6_TO_IPV4_RELAY"


def test_ipv4_ip6to4_relay_handler_boundary_upper():
    # Test with the upper boundary of the IPv6-to-IPv4 relay range (e.g., 192.88.99.255)
    handler = IPv4AddrClassifierIP6To4RelayHandler()
    upper_boundary_ip = IPv4Addr("192.88.99.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.IPV6_TO_IPV4_RELAY, "Should classify as IPV6_TO_IPV4_RELAY"


def test_ipv4_ip6to4_relay_handler_invalid_ip():
    # Test with an IP address that is not in the IPv6-to-IPv4 relay range (e.g., 8.8.8.8)
    handler = IPv4AddrClassifierIP6To4RelayHandler()
    non_ip6to4_ip = IPv4Addr("8.8.8.8")
    result = handler.handle(non_ip6to4_ip)
    assert result != IPv4AddrType.IPV6_TO_IPV4_RELAY, "Should not classify as IPV6_TO_IPV4_RELAY"


def test_ipv4_reserved_handler():
    # Create an instance of the handler
    handler = IPv4AddrClassifierReservedHandler()

    # Test with a reserved IP address (e.g., 240.0.0.1)
    reserved_ip = IPv4Addr("240.0.0.1")
    result = handler.handle(reserved_ip)
    assert result == IPv4AddrType.RESERVED, "Should classify as RESERVED"


def test_ipv4_reserved_handler_boundary_lower():
    # Test with the lower boundary of the reserved IP range (e.g., 240.0.0.0)
    handler = IPv4AddrClassifierReservedHandler()
    lower_boundary_ip = IPv4Addr("240.0.0.0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv4AddrType.RESERVED, "Should classify as RESERVED"


def test_ipv4_reserved_handler_boundary_upper():
    # Test with the upper boundary of the reserved IP range (e.g., 255.255.255.254)
    handler = IPv4AddrClassifierReservedHandler()
    upper_boundary_ip = IPv4Addr("255.255.255.254")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv4AddrType.RESERVED, "Should classify as RESERVED"


def test_ipv4_reserved_handler_invalid_ip():
    # Test with an IP address that is not in the reserved range (e.g., 192.168.1.1)
    handler = IPv4AddrClassifierReservedHandler()
    non_reserved_ip = IPv4Addr("192.168.1.1")
    result = handler.handle(non_reserved_ip)
    assert result != IPv4AddrType.RESERVED, "Should not classify as RESERVED"


def test_ipv6_loopback_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierLoopbackHandler()

    # Test with the IPv6 loopback address (::1)
    loopback_ip = IPv6Addr("::1")
    result = handler.handle(loopback_ip)
    assert result == IPv6AddrType.LOOPBACK, "Should classify as LOOPBACK"


def test_ipv6_loopback_handler_invalid_ip():
    # Test with an IP address that is not the loopback address (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierLoopbackHandler()
    non_loopback_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_loopback_ip)
    assert result != IPv6AddrType.LOOPBACK, "Should not classify as LOOPBACK"


def test_ipv6_ipv4mapped_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierIPv4MappedHandler()

    # Test with an IPv4-mapped IPv6 address (::ffff:192.168.1.1)
    ipv4_mapped_ip = IPv6Addr("::ffff:192.168.1.1")
    result = handler.handle(ipv4_mapped_ip)
    assert result == IPv6AddrType.IPV4_MAPPED, "Should classify as IPV4_MAPPED"


def test_ipv6_ipv4mapped_handler_boundary_lower():
    # Test with the lower boundary of the IPv4-mapped range (::ffff:0:0/96)
    handler = IPv6AddrClassifierIPv4MappedHandler()
    lower_boundary_ip = IPv6Addr("::ffff:0:0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.IPV4_MAPPED, "Should classify as IPV4_MAPPED"


def test_ipv6_ipv4mapped_handler_boundary_upper():
    # Test with the upper boundary of the IPv4-mapped range (::ffff:255.255.255.255/96)
    handler = IPv6AddrClassifierIPv4MappedHandler()
    upper_boundary_ip = IPv6Addr("::ffff:255.255.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.IPV4_MAPPED, "Should classify as IPV4_MAPPED"


def test_ipv6_ipv4mapped_handler_invalid_ip():
    # Test with an IP address that is not in the IPv4-mapped range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierIPv4MappedHandler()
    non_ipv4_mapped_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_ipv4_mapped_ip)
    assert result != IPv6AddrType.IPV4_MAPPED, "Should not classify as IPV4_MAPPED"


def test_ipv6_ipv4translated_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierIPv4TranslatedHandler()

    # Test with an IPv4-translated IPv6 address (::ffff:0:0:0:192.168.1.1)
    ipv4_translated_ip = IPv6Addr("::ffff:0:0:192.168.1.1")
    result = handler.handle(ipv4_translated_ip)
    assert result != IPv6AddrType.IPV4_TRANSLATED, "Should classify as IPV4_TRANSLATED"


def test_ipv6_ipv4translated_handler_boundary_lower():
    # Test with the lower boundary of the IPv4-translated range (::ffff:0:0:0/96)
    handler = IPv6AddrClassifierIPv4TranslatedHandler()
    lower_boundary_ip = IPv6Addr("::ffff:0:0:0")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.IPV4_TRANSLATED, "Should classify as IPV4_TRANSLATED"


def test_ipv6_ipv4translated_handler_boundary_upper():
    # Test with the upper boundary of the IPv4-translated range (::ffff:0:0:255.255.255.255/96)
    handler = IPv6AddrClassifierIPv4TranslatedHandler()
    upper_boundary_ip = IPv6Addr("::ffff:0:255.255.255.255")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.IPV4_TRANSLATED, "Should classify as IPV4_TRANSLATED"


def test_ipv6_ipv4translated_handler_invalid_ip():
    # Test with an IP address that is not in the IPv4-translated range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierIPv4TranslatedHandler()
    non_ipv4_translated_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_ipv4_translated_ip)
    assert result != IPv6AddrType.IPV4_TRANSLATED, "Should not classify as IPV4_TRANSLATED"


def test_ipv6_ipv4to6_translation_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierIPv4To6TranslationHandler()

    # Test with an IPv4-to-IPv6 translation address (e.g., 64:ff9b::192.168.1.1)
    ipv4_to6_ip = IPv6Addr("64:ff9b::192.168.1.1")
    result = handler.handle(ipv4_to6_ip)
    assert result == IPv6AddrType.IPV4_IPV6_TRANSLATION, "Should classify as IPV4_IPV6_TRANSLATION"


def test_ipv6_ipv4to6_translation_handler_boundary_lower():
    # Test with the lower boundary of the IPv4-to-IPv6 translation range (64:ff9b::/96)
    handler = IPv6AddrClassifierIPv4To6TranslationHandler()
    lower_boundary_ip = IPv6Addr("64:ff9b::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.IPV4_IPV6_TRANSLATION, "Should classify as IPV4_IPV6_TRANSLATION"


def test_ipv6_ipv4to6_translation_handler_upper():
    # Test with the upper boundary of the IPv4-to-IPv6 translation range (64:ff9b:1::/48)
    handler = IPv6AddrClassifierIPv4To6TranslationHandler()
    upper_boundary_ip = IPv6Addr("64:ff9b:1::")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.IPV4_IPV6_TRANSLATION, "Should classify as IPV4_IPV6_TRANSLATION"


def test_ipv6_ipv4to6_translation_handler_invalid_ip():
    # Test with an IP address that is not in the IPv4-to-IPv6 translation range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierIPv4To6TranslationHandler()
    non_ipv4_to6_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_ipv4_to6_ip)
    assert result != IPv6AddrType.IPV4_IPV6_TRANSLATION, "Should not classify as IPV4_IPV6_TRANSLATION"


def test_ipv6_discard_prefix_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierDiscardPrefixHandler()

    # Test with an IPv6 discard prefix address (100::1)
    discard_prefix_ip = IPv6Addr("100::1")
    result = handler.handle(discard_prefix_ip)
    assert result == IPv6AddrType.DISCARD_PREFIX, "Should classify as DISCARD_PREFIX"


def test_ipv6_discard_prefix_handler_boundary_lower():
    # Test with the lower boundary of the discard prefix range (100::/64)
    handler = IPv6AddrClassifierDiscardPrefixHandler()
    lower_boundary_ip = IPv6Addr("100::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.DISCARD_PREFIX, "Should classify as DISCARD_PREFIX"


def test_ipv6_discard_prefix_handler_invalid_ip():
    # Test with an IP address that is not in the discard prefix range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierDiscardPrefixHandler()
    non_discard_prefix_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_discard_prefix_ip)
    assert result != IPv6AddrType.DISCARD_PREFIX, "Should not classify as DISCARD_PREFIX"


def test_ipv6_teredo_tunneling_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierTeredoTunnelingHandler()

    # Test with an IPv6 Teredo tunneling address (2001::1)
    teredo_ip = IPv6Addr("2001::1")
    result = handler.handle(teredo_ip)
    assert result == IPv6AddrType.TEREDO_TUNNELING, "Should classify as TEREDO_TUNNELING"


def test_ipv6_teredo_tunneling_handler_boundary_lower():
    # Test with the lower boundary of the Teredo tunneling range (2001::/32)
    handler = IPv6AddrClassifierTeredoTunnelingHandler()
    lower_boundary_ip = IPv6Addr("2001::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.TEREDO_TUNNELING, "Should classify as TEREDO_TUNNELING"


def test_ipv6_teredo_tunneling_handler_invalid_ip():
    # Test with an IP address that is not in the Teredo tunneling range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierTeredoTunnelingHandler()
    non_teredo_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_teredo_ip)
    assert result != IPv6AddrType.TEREDO_TUNNELING, "Should not classify as TEREDO_TUNNELING"


def test_ipv6_documentation_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierDocumentationHandler()

    # Test with an IPv6 documentation address (2001:db8::1)
    documentation_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(documentation_ip)
    assert result == IPv6AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv6_documentation_handler_boundary_lower():
    # Test with the lower boundary of the documentation range (2001:db8::/32)
    handler = IPv6AddrClassifierDocumentationHandler()
    lower_boundary_ip = IPv6Addr("2001:db8::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv6_documentation_handler_boundary_upper():
    # Test with the upper boundary of the documentation range (2001:db8:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierDocumentationHandler()
    upper_boundary_ip = IPv6Addr("2001:db8:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.DOCUMENTATION, "Should classify as DOCUMENTATION"


def test_ipv6_documentation_handler_invalid_ip():
    # Test with an IP address that is not in the documentation range (e.g., 2001:db9::1)
    handler = IPv6AddrClassifierDocumentationHandler()
    non_documentation_ip = IPv6Addr("2001:db9::1")
    result = handler.handle(non_documentation_ip)
    assert result != IPv6AddrType.DOCUMENTATION, "Should not classify as DOCUMENTATION"


def test_ipv6_orchidv2_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierORCHIDV2Handler()

    # Test with an ORCHIDv2 address (e.g., 2001:20::1)
    orchidv2_ip = IPv6Addr("2001:20::1")
    result = handler.handle(orchidv2_ip)
    assert result == IPv6AddrType.ORCHIDV2, "Should classify as ORCHID_V2"


def test_ipv6_orchidv2_handler_boundary_lower():
    # Test with the lower boundary of the ORCHIDv2 range (e.g., 2001:20::/28)
    handler = IPv6AddrClassifierORCHIDV2Handler()
    lower_boundary_ip = IPv6Addr("2001:20::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.ORCHIDV2, "Should classify as ORCHID_V2"


def test_ipv6_orchidv2_handler_boundary_upper():
    # Test with the upper boundary of the ORCHIDv2 range (e.g., 2001:2f:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierORCHIDV2Handler()
    upper_boundary_ip = IPv6Addr("2001:2f:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.ORCHIDV2, "Should classify as ORCHID_V2"


def test_ipv6_orchidv2_handler_invalid_ip():
    # Test with an IP address that is not in the ORCHIDv2 range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierORCHIDV2Handler()
    non_orchidv2_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_orchidv2_ip)
    assert result != IPv6AddrType.ORCHIDV2, "Should not classify as ORCHID_V2"


def test_ipv6_6to4_scheme_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifier6To4SchemeHandler()

    # Test with a 6to4 address (e.g., 2002::1)
    ip_6to4 = IPv6Addr("2002::1")
    result = handler.handle(ip_6to4)
    assert result == IPv6AddrType.IP6_TO4, "Should classify as SIX_TO_FOUR"


def test_ipv6_6to4_scheme_handler_boundary_lower():
    # Test with the lower boundary of the 6to4 range (2002::/16)
    handler = IPv6AddrClassifier6To4SchemeHandler()
    lower_boundary_ip = IPv6Addr("2002::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.IP6_TO4, "Should classify as SIX_TO_FOUR"


def test_ipv6_6to4_scheme_handler_boundary_upper():
    # Test with the upper boundary of the 6to4 range (2002:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifier6To4SchemeHandler()
    upper_boundary_ip = IPv6Addr("2002:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.IP6_TO4, "Should classify as SIX_TO_FOUR"


def test_ipv6_6to4_scheme_handler_invalid_ip():
    # Test with an IP address that is not in the 6to4 range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifier6To4SchemeHandler()
    non_6to4_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_6to4_ip)
    assert result != IPv6AddrType.IP6_TO4, "Should not classify as SIX_TO_FOUR"


def test_ipv6_srv6_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierSRV6Handler()

    # Test with an SRv6 address (e.g., 5f00::1)
    srv6_ip = IPv6Addr("5f00::1")
    result = handler.handle(srv6_ip)
    assert result == IPv6AddrType.SRV6, "Should classify as SRV6"


def test_ipv6_srv6_handler_boundary_lower():
    # Test with the lower boundary of the SRv6 range (e.g., 5f00::/16)
    handler = IPv6AddrClassifierSRV6Handler()
    lower_boundary_ip = IPv6Addr("5f00::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.SRV6, "Should classify as SRV6"


def test_ipv6_srv6_handler_boundary_upper():
    # Test with the upper boundary of the SRv6 range (e.g., 5fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierSRV6Handler()
    upper_boundary_ip = IPv6Addr("5f00:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.SRV6, "Should classify as SRV6"


def test_ipv6_srv6_handler_invalid_ip():
    # Test with an IP address that is not in the SRv6 range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierSRV6Handler()
    non_srv6_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_srv6_ip)
    assert result != IPv6AddrType.SRV6, "Should not classify as SRV6"


def test_ipv6_linklocal_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierLinkLocalHandler()

    # Test with a link-local IPv6 address (e.g., fe80::1)
    linklocal_ip = IPv6Addr("fe80::1")
    result = handler.handle(linklocal_ip)
    assert result == IPv6AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv6_linklocal_handler_boundary_lower():
    # Test with the lower boundary of the link-local range (fe80::/64)
    handler = IPv6AddrClassifierLinkLocalHandler()
    lower_boundary_ip = IPv6Addr("fe80::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv6_linklocal_handler_boundary_upper():
    # Test with the upper boundary of the link-local range (fe80::ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierLinkLocalHandler()
    upper_boundary_ip = IPv6Addr("fe80::ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.LINK_LOCAL, "Should classify as LINK_LOCAL"


def test_ipv6_linklocal_handler_invalid_ip():
    # Test with an IP address that is not in the link-local range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierLinkLocalHandler()
    non_linklocal_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_linklocal_ip)
    assert result != IPv6AddrType.LINK_LOCAL, "Should not classify as LINK_LOCAL"


def test_ipv6_multicast_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierMulticastHandler()

    # Test with a multicast IPv6 address (e.g., ff00::1)
    multicast_ip = IPv6Addr("ff00::1")
    result = handler.handle(multicast_ip)
    assert result == IPv6AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv6_multicast_handler_boundary_lower():
    # Test with the lower boundary of the multicast range (ff00::/8)
    handler = IPv6AddrClassifierMulticastHandler()
    lower_boundary_ip = IPv6Addr("ff00::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv6_multicast_handler_boundary_upper():
    # Test with the upper boundary of the multicast range (ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierMulticastHandler()
    upper_boundary_ip = IPv6Addr("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.MULTICAST, "Should classify as MULTICAST"


def test_ipv6_multicast_handler_invalid_ip():
    # Test with an IP address that is not in the multicast range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierMulticastHandler()
    non_multicast_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_multicast_ip)
    assert result != IPv6AddrType.MULTICAST, "Should not classify as MULTICAST"


def test_ipv6_unique_local_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierUniqueLocalHandler()

    # Test with a unique local IPv6 address (e.g., fc00::1)
    unique_local_ip = IPv6Addr("fc00::1")
    result = handler.handle(unique_local_ip)
    assert result == IPv6AddrType.UNIQUE_LOCAL, "Should classify as UNIQUE_LOCAL"


def test_ipv6_unique_local_handler_boundary_lower():
    # Test with the lower boundary of the unique local range (fc00::/7)
    handler = IPv6AddrClassifierUniqueLocalHandler()
    lower_boundary_ip = IPv6Addr("fc00::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.UNIQUE_LOCAL, "Should classify as UNIQUE_LOCAL"


def test_ipv6_unique_local_handler_boundary_upper():
    # Test with the upper boundary of the unique local range (fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierUniqueLocalHandler()
    upper_boundary_ip = IPv6Addr("fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.UNIQUE_LOCAL, "Should classify as UNIQUE_LOCAL"


def test_ipv6_unique_local_handler_invalid_ip():
    # Test with an IP address that is not in the unique local range (e.g., 2001:db8::1)
    handler = IPv6AddrClassifierUniqueLocalHandler()
    non_unique_local_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(non_unique_local_ip)
    assert result != IPv6AddrType.UNIQUE_LOCAL, "Should not classify as UNIQUE_LOCAL"


def test_ipv6_global_unicast_handler():
    # Create an instance of the handler
    handler = IPv6AddrClassifierGlobalUnicastHandler()

    # Test with a global unicast IPv6 address (e.g., 2001:db8::1)
    global_unicast_ip = IPv6Addr("2001:db8::1")
    result = handler.handle(global_unicast_ip)
    assert result == IPv6AddrType.GLOBAL_UNICAST, "Should classify as GLOBAL_UNICAST"


def test_ipv6_global_unicast_handler_boundary_lower():
    # Test with the lower boundary of the global unicast range (2000::/3)
    handler = IPv6AddrClassifierGlobalUnicastHandler()
    lower_boundary_ip = IPv6Addr("2000::")
    result = handler.handle(lower_boundary_ip)
    assert result == IPv6AddrType.GLOBAL_UNICAST, "Should classify as GLOBAL_UNICAST"


def test_ipv6_global_unicast_handler_boundary_upper():
    # Test with the upper boundary of the global unicast range (3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    handler = IPv6AddrClassifierGlobalUnicastHandler()
    upper_boundary_ip = IPv6Addr("3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    result = handler.handle(upper_boundary_ip)
    assert result == IPv6AddrType.GLOBAL_UNICAST, "Should classify as GLOBAL_UNICAST"


def test_ipv6_global_unicast_handler_invalid_ip():
    # Test with an IP address that is not in the global unicast range (e.g., fc00::1)
    handler = IPv6AddrClassifierGlobalUnicastHandler()
    non_global_unicast_ip = IPv6Addr("fc00::1")
    result = handler.handle(non_global_unicast_ip)
    assert result != IPv6AddrType.GLOBAL_UNICAST, "Should not classify as GLOBAL_UNICAST"
