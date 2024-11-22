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

> [!Note]\
> The functionalities of these classes can also be achieved through the `ip_factory` module, which provides a more flexible and dynamic approach to generating various IP configurations. However, these classes can still be utilized directly when a more specific or tailored solution is required for certain use cases.</font>

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

## 6. `ip_type_classifiers` - IP Type Classifiers for IPv4 and IPv6

The `ip_type_classifiers` module provides functions to classify IP address types. It uses the Chain of Responsibility (CoR) design pattern to implement a set of classifier handlers, which determine whether an input is an IPv4 or IPv6 address. This module is primarily used to verify if an input belongs to a specific IP type. If the input does not match any handler, the module returns `None`. If the input matches a handler, the module returns the corresponding IP type.

<details>
<summary>(Click to Expand) Example: Verify IP Types</summary>

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
ip_type_classifier = IPTypeClassifier

print('Verify IPv4 Addresses'.center(80, '-'))
ipv4_address1 = '192.168.1.10'
ipv4_address2 = '192.168.1.256'
ipv4_address3 = b'\xc0\xa8\x012'
ipv4_address4 = b'\xc0\xa8\xff\xff\xff'

print('Input1:', '%-25s'%ipv4_address1, '->', 'Output1:', ip_type_classifier.classify_ipv4_address(ipv4_address1))
print('Input2:', '%-25s'%ipv4_address2, '->', 'Output2:', ip_type_classifier.classify_ipv4_address(ipv4_address2))
print('Input3:', '%-25s'%ipv4_address3, '->', 'Output3:', ip_type_classifier.classify_ipv4_address(ipv4_address3))
print('Input4:', '%-25s'%ipv4_address4, '->', 'Output4:', ip_type_classifier.classify_ipv4_address(ipv4_address4))

print('Verify IPv4 Netmasks'.center(80, '-'))
ipv4_netmask1 = '192.168.1.0'
ipv4_netmask2 = '255.255.255.0'
ipv4_netmask3 = '/33'
ipv4_netmask4 = '/24'

print('Input1:', '%-25s'%ipv4_netmask1, '->', 'Output1:', ip_type_classifier.classify_ipv4_netmask(ipv4_netmask1))
print('Input2:', '%-25s'%ipv4_netmask2, '->', 'Output2:', ip_type_classifier.classify_ipv4_netmask(ipv4_netmask2))
print('Input3:', '%-25s'%ipv4_netmask3, '->', 'Output3:', ip_type_classifier.classify_ipv4_netmask(ipv4_netmask3))
print('Input4:', '%-25s'%ipv4_netmask4, '->', 'Output4:', ip_type_classifier.classify_ipv4_netmask(ipv4_netmask4))


print('Verify IPv6 Addresses'.center(80, '-'))
ipv6_address1 = '2001:0db8:85a3::'
ipv6_address2 = '2001:0db8:85a3::1111::'
print('Input1:', '%-25s'%ipv6_address1, '->', 'Output1:', ip_type_classifier.classify_ipv6_address(ipv6_address1))
print('Input2:', '%-25s'%ipv6_address2, '->', 'Output2:', ip_type_classifier.classify_ipv6_address(ipv6_address2))

