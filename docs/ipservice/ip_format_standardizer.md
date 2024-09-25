# `ip_format_standardizer.py` Module Documentation

## Overview

The `ip_format_standardizer.py` module provides a set of classes and methods designed to standardize various formats of IP addresses and netmasks for both IPv4 and IPv6. Utilizing the Chain of Responsibility design pattern, this module allows for flexible and extensible handling of different IP representations, converting them into standardized objects that can be easily manipulated within networking applications.

This module is essential for systems that need to interpret and normalize a wide range of IP address formats, ensuring consistent processing regardless of the input format. By abstracting the complexities of IP address parsing and validation, it simplifies the development of network-related functionalities.

---


## Description

### Purpose

The primary purpose of the `ip_format_standardizer.py` module is to provide a robust framework for standardizing IP addresses and netmasks provided in various formats. This includes handling IP addresses in CIDR notation, dotted-decimal notation, colon-hexadecimal notation, and with accompanying netmasks or wildcard masks. The module ensures that regardless of how the IP address is initially presented, it can be transformed into a standardized object representation (`IPv4Addr`, `IPv6Addr`, `IPv4NetMask`, `IPv6NetMask`, `IPv4WildCard`, `IPv6WildCard`) suitable for further processing.

### Key Features

- **Chain of Responsibility Pattern**: Implements a chain of handlers that attempt to standardize the IP address until one succeeds or all fail, promoting flexibility and extensibility.
- **Support for Multiple Formats**: Capable of handling IP addresses in various formats, including CIDR notation, dotted-decimal with netmask, and dotted-decimal with wildcard for IPv4; and CIDR notation, colon-hexadecimal with netmask, and colon-hexadecimal with wildcard for IPv6.
- **Seamless Integration**: Designed to work seamlessly with other modules, particularly those dealing with IP address manipulation and network configuration.
- **Error Handling**: If an input cannot be standardized by any handler, the module gracefully handles the situation by returning `None` or passing the request along the chain, ensuring that the system remains robust.

### Contents

1. **Abstract Base Classes**
   - `IPStandardizerHandler`: An abstract base class defining the interface for all standardizer handlers.

2. **IPv4 Standardizer Handlers**
   - `CIDRInterfaceIPv4StandardizerHandler`: Handles IPv4 addresses in CIDR notation.
   - `DotInterfaceIPv4StandardizerHandler`: Handles IPv4 addresses in dotted-decimal format with a netmask.
   - `IPAddrInterfaceIPv4StandardizerHandler`: Handles IPv4 addresses provided as `IPv4Addr` and `IPv4NetMask` objects.
   - `DotWildcardIPv4StandardizerHandler`: Handles IPv4 addresses with a wildcard mask in dotted-decimal format.
   - `IPAddrWildcardIPv4StandardizerHandler`: Handles IPv4 addresses provided as `IPv4Addr` and `IPv4WildCard` objects.

3. **IPv6 Standardizer Handlers**
   - `CIDRInterfaceIPv6StandardizerHandler`: Handles IPv6 addresses in CIDR notation.
   - `ColonInterfaceIPv6StandardizerHandler`: Handles IPv6 addresses in colon-hexadecimal format with a netmask.
   - `IPAddrInterfaceIPv6StandardizerHandler`: Handles IPv6 addresses provided as `IPv6Addr` and `IPv6NetMask` objects.
   - `ColonWildcardIPv6StandardizerHandler`: Handles IPv6 addresses with a wildcard mask in colon-hexadecimal format.
   - `IPAddrWildcardIPv6StandardizerHandler`: Handles IPv6 addresses provided as `IPv6Addr` and `IPv6WildCard` objects.

4. **Utility Class**
   - `IPStandardizer`: Provides static methods to standardize IP addresses using the appropriate chain of handlers.

---

## Class: `IPStandardizer`

#### Description

The `IPStandardizer` class provides a set of static methods designed to standardize various formats of IP addresses and netmasks for both IPv4 and IPv6. By leveraging the Chain of Responsibility (CoR) design pattern, it manages a sequence of handlers that attempt to standardize the input until one succeeds or all have been tried. This class simplifies the process of handling different IP address formats by abstracting the complexity of parsing and validation, ensuring consistent and usable representations of IP addresses and netmasks across networking applications.

