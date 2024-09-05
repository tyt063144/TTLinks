### 1. `IPv4HostIPConfig`

#### Overview
The `IPv4HostIPConfig` class is specifically designed for managing IPv4 configurations for individual hosts within a network. It extends `InterfaceIPv4Config` to provide additional functionalities such as calculating the broadcast address, network ID, and classifying the IP address based on its network characteristics.

#### Features

- **Broadcast Address Calculation:** Automatically calculates the broadcast address for the network based on the provided IP address and netmask.
- **Network ID Calculation:** Computes the network identifier by applying the netmask to the IP address.
- **IP Classification:** Utilizes a series of classifiers to determine the type of IP address (e.g., private, public, multicast).

#### Key Methods

- **`_validate(ip_addr, netmask)`**: Confirms that the provided IP address and netmask are instances of `IPv4Addr` and `IPv4NetMask` respectively. It ensures that the address and netmask are compatible and throws a `ValueError` if validation fails.
- **`_adjust_ip()`**: Adjusts the IP address based on the netmask to align it within the correct network range and recalculates network details.
- **`calculate_broadcast_ip()`**: Determines the broadcast address for the network by setting all host bits (as per the netmask) to '1'.
- **`calculate_network_id()`**: Calculates the network ID by zeroing out all host bits in the IP address according to the netmask.
- **`_classify_ip_address()`**: Runs the IP address through various classifiers to determine its type (e.g., UNSPECIFIED, PRIVATE).

#### Properties

- **`broadcast_ip`**: Returns the calculated broadcast IP address for the subnet.
- **`network_id`**: Returns the network ID, which marks the beginning of the IP range for the subnet.
- **`host_counts`**: Calculates and returns the number of usable host addresses within the subnet, excluding the network and broadcast addresses.
- **`ip_type`**: Identifies and returns the type of the IP address based on predefined network characteristics.


#### Special Boolean Properties for IP Classification

These boolean properties help identify specific characteristics of the IP address:

- **`is_unspecified`**: Returns `True` if the IP address is unspecified, otherwise `False`.
- **`is_public`**: Returns `True` if the IP address is public, otherwise `False`.
- **`is_private`**: Returns `True` if the IP address is private, otherwise `False`.
- **`is_multicast`**: Returns `True` if the IP address is a multicast address, otherwise `False`.
- **`is_link_local`**: Returns `True` if the IP address is link-local, otherwise `False`.
- **`is_loopback`**: Returns `True` if the IP address is a loopback address, otherwise `False`.

#### Usage Example

```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask
from ttlinks.ipservice.ip_configs import IPv4HostIPConfig


# Create IP and netmask objects
ip_address = IPv4Addr("192.168.1.10")
netmask = IPv4NetMask("255.255.255.0")

# Initialize the configuration
host_config = IPv4HostIPConfig(ip_address, netmask)

# Access properties and methods
print("Address:", host_config.ip_addr)
print("Broadcast IP:", host_config.broadcast_ip)
print("Network ID:", host_config.network_id)
print("Host Count:", host_config.host_counts)
print("IP Type:", host_config.ip_type)
print('Is Loopback:', host_config.is_loopback)
```
Expected Output:
```
Address: 192.168.1.10
Broadcast IP: 192.168.1.255
Network ID: 192.168.1.0
Host Count: 254
IP Type: IPv4AddrType.PRIVATE
Is Loopback?: False
```


### 2. `IPv4SubnetConfig`

#### Overview
The `IPv4SubnetConfig` class extends the `IPv4HostIPConfig` to provide specialized functionalities for managing subnets within IPv4 networks. This class includes advanced capabilities to calculate the first and last hosts within a subnet, divide or merge subnets, and manage the range of IP addresses effectively.

#### Features

- **Subnet Range Management:** Manages the start and end addresses of the subnet, allowing for precise control over IP address allocations.
- **Subnet Division:** Facilitates the division of a subnet into smaller segments based on a more restrictive subnet mask.
- **Subnet Merging:** Enables the merging of multiple subnets into a larger one, provided they are contiguous and compatible.

#### Properties

