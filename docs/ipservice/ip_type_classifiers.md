# `ip_type_classifiers.py` Module Documentation

## Overview

The `ip_type_classifiers.py` module provides a series of classes designed to classify IP addresses and netmasks for both IPv4 and IPv6. It utilizes the Chain of Responsibility pattern to allow a sequence of handlers to process classification requests. This module is essential for applications requiring precise determination of IP types based on different input formats.


---

## `IPTypeClassifier` Class

### Description
The `IPTypeClassifier` provides a high-level interface to classify both IP addresses and netmasks quickly. It abstracts the complexities involved in the classification process by encapsulating the Chain of Responsibility pattern within static methods that can be easily accessed by users.

### Contents
1. **IPTypeClassifier**
2. **IPv4 Address Handlers**
3. **IPv6 Address Handlers**
4. **IPv4 Netmask Handlers**
5. **IPv6 Netmask Handlers**
6. **Utility Classes and Methods**

### Methods
- **classify_ip**: Classifies any IP address, determining whether it is IPv4 or IPv6.
- **classify_ipv4_address**: Specifically classifies IPv4 addresses.
- **classify_ipv6_address**: Specifically classifies IPv6 addresses.
- **classify_ipv4_netmask**: Classifies IPv4 netmasks.
- **classify_ipv6_netmask**: Classifies IPv6 netmasks.

### Usage Example
**1. classifying IPv4 Addresses**: To classify an IPv4 address, use the classify_ipv4_address method. The input can be either a list of octets or a dotted-decimal string.

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory

# Example 1: Classifying an IPv4 address from a dotted-decimal string
ipv4_address = '192.168.1.1'
ipv4_type = IPTypeClassifier.classify_ipv4_address(ipv4_address)
print(f'The IP address {ipv4_address} is classified as {ipv4_type}.')

# Example 2: Classifying an IPv4 address from a list of octets
ipv4_octet_list = [
    OctetFlyWeightFactory.get_octet('11000000'),  # 192
    OctetFlyWeightFactory.get_octet('10101000'),  # 168
    OctetFlyWeightFactory.get_octet('00000001'),  # 1
    OctetFlyWeightFactory.get_octet('00000001')   # 1
]
ipv4_type_from_octet = IPTypeClassifier.classify_ipv4_address(ipv4_octet_list)
print(f'The octet list is classified as {ipv4_type_from_octet}.')
```
Expected Output:
```
The IP address 192.168.1.1 is classified as IPType.IPv4.
The octet list is classified as IPType.IPv4.
```

**2. Classifying IPv6 Addresses**: To classify an IPv6 address, use the `classify_ipv6_address` method. The input can be either a colon-hexadecimal string or a list of octets.

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory

# Example 1: Classifying an IPv6 address from a colon-hexadecimal string
ipv6_address = '2001:0db8::1'
ipv6_type = IPTypeClassifier.classify_ipv6_address(ipv6_address)
print(f'The IP address {ipv6_address} is classified as {ipv6_type}.')

# Example 2: Classifying an IPv6 address from a list of octets
ipv6_octet_list = [OctetFlyWeightFactory.get_octet('00100000') for _ in range(16)]  # 16 octets
ipv6_type_from_octet = IPTypeClassifier.classify_ipv6_address(ipv6_octet_list)
print(f'The octet list is classified as {ipv6_type_from_octet}.')
```
Expected Output:
```
The IP address 2001:0db8::1 is classified as IPType.IPv6.
The octet list is classified as IPType.IPv6.
```

**3. Classifying IPv4 Netmasks**: Use the `classify_ipv4_netmask` method to classify IPv4 netmasks. The input can be a dotted-decimal string, a list of octets, or CIDR notation.

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory

# Example 1: Classifying an IPv4 netmask from a dotted-decimal string
ipv4_netmask = '255.255.255.0'
netmask_type = IPTypeClassifier.classify_ipv4_netmask(ipv4_netmask)
print(f'The netmask {ipv4_netmask} is classified as {netmask_type}.')

