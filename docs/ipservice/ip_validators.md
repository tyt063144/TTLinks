# `IPv4IPValidatorHandler`

1. `IPv4IPBinaryValidator` - The `IPv4IPBinaryValidator` class validates IPv4 addresses provided as lists of binary class instances. It checks each octet to ensure it is within the valid range (0-255). The method returns the IPType.IPv4 if the address is valid or None otherwise.
```python
from ttlinks.ipservice.ip_validators import IPv4IPBinaryValidator
from ttlinks.ipservice.ip_utils import IPType
from ttlinks.common.base_utils import BinaryFlyWeightFactory


# Example IPv4 address in binary class format
ipv4_binary = [
  BinaryFlyWeightFactory.get_binary_class('11000000'),  # 192
  BinaryFlyWeightFactory.get_binary_class('10101000'),  # 168
  BinaryFlyWeightFactory.get_binary_class('01100100'),  # 100
  BinaryFlyWeightFactory.get_binary_class('10010110')   # 150
]
validator = IPv4IPBinaryValidator()
result = validator.handle(ipv4_binary)

if result == IPType.IPv4:
  print("The IPv4 binary address is valid.")
else:
  print("The IPv4 binary address is invalid.")
```
Expected Output:
```
The IPv4 binary address is valid.
```
2. `IPv4IPStringValidator` - The `IPv4IPStringValidator` class validates IPv4 addresses provided in dot-decimal notation. It converts the string representation of the IP address into binary class instances and validates each octet to ensure it is within the valid range. The method returns IPType.IPv4 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv4IPStringValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv4 address in dot-decimal notation
ipv4_string = "192.168.100.150"
validator = IPv4IPStringValidator()
result = validator.handle(ipv4_string)

if result == IPType.IPv4:
    print("The IPv4 address string is valid.")
else:
    print("The IPv4 address string is invalid.")
```
Expected Output:
```
The IPv4 address string is valid.
```
3. `IPv4NetmaskBinaryValidator` - The `IPv4NetmaskBinaryValidator` class validates IPv4 netmasks provided as binary class instances. It ensures that the netmask consists of a contiguous sequence of 1s followed by 0s. The method returns IPType.IPv4 if the netmask is valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv4NetmaskBinaryValidator
from ttlinks.common.base_utils import BinaryFlyWeightFactory
from ttlinks.ipservice.ip_utils import IPType

# Example IPv4 netmask in binary class format
netmask_binary = [
    BinaryFlyWeightFactory.get_binary_class('11111111'),  # 255
    BinaryFlyWeightFactory.get_binary_class('11111111'),  # 255
    BinaryFlyWeightFactory.get_binary_class('11111111'),  # 255
    BinaryFlyWeightFactory.get_binary_class('00000000')   # 0
]
validator = IPv4NetmaskBinaryValidator()
result = validator.handle(netmask_binary)

if result == IPType.IPv4:
    print("The IPv4 binary netmask is valid.")
else:
    print("The IPv4 binary netmask is invalid.")
```
Expected Output:
```
The IPv4 binary netmask is valid.
```
4. `IPv4NetmaskDotDecimalValidator` - The `IPv4NetmaskDotDecimalValidator` class validates IPv4 netmasks provided in dot-decimal notation. It converts the string representation of the netmask into binary class instances and ensures that it represents a valid contiguous sequence of 1s followed by 0s. The method returns IPType.IPv4 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv4NetmaskDotDecimalValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv4 netmask in dot-decimal notation
netmask_string = "255.255.255.0"
validator = IPv4NetmaskDotDecimalValidator()
result = validator.handle(netmask_string)

if result == IPType.IPv4:
    print("The IPv4 netmask string is valid.")
else:
    print("The IPv4 netmask string is invalid.")
```
Expected Output:
```
The IPv4 netmask string is valid.
```
5. `IPv4NetmaskCIDRValidator` - The `IPv4NetmaskCIDRValidator` class validates IPv4 netmasks provided in CIDR notation (e.g., /24). It converts the CIDR representation into a binary mask and validates that it represents a valid contiguous sequence of 1s followed by 0s. The method returns IPType.IPv4 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv4NetmaskCIDRValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv4 netmask in CIDR notation
netmask_cidr = "/24"
validator = IPv4NetmaskCIDRValidator()
result = validator.handle(netmask_cidr)

if result == IPType.IPv4:
    print("The IPv4 CIDR netmask is valid.")
else:
    print("The IPv4 CIDR netmask is invalid.")
```
Expected Output:
```
The IPv4 CIDR netmask is valid.
```
   
# `IPv6IPValidatorHandler`
1. `IPv6IPBinaryValidator` - The `IPv6IPBinaryValidator` class validates IPv6 addresses provided as lists of binary class instances. It ensures that each segment is within the valid range. The method returns IPType.IPv6 if the address is valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv6IPBinaryValidator
from ttlinks.common.base_utils import BinaryFlyWeightFactory
from ttlinks.ipservice.ip_utils import IPType

