# `IPFactory` Module Documentation

## Overview

The `IPFactory` module provides a flexible and extensible framework for generating and managing IP configurations, including host addresses, subnets, and wildcard addresses. This module supports both IPv4 and IPv6 configurations and includes abstractions for handling various IP address types and ranges. With the ability to generate random IPs, batch process IP configurations, and perform subnet operations, this module is essential for network management and simulation tasks.

## Features

- **Abstract Base Class for IP Generation**: The `IPFactory` class defines an abstract interface for generating host, subnet, and wildcard configurations. Concrete implementations like `IPv4Factory` and `IPv6Factory` extend this class to handle specific IP versions.

- **Batch Processing**: The module supports generating multiple host or subnet configurations in parallel, leveraging multi-threading and multi-processing for enhanced performance.

- **Random IP and Subnet Generation**: Generate random IPv4 or IPv6 hosts and subnets based on various IP address blocks, such as public, private, or multicast ranges.

- **IP Address Types**: Enum-based classification of IP address types, including public, private, multicast, loopback, and more, for both IPv4 and IPv6.

- **Caching for Performance**: Subnet configurations are cached to reduce redundant calculations and improve efficiency when generating multiple IP configurations.

---


## Class: `IPFactory` (Interface)

#### Description

The `IPFactory` class is an abstract base class (ABC) that defines a framework for generating and managing IP configurations. This includes generating host IP addresses, subnet configurations, and wildcard configurations. The class provides a flexible interface for handling both IPv4 and IPv6 addresses. Subclasses like `IPv4Factory` and `IPv6Factory` extend `IPFactory` to provide concrete implementations for IPv4 and IPv6 address management.

The class also supports batch processing of IP configurations (hosts and subnets) using parallelization techniques such as multi-threading and multi-processing to improve performance, especially when generating large numbers of IP configurations.

#### Attributes

- **_subnet_cache (dict)**:  
  A cache used to store pre-generated subnet configurations, allowing for reuse and preventing redundant calculations.

#### Methods

- **`__init__(self)`**:  
  Initializes the `IPFactory` object and sets up the subnet cache for improved performance by reusing existing configurations.
  
- **`abstractmethod host(self, host: str) -> InterfaceIPConfig`**:  
  Abstract method for generating a host IP configuration.
  - **Parameters**:
    - `host (str)`: The string representation of the host IP.
  - **Returns**:
    - `InterfaceIPConfig`: The configuration object representing the host IP.

- **`abstractmethod subnet(self, subnet: str) -> InterfaceIPConfig`**:  
  Abstract method for generating a subnet configuration.
  - **Parameters**:
    - `subnet (str)`: The string representation of the subnet.
  - **Returns**:
    - `InterfaceIPConfig`: The configuration object representing the subnet.

- **`abstractmethod wildcard(self, wildcard: str) -> InterfaceIPConfig`**:  
  Abstract method for generating a wildcard configuration.
  - **Parameters**:
    - `wildcard (str)`: The string representation of the wildcard.
  - **Returns**:
    - `InterfaceIPConfig`: The configuration object representing the wildcard.

- **`abstractmethod batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup=True) -> List[InterfaceIPConfig]`**:  
  Abstract method for generating a batch of host IP configurations in parallel.
  - **Parameters**:
    - `hosts (List[str])`: A list of host IP strings.
    - `max_workers (int)`: Maximum number of workers for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate host IPs.
  - **Returns**:
    - `List[InterfaceIPConfig]`: A list of configuration objects representing the host IPs.

- **`abstractmethod batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup=True) -> List[InterfaceIPConfig]`**:  
  Abstract method for generating a batch of subnet configurations in parallel.
  - **Parameters**:
    - `subnets (List[str])`: A list of subnet strings.
    - `max_workers (int)`: Maximum number of workers for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate subnet IPs.
  - **Returns**:
    - `List[InterfaceIPConfig]`: A list of configuration objects representing the subnets.