# Example 2: Classifying an IPv4 netmask from CIDR notation
ipv4_cidr_netmask = '/24'
netmask_type_cidr = IPTypeClassifier.classify_ipv4_netmask(ipv4_cidr_netmask)
print(f'The CIDR notation {ipv4_cidr_netmask} is classified as {netmask_type_cidr}.')

# Example 3: Classifying an IPv4 netmask from a list of octets
ipv4_netmask_octets = [
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('00000000')   # 0
]
netmask_type_octet = IPTypeClassifier.classify_ipv4_netmask(ipv4_netmask_octets)
print(f'The octet list is classified as {netmask_type_octet}.')
```
Expected Output:
```
The netmask 255.255.255.0 is classified as IPType.IPv4.
The CIDR notation /24 is classified as IPType.IPv4.
The octet list is classified as IPType.IPv4.
```

**4. Classifying IPv6 Netmasks**: Use the `classify_ipv6_netmask` method to classify IPv6 netmasks. The input can be a colon-hexadecimal string, a list of octets, or CIDR notation.

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory

# Example 1: Classifying an IPv6 netmask from a colon-hexadecimal string
ipv6_netmask = 'ffff:ffff:ffff:ffff::'
ipv6_netmask_type = IPTypeClassifier.classify_ipv6_netmask(ipv6_netmask)
print(f'The IPv6 netmask {ipv6_netmask} is classified as {ipv6_netmask_type}.')

# Example 2: Classifying an IPv6 netmask from CIDR notation
ipv6_cidr_netmask = '/64'
ipv6_netmask_type_cidr = IPTypeClassifier.classify_ipv6_netmask(ipv6_cidr_netmask)
print(f'The CIDR notation {ipv6_cidr_netmask} is classified as {ipv6_netmask_type_cidr}.')

# Example 3: Classifying an IPv6 netmask from a list of octets
ipv6_netmask_octets = [
    OctetFlyWeightFactory.get_octet('11111111') for _ in range(8)
] + [OctetFlyWeightFactory.get_octet('00000000') for _ in range(8)]
ipv6_netmask_type_octet = IPTypeClassifier.classify_ipv6_netmask(ipv6_netmask_octets)
print(f'The octet list is classified as {ipv6_netmask_type_octet}.')
```
Expected Output:
```
The IPv6 netmask ffff:ffff:ffff:ffff:: is classified as IPType.IPv6.
The CIDR notation /64 is classified as IPType.IPv6.
The octet list is classified as IPType.IPv6.
```

**5. Classifying General IP Addresses (IPv4 or IPv6)**: Use the `classify_ip` method to classify any IP address. This method automatically detects whether the address is IPv4 or IPv6 based on the input format.

```python
from ttlinks.ipservice.ip_type_classifiers import IPTypeClassifier

# Example 1: Classifying an IPv6 address
ipv6_address = '2001:0db8::1'
ip_type = IPTypeClassifier.classify_ip(ipv6_address)
print(f'The IP address {ipv6_address} is classified as {ip_type}.')

# Example 2: Classifying an IPv4 address
ipv4_address = '192.168.1.1'
ipv4_type = IPTypeClassifier.classify_ip(ipv4_address)
print(f'The IP address {ipv4_address} is classified as {ipv4_type}.')
```
Expected Output:
```
The IP address 2001:0db8::1 is classified as IPType.IPv6.
The IP address 192.168.1.1 is classified as IPType.IPv4.
```

---

Following this section, continue with detailed explanations of each specific handler class. 

---

## Abstract Classes

### 1. `IPTypeClassifierHandler`
#### Description

This abstract method processes a classification request, which consists of a list of octets representing an IP address. The method attempts to classify the IP type based on the criteria defined in the subclasses. If the current handler cannot process the request, it passes the request along to the next handler in the chain, if such a handler exists.

