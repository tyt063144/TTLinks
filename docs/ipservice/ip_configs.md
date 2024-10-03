
# `ip_configs.py` Module Documentation

## Overview

The `ip_configs.py` module offers a comprehensive set of classes and utilities for configuring IP addresses on network interfaces, supporting both IPv4 and IPv6 protocols. It provides abstractions for host configurations, subnet configurations, and wildcard configurations, enabling advanced network management tasks such as subnetting, wildcard masking, and IP address classification. This module facilitates operations like calculating network IDs, broadcast addresses, iterating over hosts in a subnet, and merging or dividing subnets.

## Features

- **Abstract Base Classes for IP Configurations**: Establishes a unified interface for IP configurations through abstract base classes like `InterfaceIPConfig`, `InterfaceIPv4Config`, and `InterfaceIPv6Config`, promoting consistency and extensibility.

- **IPv4 Host Configuration**: The `IPv4HostConfig` class manages IPv4 host addresses, including calculating network IDs, broadcast addresses, and classifying IP address types (e.g., public, private).

- **IPv4 Subnet Configuration**: The `IPv4SubnetConfig` class extends host configurations to support subnet-specific operations such as host iteration, subnet division, and merging.

- **IPv4 Wildcard Configuration**: The `IPv4WildCardConfig` class handles wildcard configurations for IPv4 addresses, allowing for the matching of IP address ranges using wildcard masks.

- **IPv6 Host Configuration**: Similar to its IPv4 counterpart, the `IPv6HostConfig` class manages IPv6 host addresses, providing methods for network ID calculation and IP address type classification.

- **IPv6 Subnet Configuration**: The `IPv6SubnetConfig` class extends IPv6 host configurations to support subnet operations, including iterating over hosts, subnet division, and merging.

- **IPv6 Wildcard Configuration**: The `IPv6WildCardConfig` class supports wildcard configurations for IPv6 addresses.

- **Wildcard Calculator**: The `IPWildCardCalculator` class offers static methods to compute minimal wildcard configurations that cover a given set of IPv4 or IPv6 subnets, optimizing network policies and ACLs.

---

## Class: `IPv4HostConfig`

#### Description

The `IPv4HostConfig` class represents a host configuration for an IPv4 network interface. It extends `InterfaceIPv4Config` and provides methods for calculating the network ID, broadcast address, classifying the IP address type, and determining the number of usable hosts in the network. This class is designed to manage IPv4-specific host configurations, allowing for easy access to network properties and classification of IP addresses.

#### Inherits: `InterfaceIPv4Config`

#### Attributes

- `_ip_type (IPv4AddrType)`: The type of the IPv4 address (e.g., public, private, multicast).
- `_broadcast_ip (IPv4Addr)`: The broadcast IP address for the configured network.
- `_network_id (IPv4Addr)`: The network ID calculated from the IPv4 address and netmask.

#### Methods

- **`__init__(*args)`**:
  Initializes the IPv4 host configuration by setting up the IP address and netmask, and calculating network-specific attributes.
  - **Parameters**:
    - `*args`: Variable-length argument list for the IPv4 address and netmask.

- **`_initialize(*args) -> None`**:
  Internal method that initializes the IPv4 host configuration, validates the inputs, and calculates network properties.

- **`_validate(*args) -> None`**:
  Validates the provided IPv4 address and netmask using the `IPStandardizer`.

- **`_calculate_network_id() -> None`**:
  Calculates the network ID by applying the netmask to the IP address.

- **`_calculate_broadcast_ip() -> None`**:
  Calculates the broadcast IP address for the network.

- **`_classify_ip_address_type() -> None`**:
  Classifies the IP address type (e.g., private, public) using `IPAddrTypeClassifier`.

- **`ip_addr`** (property):
  Returns the configured IPv4 address.
  - **Returns**:
    - `IPv4Addr`: The IPv4 address assigned to the interface.

- **`netmask`** (property):
  Returns the netmask associated with the IPv4 address.
  - **Returns**:
    - `IPv4NetMask`: The netmask of the IPv4 address.

- **`broadcast_ip`** (property):
  Returns the broadcast IP address.
  - **Returns**:
    - `IPv4Addr`: The broadcast IP address of the network.