- **`abstractmethod random_host(self, addr_type=None) -> InterfaceIPConfig`**:  
  Abstract method for generating a random host IP configuration.
  - **Parameters**:
    - `addr_type (Any)`: The type of address block for generating the random host IP.
  - **Returns**:
    - `InterfaceIPConfig`: A configuration object representing the random host IP.

- **`abstractmethod random_subnet(self, addr_type=None) -> InterfaceIPConfig`**:  
  Abstract method for generating a random subnet configuration.
  - **Parameters**:
    - `addr_type (Any)`: The type of address block for generating the random subnet.
  - **Returns**:
    - `InterfaceIPConfig`: A configuration object representing the random subnet.

- **`abstractmethod random_hosts_batch(self, addr_type=None, num_ips=10) -> List[InterfaceIPConfig]`**:  
  Abstract method for generating a batch of random host IP configurations in parallel using multi-processing.
  - **Parameters**:
    - `addr_type (Any)`: The type of address block for generating the random host IPs.
    - `num_ips (int)`: Number of random host IPs to generate.
  - **Returns**:
    - `List[InterfaceIPConfig]`: A list of configuration objects representing the random host IPs.

- **`abstractmethod random_subnets_batch(self, addr_type=None, num_ips=10) -> List[InterfaceIPConfig]`**:  
  Abstract method for generating a batch of random subnet configurations in parallel using multi-processing.
  - **Parameters**:
    - `addr_type (Any)`: The type of address block for generating the random subnets.
    - `num_ips (int)`: Number of random subnets to generate.
  - **Returns**:
    - `List[InterfaceIPConfig]`: A list of configuration objects representing the random subnets.

- **`abstractmethod _random_subnet_for_type(self, addr_type) -> InterfaceIPConfig`**:  
  Abstract method for generating a random subnet configuration for a given address type. This method utilizes caching for performance by storing subnet configurations for reuse.
  - **Parameters**:
    - `addr_type (Any)`: The type of address block for generating the random subnet.
  - **Returns**:
    - `InterfaceIPConfig`: A configuration object representing the random subnet for the given address type.

Here’s the documentation for the `IPv4Factory` and `IPv6Factory` classes:

---

## Class: `IPv4Factory`

#### Description

The `IPv4Factory` class is a concrete implementation of the `IPFactory` abstract base class, designed specifically for handling IPv4 addresses. It provides methods for generating and managing IPv4 host, subnet, and wildcard configurations. The class also supports batch processing of IPv4 configurations, parallelized using multi-threading or multi-processing, as well as generating random IPv4 addresses from specific address blocks such as public or private IP ranges.

#### Inherits: `IPFactory`

#### Methods

- **`host(self, host: str) -> IPv4HostConfig`**:  
  Generates an IPv4 host configuration.
  - **Parameters**:
    - `host (str)`: The string representation of the host IP.
  - **Returns**:
    - `IPv4HostConfig`: The configuration object representing the host IP.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4 = ipv4_factory.host("192.168.1.1/30")
print(ipv4)
print(ipv4.mask)
print(ipv4.ip_type)
print(ipv4.network_id)
print(ipv4.broadcast_ip)
```
Example Output:
```
192.168.1.1/30
255.255.255.252
IPv4AddrType.PRIVATE
192.168.1.0
192.168.1.3
```

- **`subnet(self, subnet: str) -> IPv4SubnetConfig`**:  
  Generates an IPv4 subnet configuration. If a host IP is provided, it will be converted to a subnet configuration.
  - **Parameters**:
    - `subnet (str)`: The string representation of the subnet.
  - **Returns**:
    - `IPv4SubnetConfig`: The configuration object representing the subnet.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4 = ipv4_factory.subnet("192.168.1.213/25")
print(ipv4)
print(ipv4.mask)
print(ipv4.ip_type)
print(ipv4.network_id)
print(ipv4.broadcast_ip)
print(ipv4.subnet_range)
print(ipv4.first_host)
print(ipv4.last_host)
```
Example Output:
```
192.168.1.128/25
255.255.255.128
IPv4AddrType.PRIVATE
192.168.1.128
192.168.1.255
192.168.1.128-192.168.1.255
192.168.1.129
192.168.1.254
```

