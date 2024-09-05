# 1. `IPv4Addr`

The `IPv4Addr` class is designed to handle and validate IPv4 addresses, ensuring they comply with IPv4 standards.

## Properties
- **`_address`**: A list of `BinaryClass` instances representing the validated IPv4 address.

## Methods
- **`_validate(address)`**: Validates the provided IPv4 address using both binary and string formats. Raises a `ValueError` if the address is invalid.
- **`get_binary_strings()`**: Returns a concatenated string of binary values from the IPv4 address.
- **`get_binary_digits()`**: Generates each binary digit in the IPv4 address as integers.
- **`__str__()`**: Returns the standard dot-separated decimal format of the IPv4 address.
- **`__repr__()`**: Provides a detailed representation of the IPv4Addr instance for debugging purposes.

## Usage Example
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv4Addr

# Example IPv4 address in binary class format
ipv4_binary = [
    BinaryClass('11000000'),  # Represents 192
    BinaryClass('10101000'),  # Represents 168
    BinaryClass('00000001'),  # Represents 1
    BinaryClass('00000001')  # Represents 1
]
ipv4_addr1 = IPv4Addr(ipv4_binary)
print(f'Binary string is: {ipv4_addr1.get_binary_strings()}')
print(f'Binary digits is: {ipv4_addr1.get_binary_digits()}')
print(list(ipv4_addr1.get_binary_digits()))
print(str(ipv4_addr1))
print(repr(ipv4_addr1))
print('---')
ipv4_addr2 = IPv4Addr('8.8.8.8')
print(f'Binary string is: {ipv4_addr2.get_binary_strings()}')
print(f'Binary digits is: {ipv4_addr2.get_binary_digits()}')
print(list(ipv4_addr2.get_binary_digits()))
print(str(ipv4_addr2))
print(repr(ipv4_addr2))
```
Expected Output:
```
Binary string is: 11000000101010000000000100000001
Binary digits is: <generator object IPv4Addr.get_binary_digits at 0x00000247CBBE8F20>
[1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
192.168.1.1
IPv4Addr('_address=[BinaryClass(binary_string='11000000'), BinaryClass(binary_string='10101000'), BinaryClass(binary_string='00000001'), BinaryClass(binary_string='00000001')])
---
Binary string is: 00001000000010000000100000001000
Binary digits is: <generator object IPv4Addr.get_binary_digits at 0x00000247CBBE9000>
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
8.8.8.8
IPv4Addr('_address=[BinaryClass(binary_string='00001000'), BinaryClass(binary_string='00001000'), BinaryClass(binary_string='00001000'), BinaryClass(binary_string='00001000')])
```

# 2. `IPv4NetMask`

The `IPv4NetMask` class is specifically designed for handling and validating IPv4 netmasks. It ensures that the netmask values and formats are correct, utilizing various validators for thorough checks.

## Properties
- **`_address`**: Stores the validated IPv4 netmask as a list of `BinaryClass` instances.

## Methods
- **`_validate(address)`**: Validates the IPv4 netmask using a chain of responsibility pattern linking different format validators. It handles both binary class list and string format inputs and raises a `ValueError` if the netmask is invalid.
- **`get_mask_size()`**: Calculates the size of the netmask by counting the number of '1's in the binary representation.
- **`get_binary_strings()`**: Concatenates the binary strings of each segment in the IPv4 netmask.
- **`get_binary_digits()`**: Generates each binary digit in the IPv4 netmask as integers.
- **`__str__()`**: Returns the standard dot-separated decimal format of the IPv4 netmask.
- **`__repr__()`**: Provides a detailed representation of the IPv4NetMask instance for debugging purposes.

## Usage Example
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv4NetMask

# Example IPv4 netmask in binary class format
ipv4_netmask_binary = [
    BinaryClass('11111111'),  # Represents 255
    BinaryClass('11111111'),  # Represents 255
    BinaryClass('11111111'),  # Represents 255
    BinaryClass('00000000')  # Represents 0
]
ipv4_netmask1 = IPv4NetMask(ipv4_netmask_binary)
print(str(ipv4_netmask1))
print("Netmask size:", ipv4_netmask1.get_mask_size())

ipv4_netmask2 = IPv4NetMask('255.255.192.0')
print(str(ipv4_netmask2))
print("Netmask size:", ipv4_netmask2.get_mask_size())

ipv4_netmask3 = IPv4NetMask('/27')
print(str(ipv4_netmask3))
print("Netmask size:", ipv4_netmask3.get_mask_size())
print("Binary string:", ipv4_netmask3.get_binary_strings())
print("Binary digits:", list(ipv4_netmask3.get_binary_digits()))
```
Expected Output:
```
255.255.255.0
Netmask size: 24
255.255.192.0
Netmask size: 18
255.255.255.224
Netmask size: 27
Binary string: 11111111111111111111111111100000
Binary digits: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
```

# 3. `IPv4WildCard`

The `IPv4WildCard` class is designed to handle IPv4 wildcard masks, which specify bits that should not match in networking operations, effectively inverting the usual function of netmasks.

## Properties
- **`_address`**: Stores the validated IPv4 wildcard mask as a list of `BinaryClass` instances.

## Methods
- **`_validate(address)`**: Validates the IPv4 wildcard mask using a chain of responsibility pattern designed for both binary and string formats. Raises a `ValueError` if the wildcard mask is invalid.
- **`get_mask_size()`**: Calculates the effective size of the wildcard mask by counting the number of '1' bits, which are treated as "don't care" positions.
- **`get_binary_strings()`**: Concatenates the binary strings of each segment in the IPv4 wildcard mask.
- **`get_binary_digits()`**: Generates each binary digit in the IPv4 wildcard mask as integers.
- **`__str__()`**: Returns the standard dot-separated decimal format of the IPv4 wildcard mask.
- **`__repr__()`**: Provides a detailed string representation of the IPv4WildCard instance for debugging purposes.

## Usage Example

```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv4WildCard

# Example IPv4 wildcard mask in binary class format
ipv4_wildcard_binary = [
    BinaryClass('00000000'),
    BinaryClass('00000000'),
    BinaryClass('00000011'),
    BinaryClass('11111111')
]
ipv4_wildcard1 = IPv4WildCard(ipv4_wildcard_binary)
print(str(ipv4_wildcard1))
print("Effective size of the wildcard mask:", ipv4_wildcard1.get_mask_size())

ipv4_wildcard2 = IPv4WildCard('0.255.0.255')
print(str(ipv4_wildcard2))
print("Effective size of the wildcard mask:", ipv4_wildcard2.get_mask_size())
print("Binary string:", ipv4_wildcard2.get_binary_strings())
print("Binary digits:", list(ipv4_wildcard2.get_binary_digits()))
```

Expected Output:
```
0.0.3.255
Effective size of the wildcard mask: 1024
0.255.0.255
Effective size of the wildcard mask: 65536
Binary string: 00000000111111110000000011111111
Binary digits: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
```

# 4. `IPv6Addr`

The `IPv6Addr` class is tailored to manage and validate IPv6 addresses, ensuring compliance with IPv6 standards.

## Properties
- **`_address`**: Stores the validated IPv6 address as a list of `BinaryClass` instances.

## Methods
- **`_validate(address)`**: Validates the provided IPv6 address using binary and colon-separated hexadecimal validation handlers. Raises a `ValueError` if the address is invalid.
- **`get_binary_strings()`**: Returns a concatenated string of binary values from the IPv6 address.
- **`get_binary_digits()`**: Generates each binary digit in the IPv6 address as integers.
- **`__str__()`**: Returns the standard colon-separated hexadecimal format of the IPv6 address.
- **`__repr__()`**: Provides a detailed representation of the IPv6Addr instance for debugging purposes.

## Usage Example
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv6Addr

# Example IPv6 address in binary class format
ipv6_binary = [
    BinaryClass('00100000'),  # Represents 2001
    BinaryClass('00000001'),  # Represents 0001
    BinaryClass('00001101'),  # Represents 0db8
    BinaryClass('10111000'),  # Represents db80
    BinaryClass('00000000'),  # Represents 0000
    # BinaryClass('00000000'), x 10
    BinaryClass('00000001')  # Represents 0001
]
ipv6_addr1 = IPv6Addr(ipv6_binary)
print(f'Binary string is: {ipv6_addr1.get_binary_strings()}')
print(f'Binary digits is: {ipv6_addr1.get_binary_digits()}')
print(list(ipv6_addr1.get_binary_digits()))
print(str(ipv6_addr1))
print(repr(ipv6_addr1))
print('---')
ipv6_addr2 = IPv6Addr('fe80::')
print(f'Binary string is: {ipv6_addr2.get_binary_strings()}')
print(f'Binary digits is: {ipv6_addr2.get_binary_digits()}')
print(list(ipv6_addr2.get_binary_digits()))
print(str(ipv6_addr2))
print(repr(ipv6_addr2))
```

Expected Output:
```
Binary string is: 00100000000000010000110110111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
Binary digits is: <generator object IPv6Addr.get_binary_digits at 0x0000027D269F90E0>
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
2001:0DB8:0000:0000:0000:0000:0000:0001
IPv6Addr('_address=[BinaryClass(binary_string='00100000'), BinaryClass(binary_string='00000001'), BinaryClass(binary_string='00001101'), BinaryClass(binary_string='10111000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000001')])
---
Binary string is: 11111110100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
Binary digits is: <generator object IPv6Addr.get_binary_digits at 0x0000027D269F90E0>
[1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FE80:0000:0000:0000:0000:0000:0000:0000
IPv6Addr('_address=[BinaryClass(binary_string='11111110'), BinaryClass(binary_string='10000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000'), BinaryClass(binary_string='00000000')])
```

## Description

The `IPv6Addr` class provides comprehensive validation through a combination of binary and hexadecimal format checks, using validators like `IPv6IPBinaryValidator` and `IPv6IPColonHexValidator`. The validation ensures that each part of the IPv6 address is within the acceptable range and correctly formatted. If validation fails, a detailed error message is raised to assist in debugging.

# 5. `IPv6NetMask`

The `IPv6NetMask` class is designed to handle and validate IPv6 netmasks, ensuring they conform to the correct formats and rules essential for IPv6 networking.

## Properties
- **`_address`**: Stores the validated IPv6 netmask as a list of `BinaryClass` instances.

## Methods
- **`_validate(address)`**: Validates the IPv6 netmask using a comprehensive chain of responsibility pattern that includes binary, colon-hexadecimal, and CIDR format validators. If the netmask is invalid, it raises a `ValueError` with a detailed error message.
- **`get_mask_size()`**: Calculates the size of the netmask by counting the number of '1' bits in its binary representation. This size is critical for defining the network and broadcast portions of an IP address range.
- **`get_binary_strings()`**: Concatenates the binary strings of each segment in the IPv6 netmask, providing a complete binary representation.
- **`get_binary_digits()`**: Generates each binary digit in the IPv6 netmask as integers, useful for operations that require bit-level manipulation.
- **`__str__()`**: Returns the standard colon-separated hexadecimal format of the IPv6 netmask, making it readable and consistent with common network configuration formats.
- **`__repr__()`**: Provides a detailed string representation of the IPv6NetMask instance, useful for debugging and logging.

## Usage Example

```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv6NetMask

# Example IPv6 netmask in binary class format
ipv6_netmask_binary = [
    BinaryClass('11111111'),  # Represents FFFF
    BinaryClass('11111111'),  # Represents FFFF
    BinaryClass('11111111'),  # Represents FFFF
    BinaryClass('11111000'),  # Represents FFF8
    BinaryClass('00000000'),  # Represents 0000
    # BinaryClass('00000000'), x 11
]
ipv6_netmask1 = IPv6NetMask(ipv6_netmask_binary)
print(str(ipv6_netmask1))
print("Netmask size:", ipv6_netmask1.get_mask_size())

ipv6_netmask2 = IPv6NetMask('FF00::')
print(str(ipv6_netmask2))
print("Netmask size:", ipv6_netmask2.get_mask_size())

ipv6_netmask3 = IPv6NetMask('/64')
print(str(ipv6_netmask3))
print("Netmask size:", ipv6_netmask3.get_mask_size())
print("Binary string:", ipv6_netmask3.get_binary_strings())
print("Binary digits:", list(ipv6_netmask3.get_binary_digits()))
```

Expected Output:
```
FFFF:FFF8:0000:0000:0000:0000:0000:0000
Netmask size: 29
FF00:0000:0000:0000:0000:0000:0000:0000
Netmask size: 8
FFFF:FFFF:FFFF:FFFF:0000:0000:0000:0000
Netmask size: 64
Binary string: 11111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000
Binary digits: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

## Description

The `IPv6NetMask` class provides crucial validation for IPv6 netmasks, utilizing a set of validators that check the netmask's compliance with IPv6 standards. This validation ensures that the netmask is appropriately structured for network operations, supporting routing and subnetting practices in IPv6 networks. The calculated mask size indicates how many bits are used for the network portion of addresses, a key factor in network design and management.

# 6. `IPv6WildCard`

The `IPv6WildCard` class handles IPv6 wildcard masks, which are used to specify bits that should not match in network configurations, essentially inverting the typical function of netmasks.

## Properties
- **`_address`**: Stores the validated IPv6 wildcard mask as a list of `BinaryClass` instances.

## Methods
- **`_validate(address)`**: Validates the IPv6 wildcard mask using a combination of binary and colon-hexadecimal format validators. If the wildcard mask is invalid, it raises a `ValueError` with detailed error messages from the validators.
- **`get_mask_size()`**: Calculates the effective size of the wildcard mask based on the count of '1' bits, which are interpreted as 'do not care' bits in the wildcard context. This calculation translates to the potential combinations that the wildcard mask covers.
- **`get_binary_strings()`**: Concatenates the binary strings of each segment in the IPv6 wildcard mask, providing a complete binary representation.
- **`get_binary_digits()`**: Generates each binary digit in the IPv6 wildcard mask as integers, which can be essential for bitwise operations in network protocols.
- **`__str__()`**: Returns the standard colon-separated hexadecimal format of the IPv6 wildcard mask, aligning it with common notation in network configurations.
- **`__repr__()`**: Provides a detailed string representation of the IPv6WildCard instance, useful for debugging purposes.

## Usage Example

```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv6WildCard

# Example IPv6 wildcard mask in binary class format
ipv6_wildcard_binary = [
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('11111111'), 
    BinaryClass('11111111'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000000'), 
    BinaryClass('00000001')  
]
ipv6_wildcard1 = IPv6WildCard(ipv6_wildcard_binary)
print(str(ipv6_wildcard1))
print("Effective size of the wildcard mask:", ipv6_wildcard1.get_mask_size())

ipv6_wildcard2 = IPv6WildCard('::AB00:0:0')
print(str(ipv6_wildcard2))
print("Effective size of the wildcard mask:", ipv6_wildcard2.get_mask_size())
print("Binary string:", ipv6_wildcard2.get_binary_strings())
print("Binary digits:", list(ipv6_wildcard2.get_binary_digits()))
```

Expected Output:
```
0000:FFFF:0000:0000:0000:0000:0000:0001
Effective size of the wildcard mask: 131072
0000:0000:0000:0000:0000:AB00:0000:0000
Effective size of the wildcard mask: 32
Binary string: 00000000000000000000000000000000000000000000000000000000000000000000000000000000101010110000000000000000000000000000000000000000
Binary digits: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

## Description

The `IPv6WildCard` class is critical for network configurations where specific bits within an IPv6 address should be ignored, such as in access control lists (ACLs) or routing policies. This class utilizes validators like `IPv6IPBinaryValidator` and `IPv6IPColonHexValidator` to ensure the wildcard mask's validity. The `get_mask_size()` method offers an understanding of the wildcard's breadth, indicating how many address combinations it can represent, which is crucial for precise network traffic management.