#### Inherits: `BidirectionalCoRHandler` from `ttlinks.common.design_template.cor`

### 2. `IPv4IPTypeClassifierHandler`
#### Description

This abstract handler class for classifying IPv4 IP types inherits from `IPTypeClassifierHandler`. It provides the foundational logic to determine if a request pertains to an IPv4 address and delegates the specifics of handling and classification to its subclasses. If an instance of this class or its subclasses cannot definitively classify the IP type, it forwards the classification request to the next handler in the chain of responsibility.

#### Inherits: `IPTypeClassifierHandler`

This approach ensures that the responsibilities for classifying IPv4 IPs are clearly separated and handled at different stages of the chain, allowing for both flexibility and precision in how IPv4 addresses are classified and managed within a network application context.

### 3. `IPv4NetmaskClassifierHandler`
#### Description

This abstract handler class for classifying IPv4 netmasks also inherits from `IPTypeClassifierHandler`. It focuses on validating and classifying netmasks specific to IPv4 addresses, utilizing logic to ensure that netmasks consist of contiguous ones followed by zeros. This handler passes any unprocessable requests to the next handler in the responsibility chain, facilitating a comprehensive approach to IPv4 netmask classification.

#### Inherits: `IPTypeClassifierHandler`

The design allows for modular and extendable classification logic, catering to various validation and classification needs specific to IPv4 netmasks within networking applications.

### 4. `IPv6IPTypeClassifierHandler`
#### Description

This abstract handler class is dedicated to the classification of IPv6 IP types. It inherits from `IPTypeClassifierHandler` and provides the core logic to identify whether a request is related to an IPv6 address, based on the presence of 16 octets. Unhandled requests are forwarded to the next handler in the chain, ensuring robust and accurate IPv6 classification.

#### Inherits: `IPTypeClassifierHandler`

This structure supports a detailed and orderly process for handling IPv6 addresses, promoting efficient classification across diverse networking scenarios.

### 5. `IPv6NetmaskClassifierHandler`
#### Description

Inherits from `IPTypeClassifierHandler`, this abstract class handles the classification of IPv6 netmasks. It verifies that the netmask conforms to the expected format of contiguous ones followed by zeros over 16 octets. If the classification cannot be completed, the request is passed to the subsequent handler in the chain.

#### Inherits: `IPTypeClassifierHandler`

This handler facilitates precise and effective classification of IPv6 netmasks, integrating seamlessly into systems that require detailed and reliable netmask validation and categorization.

---

## Concrete Classes
### 1. `OctetIPv4IPTypeClassifierHandler`
#### Description

This concrete handler class specializes in classifying an IP as IPv4 based solely on the octet count. It inherits from `IPv4IPTypeClassifierHandler` and is a specific implementation within the chain of responsibility, designed to validate and classify IPv4 addresses that consist exactly of 4 octets.

#### Inherits: `IPv4IPTypeClassifierHandler`

#### Methods

- **handle(request: Any)**: Examines the request to determine if it contains exactly 4 octets. If it does, the IP is classified as IPv4. If the condition is not met, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list of octets representing an IP address.
  - **Returns**:
    - `IPType`: `IPType.IPv4` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: List[Octet]) -> bool**: Validates whether the request consists of exactly 4 octets, indicating a valid IPv4 address.
  - **Parameters**:
    - `request (List[Octet])`: A list of octets representing the IP address.
  - **Returns**:
    - `bool`: True if the request is a valid IPv4 address (i.e., contains 4 octets), otherwise False.

#### Properties

- **next_handler**: Optional property that holds a reference to the next handler in the chain, allowing the classification process to continue if this handler cannot definitively classify the request.

#### Example Usage