- **`wildcard(self, wildcard: str) -> IPv4WildCardConfig`**:  
  Generates an IPv4 wildcard configuration. This method will convert any bits of the IP address to 0 where the corresponding bits in the wildcard mask are 1, as those bits are not relevant.
  - **Parameters**:
    - `wildcard (str)`: The string representation of the wildcard IP.
  - **Returns**:
    - `IPv4WildCardConfig`: The configuration object representing the wildcard IP.
```python
from ttlinks.ipservice.ip_factory import IPv4Factory
import random

ipv4_factory = IPv4Factory()
ipv4 = ipv4_factory.wildcard("10.15.80.25 0.255.0.255")
print(ipv4)
print(ipv4.mask)
hosts = list(ipv4.get_hosts())  # use list() carefully. The generator can be very large.
random_ipv4s = random.choices(hosts, k=2)
for ip in random_ipv4s:
    print(ip)
print(ipv4.is_within("10.80.80.2"))
print(ipv4.is_within("10.80.81.2"))
```
Example Output:
```
10.0.80.0 0.255.0.255
0.255.0.255
10.243.80.70
10.154.80.104
True
False
```

- **`batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv4HostConfig]`**:  
  Generates a batch of IPv4 host configurations using multi-threading.
  - **Parameters**:
    - `hosts (List[str])`: A list of host IP strings.
    - `max_workers (int)`: Maximum number of threads to use for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate host IPs.
  - **Returns**:
    - `List[IPv4HostConfig]`: A list of configuration objects representing the host IPs.
```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4s = ipv4_factory.batch_hosts(["192.168.1.213/25", "192.168.100.10/24"])
for ipv4 in ipv4s:
    print(ipv4)
```
Example Output:
```
192.168.1.213/25
192.168.100.10/24
```

- **`batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv4SubnetConfig]`**:  
  Generates a batch of IPv4 subnet configurations using multi-threading.
  - **Parameters**:
    - `subnets (List[str])`: A list of subnet IP strings.
    - `max_workers (int)`: Maximum number of threads to use for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate subnet IPs.
  - **Returns**:
    - `List[IPv4SubnetConfig]`: A list of configuration objects representing the subnets.
```python
from ttlinks.ipservice.ip_factory import IPv4Factory

ipv4_factory = IPv4Factory()
ipv4s = ipv4_factory.batch_subnets(["192.168.1.213/25", "192.168.100.10/24"])
for ipv4 in ipv4s:
    print(ipv4)
```
Example Output:
```
192.168.1.128/25
192.168.100.0/24
```

- **`random_host(self, addr_type: IPv4TypeAddrBlocks = None) -> IPv4HostConfig`**:  
  Generates a random IPv4 host configuration based on the specified address type (e.g., public, private).
  - **Parameters**:
    - `addr_type (IPv4TypeAddrBlocks)`: The type of address block for generating the random host IP. If not specified, the host will be randomly generated from all IPv4 ranges.
  - **Returns**:
    - `IPv4HostConfig`: A randomly generated IPv4 host configuration.
```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_factory import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4 = ipv4_factory.random_host()
print(ipv4)

ipv4_private = ipv4_factory.random_host(IPv4TypeAddrBlocks.PRIVATE)
print(ipv4_private)
```
Example Output:
```
230.63.179.95/19
10.58.156.224/15
```

- **`random_subnet(self, addr_type: IPv4TypeAddrBlocks = None) -> IPv4SubnetConfig`**:  
  Generates a random IPv4 subnet configuration based on the specified address type.
  - **Parameters**:
    - `addr_type (IPv4TypeAddrBlocks)`: The type of address block for generating the random subnet. If not specified, the subnet will be randomly generated from all IPv4 ranges.
  - **Returns**:
    - `IPv4SubnetConfig`: A randomly generated IPv4 subnet configuration.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_factory import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4 = ipv4_factory.random_subnet()