print('Verify IPv6 Netmasks'.center(80, '-'))
ipv6_netmask1 = '2001:0db8:85a3::'
ipv6_netmask2 = '/96'
ipv6_netmask3 = '/129'
print('Input1:', '%-25s'%ipv6_netmask1, '->', 'Output1:', ip_type_classifier.classify_ipv6_netmask(ipv6_netmask1))
print('Input2:', '%-25s'%ipv6_netmask2, '->', 'Output2:', ip_type_classifier.classify_ipv6_netmask(ipv6_netmask2))
print('Input3:', '%-25s'%ipv6_netmask3, '->', 'Output3:', ip_type_classifier.classify_ipv6_netmask(ipv6_netmask3))
```
Example output:
```
-----------------------------Verify IPv4 Addresses------------------------------
Input1: 192.168.1.10              -> Output1: IPType.IPv4
Input2: 192.168.1.256             -> Output2: None
Input3: b'\xc0\xa8\x012'          -> Output3: IPType.IPv4
Input4: b'\xc0\xa8\xff\xff\xff'   -> Output4: None
------------------------------Verify IPv4 Netmasks------------------------------
Input1: 192.168.1.0               -> Output1: None
Input2: 255.255.255.0             -> Output2: IPType.IPv4
Input3: /33                       -> Output3: None
Input4: /24                       -> Output4: IPType.IPv4
-----------------------------Verify IPv6 Addresses------------------------------
Input1: 2001:0db8:85a3::          -> Output1: IPType.IPv6
Input2: 2001:0db8:85a3::1111::    -> Output2: None
------------------------------Verify IPv6 Netmasks------------------------------
Input1: 2001:0db8:85a3::          -> Output1: None
Input2: /96                       -> Output2: IPType.IPv6
Input3: /129                      -> Output3: None
```

There are more specific handlers under `ip_type_classifiers` that can be used to classify IP addresses based on specific criteria. You can use them individually or in combination to classify IP addresses based on your requirements. Supported handlers include:

- `DotIPv4IPTypeClassifierHandler`
- `CIDRIPv4NetmaskClassifierHandler`
- `BytesIPv4IPTypeClassifierHandler`
- `ColonIPv6IPTypeClassifierHandler`
- `CIDRIPv6NetmaskClassifierHandler`
- `BytesIPv6IPTypeClassifierHandler`

</details>


## 7. `ip_addr_type_classifiers` - IP Address Type Classifiers for IPv4 and IPv6 address types

`ip_addr_type_classifiers` module provides functions to classify IP address types based on specific criteria. It uses the Chain of Responsibility (CoR) design pattern to implement a set of classifier handlers, which determine whether an input of an IPv4 or IPv6 address belongs to a specific range, such as public, private, multicast, or reserved.

<details>
<summary>(Click to Expand) Example: Classify Address Types</summary>

```python
from ttlinks.ipservice.ip_addr_type_classifiers import IPAddrTypeClassifier
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr

# IPAddrTypeClassifier is a utility class that classifies IP addresses based on their type.
ip_addr_type_classifier = IPAddrTypeClassifier

# Example usage of the IPAddrTypeClassifier class for IPv4 addresses.
print('IPv4 Address Types'.center(50, '-'))
ipv4_address1 = IPv4Addr('192.168.1.1')
ipv4_address2 = IPv4Addr('239.255.1.1')
ipv4_address3 = IPv4Addr('8.8.8.8')
ipv4_address4 = IPv4Addr('127.0.0.1')
ipv4_address5 = IPv4Addr('169.254.10.10')
print('IPv4 Address 1 is:', ip_addr_type_classifier.classify_ipv4_host_type(ipv4_address1))
print('IPv4 Address 2 is:', ip_addr_type_classifier.classify_ipv4_host_type(ipv4_address2))
print('IPv4 Address 3 is:', ip_addr_type_classifier.classify_ipv4_host_type(ipv4_address3))
print('IPv4 Address 4 is:', ip_addr_type_classifier.classify_ipv4_host_type(ipv4_address4))
print('IPv4 Address 5 is:', ip_addr_type_classifier.classify_ipv4_host_type(ipv4_address5))

