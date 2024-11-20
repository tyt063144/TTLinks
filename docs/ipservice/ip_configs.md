# `ip_configs` Module


<details>

**TTLinks** provides a way to create host interface IP object for IPv4. The following example demonstrates how to create an IPv4 host object and access its properties:

<summary>(Click to Expand) Example 1: IPv4 Host</summary>

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

<details>
<summary>(Click to Expand) Example 2: IPv4 Subnet</summary>

Under `.subnet` method, **TTLinks** simplifies address configuration by automatically adjusting an address to match its corresponding network ID, treating it as a subnet rather than a host. Users don’t need to manually calculate the network ID or broadcast IP when creating a subnet object. The following example illustrates how to create an IPv4 subnet object and access its properties: `192.170.50.10/14` -> `192.168.1.0/24`. It also inherits all the properties and methods from the IPv4Host class.

```python
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig

ipv4_subnet = IPv4SubnetConfig('192.170.50.10/14')

print('Display Address Information'.center(50, '-'))
address = ipv4_subnet.addr  # IPv4Addr object. TTLinks helps to adjust the address to the network ID of given value automatically because it is a subnet instead of a host.
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
mask = ipv4_subnet.mask  # IPv4Netmask object
mask_in_bytes = mask.as_bytes  # mask in bytes format, big-endian
mask_in_binary_string = mask.binary_string  # mask in binary string format
mask_in_binary_digits = mask.binary_digits  # mask in binary digits format
mask_in_decimal = mask.decimal  # mask in decimal format
print('%-8s'%'mask:', mask)
print('%-8s'%'bytes:', mask_in_bytes)
print('%-8s'%'binary:', mask_in_binary_string)
print('%-8s'%'digits:', mask_in_binary_digits)
print('%-8s'%'decimal:', mask_in_decimal)

print('Display Subnet Information'.center(50, '-'))
ip_address = ipv4_subnet.addr.address  # Dot-decimal notation of IPv4Addr object
ip_mask = ipv4_subnet.mask.address  # Dot-decimal notation of IPv4Netmask object
ip_type = ipv4_subnet.ip_type  # Return all possible IPv4AddrType objects the subnet may lie in
network_id = ipv4_subnet.network_id  # IPv4Addr object of network ID. Use .address to get the string format
broadcast_ip = ipv4_subnet.broadcast_ip  # IPv4Addr object of broadcast IP. Use .address to get the string format
subnet_range = ipv4_subnet.subnet_range  # Return the range of the subnet. Left is the network ID, right is the broadcast IP
first_host = ipv4_subnet.first_host  # IPv4Addr object of the first host IP. Use .address to get the string format
last_host = ipv4_subnet.last_host  # IPv4Addr object of the last host IP. Use .address to get the string format
hosts = ipv4_subnet.get_hosts()  # Return a generator of all host IPs in the subnet
is_within1 = ipv4_subnet.is_within('192.168.169.50')  # Check if the given IP address is within the subnet
is_within2 = ipv4_subnet.is_within('192.172.1.1')  # Check if the given IP address is within the subnet
print('%-10s'%'subnet:', ipv4_subnet)
print('%-10s'%'address:', ip_address)
print('%-10s'%'mask:', ip_mask)
print('%-10s'%'type:', ip_type)
print('%-10s'%'NET ID:', network_id)
print('%-10s'%'broadcast:', broadcast_ip)
print('%-10s'%'range:', subnet_range)
print('%-10s'%'first:', first_host)
print('%-10s'%'last:', last_host)
print('%-10s'%'hosts:', [next(hosts) for _ in range(5)])
print('%-10s'%'is within1:', is_within1)
print('%-10s'%'is within2:', is_within2)

print('Display Subnet Operation'.center(50, '-'))  # Exclusive for subnet object
new_subnet = ipv4_subnet.division(16)  # Divide the subnet into /16 subnets.
merged_subnet = ipv4_subnet.merge('192.172.0.0/14')  # Merge the subnet with another subnet.
print('%-14s'%'new subnet:', list(new_subnet))
print('%-14s'%'merged subnet:', merged_subnet)
```
Example output:
```
-----------Display Address Information------------
address: 192.168.0.0
bytes:   b'\xc0\xa8\x00\x00'
binary:  11000000101010000000000000000000
digits:  [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
decimal: 3232235520
-------------Display Mask Information-------------
mask:    255.252.0.0
bytes:   b'\xff\xfc\x00\x00'
binary:  11111111111111000000000000000000
digits:  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
decimal: 4294705152
------------Display Subnet Information------------
subnet:    192.168.0.0/14
address:   192.168.0.0
mask:      255.252.0.0
type:      [<IPv4AddrType.PRIVATE: 4>, <IPv4AddrType.PUBLIC: 3>]
NET ID:    192.168.0.0
broadcast: 192.171.255.255
range:     [IPv4Addr('_address=192.168.0.0'), IPv4Addr('_address=192.171.255.255')]
first:     192.168.0.1
last:      192.171.255.254
hosts:     [
                IPv4Addr('_address=192.168.0.1'), 
                IPv4Addr('_address=192.168.0.2'), 
                IPv4Addr('_address=192.168.0.3'), 
                IPv4Addr('_address=192.168.0.4'), 
                IPv4Addr('_address=192.168.0.5')
            ]
is within1: True
is within2: False
-------------Display Subnet Operation-------------
new subnet:    [IPv4SubnetConfig(192.168.0.0/16), IPv4SubnetConfig(192.169.0.0/16), IPv4SubnetConfig(192.170.0.0/16), IPv4SubnetConfig(192.171.0.0/16)]
merged subnet: 192.168.0.0/13
```
</details>