print(ipv4)

ipv4_private = ipv4_factory.random_subnet(IPv4TypeAddrBlocks.MULTICAST)
print(ipv4_private)
```
Example Output:
```
40.0.0.0/5
239.135.232.0/21
```

- **`random_hosts_batch(self, addr_type: IPv4TypeAddrBlocks = None, num_ips: int = 10) -> List[IPv4HostConfig]`**:  
  Generates a batch of random IPv4 host configurations using multi-processing.
  - **Parameters**:
    - `addr_type (IPv4TypeAddrBlocks)`: The type of address block for generating the random hosts. If not specified, hosts will be randomly generated from all IPv4 ranges.
    - `num_ips (int)`: The number of random IPs to generate in the batch. Default is 10.
  - **Returns**:
    - `List[IPv4HostConfig]`: A list of randomly generated host configurations.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_factory import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4s = ipv4_factory.random_hosts_batch(num_ips=5)
for ipv4 in ipv4s:
    print(ipv4)
print('-' * 50)
ipv4s_private = ipv4_factory.random_hosts_batch(IPv4TypeAddrBlocks.PRIVATE, num_ips=5)
for ipv4_private in ipv4s_private:
    print(ipv4_private)
```
Example Output:
```
14.143.130.237/14
192.243.229.109/10
94.247.197.13/31
103.81.166.163/10
220.79.122.80/23
--------------------------------------------------
192.168.122.196/25
172.18.188.124/26
10.47.151.42/26
192.168.243.166/20
192.168.89.0/19
```

- **`random_subnets_batch(self, addr_type: IPv4TypeAddrBlocks = None, num_ips: int = 10) -> List[IPv4SubnetConfig]`**:  
  Generates a batch of random IPv4 subnet configurations using multi-processing.
  - **Parameters**:
    - `addr_type (IPv4TypeAddrBlocks)`: The type of address block for generating the random subnets. If not specified, subnets will be randomly generated from all IPv4 ranges.
    - `num_ips (int)`: The number of random subnets to generate in the batch. Default is 10.
  - **Returns**:
    - `List[IPv4SubnetConfig]`: A list of randomly generated subnet configurations.

```python
from ttlinks.ipservice.ip_factory import IPv4Factory
from ttlinks.ipservice.ip_factory import IPv4TypeAddrBlocks

ipv4_factory = IPv4Factory()
ipv4s = ipv4_factory.random_subnets_batch(num_ips=5)
for ipv4 in ipv4s:
    print(ipv4)
print('-' * 50)
ipv4s_private = ipv4_factory.random_subnets_batch(IPv4TypeAddrBlocks.LOOPBACK, num_ips=5)
for ipv4_private in ipv4s_private:
    print(ipv4_private)
```
Example Output:
```
0.0.0.0/1
244.199.228.0/22
133.18.0.0/15
101.88.148.0/23
51.226.64.0/18
--------------------------------------------------
127.251.45.216/30
127.96.0.0/11
127.176.88.0/21
127.30.0.0/15
127.0.0.0/8
```

- **`_random_subnet_for_type(self, addr_type: IPv4TypeAddrBlocks) -> IPv4SubnetConfig`**:  
  Generates a random subnet configuration for a given address type, utilizing a cache for improved performance. This method is a private helper function used by the `random_subnet` and `random_host` method.
  - **Parameters**:
    - `addr_type (IPv4TypeAddrBlocks)`: The type of address block for generating the random subnet.
  - **Returns**:
    - `IPv4SubnetConfig`: A random subnet configuration for the given address type.

---

## Class: `IPv6Factory`

#### Description

The `IPv6Factory` class is a concrete implementation of the `IPFactory` abstract base class, designed specifically for handling IPv6 addresses. It provides methods for generating and managing IPv6 host, subnet, and wildcard configurations. The class also supports batch processing of IPv6 configurations and random IPv6 address generation from specific address types, such as link-local, global unicast, or multicast.

#### Inherits: `IPFactory`

#### Methods

