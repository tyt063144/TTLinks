# `ip_service`
The `ip_service` module offers a comprehensive suite of tools for managing and interacting with IP addresses and related services. Its functionality spans both IPv4 and IPv6, making it versatile for modern networking needs.


## 1. `ip_factory` - IP Factory for Generating IP Configurations
The `ip_factory` module provides IPv4 and IPv6 factories for generating a wide range of IP configurations. While it supports host, subnet, and wildcard configurations similar to those in the `ip_configs` module, the `ip_factory` module offers additional features. For example, it can instantiate multiple IP objects simultaneously, generate random IP addresses, and more. This module is the most recommended option, as it includes all the functionalities of the `ip_configs` module and extends them with greater flexibility and versatility.

The following example demonstrates how to use the `ip_factory` module to randomly create an IPv4 host configuration and access its properties.

<details>
<summary>(Click to Expand) Example:</summary>

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4_host = ipv4_factory.random_host(addr_type=IPv4TypeAddrBlocks.PRIVATE)

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
address: 192.168.158.28
bytes:   b'\xc0\xa8\x9e\x1c'
binary:  11000000101010001001111000011100
digits:  [
            1, 1, 0, 0, 0, 0, 0, 0, 
            1, 0, 1, 0, 1, 0, 0, 0, 
            1, 0, 0, 1, 1, 1, 1, 0, 
            0, 0, 0, 1, 1, 1, 0, 0
        ]
decimal: 3232275996
-------------Display Mask Information-------------
mask:    255.255.240.0
bytes:   b'\xff\xff\xf0\x00'
binary:  11111111111111111111000000000000
digits:  [
            1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0
        ]
decimal: 4294963200
-------------Display Host Information-------------
host:      192.168.158.28/20
address:   192.168.158.28
mask:      255.255.240.0
type:      IPv4AddrType.PRIVATE
NET ID:    192.168.144.0
broadcast: 192.168.159.255
public?:   False
private?:  True
```
</details>

For more examples, refer to
- [IPv4 Factory Examples](ip_factory.md)


## 2. `ip_address` - IPv4 and IPv6 IPAddr and IPMask
The `ip_address` module provides a class for representing both IPv4 and IPv6 addresses. Below is an example of how to use the `ip_address` class to create IPv4 and IPv6 addresses.

<details>
<summary>(Click to Expand) Example:</summary>


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

For more examples, refer to 
- [IP Address Examples](ip_address.md).

## 3. `ip_configs` - IPv4 and IPv6 HostConfig, SubnetConfig, and WildCardConfig
The `ip_config` module provides advanced classes for configuring IP host interfaces, subnets, and wildcard objects, essential for efficient network setup and management. Each class combines an `IPAddr` object for representing IP addresses with an `IPMask` object tailored to the specific use case, such as netmask or wildcard configurations. These classes offer more properties and methods you can leverage to streamline network IP configurations.

<font color='#FD7E14'>**Note:** The functionalities of these classes can also be achieved through the `ip_factory` module, which provides a more flexible and dynamic approach to generating various IP configurations. However, these classes can still be utilized directly when a more specific or tailored solution is required for certain use cases.</font>

<details>
<summary>(Click to Expand) Example:</summary>

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
</details>

For more examples, refer to
- [IPv4 Config Examples](ip_configs.md)

## 4. `wildcard_calculator` - Wildcard Calculators for IPv4 and IPv6

The `wildcard_calculator` module provides functions to calculate the minimum wildcard configuration objects for IPv4 and IPv6 subnets. It is specifically designed to simplify the process of determining the smallest wildcard masks for a given set of subnets, making it an essential tool for efficient network configuration. This is particularly helpful for administrators who find it challenging to determine the correct wildcard mask along with the correct network ID.

<details>
<summary>(Click to Expand) Example 1: IPv4 Wildcard Calculation</summary>

```python
from ttlinks.ipservice.wildcard_calculator import calculate_minimum_ipv4_wildcard

# Create a list of IPv4 subnets
subnets = [
    '10.10.25.0/24',
    '10.50.25.0/24',
    '10.90.25.0/24',
    '10.130.25.0/24',
    '10.170.25.0/24',
    '10.220.25.0/24',
    '10.255.25.0/24',
]

# Calculate the minimum wildcard mask for the list of subnets
wildcard = calculate_minimum_ipv4_wildcard(*subnets)