- **`network_id`** (property):
  Returns the network ID of the subnet.
  - **Returns**:
    - `IPv4Addr`: The network ID calculated from the IP address and netmask.

- **`host_counts`** (property):
  Calculates and returns the number of usable host addresses in the network.
  - **Returns**:
    - `int`: The number of usable hosts in the subnet.

- **`ip_type`** (property):
  Returns the classified IP address type.
  - **Returns**:
    - `IPv4AddrType`: The type classification of the IP address.

- **`is_unspecified`** (property):
  Returns `True` if the IP address is unspecified.
  - **Returns**:
    - `bool`: `True` if the IP address is unspecified, otherwise `False`.

- **`is_public`** (property):
  Returns `True` if the IP address is public.
  - **Returns**:
    - `bool`: `True` if the IP address is public, otherwise `False`.

- **`is_private`** (property):
  Returns `True` if the IP address is private.
  - **Returns**:
    - `bool`: `True` if the IP address is private, otherwise `False`.

- **`is_multicast`** (property):
  Returns `True` if the IP address is a multicast address.
  - **Returns**:
    - `bool`: `True` if the IP address is multicast, otherwise `False`.

- **`is_link_local`** (property):
  Returns `True` if the IP address is link-local.
  - **Returns**:
    - `bool`: `True` if the IP address is link-local, otherwise `False`.

- **`is_loopback`** (property):
  Returns `True` if the IP address is a loopback address.
  - **Returns**:
    - `bool`: `True` if the IP address is loopback, otherwise `False`.

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv4HostConfig

# Create an IPv4 host configuration
ipv4_host_config = IPv4HostConfig('192.168.1.10/24')