# Example usage of the IPAddrTypeClassifier class for IPv6 addresses.
print('IPv6 Address Types'.center(50, '-'))
ipv6_address1 = IPv6Addr('2001:db8::1')
ipv6_address2 = IPv6Addr('fe80::1')
ipv6_address3 = IPv6Addr('ff02::1')
ipv6_address4 = IPv6Addr('::1')
ipv6_address5 = IPv6Addr('2003::1')
print('IPv6 Address 1 is:', ip_addr_type_classifier.classify_ipv6_host_type(ipv6_address1))
print('IPv6 Address 2 is:', ip_addr_type_classifier.classify_ipv6_host_type(ipv6_address2))
print('IPv6 Address 3 is:', ip_addr_type_classifier.classify_ipv6_host_type(ipv6_address3))
print('IPv6 Address 4 is:', ip_addr_type_classifier.classify_ipv6_host_type(ipv6_address4))
print('IPv6 Address 5 is:', ip_addr_type_classifier.classify_ipv6_host_type(ipv6_address5))
```
Example output:
```
----------------IPv4 Address Types----------------
IPv4 Address 1 is: IPv4AddrType.PRIVATE
IPv4 Address 2 is: IPv4AddrType.MULTICAST
IPv4 Address 3 is: IPv4AddrType.PUBLIC
IPv4 Address 4 is: IPv4AddrType.LOOPBACK
IPv4 Address 5 is: IPv4AddrType.LINK_LOCAL
----------------IPv6 Address Types----------------
IPv6 Address 1 is: IPv6AddrType.DOCUMENTATION
IPv6 Address 2 is: IPv6AddrType.LINK_LOCAL
IPv6 Address 3 is: IPv6AddrType.MULTICAST
IPv6 Address 4 is: IPv6AddrType.LOOPBACK
IPv6 Address 5 is: IPv6AddrType.GLOBAL_UNICAST
```

There are more specific handlers under `ip_addr_type_classifiers` that can be used to classify IP addresses based on specific criteria. You can use them individually or in combination to classify IP addresses based on your requirements. Supported handlers include:

- `IPv4AddrTypeUnspecifiedHandler`
- `IPv4AddrTypeLimitedBroadcastHandler`
- `IPv4AddrTypeCurrentNetworkHandler`
- `IPv4AddrClassifierPrivateHandler`
- `IPv4AddrClassifierPublicHandler`
- `IPv4AddrClassifierDocumentationHandler`
- `IPv4AddrClassifierMulticastHandler`
- `IPv4AddrClassifierLinkLocalHandler`
- `IPv4AddrClassifierLoopbackHandler`
- `IPv4AddrClassifierDSLiteHandler`
- `IPv4AddrClassifierCarrierNATHandler`
- `IPv4AddrClassifierBenchmarkTestingHandler`
- `IPv4AddrClassifierIP6To4RelayHandler`
- `IPv4AddrClassifierReservedHandler`
- `IPv6AddrClassifierUnspecifiedHandler`
- `IPv6AddrClassifierLoopbackHandler`
- `IPv6AddrClassifierIPv4MappedHandler`
- `IPv6AddrClassifierIPv4TranslatedHandler`
- `IPv6AddrClassifierIPv4To6TranslationHandler`
- `IPv6AddrClassifierDiscardPrefixHandler`
- `IPv6AddrClassifierTeredoTunnelingHandler`
- `IPv6AddrClassifierDocumentationHandler`
- `IPv6AddrClassifierORCHIDV2Handler`
- `IPv6AddrClassifier6To4SchemeHandler`
- `IPv6AddrClassifierSRV6Handler`
- `IPv6AddrClassifierLinkLocalHandler`
- `IPv6AddrClassifierMulticastHandler`
- `IPv6AddrClassifierUniqueLocalHandler`
- `IPv6AddrClassifierGlobalUnicastHandler`

</details>

## 8. `ip_subnet_type_classifiers` - IP Subnet Type Classifiers for IPv4 and IPv6 subnets

`ip_subnet_type_classifiers` module provides similar functionalities as `ip_addr_type_classifiers` but for IP subnets. Instead of returning one type that `ip_addr_type_classifiers` does, `ip_subnet_type_classifiers` returns a list of types that the subnet belongs to. This is because a subnet can belong to multiple types.

<details>
<summary>(Click to Expand) Example: Classify Subnet Types</summary>

```python
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig, IPv6SubnetConfig
from ttlinks.ipservice.ip_subnet_type_classifiers import IPSubnetTypeClassifier