#### Inherits: None

#### Methods

- **ipv4_interface(*args, standardizer: List[IPStandardizerHandler] = None) -> Tuple[IPv4Addr, IPv4NetMask]**

  Standardizes an IPv4 interface, which includes an IPv4 address and a netmask. It accepts various formats such as CIDR notation, dotted-decimal with netmask, or objects of type `IPv4Addr` and `IPv4NetMask`.

  - **Parameters**:
    - `*args`: The arguments representing the IPv4 address and netmask in various formats (e.g., '192.168.1.1/24', '192.168.1.1 255.255.255.0').
    - `standardizer (List[IPStandardizerHandler], optional)`: A list of custom handlers for standardizing the IPv4 address and netmask. If not provided, the default chain of handlers is used.

  - **Returns**:
    - `Tuple[IPv4Addr, IPv4NetMask]`: A tuple containing the standardized IPv4 address and netmask objects.

- **ipv4_wildcard(*args, standardizer: List[IPStandardizerHandler] = None) -> Tuple[IPv4Addr, IPv4WildCard]**

  Standardizes an IPv4 address and a wildcard mask. It handles formats where wildcard masks are used instead of netmasks, accepting inputs like dotted-decimal strings with space-separated wildcard masks.

  - **Parameters**:
    - `*args`: The arguments representing the IPv4 address and wildcard mask in various formats (e.g., '192.168.1.1 0.0.1.255').
    - `standardizer (List[IPStandardizerHandler], optional)`: A list of custom handlers for standardizing the IPv4 address and wildcard mask. If not provided, the default chain of handlers is used.

  - **Returns**:
    - `Tuple[IPv4Addr, IPv4WildCard]`: A tuple containing the standardized IPv4 address and wildcard mask objects.

- **ipv6_interface(*args, standardizer: List[IPStandardizerHandler] = None) -> Tuple[IPv6Addr, IPv6NetMask]**

  Standardizes an IPv6 interface, including an IPv6 address and a netmask. It accepts various formats such as CIDR notation, colon-hexadecimal with netmask, or objects of type `IPv6Addr` and `IPv6NetMask`.

  - **Parameters**:
    - `*args`: The arguments representing the IPv6 address and netmask in various formats (e.g., 'fe80::1/64', 'fe80::1 ff00::').
    - `standardizer (List[IPStandardizerHandler], optional)`: A list of custom handlers for standardizing the IPv6 address and netmask. If not provided, the default chain of handlers is used.

  - **Returns**:
    - `Tuple[IPv6Addr, IPv6NetMask]`: A tuple containing the standardized IPv6 address and netmask objects.

- **ipv6_wildcard(*args, standardizer: List[IPStandardizerHandler] = None) -> Tuple[IPv6Addr, IPv6WildCard]**

  Standardizes an IPv6 address and a wildcard mask. It handles formats where wildcard masks are used instead of netmasks, accepting inputs like colon-hexadecimal strings with space-separated wildcard masks.

  - **Parameters**:
    - `*args`: The arguments representing the IPv6 address and wildcard mask in various formats (e.g., 'fe80::1 ::ff').
    - `standardizer (List[IPStandardizerHandler], optional)`: A list of custom handlers for standardizing the IPv6 address and wildcard mask. If not provided, the default chain of handlers is used.

  - **Returns**:
    - `Tuple[IPv6Addr, IPv6WildCard]`: A tuple containing the standardized IPv6 address and wildcard mask objects.

#### Example Usage