```python
# Example showing how to use the OctetIPv4IPTypeClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_type_classifiers import OctetIPv4IPTypeClassifierHandler

# Create an instance of the handler
ipv4_classifier = OctetIPv4IPTypeClassifierHandler()

# Define a request with exactly 4 octets
request_ipv4 = [OctetFlyWeightFactory.get_octet('11000000'),
                OctetFlyWeightFactory.get_octet('10101000'),
                OctetFlyWeightFactory.get_octet('00000001'),
                OctetFlyWeightFactory.get_octet('00000001')]

# Classify the request
result = ipv4_classifier.handle(request_ipv4)
if result == IPType.IPv4:
    print("The IP is classified as IPv4.")
else:
    print("The IP could not be classified as IPv4.")
```
Expected Output:
```
The IP is classified as IPv4.
```
### 2. `DotIPv4IPTypeClassifierHandler`
#### Description

This concrete handler class is responsible for classifying IPv4 addresses based on their representation in dotted-decimal format. It extends the `IPv4IPTypeClassifierHandler` and focuses specifically on handling and validating IPv4 addresses expressed as strings in the standard dotted format (e.g., "192.168.1.1"). If the address cannot be classified as IPv4 by this format, the request is forwarded to the next handler in the chain.

#### Inherits: `IPv4IPTypeClassifierHandler`

#### Methods

- **handle(request: Any)**: Determines if the input string is a valid dotted-decimal IPv4 address. If valid, the IP is classified as IPv4; otherwise, it is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically expected to be a string representing an IP address in dotted-decimal format.
  - **Returns**:
    - `IPType`: `IPType.IPv4` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the input string correctly represents a dotted-decimal IPv4 address.
  - **Parameters**:
    - `request (str)`: A string representing an IP address in dotted-decimal format.
  - **Returns**:
    - `bool`: True if the input is a correctly formatted dotted-decimal IPv4 address, otherwise False.

#### Properties

- **next_handler**: An optional reference to the next handler in the chain, which is invoked if this handler cannot classify the request.

#### Example Usage

```python
# Example demonstrating how to use the DotIPv4IPTypeClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import DotIPv4IPTypeClassifierHandler

# Create an instance of the handler
dot_ipv4_classifier = DotIPv4IPTypeClassifierHandler()

# Define a request as a dotted-decimal IPv4 string
request_ipv4 = "192.168.1.1"

# Classify the request
result = dot_ipv4_classifier.handle(request_ipv4)
if result == IPType.IPv4:
    print("The IP is classified as IPv4.")
else:
    print("The IP could not be classified as IPv4.")
```
Expected Output:
```
The IP is classified as IPv4.
```

### 3. `OctetIPv4NetmaskClassifierHandler`
#### Description

This concrete handler class specializes in classifying IPv4 netmasks that are represented as a list of octets. It inherits from `IPv4NetmaskClassifierHandler` and focuses on validating and classifying netmasks by ensuring they consist of contiguous ones followed by zeros, which is characteristic of valid IPv4 netmasks. If the netmask cannot be classified or validated by this handler, the request is passed along to the next handler in the chain of responsibility.

#### Inherits: `IPv4NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Examines the provided request, which should be a list of octets, to determine if it represents a valid IPv4 netmask. If the netmask is valid, it is classified as such; otherwise, the request is forwarded to the next handler.
  - **Parameters**:
    - `request (Any)`: The netmask to handle, typically a list of octets.
  - **Returns**:
    - `IPType`: `IPType.IPv4` if the netmask is valid, otherwise the result from the next handler.
  
- **_validate(request: List[Octet]) -> bool**: Checks if the provided netmask (a list of octets) consists of contiguous ones followed by zeros, validating it as a proper IPv4 netmask.
  - **Parameters**:
    - `request (List[Octet])`: A list of octets representing the netmask.
  - **Returns**:
    - `bool`: True if the netmask is valid (contiguous ones followed by zeros), otherwise False.

#### Properties