- **`first_host`**: Returns the first usable IP address in the subnet, excluding the network address.
- **`last_host`**: Returns the last usable IP address in the subnet, excluding the broadcast address.
- **`subnet_range`**: Provides a string representing the range of the subnet from the network address to the broadcast address.

#### Methods

- **`get_hosts()`**: Generates all possible host addresses within the subnet, which can be used for assignments.
- **`calculate_network_id()`**: Recalculates the network ID when adjustments to the IP settings are made, ensuring consistency across network operations.
- **`is_within(ip_addr)`**: Checks if a given IP address falls within the defined subnet.
- **`subnet_division(mask)`**: Divides the current subnet into multiple smaller subnets based on the provided new subnet mask.
- **`subnet_merge(*subnets)`**: Merges the current subnet with one or more additional subnets into a larger configuration if they are contiguous and have compatible subnet masks.

#### Usage Example

```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig

# Initialize subnet configuration with an IP address within the subnet
ip_string = '192.168.1.50'  # Not the network ID
subnet_config = IPv4SubnetConfig(IPv4Addr(ip_string), IPv4NetMask("255.255.255.0"))
```
* Output the adjusted network configuration
    ```python
    print("Adjusted Address to Network ID:", subnet_config.ip_addr)  # The IP address is adjusted to the network ID
    print("Network ID:", subnet_config.network_id)
    print("Broadcast Address:", subnet_config.broadcast_ip)
    ```
    Expected Output:
    ```
    Adjusted Address to Network ID: 192.168.1.0
    Network ID: 192.168.1.0
    Broadcast Address: 192.168.1.255
    ```
* Display the first and last host of the subnet
    ```python
    print("First Host:", subnet_config.first_host)
    print("Last Host:", subnet_config.last_host)
    ```
    Expected Output:
    ```
    First Host: 192.168.1.1
    Last Host: 192.168.1.254
    ```
* Example of subnet division into smaller subnets
    ```python
    new_subnets = subnet_config.subnet_division(26)
    for subnet in new_subnets:
        print("New Subnet Range:", subnet.subnet_range)
    ```
    Expected Output:
    ```
    New Subnet Range: 192.168.1.0-192.168.1.63
    New Subnet Range: 192.168.1.64-192.168.1.127
    New Subnet Range: 192.168.1.128-192.168.1.191
    New Subnet Range: 192.168.1.192-192.168.1.255
    ```
* Check if a specific IP is within the subnet
    ```python
    ip_check = IPv4Addr("192.168.1.10")
    print("Is IP within the subnet?", subnet_config.is_within(ip_check))
    ```
    Expected Output:
    ```
    Is IP within the subnet? True
    ```
* Merge with another subnet
    ```python
    another_subnet = IPv4SubnetConfig(IPv4Addr('192.168.0.0'), IPv4NetMask("255.255.255.0"))
    merged_subnet = subnet_config.subnet_merge(another_subnet)
    print("Subnet after merge:", merged_subnet)
    print("Merged Subnet Range:", merged_subnet.subnet_range)
    ```
    Expected Output:
    ```
    Subnet after merge: 192.168.0.0/23
    Merged Subnet Range: 192.168.0.0-192.168.1.255
    ```


### 3. `IPv4WildcardConfig` 

#### Overview
The `IPv4WildcardConfig` class manages IPv4 addresses by employing wildcard masks. This advanced functionality is particularly useful in network scenarios where complex and flexible IP address matching is required, such as configuring access control lists (ACLs) in network routers and firewalls.

#### Features

- **Wildcard Masking:** Utilizes wildcard masks to specify which bits in an IP address should be ignored, allowing for broad or precise IP range selections.
- **Flexible IP Matching:** Enables the matching of IP addresses against specified patterns, accommodating diverse network security and management requirements.

#### Methods

- **`_validate(ip_addr, netmask)`**: Ensures the IP address and wildcard mask are of the correct types, raising a `ValueError` if not.
- **`_adjust_ip()`**: Adjusts the IP address to match the network configuration by applying the wildcard mask.
- **`calculate_ip_addr()`**: Recalculates the IP address based on the wildcard mask, setting masked bits to zero.
- **`get_hosts()`**: Generates all potential host addresses within the range defined by the wildcard mask.
- **`is_within(ip_addr)`**: Checks if a given IP address falls within the range defined by applying the wildcard mask.

