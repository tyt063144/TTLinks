# `Enumerations`
1. `IPType` - The `IPType` enumeration defines whether an IP address is IPv4 or IPv6.<br>
**Example: Check if a value corresponds to a valid IP type**:
    ```python
    from ttlinks.ipservice.ip_utils import IPType
    is_valid = IPType.has_value(4)
    print("Is Valid IP Type:", is_valid)
    print("IP Type Values:", IPType.get_values())
    ```
    Expected Output:
    ```
    Is Valid IP Type: True
    IP Type Values: {4: <IPType.IPv4: 4>, 16: <IPType.IPv6: 16>}
    ```
2. `IPv4AddrType` - The `IPv4AddrType` enumeration categorizes various types of IPv4 addresses, such as public, private, multicast, and loopback.<br>
**Example: Retrieve the value of a specific IPv4 address type**:
    ```python
    from ttlinks.ipservice.ip_utils import IPv4AddrType
    is_private = IPv4AddrType.has_value(4)
    print("Is Private Address:", is_private)
    print("IPv4 Address Types:", IPv4AddrType.get_values())
    ```
    Expected Output:
    ```
    Is Private Address: True
    IPv4 Address Types: {0: <IPv4AddrType.UNDEFINED_TYPE: 0>, 1: <IPv4AddrType.UNSPECIFIED: 1>, ... , 14: <IPv4AddrType.DS_LITE: 14>}
    ```
3. `IPv6AddrType` - The `IPv6AddrType` enumeration categorizes various types of IPv6 addresses, such as global unicast, unique local addresses, multicast, and others.<br>
**Example: Retrieve the value of a specific IPv6 address type**:
    ```python
    from ttlinks.ipservice.ip_utils import IPv6AddrType
    is_global_unicast = IPv6AddrType.has_value(3)
    print("Is Global Unicast:", is_global_unicast)
    print("IPv6 Address Types:", IPv6AddrType.get_values())
    ```
    Expected Output:
    ```
    Is Global Unicast: True
    IPv6 Address Types: {0: <IPv6AddrType.UNDEFINED_TYPE: 0>, 1: <IPv6AddrType.UNSPECIFIED: 1>, ... , 15: <IPv6AddrType.ORCHIDV2: 15>}
    ```
---
# Network Utility Tools
1. `netmask_expand` - The `netmask_expand` method generates all possible bit combinations for a given IP address by expanding the corresponding IP and netmask bits at the same bit positions. Specifically, when a netmask bit is `0`, the corresponding IP bit can take both values `0` and `1`, allowing for the generation of all possible variations within the subnet. This is particularly useful for identifying all potential IP addresses within a network range based on the provided netmask.
    ```python
    from ttlinks.ipservice.ip_utils import NetToolsSuite
    ip_digits = [0, 1, 0, 1]  # Example IP digits that user is interested in
    netmask_digits = [0, 1, 0, 0]  # Example netmask digits that user is interested in
    expanded_ips = NetToolsSuite.netmask_expand(ip_digits, netmask_digits)
    print("Bits combination:", expanded_ips)
    ```
    Expected Output:
    ```
    Bits combination: [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1)]
    ```
2. `ip_within_range` - The `ip_within_range` method checks if a given IP address (represented as a list of binary digits) falls within a specific network range. The binary digits format can be derived from the `IPAddr.get_binary_digits()` method.<br>
**Example: Check if an IP is within a network range**
    ```python
    from ttlinks.ipservice.ip_utils import NetToolsSuite
    network_digits = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 192.168.100.0
    netmask_digits = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # 255.255.255.0
    
    # IP 192.168.100.150
    compared_digits_1 = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0]
    is_within_range_1 = NetToolsSuite.ip_within_range(network_digits, netmask_digits, compared_digits_1)
    
    # IP 192.198.100.150
    compared_digits_2 = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0]
    is_within_range_2 = NetToolsSuite.ip_within_range(network_digits, netmask_digits, compared_digits_2)
    
    print("Is 192.168.100.150 within range:", is_within_range_1)
    print("Is 192.198.100.150 within range:", is_within_range_2)
    ```
    Expected Output:
    ```
    Is 192.168.100.150 within range: True
    Is 192.198.100.150 within range: False
    ```