- **next_handler**: Holds a reference to the next handler in the chain, used if this handler cannot classify the request.

#### Example Usage

```python
# Example showing how to use the OctetIPv4NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_type_classifiers import OctetIPv4NetmaskClassifierHandler

# Create an instance of the handler
ipv4_netmask_classifier = OctetIPv4NetmaskClassifierHandler()

# Define a request as a list of octets for a typical subnet mask
request_ipv4_netmask = [
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('11111111'),  # 255
    OctetFlyWeightFactory.get_octet('00000000')  # 0
]

# Classify the netmask
result = ipv4_netmask_classifier.handle(request_ipv4_netmask)
if result == IPType.IPv4:
    print("The netmask is classified as IPv4.")
else:
    print("The netmask could not be classified as IPv4.")
```
Expected Output:
```
The netmask is classified as IPv4.
```

### 4. `DotIPv4NetmaskClassifierHandler`
#### Description

This concrete handler class is designed to classify IPv4 netmasks presented in the dotted-decimal string format. It extends the `IPv4NetmaskClassifierHandler` and specifically handles the validation and classification of netmasks that need to be represented in the common human-readable dotted format (e.g., "255.255.255.0"). This handler ensures that the netmask string is correctly formatted and contains valid subnet mask values before classifying it as IPv4. If the netmask does not meet these criteria, the handler forwards the request to the next handler in the chain.

#### Inherits: `IPv4NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Determines if the input string is a valid dotted-decimal IPv4 netmask. If valid, the netmask is classified as IPv4; otherwise, it is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically expected to be a string representing a netmask in dotted-decimal format.
  - **Returns**:
    - `IPType`: `IPType.IPv4` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the input string represents a dotted-decimal IPv4 netmask by checking for the correct format and valid subnet values.
  - **Parameters**:
    - `request (str)`: A string representing a netmask in dotted-decimal format.
  - **Returns**:
    - `bool`: True if the string is a correctly formatted and valid dotted-decimal IPv4 netmask, otherwise False.

#### Properties

- **next_handler**: An optional property that holds a reference to the next handler in the chain, used if this handler cannot definitively classify the netmask.

#### Example Usage

```python
# Example showing how to use the DotIPv4NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import DotIPv4NetmaskClassifierHandler

# Create an instance of the handler
dot_ipv4_netmask_classifier = DotIPv4NetmaskClassifierHandler()

# Define a request as a dotted-decimal netmask string
request_ipv4_netmask = "255.255.255.0"

# Classify the netmask
result = dot_ipv4_netmask_classifier.handle(request_ipv4_netmask)
if result == IPType.IPv4:
    print("The netmask is classified as IPv4.")
else:
    print("The netmask could not be classified as IPv4.")
```
Expected Output:
```
The netmask is classified as IPv4.
```

### 5. `CIDRIPv4NetmaskClassifierHandler`
#### Description

This concrete handler class specializes in classifying IPv4 netmasks represented in CIDR notation (e.g., "/24"). It inherits from `IPv4NetmaskClassifierHandler` and is designed to validate and classify CIDR-format netmasks by converting the CIDR notation into a binary string and checking if it forms a valid subnet mask pattern of contiguous ones followed by zeros. If the request does not conform to this pattern or is otherwise unclassifiable, it is forwarded to the next handler in the chain.

#### Inherits: `IPv4NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Assesses whether the provided CIDR notation string represents a valid IPv4 netmask. If valid, the netmask is classified accordingly; otherwise, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically expected to be a string in CIDR notation.
  - **Returns**:
    - `IPType`: `IPType.IPv4` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the CIDR notation string represents a valid IPv4 netmask by generating a corresponding binary string and checking the format.
  - **Parameters**:
    - `request (str)`: A string representing a netmask in CIDR notation.
  - **Returns**:
    - `bool`: True if the CIDR string represents a valid IPv4 netmask, otherwise False.

#### Properties

