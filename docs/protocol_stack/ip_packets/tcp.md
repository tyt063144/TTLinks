# Overview
This module introduces the ways to build TCP packets with different IP protocols. It's used to create TCP packets that can be sent over the network through Python raw sockets. The TCP module includes classes for constructing TCP packets with different attributes, such as source and destination ip addresses and other fields of IPv4 or IPv6 headers and fields in the TCP header. The module also provides utilities for calculating TCP checksums and managing TCP packet attributes.


## 1. TCP Packet Construction
`tcp.py` use the builder pattern to construct TCP packets. It provides classes for constructing TCP packets with different attributes. Users can create TCP packets with custom payloads and attributes using the provided classes. The TCP packet construction process involves setting the source and destination ip addresses, ports, sequence numbers, and other fields in the TCP header. The module includes classes for constructing TCP packets with different flags, such as SYN, ACK, FIN, and RST. Users can create TCP packets with custom flags and attributes using the provided classes.
```python
from ttlinks.protocol_stack.ip_packets.tcp import IPv4TCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags

tcp = IPv4TCP(
    ipv4_flags=IPv4Flags.DONT_FRAGMENT,
    ttl=32,
    destination_address='192.168.1.30',
    source_port=54156,
    destination_port=22,
    sequence_number=1370412840,
    tcp_flags=[TCPFlags.SYN],
)
# check packet in bytes
print(tcp.packet)  
# check ip header
print(tcp.ip_unit.as_bytes)
print(tcp.ip_unit.summary)
# check tcp header  
print(tcp.tcp_unit.as_bytes)
print(tcp.tcp_unit.summary)
```

## 2. IPv4TCP Packet Fields
- `ihl`: Internet Header Length (IPv4 header field)
- `dhcp`: Differentiated Services Code Point (IPv4 header field)
- `ecn`: Explicit Congestion Notification (IPv4 header field)
- `total_length`: Total Length (IPv4 header field)
- `identification`: Identification (IPv4 header field)
- `flags`: Flags (IPv4 header field)
```python
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
# IPv4Flags.DONT_FRAGMENT, IPv4Flags.MORE_FRAGMENTS, IPv4Flags.NO_FLAGS
```
- `fragment_offset`: Fragment Offset (IPv4 header field)
- `ttl`: Time to Live (IPv4 header field)
- `ipv4_checksum`: Checksum (IPv4 header field)
- `source_address`: Source IP Address (IPv4 header field)
- `destination_address`: Destination IP Address (IPv4 header field)
- `source_port`: Source Port (TCP header field)
- `destination_port`: Destination Port (TCP header field)
- `sequence_number`: Sequence Number (TCP header field)
- `acknowledgment_number`: Acknowledgment Number (TCP header field)
- `reserved`: Reserved (TCP header field)
- `tcp_flags`: TCP Flags. A list of TCPFlags objects. Each TCPFlags object represents a TCP flag. The TCP flags are used to set the flags in the TCP header. The TCP flags can be used to set the SYN, ACK, FIN, RST, and other flags in the TCP header. (TCP header field)
```python
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags
# passed as a list of TCPFlags objects, e.g. [TCPFlags.SYN, TCPFlags.ACK].
```
- `tcp_option_units`: TCP Options. A list of TCPOptionUnit objects. Each TCPOptionUnit object represents a TCP option. The TCP options are used to set additional fields in the TCP header. The TCP options can be used to set the Maximum Segment Size (MSS), Window Scale, Timestamp, and other fields in the TCP header. The TCP options will be automatically padded with NOP options to ensure that the header length is a multiple of 4 bytes. (TCP header field)
```python
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionUnit, TCPOptionBuilderDirector, TCPOption2HeaderBuilder, \
    TCPOption3HeaderBuilder, TCPOption4HeaderBuilder
tcp_option_director = TCPOptionBuilderDirector(TCPOption2HeaderBuilder)
tcp_option2_units = tcp_option_director.build(kind=2)
tcp_option_director.set_builder(TCPOption3HeaderBuilder)
tcp_option3_units = tcp_option_director.build(kind=3, length=3, value=8)
tcp_option_director.set_builder(TCPOption4HeaderBuilder)
tcp_option4_units = tcp_option_director.build(kind=4, length=2)
tcp_options = [tcp_option2_units, tcp_option3_units, tcp_option4_units]
# tcp_options can be passed to the IPv4TCP class
```
- `window_size`: Window Size (TCP header field)
- `urgent_pointer`: Urgent Pointer (TCP header field)
- `payload`: Payload (TCP header field)