# Access various properties
print("IP Address:", ipv4_host_config.ip_addr)          # Outputs: IP Address: 192.168.1.10
print("Netmask:", ipv4_host_config.netmask)             # Outputs: Netmask: 255.255.255.0
print("Network ID:", ipv4_host_config.network_id)       # Outputs: Network ID: 192.168.1.0
print("Broadcast IP:", ipv4_host_config.broadcast_ip)   # Outputs: Broadcast IP: 192.168.1.255
print("Host Counts:", ipv4_host_config.host_counts)     # Outputs: Host Counts: 254
print("IP Type:", ipv4_host_config.ip_type)             # Outputs: IP Type: IPv4AddrType.PRIVATE
print("Is Private:", ipv4_host_config.is_private)       # Outputs: Is Private: True
print("Is Public:", ipv4_host_config.is_public)         # Outputs: Is Public: False
```
Expected Output:
```
IP Address: 192.168.1.10
Netmask: 255.255.255.0
Network ID: 192.168.1.0
Broadcast IP: 192.168.1.255
Host Counts: 254
IP Type: IPv4AddrType.PRIVATE
Is Private: True
Is Public: False
```
---

## Class: `IPv4SubnetConfig`

#### Description

The `IPv4SubnetConfig` class represents a subnet configuration for an IPv4 network. It inherits from `IPv4HostConfig` and adds functionality for working with subnet ranges and hosts within a subnet. This includes operations such as retrieving the first and last host, iterating over all hosts, checking if an IP address is within the subnet, dividing the subnet into smaller subnets, and merging subnets.

#### Inherits: `IPv4HostConfig`

#### Attributes

- Inherits all attributes from `IPv4HostConfig`:
  - `_ip_type (IPv4AddrType)`: The type of the IPv4 address (e.g., public, private).
  - `_broadcast_ip (IPv4Addr)`: The broadcast IP address for the subnet.
  - `_network_id (IPv4Addr)`: The network ID for the subnet.

#### Methods

- **`first_host`** (property):
  Returns the first usable host address within the subnet.
  - **Returns**:
    - `IPv4Addr`: The first usable host address.

- **`last_host`** (property):
  Returns the last usable host address within the subnet.
  - **Returns**:
    - `IPv4Addr`: The last usable host address.

- **`subnet_range`** (property):
  Returns the range of the subnet, from the network ID to the broadcast address.
  - **Returns**:
    - `str`: A string representing the subnet range in the format "network_id - broadcast_ip".

- **`get_hosts() -> Generator[IPv4Addr, None, None]`**:
  Generates all usable hosts within the subnet by iterating over possible host addresses.
  - **Returns**:
    - `Generator[IPv4Addr, None, None]`: A generator yielding each host in the subnet.

- **`is_within(ip_addr: Any) -> bool`**:
  Checks whether a given IP address falls within the subnet.
  - **Parameters**:
    - `ip_addr (Any)`: The IP address to check.
  - **Returns**:
    - `bool`: `True` if the IP address is within the subnet, otherwise `False`.

- **`subnet_division(mask: int) -> List[IPv4SubnetConfig]`**:
  Divides the current subnet into smaller subnets based on a new mask size.
  - **Parameters**:
    - `mask (int)`: The new mask size for the smaller subnets.
  - **Returns**:
    - `List[IPv4SubnetConfig]`: A list of new subnet configurations.

- **`subnet_merge(*subnets: str) -> IPv4SubnetConfig`**:
  Attempts to merge multiple subnets into a larger subnet.
  - **Parameters**:
    - `*subnets (str)`: Variable-length argument list of subnet strings to merge.
  - **Returns**:
    - `IPv4SubnetConfig`: A new subnet configuration representing the merged subnet.

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig

# Create an IPv4 subnet configuration
ipv4_subnet_config = IPv4SubnetConfig('192.168.1.0/29')

# Access various properties
print("Subnet Range:", ipv4_subnet_config.subnet_range)    
print("First Host:", ipv4_subnet_config.first_host)        
print("Last Host:", ipv4_subnet_config.last_host)          
print("Host Counts:", ipv4_subnet_config.host_counts)      

# Iterate over hosts in the subnet
print("Hosts in Subnet:")
for host in ipv4_subnet_config.get_hosts():
    print(host)

# Check if an IP address is within the subnet
print("Is 192.168.1.5 within subnet?", ipv4_subnet_config.is_within('192.168.1.5')) 

# Divide the subnet into smaller subnets
smaller_subnets = ipv4_subnet_config.subnet_division(30)
print("Divided Subnets:")
for subnet in smaller_subnets:
    print(subnet)

# Merge subnets (assuming adjacent subnets)
merged_subnet = ipv4_subnet_config.subnet_merge('192.168.1.8/29')
print("Merged Subnet:", merged_subnet)  
```
Expected Output:
```
Subnet Range: 192.168.1.0-192.168.1.7
First Host: 192.168.1.1
Last Host: 192.168.1.6
Host Counts: 6
Hosts in Subnet:
192.168.1.0
192.168.1.1
192.168.1.2
192.168.1.3
192.168.1.4
192.168.1.5
192.168.1.6
192.168.1.7
Is 192.168.1.5 within subnet? True
Divided Subnets:
192.168.1.0/30
192.168.1.4/30
Merged Subnet: 192.168.1.0/28
```
---

## Class: `IPv4WildCardConfig`

#### Description

The `IPv4WildCardConfig` class handles wildcard configurations for IPv4 addresses, which are used to match ranges of IP addresses by allowing certain bits to "wildcard" or vary. This is particularly useful in network policies and access lists where you need to specify a range of addresses without enumerating each one.

#### Inherits: `InterfaceIPv4Config`

#### Methods

- **`__init__(*args)`**:
  Initializes the IPv4 wildcard configuration by setting up the wildcard IP address and netmask.
  - **Parameters**:
    - `*args`: Variable-length argument list for the IPv4 address and wildcard netmask.

- **`_initialize(*args) -> None`**:
  Internal method that initializes the wildcard configuration and recalculates the IP address.

- **`_validate(*args) -> None`**:
  Validates the wildcard IP address and netmask using the `IPStandardizer`.

- **`_recalculate_ip_addr() -> None`**:
  Recalculates the IP address based on the wildcard netmask.

- **`ip_addr`** (property):
  Returns the wildcard IP address.
  - **Returns**:
    - `IPv4Addr`: The wildcard IP address.

- **`netmask`** (property):
  Returns the wildcard netmask.
  - **Returns**:
    - `IPv4NetMask`: The wildcard netmask.

- **`get_hosts() -> Generator[IPv4Addr, None, None]`**:
  Generates all possible host IPs that match the wildcard pattern.
  - **Returns**:
    - `Generator[IPv4Addr, None, None]`: A generator yielding all matching host addresses.