```python
from ttlinks.ipservice.ip_format_standardizer import IPStandardizer
from ttlinks.ipservice.ip_address import (
    IPv4Addr, IPv4NetMask, IPv4WildCard,
    IPv6Addr, IPv6NetMask, IPv6WildCard
)

# Example 1: Standardizing an IPv4 interface in CIDR notation
ipv4_address_cidr = '192.168.1.1/24'
ipv4_addr, ipv4_netmask = IPStandardizer.ipv4_interface(ipv4_address_cidr)
print(f"IPv4 Address: {ipv4_addr}, Netmask: {ipv4_netmask}")
# Expected Output:
# IPv4 Address: 192.168.1.1, Netmask: 255.255.255.0

# Example 2: Standardizing an IPv4 interface in dotted-decimal notation with netmask
ipv4_address_netmask = '192.168.1.1 255.255.255.0'
ipv4_addr, ipv4_netmask = IPStandardizer.ipv4_interface(ipv4_address_netmask)
print(f"IPv4 Address: {ipv4_addr}, Netmask: {ipv4_netmask}")
# Expected Output:
# IPv4 Address: 192.168.1.1, Netmask: 255.255.255.0

# Example 3: Standardizing an IPv4 address and wildcard mask
ipv4_address_wildcard = '192.168.1.1 0.0.1.255'
ipv4_addr, ipv4_wildcard = IPStandardizer.ipv4_wildcard(ipv4_address_wildcard)
print(f"IPv4 Address: {ipv4_addr}, Wildcard Mask: {ipv4_wildcard}")
# Expected Output:
# IPv4 Address: 192.168.1.1, Wildcard Mask: 0.0.1.255

# Example 4: Standardizing an IPv6 interface in CIDR notation
ipv6_address_cidr = 'fe80::1/64'
ipv6_addr, ipv6_netmask = IPStandardizer.ipv6_interface(ipv6_address_cidr)
print(f"IPv6 Address: {ipv6_addr}, Netmask: {ipv6_netmask}")
# Expected Output:
# IPv6 Address: fe80::1, Netmask: ffff:ffff:ffff:ffff::

# Example 5: Standardizing an IPv6 interface in colon-hexadecimal notation with netmask
ipv6_address_netmask = 'fe80::1 ff00::'
ipv6_addr, ipv6_netmask = IPStandardizer.ipv6_interface(ipv6_address_netmask)
print(f"IPv6 Address: {ipv6_addr}, Netmask: {ipv6_netmask}")
# Expected Output:
# IPv6 Address: fe80::1, Netmask: ff00::

# Example 6: Standardizing an IPv6 address and wildcard mask
ipv6_address_wildcard = 'fe80::1 ::ff'
ipv6_addr, ipv6_wildcard = IPStandardizer.ipv6_wildcard(ipv6_address_wildcard)
print(f"IPv6 Address: {ipv6_addr}, Wildcard Mask: {ipv6_wildcard}")
# Expected Output:
# IPv6 Address: fe80::1, Wildcard Mask: ::ff

# Example 7: Standardizing IPv4 address and netmask objects
ipv4_addr_obj = IPv4Addr('192.168.1.1')
ipv4_netmask_obj = IPv4NetMask('255.255.255.0')
ipv4_addr, ipv4_netmask = IPStandardizer.ipv4_interface(ipv4_addr_obj, ipv4_netmask_obj)
print(f"IPv4 Address: {ipv4_addr}, Netmask: {ipv4_netmask}")
# Expected Output:
# IPv4 Address: 192.168.1.1, Netmask: 255.255.255.0

# Example 8: Standardizing IPv6 address and netmask objects
ipv6_addr_obj = IPv6Addr('fe80::1')
ipv6_netmask_obj = IPv6NetMask('/64')
ipv6_addr, ipv6_netmask = IPStandardizer.ipv6_interface(ipv6_addr_obj, ipv6_netmask_obj)
print(f"IPv6 Address: {ipv6_addr}, Netmask: {ipv6_netmask}")
# Expected Output:
# IPv6 Address: fe80::1, Netmask: ffff:ffff:ffff:ffff::
```

In these examples:

- **Example 1 & 2**: Demonstrate how to standardize IPv4 addresses provided in CIDR notation and dotted-decimal format with netmask.
- **Example 3**: Shows standardization of an IPv4 address with a wildcard mask.
- **Example 4 & 5**: Illustrate standardization of IPv6 addresses provided in CIDR notation and colon-hexadecimal format with netmask.
- **Example 6**: Demonstrates standardization of an IPv6 address with a wildcard mask.
- **Example 7 & 8**: Show how to standardize when IPv4 or IPv6 address and netmask are provided as objects.

---