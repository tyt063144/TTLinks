# Overview
This module introduces various modules related to ICMP (Internet Control Message Protocol) and its functionalities. ICMP is a network layer protocol used to send error messages and operational information indicating network issues. The ICMP module includes classes for parsing and constructing ICMP packets, handling ICMP error messages, and managing ICMP message types. The module also provides utilities for calculating ICMP checksums and managing ICMP message attributes.


## 1. Parsers
The parsers methods use similar patterns as ethernet and IPv4 parsers, where they parse binary data into ICMP packets and extract relevant information from the parsed data. The ICMP module includes parsers for different ICMP message types, allowing users to work with ICMP packets efficiently. The [protocol_stack](/docs/protocol_stack/protocol_stack.md) module includes ethernet parsers use examples. The parsers under ICMP follow the same pattern.

## 2. ICMP Packet Construction
`icmp_builder.py` use the builder pattern to construct ICMP packets. It provides classes for constructing ICMP packets with different message types and codes. Users can create ICMP packets with custom payloads and attributes using the provided classes. The ICMP packet construction process involves setting the message type, code, checksum, and payload data. For current support, the module includes classes for constructing ICMP Echo Request packets only because of the limited scope of the project of targeting ICMP scanning. However, the module can be extended to support other ICMP message types in the future.
```python
from ttlinks.protocol_stack.network_layer.ICMP.icmp_builder import ICMPHeaderBuilderDirector, ICMPEchoRequestHeaderBuilder, ICMPEchoRequestHeader
icmp_header_director = ICMPHeaderBuilderDirector(ICMPEchoRequestHeaderBuilder(ICMPEchoRequestHeader()))
icmp_header = icmp_header_director.build_echo_request()
print(icmp_header.__dict__)
```
Expected Output
```
{'_fields': 
    {
        'icmp_type': 8, 
        'icmp_code': 0, 
        'checksum': 0, 
        'identifier': 25489, 
        'sequence_number': 21866, 
        'payload': b''
    }
}
```

## 3. ICMP Ping Manager
`icmp_ping_manager.py` provides a class for managing ICMP ping operations. The `ICMPPingManager` class allows users to send ICMP Echo Request packets to a target IP address and receive ICMP Echo Reply packets. The class handles the construction and sending of ICMP packets, as well as the reception and parsing of ICMP replies. Users can specify the target IP address, the number of packets to send, and the timeout for waiting for replies. The `ICMPPingManager` class provides methods for sending and receiving ICMP packets, as well as calculating round-trip times (RTTs) for each packet sent.

### 3.1. Sending single ICMP Echo Request
ICMPPingManager can define semaphore when initializing the class to limit the number of concurrent ICMP requests. The default value is 255. Meaning the class can send 255 ICMP requests concurrently through asyncio by default. The class provides a method for sending a single ICMP Echo Request packet to a target IP address and waiting for an ICMP Echo Reply packet. The method returns a dictionary containing the number of packets sent, received, and lost, as well as the success status of the operation. The method also provides verbose output to display the status of each ICMP packet sent and received.

def ping() - parameters:
- `target_ip`: The target IP address to ping.
- `timeout`: The time to wait for an ICMP reply in seconds. Default is 2 seconds.
- `interval`: The time to wait between sending ICMP packets in seconds. Default is 1 second.
- `count`: The number of ICMP packets to send. Default is 4 packets.
- `verbose`: A boolean flag to enable verbose output. Default is False.
```python
from ttlinks.protocol_stack.network_layer.ICMP.icmp_manager import ICMPPingManager
manager = ICMPPingManager()
responses = manager.ping('8.8.8.8', timeout=2, interval=1, count=2, verbose=True)
print(responses)
```
Expected Output
```
(Successful) Reply from 8.8.8.8: bytes=28 TTL=116: Echo reply
(Successful) Reply from 8.8.8.8: bytes=28 TTL=116: Echo reply
{
    'total_packets_sent': 2, 
    'total_packets_received': 2, 
    'packet_loss': 0.0, 
    'is_successful': True
}
```

### 3.2. Sending multiple ICMP Echo Requests

```python
from ttlinks.protocol_stack.network_layer.ICMP.icmp_manager import ICMPPingManager
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig
manager = ICMPPingManager()
ips = IPv4SubnetConfig('8.8.8.8/31').get_hosts()
responses = manager.ping_multiple(ips, timeout=2, interval=1, count=2, verbose=True)
print(responses)
```
Expected Output
```
(Successful) Reply from 8.8.8.8: bytes=28 TTL=116: Echo reply
(Successful) Reply from 8.8.8.8: bytes=28 TTL=116: Echo reply
(Failed) Request to 8.8.8.9 timed out
(Failed) Request to 8.8.8.9 timed out
{
    '8.8.8.8': 
        {
            'total_packets_sent': 2, 
            'total_packets_received': 2, 
            'packet_loss': 0.0, 
            'is_successful': True
        }, 
    '8.8.8.9': 
        {
            'total_packets_sent': 2, 
            'total_packets_received': 0, 
            'packet_loss': 100.0, 
            'is_successful': False
        }
}
```