- **`is_within(ip_addr: Any) -> bool`**:
  Checks whether a given IP address matches the wildcard range.
  - **Parameters**:
    - `ip_addr (Any)`: The IP address to check.
  - **Returns**:
    - `bool`: `True` if the IP address matches the wildcard pattern, otherwise `False`.

- **`__str__() -> str`**:
  Returns a string representation of the wildcard configuration.
  - **Returns**:
    - `str`: A string representing the wildcard IP address and netmask (e.g., "192.168.1.50 0.0.0.15").

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv4WildCardConfig

# Create an IPv4 wildcard configuration
ipv4_wildcard_config = IPv4WildCardConfig('192.168.1.50 0.0.0.15')

# Access properties
print("Wildcard IP Address:", ipv4_wildcard_config.ip_addr)    
print("Wildcard Netmask:", ipv4_wildcard_config.netmask)       

# Generate hosts matching the wildcard pattern
print("Hosts matching the wildcard:")
for host in ipv4_wildcard_config.get_hosts():
    print(host)

# Check if an IP address matches the wildcard
print("Is 192.168.1.52 within wildcard?", ipv4_wildcard_config.is_within('192.168.1.52'))  
print("Is 192.168.1.64 within wildcard?", ipv4_wildcard_config.is_within('192.168.1.64'))  
```
Expected Output:
```
Wildcard IP Address: 192.168.1.48
Wildcard Netmask: 0.0.0.15
Hosts matching the wildcard:
192.168.1.48
192.168.1.49
192.168.1.50
192.168.1.51
192.168.1.52
192.168.1.53
192.168.1.54
192.168.1.55
192.168.1.56
192.168.1.57
192.168.1.58
192.168.1.59
192.168.1.60
192.168.1.61
192.168.1.62
192.168.1.63
Is 192.168.1.52 within wildcard? True
Is 192.168.1.64 within wildcard? False
```

---

## Class: `IPv6HostConfig`

#### Description

The `IPv6HostConfig` class represents a host configuration for an IPv6 network interface. It extends `InterfaceIPv6Config` and provides methods for calculating the network ID, classifying the IP address type (e.g., global unicast, link-local), and determining the number of usable hosts in the network. This class is designed to manage IPv6-specific host configurations, allowing for easy access to network properties and classification of IP addresses.

#### Inherits: `InterfaceIPv6Config`

#### Attributes

- `_ip_type (IPv6AddrType)`: The type of the IPv6 address (e.g., global unicast, link-local, multicast).
- `_network_id (IPv6Addr)`: The network ID calculated from the IPv6 address and netmask.

#### Methods

- **`__init__(*args)`**:
  Initializes the IPv6 host configuration by setting up the IP address and netmask, and calculating network-specific attributes.
  - **Parameters**:
    - `*args`: Variable-length argument list for the IPv6 address and netmask.

- **`_initialize(*args) -> None`**:
  Internal method that initializes the IPv6 host configuration, validates the inputs, and calculates network properties.

- **`_validate(*args) -> None`**:
  Validates the provided IPv6 address and netmask using the `IPStandardizer`.

- **`_calculate_network_id() -> None`**:
  Calculates the network ID by applying the netmask to the IP address.

- **`_classify_ip_address_type() -> None`**:
  Classifies the IP address type (e.g., global unicast, link-local) using `IPAddrTypeClassifier`.

- **`ip_addr`** (property):
  Returns the configured IPv6 address.
  - **Returns**:
    - `IPv6Addr`: The IPv6 address assigned to the interface.

- **`netmask`** (property):
  Returns the netmask associated with the IPv6 address.
  - **Returns**:
    - `IPv6NetMask`: The netmask of the IPv6 address.

- **`network_id`** (property):
  Returns the network ID of the subnet.
  - **Returns**:
    - `IPv6Addr`: The network ID calculated from the IP address and netmask.

- **`host_counts`** (property):
  Calculates and returns the number of usable host addresses in the network.
  - **Returns**:
    - `int`: The number of usable hosts in the subnet.

- **`ip_type`** (property):
  Returns the classified IP address type.
  - **Returns**:
    - `IPv6AddrType`: The type classification of the IP address.

- **`is_unspecified`** (property):
  Returns `True` if the IP address is unspecified.
  - **Returns**:
    - `bool`: `True` if the IP address is unspecified, otherwise `False`.

- **`is_loopback`** (property):
  Returns `True` if the IP address is a loopback address.
  - **Returns**:
    - `bool`: `True` if the IP address is loopback, otherwise `False`.

- **`is_multicast`** (property):
  Returns `True` if the IP address is a multicast address.
  - **Returns**:
    - `bool`: `True` if the IP address is multicast, otherwise `False`.

- **`is_link_local`** (property):
  Returns `True` if the IP address is link-local.
  - **Returns**:
    - `bool`: `True` if the IP address is link-local, otherwise `False`.

- **`is_global_unicast`** (property):
  Returns `True` if the IP address is a global unicast address.
  - **Returns**:
    - `bool`: `True` if the IP address is global unicast, otherwise `False`.

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv6HostConfig

# Create an IPv6 host configuration
ipv6_host_config = IPv6HostConfig('2001:db8::1/64')

# Access various properties
print("IP Address:", ipv6_host_config.ip_addr)          
print("Netmask:", ipv6_host_config.netmask)             
print("Network ID:", ipv6_host_config.network_id)       
print("Host Counts:", ipv6_host_config.host_counts)     
print("IP Type:", ipv6_host_config.ip_type)             
print("Is Global Unicast:", ipv6_host_config.is_global_unicast)  
```
Expected Output:
```
IP Address: 2001:db8::1
Netmask: ffff:ffff:ffff:ffff::
Network ID: 2001:db8::
Host Counts: 18446744073709551616
IP Type: IPv6AddrType.DOCUMENTATION
Is Global Unicast: False
```