#### Usage Example
```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4WildCard
from ttlinks.ipservice.ip_configs import IPv4WildcardConfig

# Initialize wildcard configuration
ip_address = IPv4Addr("192.168.1.0")
wildcard_mask = IPv4WildCard("0.0.1.3")  # Wildcard mask allowing variations in the last two octets
wildcard_config = IPv4WildcardConfig(ip_address, wildcard_mask)  # recalculate address will be done during initialization
```
* Output the recalculated IP address
    ```python
    print("Recalculated IP Address:", wildcard_config.ip_addr)
    ```
    Expected Output:
    ```
    Recalculated IP Address: 192.168.0.0
    ```
* Generate and print possible host addresses within the defined range
    ```python
    for host in wildcard_config.get_hosts():
    print("Host IP:", host)
    ```
    Expected Output:
    ```
    Host IP: 192.168.0.0
    Host IP: 192.168.0.1
    Host IP: 192.168.0.2
    Host IP: 192.168.0.3
    Host IP: 192.168.1.0
    Host IP: 192.168.1.1
    Host IP: 192.168.1.2
    Host IP: 192.168.1.3
    ```
* Check if a specific IP is within the range defined by the wildcard mask
    ```python
    ip_check1 = IPv4Addr("192.168.1.255")
    print("Is 192.168.1.255 within the range?", wildcard_config.is_within(ip_check1))
    ip_check2 = IPv4Addr("192.168.0.1")
    print("Is 192.168.1.255 within the range?", wildcard_config.is_within(ip_check2))
    ```
    Expected Output:
    ```
    Is 192.168.1.255 within the range? False
    Is 192.168.1.255 within the range? True
    ```

### 4. `IPv6HostIPConfig`

#### Overview
The `IPv6HostIPConfig` class is designed for configuring IPv6 addresses specifically for host IPs. It includes functionality to calculate and store detailed network information, extending the capabilities of `InterfaceIPv6Config`.

#### Features

- **Network Detail Calculation:** Automatically calculates network ID (Prefix) and classifies the IP type based on network characteristics.
- **IP Type Classification:** Determines the type of the IPv6 address, such as loopback, multicast, or global unicast.
- **Host Count Calculation:** Calculates the total number of usable hosts within the subnet.

#### Key Methods

- **`_validate(ip_addr, netmask)`**: Ensures that the provided IP address and netmask are appropriate instances. Raises a `ValueError` if the validation fails.
- **`_adjust_ip()`**: Adjusts the IP address based on the netmask and classifies the IP type.
- **`calculate_network_id()`**: Calculates the network ID by setting all host bits to '0' based on the netmask.
- **`_classify_ip_address()`**: Classifies the IP address into categories like UNSPECIFIED, MULTICAST, and GLOBAL UNICAST based on predefined rules.

#### Properties

- **`ip_type`**: Returns the type of the IP address as an enum value.
- **`network_id`**: Provides the calculated network ID for the subnet.
- **`host_counts`**: Returns the number of usable host addresses within the subnet.
- **`is_unspecified`**: Checks if the IP address is unspecified.
- **`is_loopback`**: Checks if the IP address is a loopback address.
- **`is_multicast`**: Checks if the IP address is a multicast address.
- **`is_link_local`**: Checks if the IP address is link-local.
- **`is_global_unicast`**: Checks if the IP address is a global unicast address.

#### Usage Example
```python
from ttlinks.ipservice.ip_address import IPv6Addr, IPv6NetMask
from ttlinks.ipservice.ip_configs import IPv6HostIPConfig

# Create IP and netmask objects
ip_address = IPv6Addr("fe80::0000:0000:8a2e:0370:7334")
netmask = IPv6NetMask("/10")

# Initialize the configuration
host_config = IPv6HostIPConfig(ip_address, netmask)

# Access properties and methods
print("IP Type:", host_config.ip_type)
print("Network ID:", host_config.network_id)
print("Host Count:", host_config.host_counts)
print("Is Global Unicast:", host_config.is_global_unicast)
```
Expected Output:
```
IP Type: IPv6AddrType.LINK_LOCAL
Network ID: FE80:0000:0000:0000:0000:0000:0000:0000
Host Count: 332306998946228968225951765070086144
Is Global Unicast: False
```