- **`host(self, host: str) -> IPv6HostConfig`**:  
  Generates an IPv6 host configuration.
  - **Parameters**:
    - `host (str)`: The string representation of the host IPv6 address.
  - **Returns**:
    - `IPv6HostConfig`: The configuration object representing the host IPv6 address.
```python
from ttlinks.ipservice.ip_factory import IPv6Factory

ipv6_factory = IPv6Factory()
ipv6 = ipv6_factory.host("fe80::1/64")
print(ipv6)
print(ipv6.mask)
print(ipv6.ip_type)
print(ipv6.network_id)
```
Example Output:
```
fe80::1/64
ffff:ffff:ffff:ffff::
IPv6AddrType.LINK_LOCAL
fe80::
```

- **`subnet(self, subnet: str) -> IPv6SubnetConfig`**:  
  Generates an IPv6 subnet configuration. If a host IP is provided, it will be converted to a subnet configuration.
  - **Parameters**:
    - `subnet (str)`: The string representation of the IPv6 subnet.
  - **Returns**:
    - `IPv6SubnetConfig`: The configuration object representing the IPv6 subnet.
```python
from ttlinks.ipservice.ip_factory import IPv6Factory

ipv6_factory = IPv6Factory()
ipv6 = ipv6_factory.subnet("fe80::1/64")
print(ipv6)
print(ipv6.mask)
print(ipv6.ip_type)
print(ipv6.network_id)
print(ipv6.subnet_range)
print(ipv6.first_host)
print(ipv6.last_host)
```
Example Output:
```
fe80::/64
ffff:ffff:ffff:ffff::
IPv6AddrType.LINK_LOCAL
fe80::
fe80:: - fe80::ffff:ffff:ffff:ffff
fe80::
fe80::ffff:ffff:ffff:ffff
```

- **`wildcard(self, wildcard: str) -> IPv6WildCardConfig`**:  
  Generates an IPv6 wildcard configuration.
  - **Parameters**:
    - `wildcard (str)`: The string representation of the wildcard IPv6 address. This method will convert any bits of the IP address to 0 where the corresponding bits in the wildcard mask are 1, as those bits are not relevant.
  - **Returns**:
    - `IPv6WildCardConfig`: The configuration object representing the wildcard IPv6 address.

```python
from ttlinks.ipservice.ip_factory import IPv6Factory
import random

ipv6_factory = IPv6Factory()
ipv6 = ipv6_factory.wildcard("fe80::1 ::ff:0")
print(ipv6)
print(ipv6.mask)
hosts = list(ipv6.get_hosts())  # use list() carefully. The generator can be very large.
random_ipv6s = random.choices(hosts, k=2)
for ip in random_ipv6s:
    print(ip)
print(len(hosts))
```
Example Output:
```
fe80::1 ::ff:0
::ff:0
fe80::f3:1
fe80::4f:1
256
```

- **`batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6HostConfig]`**:  
  Generates a batch of IPv6 host configurations using multi-threading.
  - **Parameters**:
    - `hosts (List[str])`: A list of IPv6 host strings.
    - `max_workers (int)`: Maximum number of threads to use for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate IPv6 host addresses.
  - **Returns**:
    - `List[IPv6HostConfig]`: A list of configuration objects representing the IPv6 hosts.
```python
from ttlinks.ipservice.ip_factory import IPv6Factory

ipv6_factory = IPv6Factory()
ipv6s = ipv6_factory.batch_hosts(["fe80::1/64", "2001:db8::1/96"])
for ipv6 in ipv6s:
    print(ipv6)
```
Example Output:
```
fe80::1/64
2001:db8::1/96
```

- **`batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6SubnetConfig]`**:  
  Generates a batch of IPv6 subnet configurations using multi-threading.
  - **Parameters**:
    - `subnets (List[str])`: A list of IPv6 subnet strings.
    - `max_workers (int)`: Maximum number of threads to use for parallel processing.
    - `keep_dup (bool)`: Whether to keep duplicate IPv6 subnets.
  - **Returns**:
    - `List[IPv6SubnetConfig]`: A list of configuration objects representing the IPv6 subnets.