- **next_handler**: An optional property that holds a reference to the next handler in the chain, activated if this handler cannot definitively classify the netmask.

#### Example Usage

```python
# Example demonstrating how to use the CIDRIPv4NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import CIDRIPv4NetmaskClassifierHandler

# Create an instance of the handler
cidr_ipv4_netmask_classifier = CIDRIPv4NetmaskClassifierHandler()

# Define a request as a CIDR notation netmask string
request_ipv4_netmask = "/24"

# Classify the netmask
result = cidr_ipv4_netmask_classifier.handle(request_ipv4_netmask)
if result == IPType.IPv4:
    print("The netmask is classified as IPv4.")
else:
    print("The netmask could not be classified as IPv4.")
```
Expected Output:
```
The netmask is classified as IPv4.
```

### 6. `OctetIPv6IPTypeClassifierHandler`
#### Description

This concrete handler class is designed to classify IPv6 addresses based on the count of octets provided. It inherits from `IPv6IPTypeClassifierHandler` and specifically targets requests that present IPv6 addresses as a list of 16 octets. This handler verifies that the list contains the exact number of octets required for a valid IPv6 address. If the request meets this criterion, it is classified as IPv6; otherwise, it is forwarded to the next handler in the chain for further processing.

#### Inherits: `IPv6IPTypeClassifierHandler`

#### Methods

- **handle(request: Any)**: Evaluates whether the request, expected to be a list of octets, contains exactly 16 octets, which confirms it as a valid IPv6 address. If confirmed, the address is classified as IPv6; if not, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a list of octets representing an IPv6 address.
  - **Returns**:
    - `IPType`: `IPType.IPv6` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: List[Octet]) -> bool**: Checks if the provided list of octets meets the IPv6 requirement of exactly 16 octets.
  - **Parameters**:
    - `request (List[Octet])`: A list of octets representing the IPv6 address.
  - **Returns**:
    - `bool`: True if the list contains exactly 16 octets, indicating a valid IPv6 address, otherwise False.

#### Properties

- **next_handler**: Holds a reference to the next handler in the chain, used if this handler cannot definitively classify the request.

#### Example Usage

```python
# Example showing how to use the OctetIPv6IPTypeClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_type_classifiers import OctetIPv6IPTypeClassifierHandler

# Create an instance of the handler
ipv6_classifier = OctetIPv6IPTypeClassifierHandler()

# Define a request with exactly 16 octets, representing an IPv6 address
request_ipv6 = [
    OctetFlyWeightFactory.get_octet('00100000') for _ in range(16)
]

# Classify the request
result = ipv6_classifier.handle(request_ipv6)
if result == IPType.IPv6:
    print("The IP is classified as IPv6.")
else:
    print("The IP could not be classified as IPv6.")
```
Expected Output:
```
The IP is classified as IPv6.
```

### 7. `ColonIPv6IPTypeClassifierHandler`
#### Description

This concrete handler class is tasked with classifying IPv6 addresses represented in colon-hexadecimal notation (e.g., "2001:0db8::1"). It inherits from `IPv6IPTypeClassifierHandler` and is designed to validate and classify IPv6 addresses that are formatted in this common and compact textual representation. If the provided string correctly represents an IPv6 address following the specific formatting rules, the address is classified as IPv6. If it does not meet these criteria, the request is forwarded to the next handler in the chain.

#### Inherits: `IPv6IPTypeClassifierHandler`

#### Methods

- **handle(request: Any)**: Assesses the input string to determine if it is a valid IPv6 address in colon-hexadecimal format. If valid, the address is classified as IPv6; otherwise, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically expected to be a string representing an IPv6 address in colon-hexadecimal format.
  - **Returns**:
    - `IPType`: `IPType.IPv6` if the request is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the provided string is a correctly formatted colon-hexadecimal IPv6 address. This involves expanding abbreviated zeros and verifying the overall structure.
  - **Parameters**:
    - `request (str)`: A string representing an IPv6 address in colon-hexadecimal format.
  - **Returns**:
    - `bool`: True if the string is a valid IPv6 address in the correct format, otherwise False.