# Example IPv6 address in binary class format. Total of 16 in length
ipv6_binary = [
    BinaryFlyWeightFactory.get_binary_class('00100000'),  # 2001:
    BinaryFlyWeightFactory.get_binary_class('00000001'),  # 2001:
    BinaryFlyWeightFactory.get_binary_class('00001101'),  # db8::
    BinaryFlyWeightFactory.get_binary_class('10111000'),  # db8::
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # ::
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # ::
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # ::
    # ...
    BinaryFlyWeightFactory.get_binary_class('00000001')   # 1
]
validator = IPv6IPBinaryValidator()
result = validator.handle(ipv6_binary)

if result == IPType.IPv6:
    print("The IPv6 binary address is valid.")
else:
    print("The IPv6 binary address is invalid.")
```
Expected Output:
```
The IPv6 binary address is valid.
   ```
2. `IPv6IPStringValidator` - The `IPv6IPStringValidator` class validates IPv6 addresses provided in colon-separated hexadecimal notation as a string (e.g., 2001:0db8::1). It converts the string representation into binary class instances and ensures that the address segments are within valid ranges. The method returns IPType.IPv6 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv6IPStringValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv6 address in colon-separated hexadecimal notation
ipv6_string = "2001:0db8::1"
validator = IPv6IPStringValidator()
result = validator.handle(ipv6_string)

if result == IPType.IPv6:
    print("The IPv6 address string is valid.")
else:
    print("The IPv6 address string is invalid.")
```
Expected Output:
```
The IPv6 address string is valid.
```
3. `IPv6NetmaskBinaryValidator` - The `IPv6NetmaskBinaryValidator` class validates IPv6 netmasks provided as binary class instances. It ensures that the netmask consists of a valid contiguous sequence of 1s followed by 0s. The method returns IPType.IPv6 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv6NetmaskBinaryValidator
from ttlinks.common.base_utils import BinaryFlyWeightFactory
from ttlinks.ipservice.ip_utils import IPType
# Example IPv6 netmask in binary class format. Total of 16 in length
netmask_binary = [
  BinaryFlyWeightFactory.get_binary_class('11111111'),
  BinaryFlyWeightFactory.get_binary_class('11111111'),
  # BinaryFlyWeightFactory.get_binary_class('11111111') x 10 ...
  BinaryFlyWeightFactory.get_binary_class('00000000'),
  BinaryFlyWeightFactory.get_binary_class('00000000'),
  BinaryFlyWeightFactory.get_binary_class('00000000'),  
  BinaryFlyWeightFactory.get_binary_class('00000000'),
]
validator = IPv6NetmaskBinaryValidator()
result = validator.handle(netmask_binary)

if result == IPType.IPv6:
  print("The IPv6 binary netmask is valid.")
else:
  print("The IPv6 binary netmask is invalid.")
```
Expected Output:
```
The IPv6 binary netmask is valid.
```
4. `IPv6NetmaskColonHexValidator` - The `IPv6NetmaskColonHexValidator` class validates IPv6 netmasks provided in colon-separated hexadecimal format (e.g., FFFF:FFFF:FFFF:0000::). It converts the string representation into binary class instances and ensures that the netmask is valid. The method returns IPType.IPv6 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv6NetmaskColonHexValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv6 netmask in colon-separated hexadecimal notation
netmask_string = "FFFF:FFFF:FFFF:0000::"
validator = IPv6NetmaskColonHexValidator()
result = validator.handle(netmask_string)

if result == IPType.IPv6:
    print("The IPv6 colon-separated hexadecimal netmask is valid.")
else:
    print("The IPv6 colon-separated hexadecimal netmask is invalid.")
```
Expected Output:
```
The IPv6 colon-separated hexadecimal netmask is valid.
```
5. `IPv6NetmaskCIDRValidator` - The `IPv6NetmaskCIDRValidator` class validates IPv6 netmasks provided in CIDR notation (e.g., /64). It converts the CIDR notation into binary class instances and ensures that the netmask consists of a valid contiguous sequence of 1s followed by 0s. The method returns IPType.IPv6 if valid, otherwise None.
```python
from ttlinks.ipservice.ip_validators import IPv6NetmaskCIDRValidator
from ttlinks.ipservice.ip_utils import IPType

# Example IPv6 netmask in CIDR notation
netmask_cidr = "/64"
validator = IPv6NetmaskCIDRValidator()
result = validator.handle(netmask_cidr)

if result == IPType.IPv6:
    print("The IPv6 CIDR netmask is valid.")
else:
    print("The IPv6 CIDR netmask is invalid.")
```
Expected Output:
```
The IPv6 CIDR netmask is valid.
```