ip_subnet_type_classifier = IPSubnetTypeClassifier

print('IPv4 subnet types:'.center(50, '-'))
ipv4_subnet1 = IPv4SubnetConfig("192.168.0.0/16")
ipv4_subnet2 = IPv4SubnetConfig("192.168.0.0/15")
ipv4_subnet3 = IPv4SubnetConfig("224.0.0.0/4")
print('IPv4 subnet 1 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet1)])
print('IPv4 subnet 2 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet2)])
print('IPv4 subnet 3 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv4_subnet_types(ipv4_subnet3)])

print('IPv6 subnet types:'.center(50, '-'))
ipv6_subnet1 = IPv6SubnetConfig("2001:db8::/32")
ipv6_subnet2 = IPv6SubnetConfig("fe80::/64")
ipv6_subnet3 = IPv6SubnetConfig("2002::/16")
print('IPv6 subnet 1 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet1)])
print('IPv6 subnet 2 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet2)])
print('IPv6 subnet 3 belongs to:', [subnet_type.name for subnet_type in ip_subnet_type_classifier.classify_ipv6_subnet_types(ipv6_subnet3)])
```
Example output:
```
----------------IPv4 subnet types:----------------
IPv4 subnet 1 belongs to: ['PRIVATE']
IPv4 subnet 2 belongs to: ['PRIVATE', 'PUBLIC']
IPv4 subnet 3 belongs to: ['DOCUMENTATION', 'MULTICAST']
----------------IPv6 subnet types:----------------
IPv6 subnet 1 belongs to: ['DOCUMENTATION', 'GLOBAL_UNICAST']
IPv6 subnet 2 belongs to: ['LINK_LOCAL']
IPv6 subnet 3 belongs to: ['IP6_TO4', 'GLOBAL_UNICAST']
```

Again, there are more specific handlers under `ip_subnet_type_classifiers` that can be used to classify IP subnets based on specific criteria. You can use them individually or in combination to classify IP subnets based on your requirements. Supported handlers include:

- `IPv4SubnetTypeUnspecifiedHandler`
- `IPv4SubnetTypeLimitedBroadcastHandler`
- `IPv4SubnetTypeCurrentNetworkHandler`
- `IPv4SubnetClassifierPrivateHandler`
- `IPv4SubnetClassifierPublicHandler`
- `IPv4SubnetClassifierDocumentationHandler`
- `IPv4SubnetClassifierMulticastHandler`
- `IPv4SubnetClassifierLinkLocalHandler`
- `IPv4SubnetClassifierLoopbackHandler`
- `IPv4SubnetClassifierDSLiteHandler`
- `IPv4SubnetClassifierCarrierNATHandler`
- `IPv4SubnetClassifierBenchmarkTestingHandler`
- `IPv4SubnetClassifierIP6To4RelayHandler`
- `IPv4SubnetClassifierReservedHandler`
- `IPv6SubnetClassifierUnspecifiedHandler`
- `IPv6SubnetClassifierLoopbackHandler`
- `IPv6SubnetClassifierIPv4MappedHandler`
- `IPv6SubnetClassifierIPv4TranslatedHandler`
- `IPv6SubnetClassifierIPv4To6TranslationHandler`
- `IPv6SubnetClassifierDiscardPrefixHandler`
- `IPv6SubnetClassifierTeredoTunnelingHandler`
- `IPv6SubnetClassifierDocumentationHandler`
- `IPv6SubnetClassifierORCHIDV2Handler`
- `IPv6SubnetClassifier6To4SchemeHandler`
- `IPv6SubnetClassifierSRV6Handler`
- `IPv6SubnetClassifierLinkLocalHandler`
- `IPv6SubnetClassifierMulticastHandler`
- `IPv6SubnetClassifierUniqueLocalHandler`
- `IPv6SubnetClassifierGlobalUnicastHandler`

</details>