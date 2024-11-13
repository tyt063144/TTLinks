# Modules Introduction

## Overview

The `protocol_stack` module provides classes and functions for parsing and constructing network protocol data units (PDUs) at different layers of the TCP/IP model. It includes support for parsing and constructing Ethernet frames, IPv4 packets, TCP segments, and UDP datagrams. The module is designed to be extensible, allowing users to add support for additional protocols and packet types.

Currently, the module supports the following protocols' parsing and construction:
- Ethernet II and IEEE 802.3 - document will be added soon
- IPv4 - document will be added soon
- [ICMP](/docs/protocol_stack/network_layer/ICMP.md)
---
### Parsers

Parsers are classes that provide methods for parsing binary data into protocol data units (PDUs) and extracting relevant information from the parsed data. The `protocol_stack` module includes parsers in their respective protocol layers folders. The parsers are designed to work with binary data and provide a structured representation of the parsed data.

#### 1. Parsing Network Ethernet Data Units (PDUs)

- **`ethernet_parsers.py`**: The Ethernet module provides classes for parsing and constructing Ethernet frames. It includes support for Ethernet II and IEEE 802.3 frames, allowing users to work with different Ethernet frame types. Their payloads can be parsed by the corresponding higher-layer protocol parsers.

```python
from ttlinks.protocol_stack.ethernet_layer.ethernet_parsers import EthernetFrameParser
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
print(parsed_frame)
```
Expected Output
```
{
    'dst': b'\x01\x80\xc2\x00\x00\x00', 
    'src': b'\x04*\xe2\xdaA\x05', 
    'length': b"\x00'", 
    'llc': b'BB\x03', 
    'snap': b'', 
    'payload': b'\x00\x00\x02\x02<p\x00\x08\x9b\xb9:\xfe\x82\x00\x00\x00\x04\x80(\x04*\xe2\xdaA\x00\x80\x05\x01\x00\x14\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
}
```

#### 2. Parsing Network IPv4 Data Units (PDUs)
- **`ipv4_parsers.py`**: You can also start parsing higher-layer protocols like IPv4 packets by their corresponding parsers. If ICMP, TCP, or UDP packets are encapsulated in the IPv4 packet, you can parse them using the respective parsers. Here is an example of parsing an IPv4 packet:

```python
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
# Example IPv4 packet in hexadecimal
ipv4_packet = bytes.fromhex('4500003c6d7900008001fb49c0a801460808080808004c73000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869')

# Initialize the IPv4PacketParser
parser = IPv4PacketParser()
# Parse the IPv4 packet
parsed_ipv4_packet = parser.parse(ipv4_packet)
# Print the parsed IPv4 fields
for key, value in parsed_ipv4_packet.items():
    print(f'{key}: {value.hex()}')
```
Expected Output
```
version_and_ihl: 45
tos: 00
total_length: 003c
identification: 6d79
flags_and_fragment_offset: 0000
ttl: 80
protocol: 01
header_checksum: fb49
source_address: c0a80146
destination_address: 08080808
options: 
payload: 08004c73000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869
```
---
### Protocol Units
`ProtocolUnit` is a base class for all protocol units in the `protocol_stack` module. It provides a common interface for parsing and constructing protocol data units (PDUs) at different layers of the TCP/IP model. The `ProtocolUnit` class is designed. This class is used to define the structure of a protocol unit and provide methods for parsing and constructing the unit from binary data. Meaning it will provide more detailed information about the protocol unit after parsing than the parsers.

#### 1. Ethernet Frame Protocol Unit
- **`ethernet_unit.py`**: The `EthernetFrame` class represents an Ethernet frame and provides methods for parsing and constructing Ethernet frames. It includes support for Ethernet II and IEEE 802.3 frames, allowing users to work with different Ethernet frame types.