### 5. `IPv6SubnetConfig`

#### Overview
The `IPv6SubnetConfig` class is tailored for managing IPv6 subnet configurations. Extending the `IPv6HostIPConfig`, this class includes additional capabilities to handle subnet-specific details such as calculating the first and last hosts, and provides tools for subnet division and merging.

#### Features

- **Subnet Range Management:** Controls and calculates the range of IP addresses within a subnet from the first to the last usable host.
- **Subnet Division and Merging:** Allows for the logical division of a subnet into smaller segments or merging multiple subnets, assuming they are contiguous and have compatible masks.

#### Properties

- **`first_host`**: Returns the first usable host IP address within the subnet.
- **`last_host`**: Provides the last usable host IP address in the subnet.
- **`subnet_range`**: Displays the range of IP addresses from the first to the last host.

#### Methods

- **`get_hosts()`**: Generates all possible host IP addresses within the subnet for potential assignment.
- **`calculate_network_id()`**: Recalculates the network ID when adjusting IP settings, ensuring consistency across network operations.
- **`is_within(ip_addr)`**: Verifies if a specific IP address falls within the defined subnet.
- **`subnet_division(mask)`**: Splits the current subnet into smaller subnets based on a new, more restrictive subnet mask.
- **`subnet_merge(*subnets)`**: Combines multiple subnets into a larger one if they are contiguous and have compatible masks.

#### Usage Example

```python
from ttlinks.ipservice.ip_address import IPv6Addr, IPv6NetMask
from ttlinks.ipservice.ip_configs import IPv6SubnetConfig

# Initialize subnet configuration with an IP address within the subnet
subnet_config = IPv6SubnetConfig(IPv6Addr("2001:db8::ff00"), IPv6NetMask("ffff:ffff:ffff:ffff::"))
```
* Display the adjusted network configuration
    ```python
    print("Adjusted Address to Network ID:", subnet_config.ip_addr)
    print("Network ID:", subnet_config.network_id)
    print("First Host:", subnet_config.first_host)
    print("Last Host:", subnet_config.last_host)
    print("Subnet Range:", subnet_config.subnet_range)
    print('Subnet:', subnet_config)
    ```
    Expected Output:
    ```
    Adjusted Address to Network ID: 2001:0DB8:0000:0000:0000:0000:0000:0000
    Network ID: 2001:0DB8:0000:0000:0000:0000:0000:0000
    First Host: 2001:0DB8:0000:0000:0000:0000:0000:0000
    Last Host: 2001:0DB8:0000:0000:FFFF:FFFF:FFFF:FFFF
    Subnet Range: 2001:0DB8:0000:0000:0000:0000:0000:0000 - 2001:0DB8:0000:0000:FFFF:FFFF:FFFF:FFFF
    Subnet: 2001:0DB8:0000:0000:0000:0000:0000:0000/64
    ```
* Generate and print first 3 possible hosts addresses within the subnet
    ```python
    hosts = subnet_config.get_hosts()
    print(next(hosts))
    print(next(hosts))
    print(next(hosts))
    ```
    Expected Output:
    ```
    2001:0DB8:0000:0000:0000:0000:0000:0000
    2001:0DB8:0000:0000:0000:0000:0000:0001
    2001:0DB8:0000:0000:0000:0000:0000:0002
    ```
* Example of subnet division
    ```python
    new_subnets = subnet_config.subnet_division(66)
    for subnet in new_subnets:
        print("Divided Subnet:", subnet)
    ```
    Expected Output:
    ```
    Divided Subnet: 2001:0DB8:0000:0000:0000:0000:0000:0000/66
    Divided Subnet: 2001:0DB8:0000:0000:4000:0000:0000:0000/66
    Divided Subnet: 2001:0DB8:0000:0000:8000:0000:0000:0000/66
    Divided Subnet: 2001:0DB8:0000:0000:C000:0000:0000:0000/66
    ```