<details>

<summary>(Click to Expand) Example 3: IPv4 WildCard</summary>

WildCard is a special type of subnet mask that is typically used in access control lists (ACLs) to define a range of IP addresses. **TTLinks** provides a way to calculate the address automatically based on the wildcard mask provided. The following example demonstrates how to create an IPv4 wildcard object and access its properties:

```python
from ttlinks.ipservice.ip_address import IPv4Addr
from ttlinks.ipservice.ip_configs import IPv4WildCardConfig

wildcard = IPv4WildCardConfig('10.100.65.5 0.255.1.7')

print('Display WildCard Information'.center(50, '-'))
address = wildcard.addr  # IPv4Addr object.
mask = wildcard.mask  # IPv4Wildcard object.
total_hosts = wildcard.total_hosts  # Total number of hosts covered by the wildcard mask.
hosts = [host for host in wildcard.get_hosts()]  # List of hosts covered by the wildcard mask. `.get_hosts()` returns a generator, so be careful when using it.


# WildCard address is automatically adjusted based on the wildcard mask provided. The bit in the address will be set to 0 if the corresponding bit in the wildcard mask is 1.
print('%-10s'%'wildcard:', wildcard)  
print('original:', IPv4Addr('10.100.65.5').binary_string)  # Original address in binary string format
print('%-10s'%'address:', address.binary_string)  # Adjusted address in binary string format
print('%-10s'%'mask:', mask.binary_string)  # Wildcard mask in binary string format
print('%-10s'%'total hosts:', total_hosts)  # Total number of hosts covered by the wildcard mask
print('%-10s'%'hosts:', hosts[:5], '...', hosts[-5:])  # List of hosts covered by the wildcard mask
```
Example output:
```
-----------Display WildCard Information-----------
wildcard:  10.0.64.0 0.255.1.7
original:  00001010011001000100000100000101
address:   00001010000000000100000000000000
mask:      00000000111111110000000100000111
total hosts: 4096
hosts:     [
                IPv4Addr('_address=10.0.64.0'), 
                IPv4Addr('_address=10.0.64.1'), 
                IPv4Addr('_address=10.0.64.2'), 
                IPv4Addr('_address=10.0.64.3'), 
                IPv4Addr('_address=10.0.64.4')
            ] 
            ... 
            [
                IPv4Addr('_address=10.255.65.3'), 
                IPv4Addr('_address=10.255.65.4'), 
                IPv4Addr('_address=10.255.65.5'), 
                IPv4Addr('_address=10.255.65.6'), 
                IPv4Addr('_address=10.255.65.7')
            ]
```
</details>