print('Display WildCard Information'.center(50, '-'))
address = wildcard.addr.address  # Dot-decimal notation of IPv4Addr object.
mask = wildcard.mask.address  # Dot-decimal notation of IPv4Wildcard object.
total_hosts = wildcard.total_hosts  # Total number of hosts covered by the wildcard mask.
hosts = [host for host in wildcard.get_hosts()]  # List of hosts covered by the wildcard mask. `.get_hosts()` returns a generator, so be careful when using it.
print('%-10s'%'wildcard:', wildcard)  # IPv4WildCardConfig object. Use str() to get the string format.
print('%-10s'%'address:', address) 
print('%-10s'%'mask:', mask)  
print('%-10s'%'total hosts:', total_hosts)  
print('%-10s'%'hosts:', hosts[:5], '...', hosts[-5:]) 
```
Example output:
```
-----------Display WildCard Information-----------
wildcard:  10.0.25.0 0.255.0.255 <class 'ttlinks.ipservice.ip_configs.IPv4WildCardConfig'>
address:   10.0.25.0
mask:      0.255.0.255
total hosts: 65536
hosts:     [
                IPv4Addr('_address=10.0.25.0'), 
                IPv4Addr('_address=10.0.25.1'), 
                IPv4Addr('_address=10.0.25.2'), 
                IPv4Addr('_address=10.0.25.3'), 
                IPv4Addr('_address=10.0.25.4')
            ] 
                ... 
            [
                IPv4Addr('_address=10.255.25.251'), 
                IPv4Addr('_address=10.255.25.252'), 
                IPv4Addr('_address=10.255.25.253'), 
                IPv4Addr('_address=10.255.25.254'), 
                IPv4Addr('_address=10.255.25.255')
            ]
```
</details>

<details>
<summary>(Click to Expand) Example 2: IPv6 Wildcard Calculation</summary>

```python
from ttlinks.ipservice.wildcard_calculator import calculate_minimum_ipv6_wildcard

# Create a list of IPv6 subnets
subnets = [
    '2001:db8::/96',
    '2001:db8:0:0:12::/96',
    '2001:db8:0:0:ab::/96',
]

# Calculate the minimum wildcard mask for the list of subnets
wildcard = calculate_minimum_ipv6_wildcard(*subnets)

print('Display WildCard Information'.center(50, '-'))
address = wildcard.addr.address  # Colon-hexadecimal notation of IPv6Wildcard object.
mask = wildcard.mask.address  # Colon-hexadecimal notation of the wildcard mask.
total_hosts = wildcard.total_hosts  # Total number of hosts covered by the wildcard mask.
print('%-10s'%'wildcard:', wildcard)  # IPv6WildCardConfig object. Use str() to get the string format.
print('%-10s'%'address:', address) 
print('%-10s'%'mask:', mask)  
print('%-10s'%'total hosts:', total_hosts)  
```
Example output:
```
-----------Display WildCard Information-----------
wildcard:  2001:DB8:: ::BB:0:FFFF:FFFF
address:   2001:DB8::
mask:      ::BB:0:FFFF:FFFF
total hosts: 274877906944
```
</details>

## 5. `ip_converters` - IP Address Converters for IPv4 and IPv6

The `ip_converters` module offers functions to convert IP addresses between various formats and a unified intermediate format, `bytes`. This functionality is particularly useful for standardizing IP address formats for further processing, storage, or interoperability between systems.


<details>
<summary>(Click to Expand) Example: Convert Various IPv4 Format to bytes</summary>

```python
from ttlinks.ipservice.ip_converters import IPConverter

ip_converter = IPConverter
ipv4_bytes_1 = ip_converter.convert_to_ipv4_bytes('192.168.1.1')
ipv4_bytes_2 = ip_converter.convert_to_ipv4_bytes(65535)
ipv4_bytes_3 = ip_converter.convert_to_ipv4_bytes('/24')
ipv4_bytes_4 = ip_converter.convert_to_ipv4_bytes(
    [
        1, 1, 0, 0, 0, 0, 0, 0, 
        1, 0, 1, 0, 1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 1, 
        0, 0, 0, 0, 1, 0, 1, 0
    ])
ipv4_bytes_5 = ip_converter.convert_to_ipv4_bytes('11111111111111110000000000000000')

print('IPv4 bytes 1:', ' -> ', '%-20s'%ipv4_bytes_1, ' -> ', [octet for octet in ipv4_bytes_1])
print('IPv4 bytes 2:', ' -> ', '%-20s'%ipv4_bytes_2, ' -> ', [octet for octet in ipv4_bytes_2])
print('IPv4 bytes 3:', ' -> ', '%-20s'%ipv4_bytes_3, ' -> ', [octet for octet in ipv4_bytes_3])
print('IPv4 bytes 4:', ' -> ', '%-20s'%ipv4_bytes_4, ' -> ', [octet for octet in ipv4_bytes_4])
print('IPv4 bytes 5:', ' -> ', '%-20s'%ipv4_bytes_5, ' -> ', [octet for octet in ipv4_bytes_5])
```
Example output:
```
IPv4 bytes 1:  ->  b'\xc0\xa8\x01\x01'   ->  [192, 168, 1, 1]
IPv4 bytes 2:  ->  b'\x00\x00\xff\xff'   ->  [0, 0, 255, 255]
IPv4 bytes 3:  ->  b'\xff\xff\xff\x00'   ->  [255, 255, 255, 0]
IPv4 bytes 4:  ->  b'\xc0\xa8\x01\n'     ->  [192, 168, 1, 10]
IPv4 bytes 5:  ->  b'\xff\xff\x00\x00'   ->  [255, 255, 0, 0]
```
</details>

For more examples, refer to
- [IP Converter Examples](ip_converters.md)