```python
from ttlinks.ipservice.ip_factory import IPv6Factory

ipv6_factory = IPv6Factory()
ipv6s = ipv6_factory.batch_subnets(["fe80::1/64", "2001:db8::1/96"])
for ipv6 in ipv6s:
    print(ipv6)
```
Example Output:
```
fe80::/64
2001:db8::/96
```

- **`random_host(self, addr_type: IPv6TypeAddrBlocks = None) -> IPv6HostConfig`**:  
  Generates a random IPv6 host configuration based on the specified address type.
  - **Parameters**:
    - `addr_type (IPv6TypeAddrBlocks)`: The address block type to use for generating the random IPv6 host. If not specified, the host will be randomly generated from all IPv6 ranges.
  - **Returns**:
    - `IPv6HostConfig`: A randomly generated IPv6 host configuration.
```python
from ttlinks.ipservice.ip_factory import IPv6Factory
from ttlinks.ipservice.ip_factory import IPv6TypeAddrBlocks

ipv6_factory = IPv6Factory()
ipv6 = ipv6_factory.random_host()
print(ipv6)

ipv6_global_unicast = ipv6_factory.random_host(IPv6TypeAddrBlocks.GLOBAL_UNICAST)
print(ipv6_global_unicast)
```
Example Output:
```
21ba:44a5:e9b:2f1b:965b:ce41:8fc1:dec3/74
35d5:76fd:f630:fb16:df1a:f33f:90cf:9385/67
```

- **`random_subnet(self, addr_type: IPv6TypeAddrBlocks = None) -> IPv6SubnetConfig`**:  
  Generates a random IPv6 subnet configuration based on the specified address type.
  - **Parameters**:
    - `addr_type (IPv6TypeAddrBlocks)`: The address block type to use for generating the random IPv6 subnet. If not specified, the subnet will be randomly generated from all IPv6 ranges.
  - **Returns**:
    - `IPv6SubnetConfig`: A randomly generated IPv6 subnet configuration.

```python
from ttlinks.ipservice.ip_factory import IPv6Factory
from ttlinks.ipservice.ip_factory import IPv6TypeAddrBlocks

ipv6_factory = IPv6Factory()
ipv6 = ipv6_factory.random_subnet()
print(ipv6)

ipv6_loopback = ipv6_factory.random_subnet(IPv6TypeAddrBlocks.LINK_LOCAL)
print(ipv6_loopback)
```
Example Output:
```
ab9:c0c8:3180::/41
fe80::f6f0:76a2:8000:0/98
```

- **`random_hosts_batch(self, addr_type: IPv6TypeAddrBlocks = None, num_ips: int = 10) -> List[IPv6HostConfig]`**:  
  Generates a batch of random IPv6 host configurations using multi-processing.
  - **Parameters**:
    - `addr_type (IPv6TypeAddrBlocks)`: The address block type to use for generating the random IPv6 hosts. If not specified, hosts will be randomly generated from all IPv6 ranges.
    - `num_ips (int)`: The number of random IPv6 hosts to generate in the batch.
  - **Returns**:
    - `List[IPv6HostConfig]`: A list of randomly generated IPv6 host configurations.

```python
from ttlinks.ipservice.ip_factory import IPv6Factory
from ttlinks.ipservice.ip_factory import IPv6TypeAddrBlocks

ipv6_factory = IPv6Factory()
ipv6s = ipv6_factory.random_hosts_batch(num_ips=5)
for ipv6 in ipv6s:
    print(ipv6)
print('-' * 50)
ipv6s_link_local = ipv6_factory.random_hosts_batch(IPv6TypeAddrBlocks.LINK_LOCAL, num_ips=5)
for ipv6_link_local in ipv6s_link_local:
    print(ipv6_link_local)
```
Example Output:
```
3c0c:87b6:7276:a799:76fa:fdf2:a80d:53c5/49
a4bf:fb97:25e8:78ec:90d7:478b:4bcf:6b94/87
ff22:f13d:c4d6:e453:ac40:d322:a5c0:38f6/95
b42d:a8e:b9f3:e9ae:c363:598d:5c1f:3ba1/105
3609:47a9:bec3:44e8:3ca4:be52:e503:b0a6/5
--------------------------------------------------
fe80::f55b:c77c:ad0c:58be/103
fe80::1f1d:89b:4e6a:dd9b/68
fe80::6fe4:e395:c7de:4fdc/111
fe80::601b:8d02:fb13:5ff8/77
fe80::9e18:49f9:3b45:3d26/110
```