#### Properties

- **next_handler**: An optional property that holds a reference to the next handler in the chain, used if this handler cannot definitively classify the address.

#### Example Usage

```python
# Example demonstrating how to use the ColonIPv6IPTypeClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import ColonIPv6IPTypeClassifierHandler

# Create an instance of the handler
colon_ipv6_classifier = ColonIPv6IPTypeClassifierHandler()

# Define a request as a colon-hexadecimal IPv6 string
request_ipv6 = "2001:0db8::1"

# Classify the request
result = colon_ipv6_classifier.handle(request_ipv6)
if result == IPType.IPv6:
    print("The IP is classified as IPv6.")
else:
    print("The IP could not be classified as IPv6.")
```
Expected Output:
```
The IP is classified as IPv6.
```

### 8. `OctetIPv6NetmaskClassifierHandler`
#### Description

This concrete handler class is dedicated to classifying IPv6 netmasks that are represented as a list of octets. It extends the `IPv6NetmaskClassifierHandler` and focuses on validating and classifying netmasks based on the presence of contiguous ones followed by zeros across 16 octets, which characterizes a valid IPv6 netmask. If the netmask is confirmed as valid, it is classified as IPv6; if not, the request is passed to the next handler in the chain.

#### Inherits: `IPv6NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Evaluates the provided list of octets to determine if they represent a valid IPv6 netmask. If the netmask meets the criteria, it is classified as IPv6; otherwise, the request is forwarded to the next handler for further evaluation.
  - **Parameters**:
    - `request (Any)`: The netmask to handle, typically a list of octets.
  - **Returns**:
    - `IPType`: `IPType.IPv6` if the netmask is valid, otherwise the result from the next handler.
  
- **_validate(request: List[Octet]) -> bool**: Validates whether the provided list of octets forms a netmask with contiguous ones followed by zeros, which is essential for a proper IPv6 netmask.
  - **Parameters**:
    - `request (List[Octet])`: A list of octets representing the netmask.
  - **Returns**:
    - `bool`: True if the netmask consists of contiguous ones followed by zeros, indicating a valid IPv6 netmask, otherwise False.

#### Properties

- **next_handler**: An optional property that retains a reference to the next handler in the chain, used if this handler cannot definitively classify the netmask.

#### Example Usage

```python
# Example demonstrating how to use the OctetIPv6NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.ipservice.ip_type_classifiers import OctetIPv6NetmaskClassifierHandler

# Create an instance of the handler
ipv6_netmask_classifier = OctetIPv6NetmaskClassifierHandler()

# Define a request as a list of octets for a typical subnet mask
request_ipv6_netmask = [
                           OctetFlyWeightFactory.get_octet('11111111') for _ in range(8)
                       ] + [OctetFlyWeightFactory.get_octet('00000000') for _ in range(8)]

# Classify the netmask
result = ipv6_netmask_classifier.handle(request_ipv6_netmask)
if result == IPType.IPv6:
    print("The netmask is classified as IPv6.")
else:
    print("The netmask could not be classified as IPv6.")
```
Expected Output:
```
The netmask is classified as IPv6.
```

### 9. `ColonIPv6NetmaskClassifierHandler`
#### Description

This concrete handler class specializes in classifying IPv6 netmasks that are represented in colon-hexadecimal notation (e.g., "ffff:ffff::"). It inherits from `IPv6NetmaskClassifierHandler` and is designed to handle and validate IPv6 netmasks expressed in this common textual format. The handler checks for correct formatting and the proper sequence of contiguous ones followed by zeros in the binary form of the netmask. If the netmask meets these criteria, it is classified as IPv6; if not, the request is forwarded to the next handler in the chain.

