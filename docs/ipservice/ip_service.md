# `ip_service`
The `ip_service` module offers a comprehensive suite of tools for managing and interacting with IP addresses and related services. Its functionality spans both IPv4 and IPv6, making it versatile for modern networking needs.

## 1. ip_address - IPv4 and IPv6 IPAddr and IPMask
The `ip_address` module provides a class for representing both IPv4 and IPv6 addresses. Below is an example of how to use the `ip_address` class to create IPv4 and IPv6 addresses.

<details>
<summary style="background-color: lightgray;color: black"><span style="font-weight: bold;color: black">Example:</span></summary>


```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr

ipv4_address = IPv4Addr('192.168.1.1')
ipv6_address = IPv6Addr('2001:db8::1')
ipv4_address_str = ipv4_address.address
ipv6_address_str = ipv6_address.address
ipv4_bin_str = ipv4_address.binary_string
ipv6_bin_str = ipv6_address.binary_string
ipv4_as_bytes = ipv4_address.as_bytes
ipv6_as_bytes = ipv6_address.as_bytes
# ... More

print('%-15s'% 'IPv4 Address:', ipv4_address_str)
print('%-15s'% 'IPv6 Address:', ipv6_address_str)
print('%-15s'% 'IPv4 Binary:', ipv4_bin_str)
print('%-15s'% 'IPv6 Binary:', ipv6_bin_str)
print('%-15s'% 'IPv4 as Bytes:', ipv4_as_bytes)
print('%-15s'% 'IPv6 as Bytes:', ipv6_as_bytes)
# ... More
```
Example output:
```
IPv4 Address:   192.168.1.1
IPv6 Address:   2001:DB8::1
IPv4 Binary:    11000000101010000000000100000001
IPv6 Binary:    00100000000000010000110110111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
IPv4 as Bytes:  b'\xc0\xa8\x01\x01'
IPv6 as Bytes:  b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
```
</details>



The `ip_address` module also provides properties and methods for working with the IP addresses. The following examples demonstrate how to access the properties and methods of the `ip_address` class.

For more details, refer to [IP Address](ip_address.md).


## 2. IPv4 and IPv6 HostConfig, SubnetConfig, and WildCardConfig (ip_config.py)
The `ip_config` module provides advanced classes for configuring IP host interfaces, subnets, and wildcard objects, essential for efficient network setup and management. Each class combines an `IPAddr` object for representing IP addresses with an `IPMask` object tailored to the specific use case, such as netmask or wildcard configurations. These classes offer more properties and methods you can leverage to streamline network IP configurations.

<font color='#FD7E14'>**Note:** The functionalities of these classes can also be achieved through the `ip_factory` module, which provides a more flexible and dynamic approach to generating various IP configurations. However, these classes can still be utilized directly when a more specific or tailored solution is required for certain use cases.</font>

Example:
```python
from ttlinks.ipservice.ip_configs import IPv4HostConfig
ipv4_host = IPv4HostConfig('192.168.1.10/24')

print('Display Address Information'.center(50, '-'))
address = ipv4_host.addr  # IPv4Addr object
address_in_bytes = address.as_bytes  # ipv4 address in bytes format, big-endian
address_in_binary_string = address.binary_string  # ipv4 address in binary string format
address_in_binary_digits = address.binary_digits  # ipv4 address in binary digits format
address_in_decimal = address.decimal  # ipv4 address in decimal format
print('%-8s'%'address:', address)
print('%-8s'%'bytes:', address_in_bytes)
print('%-8s'%'binary:', address_in_binary_string)
print('%-8s'%'digits:', address_in_binary_digits)
print('%-8s'%'decimal:', address_in_decimal)

print('Display Mask Information'.center(50, '-'))
mask = ipv4_host.mask  # IPv4Netmask object
mask_in_bytes = mask.as_bytes  # mask in bytes format, big-endian
mask_in_binary_string = mask.binary_string  # mask in binary string format
mask_in_binary_digits = mask.binary_digits  # mask in binary digits format
mask_in_decimal = mask.decimal  # mask in decimal format
print('%-8s'%'mask:', mask)
print('%-8s'%'bytes:', mask_in_bytes)
print('%-8s'%'binary:', mask_in_binary_string)
print('%-8s'%'digits:', mask_in_binary_digits)
print('%-8s'%'decimal:', mask_in_decimal)

print('Display Host Information'.center(50, '-'))
ip_address = ipv4_host.addr.address  # Dot-decimal notation of IPv4Addr object
ip_mask = ipv4_host.mask.address  # Dot-decimal notation of IPv4Netmask object
ip_type = ipv4_host.ip_type  # Return IPv4AddrType object
network_id = ipv4_host.network_id  # IPv4Addr object of network ID. Use .address to get the string format
broadcast_ip = ipv4_host.broadcast_ip  # IPv4Addr object of broadcast IP. Use .address to get the string format
is_public = ipv4_host.is_public  # Return True if the IP address is public
is_private = ipv4_host.is_private  # Return True if the IP address is private
# ...more attributes and methods
print('%-10s'%'host:', ipv4_host)  # IPv4Host object. Use str() to get the string format
print('%-10s'%'address:', ip_address)
print('%-10s'%'mask:', ip_mask)
print('%-10s'%'type:', ip_type)
print('%-10s'%'NET ID:', network_id)
print('%-10s'%'broadcast:', broadcast_ip)
print('%-10s'%'public?:', is_public)
print('%-10s'%'private?:', is_private)
```
Example output:
```
-----------Display Address Information------------
address: 192.168.1.10
bytes:   b'\xc0\xa8\x01\n'
binary:  11000000101010000000000100001010
digits:  [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
decimal: 3232235786
-------------Display Mask Information-------------
mask:    255.255.255.0
bytes:   b'\xff\xff\xff\x00'
binary:  11111111111111111111111100000000
digits:  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
decimal: 4294967040
-------------Display Host Information-------------
host:      192.168.1.0/24
address:   192.168.1.10
mask:      255.255.255.0
type:      IPv4AddrType.PRIVATE
NET ID:    192.168.1.0
broadcast: 192.168.1.255
public?:   False
private?:  True
```