- **`random_subnets_batch(self, addr_type: IPv6TypeAddrBlocks = None, num_ips: int = 10) -> List[IPv6SubnetConfig]`**:  
  Generates a batch of random IPv6 subnet configurations using multi-processing.
  - **Parameters**:
    - `addr_type (IPv6TypeAddrBlocks)`: The address block type to use for generating the random IPv6 subnets. If not specified, subnets will be randomly generated from all IPv6 ranges.
    - `num_ips (int)`: The number of random IPv6 subnets to generate in the batch.
  - **Returns**:
    - `List[IPv6SubnetConfig]`: A list of randomly generated IPv6 subnet configurations.
```python
from ttlinks.ipservice.ip_factory import IPv6Factory
from ttlinks.ipservice.ip_factory import IPv6TypeAddrBlocks

ipv6_factory = IPv6Factory()
ipv6s = ipv6_factory.random_subnets_batch(num_ips=5)
for ipv6 in ipv6s:
    print(ipv6)
print('-' * 50)
ipv6s_link_local = ipv6_factory.random_subnets_batch(IPv6TypeAddrBlocks.LINK_LOCAL, num_ips=5)
for ipv6_link_local in ipv6s_link_local:
    print(ipv6_link_local)
```
Example Output:
```
2aaf:cf36:27f3:2fcd:5010:3000::/86
637c:d7a0::/32
a7ef:d3f2:2c1b:a060::/60
66f4:6000::/21
9e6a:ca3e:e136:faeb:179d:300::/88
--------------------------------------------------
fe80::e438:c045:5400:0/102
fe80::2b0d:5e1:e7e8:0/109
fe80::a000:0:0:0/67
fe80::f22d:c6bf:4c1c:8000/113
fe80::ea51:cef5:7e00:0/103
```

- **`_random_subnet_for_type(self, addr_type: IPv6TypeAddrBlocks) -> IPv6SubnetConfig`**:  
  Generates a random subnet configuration for a given address type, utilizing a cache for improved performance.
  - **Parameters**:
    - `addr_type (IPv6TypeAddrBlocks)`: The address block type to use for generating the random IPv6 subnet.
  - **Returns**:
    - `IPv6SubnetConfig`: A random subnet configuration for the given address type.

---
## Dependencies

The `IPFactory` module relies on the following internal and external dependencies:

- **`concurrent.futures`**: Used for multi-threading and multi-processing to handle parallel IP configuration generation.
  
- **`random`**: Used to generate random IP addresses and subnets.

- **`abc`**: Provides the `ABC` class for defining abstract base classes.

- **`enum`**: Used for defining enumerations of IP address types.

- **`ttlinks.ipservice`**: Several classes and handlers are imported from the `ttlinks.ipservice` package, such as:
  - `IPv4Addr`, `IPv4NetMask`, `IPv6Addr`, `IPv6NetMask`
  - `IPv4HostConfig`, `IPv4SubnetConfig`, `IPv4WildCardConfig`, `IPv6HostConfig`, `IPv6SubnetConfig`, `IPv6WildCardConfig`
  - `IPv4AddrClassifierPublicHandler` for classifying public IPv4 addresses.
  - `DecimalIPv4ConverterHandler`, `DecimalIPv6ConverterHandler` for handling decimal to binary conversions of IPs.
  - `IPv4AddrType` for defining types of IPv4 addresses.