---

## Class: `IPv6SubnetConfig`

#### Description

The `IPv6SubnetConfig` class represents a subnet configuration for an IPv6 network. It inherits from `IPv6HostConfig` and adds functionality for working with subnet ranges and hosts within a subnet. This includes operations such as retrieving the first and last host, iterating over all hosts, checking if an IP address is within the subnet, dividing the subnet into smaller subnets, and merging subnets.

#### Inherits: `IPv6HostConfig`

#### Methods

- **`first_host`** (property):
  Returns the first usable host address within the subnet.
  - **Returns**:
    - `IPv6Addr`: The first usable host address.

- **`last_host`** (property):
  Returns the last usable host address within the subnet.
  - **Returns**:
    - `IPv6Addr`: The last usable host address.

- **`subnet_range`** (property):
  Returns the range of the subnet, from the first host to the last host.
  - **Returns**:
    - `str`: A string representing the subnet range in the format "first_host - last_host".

- **`get_hosts() -> Generator[IPv6Addr, None, None]`**:
  Generates all usable hosts within the subnet by iterating over possible host addresses.
  - **Returns**:
    - `Generator[IPv6Addr, None, None]`: A generator yielding each host in the subnet.

- **`is_within(ip_addr: Any) -> bool`**:
  Checks whether a given IPv6 address falls within the subnet.
  - **Parameters**:
    - `ip_addr (Any)`: The IPv6 address to check.
  - **Returns**:
    - `bool`: `True` if the IP address is within the subnet, otherwise `False`.

- **`subnet_division(mask: int) -> List[IPv6SubnetConfig]`**:
  Divides the current subnet into smaller subnets based on a new mask size.
  - **Parameters**:
    - `mask (int)`: The new mask size for the smaller subnets.
  - **Returns**:
    - `List[IPv6SubnetConfig]`: A list of new subnet configurations.

- **`subnet_merge(*subnets: Any) -> IPv6SubnetConfig`**:
  Attempts to merge multiple subnets into a larger subnet.
  - **Parameters**:
    - `*subnets (Any)`: Variable-length argument list of subnet objects to merge.
  - **Returns**:
    - `IPv6SubnetConfig`: A new subnet configuration representing the merged subnet.

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv6SubnetConfig

# Create an IPv6 subnet configuration
ipv6_subnet_config = IPv6SubnetConfig('2001:db8::/64')