<details>
<summary>(Click to Expand) Example 4: IPv6Host</summary>

```python

from ttlinks.ipservice.ip_configs import IPv6HostConfig
ipv6_host = IPv6HostConfig('2003:db8:0:1234:0:567:8:1/64')

print('Display Address Information'.center(50, '-'))
address = ipv6_host.addr  # IPv6Addr object
address_in_bytes = address.as_bytes  # ipv6 address in bytes format, big-endian
address_in_binary_string = address.binary_string  # ipv6 address in binary string format
address_in_binary_digits = address.binary_digits  # ipv6 address in binary digits format
address_in_decimal = address.decimal  # ipv6 address in decimal format
print('%-8s'%'address:', address)
print('%-8s'%'bytes:', address_in_bytes)
print('%-8s'%'binary:', address_in_binary_string)
print('%-8s'%'digits:', address_in_binary_digits)
print('%-8s'%'decimal:', address_in_decimal)

print('Display Mask Information'.center(50, '-'))
mask = ipv6_host.mask  # IPv6Netmask object
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
ip_address = ipv6_host.addr.address  # Colon-hexadecimal notation of IPv6Addr object
ip_mask = ipv6_host.mask.address  # Colon-hexadecimal notation of IPv6Netmask object
ip_type = ipv6_host.ip_type  # Return IPv6AddrType object
network_id = ipv6_host.network_id  # IPv6Addr object of network ID (ipv6 prefix). Use .address to get the string format
is_global_unicast = ipv6_host.is_global_unicast  # Return True if the IP address is a global unicast address
is_link_local = ipv6_host.is_link_local  # Return True if the IP address is a link-local address
is_loopback = ipv6_host.is_loopback  # Return True if the IP address is a loopback address
# ...more attributes and methods
print('%-10s'%'host:', ipv6_host)  # IPv6Host object. Use str() to get the string format
print('%-10s'%'address:', ip_address)
print('%-10s'%'mask:', ip_mask)
print('%-10s'%'type:', ip_type)
print('%-10s'%'NET ID:', network_id)
print('%-10s'%'global unicast:', is_global_unicast)
print('%-10s'%'link local:', is_link_local)
print('%-10s'%'loopback:', is_loopback)
```
Example output:
```
-----------Display Address Information------------
address: 2003:DB8:0:1234:0:567:8:1
bytes:   b' \x03\r\xb8\x00\x00\x124\x00\x00\x05g\x00\x08\x00\x01'
binary:  00100000000000110000110110111000000000000000000000010010001101000000000000000000000001010110011100000000000010000000000000000001
digits:  [
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 
            0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
          ]
decimal: 42551151004999748473988435370763091969
-------------Display Mask Information-------------
mask:    FFFF:FFFF:FFFF:FFFF::
bytes:   b'\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'
binary:  11111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000
digits:  [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
          ]
decimal: 340282366920938463444927863358058659840
-------------Display Host Information-------------
host:      2003:DB8:0:1234:0:567:8:1/64
address:   2003:DB8:0:1234:0:567:8:1
mask:      FFFF:FFFF:FFFF:FFFF::
type:      IPv6AddrType.GLOBAL_UNICAST
NET ID:    2003:DB8:0:1234::
global unicast: True
link local: False
loopback:  False
```
</details>

<details>
<summary>(Click to Expand) Example 5: IPv6 Subnet</summary>
Network ID (IPv6 Prefix) is automatically adjusted based on the subnet mask provided. The bit in the address will be set to 0 if the corresponding bit in the subnet mask is 1. The following example demonstrates how to create an IPv6 subnet object and access its properties:

```python
from ttlinks.ipservice.ip_configs import IPv6SubnetConfig

ipv6_subnet = IPv6SubnetConfig('2003:db8:0:1234:0:567:8:1/64')

print('Display Address Information'.center(50, '-'))
address = ipv6_subnet.addr  # IPv6Addr object. TTLinks helps to adjust the address to the network ID of given value automatically because it is a subnet instead of a host.
address_in_bytes = address.as_bytes  # ipv6 address in bytes format, big-endian
address_in_binary_string = address.binary_string  # ipv6 address in binary string format
address_in_binary_digits = address.binary_digits  # ipv6 address in binary digits format
address_in_decimal = address.decimal  # ipv6 address in decimal format
print('%-8s'%'address:', address)
print('%-8s'%'bytes:', address_in_bytes)
print('%-8s'%'binary:', address_in_binary_string)
print('%-8s'%'digits:', address_in_binary_digits)
print('%-8s'%'decimal:', address_in_decimal)

print('Display Mask Information'.center(50, '-'))
mask = ipv6_subnet.mask  # IPv6Netmask object
mask_in_bytes = mask.as_bytes  # mask in bytes format, big-endian
mask_in_binary_string = mask.binary_string  # mask in binary string format
mask_in_binary_digits = mask.binary_digits  # mask in binary digits format
mask_in_decimal = mask.decimal  # mask in decimal format
print('%-8s'%'mask:', mask)
print('%-8s'%'bytes:', mask_in_bytes)
print('%-8s'%'binary:', mask_in_binary_string)
print('%-8s'%'digits:', mask_in_binary_digits)
print('%-8s'%'decimal:', mask_in_decimal)

print('Display Subnet Information'.center(50, '-'))
ip_address = ipv6_subnet.addr.address  # Colon-hexadecimal notation of IPv6Addr object
ip_mask = ipv6_subnet.mask.address  # Colon-hexadecimal notation of IPv6Netmask object
ip_type = ipv6_subnet.ip_type  # Return all possible IPv6AddrType objects the subnet may lie in
network_id = ipv6_subnet.network_id  # IPv6Addr object of network ID (IPv6 Prefix). Use .address to get the string format
subnet_range = ipv6_subnet.subnet_range  # Return the range of the subnet. Left is the network ID, right is the broadcast IP
first_host = ipv6_subnet.first_host  # IPv6Addr object of the first host IP. Use .address to get the string format
last_host = ipv6_subnet.last_host  # IPv6Addr object of the last host IP. Use .address to get the string format
hosts = ipv6_subnet.get_hosts()  # Return a generator of all host IPs in the subnet
is_within1 = ipv6_subnet.is_within('2003:DB8:0:1234::ff:1a')  # Check if the given IP address is within the subnet
is_within2 = ipv6_subnet.is_within('2003:DB8:0:1235::ff:1a')  # Check if the given IP address is within the subnet
print('%-10s'%'subnet:', ipv6_subnet)
print('%-10s'%'address:', ip_address)
print('%-10s'%'mask:', ip_mask)
print('%-10s'%'type:', ip_type)
print('%-10s'%'NET ID:', network_id)
print('%-10s'%'range:', subnet_range)
print('%-10s'%'first:', first_host)
print('%-10s'%'last:', last_host)
print('%-10s'%'hosts:', [next(hosts) for _ in range(5)])
print('%-10s'%'is within1:', is_within1)
print('%-10s'%'is within2:', is_within2)

print('Display Subnet Operation'.center(50, '-'))  # Exclusive for subnet object
new_subnet = ipv6_subnet.division(67)  # Divide the subnet into /67 subnets.
merged_subnet = ipv6_subnet.merge('2003:DB8:0:1235::/64')  # Merge the subnet with another subnet.
print('%-14s'%'new subnet:', list(new_subnet))
print('%-14s'%'merged subnet:', merged_subnet)
```
Example output:
```
-----------Display Address Information------------
address: 2003:DB8:0:1234::
bytes:   b' \x03\r\xb8\x00\x00\x124\x00\x00\x00\x00\x00\x00\x00\x00'
binary:  00100000000000110000110110111000000000000000000000010010001101000000000000000000000000000000000000000000000000000000000000000000
digits:  [
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 
            0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
decimal: 42551151004999748473988429430822797312
-------------Display Mask Information-------------
mask:    FFFF:FFFF:FFFF:FFFF::
bytes:   b'\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'
binary:  11111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000
digits:  [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
decimal: 340282366920938463444927863358058659840
------------Display Subnet Information------------
subnet:    2003:DB8:0:1234::/64
address:   2003:DB8:0:1234::
mask:      FFFF:FFFF:FFFF:FFFF::
type:      [<IPv6AddrType.GLOBAL_UNICAST: 3>]
NET ID:    2003:DB8:0:1234::
range:     [
                IPv6Addr('_address=2003:DB8:0:1234::'), 
                IPv6Addr('_address=2003:DB8:0:1234:FFFF:FFFF:FFFF:FFFF')
            ]
first:     2003:DB8:0:1234::
last:      2003:DB8:0:1234:FFFF:FFFF:FFFF:FFFF
hosts:     [
                IPv6Addr('_address=2003:DB8:0:1234::'), 
                IPv6Addr('_address=2003:DB8:0:1234::1'), 
                IPv6Addr('_address=2003:DB8:0:1234::2'), 
                IPv6Addr('_address=2003:DB8:0:1234::3'), 
                IPv6Addr('_address=2003:DB8:0:1234::4')
            ]
is within1: True
is within2: False
-------------Display Subnet Operation-------------
new subnet:    [
                    IPv6SubnetConfig(2003:DB8:0:1234::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:2000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:4000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:6000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:8000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:A000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:C000::/67), 
                    IPv6SubnetConfig(2003:DB8:0:1234:E000::/67)
                ]
merged subnet: 2003:DB8:0:1234::/63
```
</details>

