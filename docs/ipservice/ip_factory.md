# `ip_factory` Module

Contains IPv4Factory and IPv6Factory classes that create IPv4Address and IPv6Address objects, respectively. In this document, we only use the IPv4Factory class as an example. The IPv6Factory class works similarly.


<details>
<summary>(Click to Expand) Example 1: Create IPv4 Host</summary>

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
ipv4_factory = IPv4Factory()
ipv4_host = ipv4_factory.host('192.168.1.10/24')

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
<summary>(Click to Expand) Example 2: Create IPv4 Subnet</summary>

Under `.subnet` method, **TTLinks** simplifies address configuration by automatically adjusting an address to match its corresponding network ID, treating it as a subnet rather than a host. Users don’t need to manually calculate the network ID or broadcast IP when creating a subnet object. The following example illustrates how to create an IPv4 subnet object and access its properties: `192.170.50.10/14` -> `192.168.1.0/24`. It also inherits all the properties and methods from the IPv4Host class.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
ipv4_factory = IPv4Factory()
ipv4_subnet = ipv4_factory.subnet('192.170.50.10/14')

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

<summary>(Click to Expand) Example 3: Create IPv4 WildCard</summary>

WildCard is a special type of subnet mask that is typically used in access control lists (ACLs) to define a range of IP addresses. **TTLinks** provides a way to calculate the address automatically based on the wildcard mask provided. The following example demonstrates how to create an IPv4 wildcard object and access its properties:

```python
from ttlinks.ipservice.ip_address import IPv4Addr
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
wildcard = ipv4_factory.wildcard('10.100.65.5 0.255.1.7')

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
<summary>(Click to Expand) Example 4: Create Batch IPv4 Hosts</summary>

`batch_hosts` method creates a batch of IPv4 host objects. The following example demonstrates how to create a batch of IPv4 host objects and access their properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4_hosts = ipv4_factory.batch_hosts('192.168.1.10/24', '192.168.1.20/24')
print(ipv4_hosts)  # List of IPv4HostConfig objects
``` 
Example output:
```
[IPv4HostConfig(192.168.1.10/24), IPv4HostConfig(192.168.1.20/24)]
```
</details>

<details>
<summary>(Click to Expand) Example 5: Create Batch IPv4 Subnets</summary>

`batch_subnets` method creates a batch of IPv4 subnet objects. The following example demonstrates how to create a batch of IPv4 subnet objects and access their properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4_subnets = ipv4_factory.batch_subnets('192.168.1.10/24', '192.168.20.20/24')
print(ipv4_subnets)  # List of IPv4SubnetConfig objects
```
Example output:
```
[IPv4SubnetConfig(192.168.1.0/24), IPv4SubnetConfig(192.168.20.0/24)]
```
</details>

<details>
<summary>(Click to Expand) Example 6: Create Random IPv4 Host</summary>

`random_host` method creates a random IPv4 host object. `addr_type` parameter can be used to specify the type of IP address to generate. The following example demonstrates how to create a random IPv4 host object and access its properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4_host = ipv4_factory.random_host(addr_type=IPv4TypeAddrBlocks.PRIVATE)
print(ipv4_host)
```
Example output:
```
172.20.42.162/21
```
</details>

<details>
<summary>(Click to Expand) Example 7: Create Random IPv4 Hosts In Batch</summary>

`random_hosts_batch` method creates a batch of random IPv4 host objects. `addr_type` parameter can be used to specify the type of IP address to generate. The following example demonstrates how to create a batch of random IPv4 host objects and access their properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4_hosts = ipv4_factory.random_hosts_batch(IPv4TypeAddrBlocks.PUBLIC, num_ips=5)
print(ipv4_hosts)
```
Example output:
```
[
    IPv4HostConfig(215.41.10.87/19), 
    IPv4HostConfig(221.120.47.35/23), 
    IPv4HostConfig(215.104.187.253/7), 
    IPv4HostConfig(17.89.101.52/10), 
    IPv4HostConfig(130.36.1.98/2)
]
```
</details>

<details>
<summary>(Click to Expand) Example 8: Create Random IPv4 Subnet</summary>

`random_subnet` method creates a random IPv4 subnet object. `addr_type` parameter can be used to specify the type of IP address to generate. The following example demonstrates how to create a random IPv4 subnet object and access its properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4_subnet = ipv4_factory.random_subnet(IPv4TypeAddrBlocks.PRIVATE)
print(ipv4_subnet)
```
Example output:
```
192.168.49.0/24
```
</details>

<details>
<summary>(Click to Expand) Example 9: Create Random IPv4 Hosts In Batch</summary>

`random_subnets_batch` method creates a batch of random IPv4 subnet objects. `addr_type` parameter can be used to specify the type of IP address to generate. The following example demonstrates how to create a batch of random IPv4 subnet objects and access their properties:

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_utils import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4_subnets = ipv4_factory.random_subnets_batch(IPv4TypeAddrBlocks.LOOPBACK, num_ips=5)
print(ipv4_subnets)
```
Example output:
```
[
    IPv4SubnetConfig(127.246.0.0/16), 
    IPv4SubnetConfig(127.4.0.0/17), 
    IPv4SubnetConfig(127.64.0.0/14), 
    IPv4SubnetConfig(127.210.103.64/26), 
    IPv4SubnetConfig(127.162.154.168/29)
]
```
</details>

> [!NOTE]\
> The examples above demonstrate how to create IPv4 host, subnet, wildcard, and batch objects using the `IPv4Factory` class. The `IPv6Factory` class works similarly. `IPv6TypeAddrBlocks` can be used to specify the type of IPv6 address when generating random addresses.