#### Inherits: `IPv6NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Assesses the input string to determine if it represents a valid IPv6 netmask in colon-hexadecimal format. If valid, the netmask is classified as IPv6; otherwise, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically a string representing an IPv6 netmask in colon-hexadecimal format.
  - **Returns**:
    - `IPType`: `IPType.IPv6` if the netmask is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the provided string correctly represents an IPv6 netmask in colon-hexadecimal format by expanding the notation and verifying the binary sequence of ones followed by zeros.
  - **Parameters**:
    - `request (str)`: A string representing an IPv6 netmask in colon-hexadecimal format.
  - **Returns**:
    - `bool`: True if the string is a valid IPv6 netmask in the correct format, otherwise False.

#### Properties

- **next_handler**: Holds a reference to the next handler in the chain, used if this handler cannot definitively classify the netmask.

#### Example Usage

```python
# Example showing how to use the ColonIPv6NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import ColonIPv6NetmaskClassifierHandler

# Create an instance of the handler
colon_ipv6_netmask_classifier = ColonIPv6NetmaskClassifierHandler()

# Define a request as a colon-hexadecimal IPv6 netmask string
request_ipv6_netmask = "ffff:ffff:ffff:ffff:0:0:0:0"

# Classify the netmask
result = colon_ipv6_netmask_classifier.handle(request_ipv6_netmask)
if result == IPType.IPv6:
    print("The netmask is classified as IPv6.")
else:
    print("The netmask could not be classified as IPv6.")
```
Expected Output:
```
The netmask is classified as IPv6.
```

### 10. `CIDRIPv6NetmaskClassifierHandler`
#### Description

This concrete handler class specializes in classifying IPv6 netmasks represented in CIDR notation (e.g., "/64"). It inherits from `IPv6NetmaskClassifierHandler` and is designed to validate and classify IPv6 netmasks based on the number of contiguous ones specified in the CIDR format. This handler converts the CIDR string into a binary representation and checks if it forms a valid netmask pattern of contiguous ones followed by zeros. If the CIDR notation represents a valid IPv6 netmask, it is classified accordingly; otherwise, the request is forwarded to the next handler in the chain.

#### Inherits: `IPv6NetmaskClassifierHandler`

#### Methods

- **handle(request: Any)**: Assesses whether the provided CIDR notation string represents a valid IPv6 netmask. If valid, the netmask is classified as IPv6; otherwise, the request is passed to the next handler.
  - **Parameters**:
    - `request (Any)`: The request to handle, typically expected to be a string in CIDR notation.
  - **Returns**:
    - `IPType`: `IPType.IPv6` if the netmask is valid, otherwise the result from the next handler.
  
- **_validate(request: str) -> bool**: Validates whether the CIDR notation string represents a valid IPv6 netmask by generating a corresponding binary string and checking the format.
  - **Parameters**:
    - `request (str)`: A string representing a netmask in CIDR notation.
  - **Returns**:
    - `bool`: True if the CIDR string represents a valid IPv6 netmask, otherwise False.

#### Properties

- **next_handler**: An optional property that retains a reference to the next handler in the chain, used if this handler cannot definitively classify the netmask.

#### Example Usage

```python
# Example demonstrating how to use the CIDRIPv6NetmaskClassifierHandler
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.ipservice.ip_type_classifiers import CIDRIPv6NetmaskClassifierHandler

# Create an instance of the handler
cidr_ipv6_netmask_classifier = CIDRIPv6NetmaskClassifierHandler()

# Define a request as a CIDR notation netmask string
request_ipv6_netmask = "/64"

# Classify the netmask
result = cidr_ipv6_netmask_classifier.handle(request_ipv6_netmask)
if result == IPType.IPv6:
    print("The netmask is classified as IPv6.")
else:
    print("The netmask could not be classified as IPv6.")
```
Expected Output:
```
The netmask is classified as IPv6.
```