<details>

<summary>(Click to Expand) Example 6: IPv6 WildCard</summary>

WildCard is a special type of subnet mask that is typically used in access control lists (ACLs) to define a range of IP addresses. **TTLinks** provides a way to calculate the address automatically based on the wildcard mask provided. The following example demonstrates how to create an IPv6 wildcard object and access its properties:

```python
from ttlinks.ipservice.ip_address import IPv6Addr
from ttlinks.ipservice.ip_configs import IPv6WildCardConfig

wildcard = IPv6WildCardConfig('2001:db8:ffff:1234::abcd ::ff')

print('Display WildCard Information'.center(50, '-'))
address = wildcard.addr  # IPv6Addr object.
mask = wildcard.mask  # IPv6Wildcard object.
total_hosts = wildcard.total_hosts  # Total number of hosts covered by the wildcard mask.
hosts = [host for host in wildcard.get_hosts()]  # List of hosts covered by the wildcard mask. `.get_hosts()` returns a generator, so be careful when using it.


# WildCard address is automatically adjusted based on the wildcard mask provided. The bit in the address will be set to 0 if the corresponding bit in the wildcard mask is 1.
print('%-10s'%'wildcard:', wildcard)
print('%-10s'%'original:', IPv6Addr('2001:db8:ffff:1234::abcd').binary_string)  # Original address in binary string format
print('%-10s'%'address:', address.binary_string)  # Adjusted address in binary string format
print('%-10s'%'mask:', mask.binary_string)  # Wildcard mask in binary string format
print('%-10s'%'total hosts:', total_hosts)  # Total number of hosts covered by the wildcard mask
print('%-10s'%'hosts:', hosts[:5], '...', hosts[-5:])  # List of hosts covered by the wildcard mask
```
Example output:
```
-----------Display WildCard Information-----------
wildcard:  2001:DB8:FFFF:1234::AB00 ::FF
original:  00100000000000010000110110111000111111111111111100010010001101000000000000000000000000000000000000000000000000001010101111001101
address:   00100000000000010000110110111000111111111111111100010010001101000000000000000000000000000000000000000000000000001010101100000000
mask:      00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111
total hosts: 256
hosts:     [
                IPv6Addr('_address=2001:DB8:FFFF:1234::AB00'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::AB01'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::AB02'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::AB03'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::AB04')
            ] 
                ... 
            [
                IPv6Addr('_address=2001:DB8:FFFF:1234::ABFB'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::ABFC'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::ABFD'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::ABFE'), 
                IPv6Addr('_address=2001:DB8:FFFF:1234::ABFF')
            ]
```
</details>