- Example 1 - Parsing an Ethernet Frame with properties displayed
```python
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory
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
print('frame_type', frame_type)
print('destination_mac', destination_mac)
print('source_mac', source_mac)
print('next_layer', next_layer)
print('ip_version', ip_version)
print('ip_header_length', ip_header_length)
print('ip_ttl', ip_ttl)
print('ip_dscp', ip_dscp)
print('ip_ecn', ip_ecn)
print('ip_total_length', ip_total_length)
print('ip_identification', ip_identification)
print('ip_flags', ip_flags)
print('ip_fragment_offset', ip_fragment_offset)
print('ip_protocol', ip_protocol)
print('ip_checksum', ip_checksum)
print('ip_src', ip_src)
print('ip_dst', ip_dst)
```
Expected Output
```
frame_type Ethernet_II
destination_mac 08:BF:B8:34:C6:A4
source_mac 08:9B:B9:3A:FE:82
next_layer IPv4
ip_version IPv4
ip_header_length 20
ip_ttl 118
ip_dscp 16
ip_ecn 0
ip_total_length 60
ip_identification 0
ip_flags 0
ip_fragment_offset 0
ip_protocol ICMP
ip_checksum 0x7283
ip_src 8.8.8.8
ip_dst 192.168.1.70
```

- Example 2 - Use the `summary` property to get a summary of the parsed Ethernet frame.
```python
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory

ethernet_frame = bytes.fromhex(
'08bfb834c6a4089bb93afe8208004540003c000000007601728308080808c0a8014600005473000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869')
ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
payload = ethernet_unit.payload
print(ethernet_unit.summary)
    
```
Expected Output
```
{
    'frame_type': <EthernetTypes.Ethernet_II: 0>, 
    'destination_mac': <ttlinks.macservice.mac_address.MACAddr object at 0x000001BD958C1E50>, 
    'source_mac': <ttlinks.macservice.mac_address.MACAddr object at 0x000001BD923DF290>, 
    'next_layer': <EthernetPayloadProtocolTypes.IPv4: 2048>, 
    'next_layer_payload': <ttlinks.protocol_stack.network_layer.IPv4.ipv4_packet_units.IPv4PacketUnit object at 0x000001BD958C1DF0>
}
```

- Example 3 - Use the `as_bytes` method to get the Ethernet frame in bytes, which can be used to structure the Ethernet frame or send it over the network.
```python
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory
ethernet_frame = bytes.fromhex(
'08bfb834c6a4089bb93afe8208004540003c000000007601728308080808c0a8014600005473000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869')
ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
print(ethernet_unit.as_bytes)
```
Expected Output
```
b'\x08\xbf\xb84\xc6\xa4\x08\x9b\xb9:\xfe\x82\x08\x00E@\x00<\x00\x00\x00\x00v\x01r\x83\x08\x08\x08\x08\xc0\xa8\x01F\x00\x00Ts\x00\x01\x00\xe8abcdefghijklmnopqrstuvwabcdefghi'
```

- Example 4 - Use the `attributes` property to get a dictionary of the parsed Ethernet frame attributes in bytes.
```python
from ttlinks.protocol_stack.ethernet_layer.ethernet_units import EthernetUnitFactory
ethernet_frame = bytes.fromhex(
'08bfb834c6a4089bb93afe8208004540003c000000007601728308080808c0a8014600005473000100e86162636465666768696a6b6c6d6e6f7071727374757677616263646566676869')
ethernet_unit = EthernetUnitFactory.create_unit(ethernet_frame)
print(ethernet_unit.attributes)
```
Expected Output
```
{
    'dst': b'\x08\xbf\xb84\xc6\xa4', 
    'src': b'\x08\x9b\xb9:\xfe\x82', 
    'type': b'\x08\x00', 
    'payload': b'E@\x00<\x00\x00\x00\x00v\x01r\x83\x08\x08\x08\x08\xc0\xa8\x01F\x00\x00Ts\x00\x01\x00\xe8abcdefghijklmnopqrstuvwabcdefghi'
}
```

#### 2. Other Protocol Units and Parsers 
In the `protocol_stack` Module, it uses similar methods and properties to parse and construct protocol data units at different layers of the TCP/IP model. You can explore the module to find more examples and use cases for parsing and constructing network protocol data units. The Protocol modules of various layers are placed in their respective folders in the `protocol_stack` module. For example `ICMP` and `IPv4` are placed in the `network_layer` folder, and `TCP` and `UDP` are placed in `transport_layer` folder. More protocols and layers can be added to the module to extend its functionality, which will be our future work.

- [ICMP Protocol Unit](/docs/protocol_stack/network_layer/ICMP.md)
- [IPv4 Protocol Unit](/docs/protocol_stack/network_layer/IPv4.md)
- [TCP Protocol Unit](/docs/protocol_stack/transport_layer/TCP.md)

#### 3. IP packet construction
- **`tcp.py`**: build TCP packets with IP header and TCP header. [Example](/docs/protocol_stack/transport_layer/TCP.md)