# Access various properties
print("Subnet Range:", ipv6_subnet_config.subnet_range)    
print("First Host:", ipv6_subnet_config.first_host)        
print("Last Host:", ipv6_subnet_config.last_host)          
print("Host Counts:", ipv6_subnet_config.host_counts)      

# Check if an IP address is within the subnet
print("Is 2001:db8::1 within subnet?", ipv6_subnet_config.is_within('2001:db8::1'))  

# Divide the subnet into smaller subnets
smaller_subnets = ipv6_subnet_config.subnet_division(65)
print("Divided Subnets:")
for subnet in smaller_subnets:
    print(subnet)

# Merge subnets (assuming adjacent subnets)
merged_subnet = ipv6_subnet_config.subnet_merge('2001:db8:0:1::/64')
print("Merged Subnet:", merged_subnet)  
```
Expected Output:
```
Subnet Range: 2001:db8:: - 2001:db8::ffff:ffff:ffff:ffff
First Host: 2001:db8::
Last Host: 2001:db8::ffff:ffff:ffff:ffff
Host Counts: 18446744073709551616
Is 2001:db8::1 within subnet? True
Divided Subnets:
2001:db8::/65
2001:db8:0:0:8000::/65
Merged Subnet: 2001:db8::/63 
```

---

## Class: `IPv6WildCardConfig`

#### Description

The `IPv6WildCardConfig` class handles wildcard configurations for IPv6 addresses, which are used to match ranges of IP addresses by allowing certain bits to "wildcard" or vary. This is particularly useful in network policies and access lists where you need to specify a range of addresses without enumerating each one.

#### Inherits: `InterfaceIPv6Config`

#### Methods

- **`__init__(*args)`**:
  Initializes the IPv6 wildcard configuration by setting up the wildcard IP address and netmask.
  - **Parameters**:
    - `*args`: Variable-length argument list for the IPv6 address and wildcard netmask.

- **`_initialize(*args) -> None`**:
  Internal method that initializes the wildcard configuration and recalculates the IP address.

- **`_validate(*args) -> None`**:
  Validates the wildcard IP address and netmask using the `IPStandardizer`.

- **`_recalculate_ip_addr() -> None`**:
  Recalculates the IP address based on the wildcard netmask.

- **`ip_addr`** (property):
  Returns the wildcard IPv6 address.
  - **Returns**:
    - `IPv6Addr`: The wildcard IPv6 address.

- **`netmask`** (property):
  Returns the wildcard netmask.
  - **Returns**:
    - `IPv6NetMask`: The wildcard netmask.

- **`get_hosts() -> Generator[IPv6Addr, None, None]`**:
  Generates all possible host IPs that match the wildcard pattern.
  - **Returns**:
    - `Generator[IPv6Addr, None, None]`: A generator yielding all matching host addresses.

- **`is_within(ip_addr: Any) -> bool`**:
  Checks whether a given IP address matches the wildcard range.
  - **Parameters**:
    - `ip_addr (Any)`: The IP address to check.
  - **Returns**:
    - `bool`: `True` if the IP address matches the wildcard pattern, otherwise `False`.

- **`__str__() -> str`**:
  Returns a string representation of the wildcard configuration.
  - **Returns**:
    - `str`: A string representing the wildcard IP address and netmask (e.g., "2001:db8::1 ::00FF").

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPv6WildCardConfig

# Create an IPv6 wildcard configuration
ipv6_wildcard_config = IPv6WildCardConfig('2001:db8::1 ::ff')

# Access properties
print("Wildcard IP Address:", ipv6_wildcard_config.ip_addr)  
print("Wildcard Netmask:", ipv6_wildcard_config.netmask)  

# Generate hosts matching the wildcard pattern
print("Hosts matching the wildcard:")
index = 0
for host in ipv6_wildcard_config.get_hosts():
    print(host)
    index += 1
    if index == 5:
        break

# Check if an IP address matches the wildcard
print("Is 2001:db8::2 within wildcard?", ipv6_wildcard_config.is_within('2001:db8::2'))  
print("Is 2001:db8::100 within wildcard?", ipv6_wildcard_config.is_within('2001:db8::100'))  
```
Expected Output:
```
Wildcard IP Address: 2001:db8::
Wildcard Netmask: ::ff
Hosts matching the wildcard:
2001:db8::
2001:db8::1
2001:db8::2
2001:db8::3
2001:db8::4
Is 2001:db8::2 within wildcard? True
Is 2001:db8::100 within wildcard? False
```
---

