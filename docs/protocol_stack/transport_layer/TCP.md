# Overview
This module introduces various modules related to TCP (Transmission Control Protocol) and its functionalities. TCP is a transport layer protocol used to provide reliable, ordered, and error-checked delivery of data between applications. The TCP module includes classes for parsing and constructing TCP segments, handling TCP connection management, and managing TCP segment attributes. The module also provides utilities for calculating TCP checksums, managing TCP options, and controlling TCP segment flags and fields.


## 1. Parsers
`tcp_parsers.py` provides classes for parsing binary data into TCP segments and extracting relevant information from the parsed data. The TCP module includes parsers for different TCP segment fields, allowing users to work with TCP segments efficiently. The parsers use similar patterns as ethernet and IPv4 parsers, where they parse binary data into TCP segments and extract relevant information from the parsed data. The [protocol_stack](/docs/protocol_stack/protocol_stack.md) module includes examples of ethernet parsers. The parsers under TCP follow the same pattern.

```python
from ttlinks.protocol_stack.transport_layer.TCP.tcp_parsers import TCPParser
from ttlinks.protocol_stack.transport_layer.TCP.tcp_units import TCPUnit
tcp_parser = TCPParser()
parsed_tcp = tcp_parser.parse(b'\x00\x50\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\x20\x00\x00\x00\x00\x00\x00')
tcp_unit = TCPUnit(**parsed_tcp)
print(tcp_unit.summary)
```

Expected Output
```
{'source_port': 80, 'destination_port': 80, 'sequence_number': 0, 'acknowledgment_number': 0, 'data_offset': 5, 'reserved': 0, 'flags': [SYN (0x2)], 'window_size': 8192, 'checksum': '0x0', 'urgent_pointer': 0, 'options': [], 'payload': b'\x00'}
```

## 2. TCP Segment Construction
`tcp_builder.py` uses the builder pattern to construct TCP segments. It provides classes for constructing TCP segments with different flags, options, and fields. Users can create TCP segments with custom payloads and attributes using the provided classes. The TCP segment construction process involves setting the source and destination ports, sequence and acknowledgment numbers, flags, window size, checksum, and payload data. The module includes classes for constructing TCP segments with different flags and options, such as SYN, ACK, FIN, and window scaling. Users can extend the module to support additional TCP options and flags in the future.

```python
from ttlinks.protocol_stack.transport_layer.TCP.tcp_builder import TCPBuilderDirector, TCPHeaderBuilder, TCPHeader
from ttlinks.protocol_stack.transport_layer.TCP.tcp_options import TCPOptionBuilderDirector, TCPOption2HeaderBuilder, TCPOption3HeaderBuilder, \
    TCPOption4HeaderBuilder
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags
tcp_option_director = TCPOptionBuilderDirector(TCPOption2HeaderBuilder)
tcp_option2 = tcp_option_director.build(kind=2)
tcp_option_director.set_builder(TCPOption3HeaderBuilder)
tcp_option3 = tcp_option_director.build(kind=3, length=3, value=8)
tcp_option_director.set_builder(TCPOption4HeaderBuilder)
tcp_option4 = tcp_option_director.build(kind=4, length=2)


director = TCPBuilderDirector(TCPHeaderBuilder(TCPHeader()))
# Not all fields are specified here. You can add more fields as needed.
tcp_unit = director.construct(
    source_ip='192.168.1.70',
    destination_ip='192.168.1.254',
    source_port=54156,
    destination_port=443,
    sequence_number=1370412840,
    acknowledgment_number=0,
    reserved=0,
    flags=[TCPFlags.SYN],
    window_size=64240,
    option_units=[tcp_option2, tcp_option3, tcp_option4],
)
```