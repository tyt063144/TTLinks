## `ipservice` - Module Overview

### 1. **`ip_configs.py`**
This module focuses on handling IP address configurations such as network masks and wildcards. It includes classes like `IPv4HostConfig`, `IPv4SubnetConfig`, `IPv4WildCardConfig` and their IPv6 counterparts for managing network configurations. `IPWildCardCalculator` provides static methods for calculating the minimal wildcard configuration that encompasses a given set of IPv4 or IPv6 subnets.
- [IP Configuration Utilities](/docs/ipservice/ip_configs.md)

### 2. **`ip_address.py`**
This module provides abstract and concrete classes for managing IP addresses. The `IPAddr` class serves as the base class, and it includes subclasses like `IPv4Addr` and `IPv6Addr` for handling the validation, conversion, and binary representation of IP addresses.
- [IP Address Management](/docs/ipservice/ip_address.md)

### 3. **`ip_addr_type_classifiers.py`**
This module defines enumerations and handlers for classifying IP address types, including both IPv4 and IPv6. The `IPTypeClassifierHandler` uses a Chain of Responsibility (CoR) pattern to allow different handlers to classify IP types.
- [IP Address Type Classifiers](/docs/ipservice/ip_addr_type_classifiers.md)

### 4. **`ip_converters.py`**
This module facilitates the conversion of IP addresses between different formats (e.g., CIDR, binary, dotted-decimal). It includes classes like `IPConverterHandler`, which handle conversion requests through a Chain of Responsibility (CoR) pattern.
- [IP Converters](/docs/ipservice/ip_converters.md)

### 5. **`ip_format_standardizer.py`**
This module standardizes the format of IP addresses, ensuring consistency across different representations. It uses handlers like `CIDRInterfaceIPv4StandardizerHandler` and `ColonInterfaceIPv6StandardizerHandler` to process requests in a Chain of Responsibility (CoR) pattern.
- [IP Format Standardizer](/docs/ipservice/ip_format_standardizer.md)

### 6. **`ip_type_classifiers.py`**
This module provides a series of classes designed to classify IP addresses and netmasks either an IPv4 or IPv6. It provides handlers for both IPv4 and IPv6, including the validation of the type through the `IPv4IPTypeClassifierHandler` and `IPv6IPTypeClassifierHandler`.
- [IP Type Classifiers](/docs/ipservice/ip_type_classifiers.md)

### 7. **`ip_utils.py`**
This utility module provides helper functions and classes that support common IP-related operations. It includes the `IPv4AddrType` and `IPv6AddrType` enumerations to categorize different types of IP addresses.

---

### Module Descriptions:


#### 1. `ip_configs.py`
This module handles network masks and wildcard configurations. It includes classes for managing and validating netmasks (`IPv4NetMask`, `IPv6NetMask`) and wildcard masks for IP configurations.

#### 2. `ip_address.py`
This module defines abstract base classes (`IPAddr`) and concrete implementations (`IPv4Addr`, `IPv6Addr`) for managing and validating IP addresses. It provides binary representations and string formats of IP addresses.

#### 3. `ip_addr_type_classifiers.py`
This module contains the `IPType` enumeration and a set of handlers for classifying IP addresses. It works within a Chain of Responsibility (CoR) pattern to classify addresses as IPv4, IPv6, and other types based on octet length.

#### 4. `ip_converters.py`
This module facilitates the conversion of IP addresses across different formats. It uses handlers like `CIDRIPv4ConverterHandler`, `BinaryDigitsIPv4ConverterHandler`, and `DotIPv4ConverterHandler` to manage conversions.

#### 5. `ip_format_standardizer.py`
The `IPStandardizerHandler` in this module is responsible for standardizing IP address formats. It works within a Chain of Responsibility (CoR) pattern, converting IP addresses from different notations (e.g., CIDR, dotted-decimal).

#### 6. `ip_type_classifiers.py`
This module classifies IP addresses based on their usage types (e.g., public, private). It defines the `IPv4AddrType` and `IPv6AddrType` enumerations and their associated classifiers.

#### 7. `ip_utils.py`
This utility module provides additional helper functions and enumerations for managing IP addresses. It includes tools for categorizing and validating IPv4 and IPv6 addresses.