## Class: `IPWildCardCalculator`

#### Description

The `IPWildCardCalculator` class provides static methods for calculating the minimal wildcard configuration that encompasses a given set of IPv4 or IPv6 subnets. This is particularly useful for creating concise access control lists (ACLs) or routing policies that efficiently cover multiple subnets.

#### Methods

- **`calculate_minimum_ipv4_wildcard(*subnets: Any) -> IPv4WildCardConfig`**:
  Calculates the minimal IPv4 wildcard configuration that covers the provided IPv4 subnets.
  - **Parameters**:
    - `*subnets (Any)`: Variable-length argument list of IPv4 subnet strings (e.g., '192.168.0.0/24').
  - **Returns**:
    - `IPv4WildCardConfig`: A wildcard configuration that covers all the provided subnets.

- **`calculate_minimum_ipv6_wildcard(*subnets: Any) -> IPv6WildCardConfig`**:
  Calculates the minimal IPv6 wildcard configuration that covers the provided IPv6 subnets.
  - **Parameters**:
    - `*subnets (Any)`: Variable-length argument list of IPv6 subnet strings (e.g., '2001:db8::/32').
  - **Returns**:
    - `IPv6WildCardConfig`: A wildcard configuration that covers all the provided subnets.

#### Example Usage

```python
from ttlinks.ipservice.ip_configs import IPWildCardCalculator

# Calculate minimal IPv4 wildcard covering multiple subnets
ipv4_wildcard = IPWildCardCalculator.calculate_minimum_ipv4_wildcard('192.168.0.0/30', '192.168.0.4/30')
print("IPv4 Wildcard Config:", ipv4_wildcard)
# Outputs a wildcard configuration covering the provided subnets

# Calculate minimal IPv6 wildcard covering multiple subnets
ipv6_wildcard = IPWildCardCalculator.calculate_minimum_ipv6_wildcard('2001:db8::/64', '2001:db8:7::/64')
print("IPv6 Wildcard Config:", ipv6_wildcard)
# Outputs a wildcard configuration covering the provided subnets
```
Expected Output:
```
IPv4 Wildcard Config: 192.168.0.0 0.0.0.7
IPv6 Wildcard Config: 2001:db8:: ::7:0:ffff:ffff:ffff:ffff
```


---

## Dependencies

The `ip_configs.py` module depends on the following external libraries and modules:

- **`ttlinks.common.binary_utils.binary_factory`**: Provides the `OctetFlyWeightFactory` class used for efficient handling of binary octets in IP address calculations.

- **`ttlinks.common.tools.network`**: Supplies the `BinaryTools` class, utilized for binary operations such as checking if an IP address falls within a specified range and expanding bits based on netmask.

- **`ttlinks.ipservice.ip_addr_type_classifiers`**: Imports the `IPAddrTypeClassifier` class, which is used to classify IP address types (e.g., public, private, multicast) for both IPv4 and IPv6.

- **`ttlinks.ipservice.ip_converters`**: Provides `BinaryDigitsIPv4ConverterHandler` and `BinaryDigitsIPv6ConverterHandler` for converting lists of binary digits into IPv4 and IPv6 addresses, respectively.

- **`ttlinks.ipservice.ip_address`**: Includes classes like `IPv4Addr`, `IPv4NetMask`, `IPv4WildCard`, `IPv6Addr`, `IPv6NetMask`, and `IPv6WildCard` to represent and manipulate IP addresses and netmasks.

- **`ttlinks.ipservice.ip_format_standardizer`**: Imports the `IPStandardizer` class, used for validating and standardizing IP address formats and configurations.

- **`ttlinks.ipservice.ip_utils`**: Imports `IPv4AddrType` and `IPv6AddrType` to define and categorize different IP address types for classification purposes.

- **`itertools`**: A Python standard library module used for efficient looping and generating combinations of bits, essential for subnet calculations and host iterations.

- **`typing`**: A Python standard library module used for type hints and annotations, including `Generator`, `List`, and `Any`, enhancing code readability and maintenance.

---
