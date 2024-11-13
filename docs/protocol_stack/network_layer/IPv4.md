# Overview
This module introduces various modules related to IPv4 (Internet Protocol version 4) and its functionalities. IPv4 is a network layer protocol used to provide logical addressing and routing of packets between devices on a network. The IPv4 module includes classes for parsing and constructing IPv4 packets, handling IPv4 addressing and fragmentation, and managing IPv4 packet attributes. The module also provides utilities for calculating IPv4 checksums, managing IPv4 options, and controlling IPv4 packet fields.

## 1. Parsers
The parsers methods use similar patterns as ethernet parsers, where they parse binary data into IPv4 packets and extract relevant information from the parsed data. The IPv4 module includes parsers for different IPv4 packet fields, allowing users to work with IPv4 packets efficiently. The [protocol_stack](/docs/protocol_stack/protocol_stack.md) module includes examples of ethernet parsers. The parsers under IPv4 follow the same pattern.

```python
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_units import IPv4Unit
ipv4_parser = IPv4PacketParser()
parsed_ipv4 = ipv4_parser.parse(b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02')
ipv4_unit = IPv4Unit(**parsed_ipv4)
print(ipv4_unit.summary)
```
Expected Output
```
{'version': <IPType.IPv4: 4>, 'ihl': 5, 'header_length': 20, 'dscp': <DSCP.CS0: 0>, 'ecn': 0, 'total_length': 60, 'identification': 7238, 'flags': <IPv4Flags.DONT_FRAGMENT: 2>, 'fragment_offset': 0, 'ttl': 64, 'protocol': <IPPayloadProtocolTypes.TCP: 6>, 'header_checksum': '0x0', 'source_address': IPv4Addr('_address=[Octet(_binary_string=11000000), Octet(_binary_string=10101000), Octet(_binary_string=00000001), Octet(_binary_string=00000001)]), 'destination_address': IPv4Addr('_address=[Octet(_binary_string=11000000), Octet(_binary_string=10101000), Octet(_binary_string=00000001), Octet(_binary_string=00000010)]), 'options': b'', 'payload': b''}
```