* Check if a specific IP is within the subnet
    ```python
    ip_check = IPv6Addr("2001:db8::ff01")
    print("Is IP within the subnet?", subnet_config.is_within(ip_check))
    ```
    Expected Output:
    ```
    Is IP within the subnet? True
    ```
* Merge with another subnet
    ```python
    another_subnet = IPv6SubnetConfig(IPv6Addr("2001:db8:0:1::"), IPv6NetMask("ffff:ffff:ffff:ffff::"))
    print('Subnet1:', subnet_config)
    print('Subnet2:', another_subnet)
    merged_subnet = subnet_config.subnet_merge(another_subnet)
    print("Merged Subnet:", merged_subnet)
    print("Merged Subnet Range:", merged_subnet.subnet_range)
    ```
    Expected Output:
    ```
    Subnet1: 2001:0DB8:0000:0000:0000:0000:0000:0000/64
    Subnet2: 2001:0DB8:0000:0001:0000:0000:0000:0000/64
    Merged Subnet: 2001:0DB8:0000:0000:0000:0000:0000:0000/63
    Merged Subnet Range: 2001:0DB8:0000:0000:0000:0000:0000:0000 - 2001:0DB8:0000:0001:FFFF:FFFF:FFFF:FFFF
    ```
  
### 6. `IPv6WildcardConfig`

#### Overview
The `IPv6WildcardConfig` class is specialized for configuring IPv6 addresses using wildcard masks. This functionality is particularly useful in network scenarios where flexible and complex IP address matching is required, such as in configuring access control lists (ACLs) in routers and firewalls.

#### Features

- **Wildcard Masking:** Employs wildcard masks to specify which bits in an IP address should be ignored, enabling both broad and precise IP range selections.
- **Flexible IP Matching:** Facilitates the matching of IP addresses against specified patterns to meet diverse network security and management needs.

#### Key Methods

- **`_validate(ip_addr, wildcard_mask)`**: Confirms that the IP address and wildcard mask are correct instances; raises a `ValueError` if they are not.
- **`_adjust_ip()`**: Adjusts the IP address to conform to the wildcard mask by setting masked bits to zero.
- **`calculate_ip_addr()`**: Recalculates the IP address by applying the wildcard mask, setting masked bits to zero while retaining the original values of unmasked bits.
- **`get_hosts()`**: Generates all possible host addresses within the defined range by applying the wildcard mask.
- **`is_within(ip_addr)`**: Checks if a given IP address falls within the range defined by the wildcard mask.

#### Properties

There are no specific properties listed for this class as its primary function revolves around methods that manipulate and check IP addresses based on the wildcard configuration.

#### Usage Example

```python
from ttlinks.ipservice.ip_address import IPv6Addr, IPv6WildCard
from ttlinks.ipservice.ip_configs import IPv6WildcardConfig

# Initialize wildcard configuration
ip_address = IPv6Addr("2001:db8:0:FFFF::1:0")
wildcard_mask = IPv6WildCard("0:0:0:ffff:ffff::")
wildcard_config = IPv6WildcardConfig(ip_address, wildcard_mask)
```
* Output the self-adjusted IP address
    ```python
    print("Recalculated IP Address:", wildcard_config.ip_addr)
    ```
    Expected Output:
    ```
    Recalculated IP Address: 2001:0DB8:0000:0000:0000:0000:0001:0000
    ```
* Generate and print first 3 possible hosts addresses within the defined range
    ```python
    hosts = wildcard_config.get_hosts()
    print(next(hosts))
    print(next(hosts))
    print(next(hosts))
    ```
    Expected Output:
    ```
    2001:0DB8:0000:0000:0000:0000:0001:0000
    2001:0DB8:0000:0000:0001:0000:0001:0000
    2001:0DB8:0000:0000:0002:0000:0001:0000
    ```
* Check if a specific IP is within the range
    ```python
    ip_check = IPv6Addr("2001:db8:0:ABCD::1:0")
    print("Is 2001:db8:0:ABCD::1:0 within the range?", wildcard_config.is_within(ip_check))
    ```
    Expected Output:
    ```
    Is 2001:db8:0:ABCD::1:0 within the range? True
    ```
