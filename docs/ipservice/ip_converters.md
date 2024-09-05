
# `NumeralConverter`
The `NumeralConverter` class in the `converters` module allows you to convert between binary, decimal, and hexadecimal formats easily.

```python
from ttlinks.ipservice.ip_converters import NumeralConverter
```
1. `binary_to_decimal` - Convert a binary string to its decimal representation:
```python
from ttlinks.ipservice.ip_converters import NumeralConverter
octet1 = NumeralConverter.binary_to_decimal('11000000')
octet2 = NumeralConverter.binary_to_decimal('10101000')
octet3 = NumeralConverter.binary_to_decimal('00000001')
octet4 = NumeralConverter.binary_to_decimal('00000001')
print(f"{octet1}.{octet2}.{octet3}.{octet4}")
```

Expected Output:
```
192.168.1.1
```

2. `decimal_to_binary` - Convert a decimal number to a binary string, right-justified to 8 bits by default:
```python
from ttlinks.ipservice.ip_converters import NumeralConverter

decimal_number = 172
binary_string = NumeralConverter.decimal_to_binary(decimal_number)
print("Decimal:", decimal_number)
print("Binary (8 bits):", binary_string)
```
Expected Output:
```
Decimal: 172
Binary (8 bits): 10101100
```
3. `binary_to_hexadecimal` -  Convert a binary string to its hexadecimal representation:
```python
from ttlinks.ipservice.ip_converters import NumeralConverter

binary_string = "11110000"
hexadecimal_string = NumeralConverter.binary_to_hexadecimal(binary_string)
print("Binary:", binary_string)
print("Hexadecimal:", hexadecimal_string)
```
Expected Output:
```
Binary: 11110000
Hexadecimal: F0
```
4. `hexadecimal_to_binary` - Convert a binary string to its hexadecimal representation:
```python
from ttlinks.ipservice.ip_converters import NumeralConverter

hexadecimal_string = "F0"
binary_string = NumeralConverter.hexadecimal_to_binary(hexadecimal_string)
print("Hexadecimal:", hexadecimal_string)
print("Binary (8 bits):", binary_string)
```
Expected Output:
```
Hexadecimal: F0
Binary (8 bits): 11110000
```

---
# IPConverterHandler
The IPConverterHandler is an abstract base class in the IP address management toolkit that implements the Chain of Responsibility pattern. It provides a framework for converting IP addresses between different formats (e.g., dot-decimal, CIDR, binary). The class defines a chainable method for handling conversion requests, allowing multiple handlers to process an IP address sequentially.
## IPv4
1. `DotDecimalIPv4ConverterHandler` - Convert a standard dot-decimal IPv4 address to its binary representation:
```python
from ttlinks.ipservice.ip_converters import DotDecimalIPv4ConverterHandler

ipv4_address = "192.168.1.1"
converter = DotDecimalIPv4ConverterHandler()
binary_classes = converter.handle(ipv4_address)

print("Dot-Decimal IPv4:", ipv4_address)
print("Binary Representation:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Dot-Decimal IPv4: 192.168.1.1 
Binary Representation: ['11000000', '10101000', '00000001', '00000001']
```
2. `CIDRIPv4ConverterHandler` - Convert a CIDR notation IPv4 address to its binary representation:
```python
from ttlinks.ipservice.ip_converters import CIDRIPv4ConverterHandler

cidr_ipv4_address = "/24"
converter = CIDRIPv4ConverterHandler()
binary_classes = converter.handle(cidr_ipv4_address)

print("CIDR IPv4:", cidr_ipv4_address)
print("Binary Network Mask:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
CIDR IPv4: /24
Binary Network Mask: ['11111111', '11111111', '11111111', '00000000']
```

3. `BinaryIPv4ConverterHandler` - Convert an IPv4 address represented as a list of `BinaryClass` instances to its processed binary format:
```python
from ttlinks.ipservice.ip_converters import BinaryIPv4ConverterHandler
from ttlinks.common.base_utils import BinaryFlyWeightFactory

binary_ipv4 = [
    BinaryFlyWeightFactory.get_binary_class('11000000'),  # 192
    BinaryFlyWeightFactory.get_binary_class('10101000'),  # 168
    BinaryFlyWeightFactory.get_binary_class('00000001'),  # 1
    BinaryFlyWeightFactory.get_binary_class('00000001')   # 1
]
converter = BinaryIPv4ConverterHandler()
binary_classes = converter.handle(binary_ipv4)
 
print("Processed Binary IPv4:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Processed Binary IPv4: ['11000000', '10101000', '00000001', '00000001']
```
4. `BinaryDigitsIPv4ConverterHandler` - Convert a list of binary digits (0s and 1s) representing an IPv4 address to `BinaryClass` instances:
```python
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler

binary_digits_ipv4 = [
    1, 1, 0, 0, 0, 0, 0, 0,  # 192
    1, 0, 1, 0, 1, 0, 0, 0,  # 168
    0, 0, 0, 0, 0, 0, 0, 1,  # 1
    0, 0, 0, 0, 0, 0, 0, 1   # 1
]
converter = BinaryDigitsIPv4ConverterHandler()
binary_classes = converter.handle(binary_digits_ipv4)
 
print("Binary Digits IPv4 as BinaryClass:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Binary Digits IPv4 as BinaryClass: ['11000000', '10101000', '00000001', '00000001']
```

5. Using a Chain of Handlers to Determine and Process an IPv4 Address:
* The chain method can validate multiple formats simultaneously, so users don't need to run handlers individually.
```python
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import CIDRIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import DotDecimalIPv4ConverterHandler
from ttlinks.ipservice.ip_converters import BinaryIPv4ConverterHandler

binary_digits_ipv4 = [
 1, 1, 0, 0, 0, 0, 0, 0,  # 192
 1, 0, 1, 0, 1, 0, 0, 0,  # 168
 0, 0, 0, 0, 0, 0, 0, 1,  # 1
 0, 0, 0, 0, 0, 0, 0, 1   # 1
]
cidr_ipv4 = "/25"
# Initialize handlers
binary_digits_handler = BinaryDigitsIPv4ConverterHandler()
binary_handler = BinaryIPv4ConverterHandler()
dot_decimal_handler = DotDecimalIPv4ConverterHandler()
cidr_handler = CIDRIPv4ConverterHandler()

# Set up the chain
binary_digits_handler.set_next(binary_handler).set_next(dot_decimal_handler).set_next(cidr_handler)

# Process the request through the chain
result_binary_digits = binary_digits_handler.handle(binary_digits_ipv4)
result_cidr = binary_digits_handler.handle(cidr_ipv4)

print("Binary Digits as BinaryClass:", [str(bc) for bc in result_binary_digits])
print("CIDR as BinaryClass:", [str(bc) for bc in result_cidr])
```
Expected Output:
```
Binary Digits as BinaryClass: ['11000000', '10101000', '00000001', '00000001']
CIDR as BinaryClass: ['11111111', '11111111', '11111111', '10000000']
```
## IPv6
1. `ColonHexIPv6ConverterHandler` - Convert a colon-separated hexadecimal IPv6 address to its binary representation:
```python
from ttlinks.ipservice.ip_converters import ColonHexIPv6ConverterHandler

ipv6_address = "2001:0db8::1"
converter = ColonHexIPv6ConverterHandler()
binary_classes = converter.handle(ipv6_address)

print("Colon-Hex IPv6:", ipv6_address)
print("Binary Representation:", [str(bc) for bc in binary_classes])
```
  Expected Output:
```
Binary Representation: ['00100000', '00000001', '00001101', '10111000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000001']
```
2. `CIDRIPv6ConverterHandler` - Convert a CIDR notation IPv6 address to its binary representation:
```python
from ttlinks.ipservice.ip_converters import CIDRIPv6ConverterHandler

cidr_ipv6_address = "/64"
converter = CIDRIPv6ConverterHandler()
binary_classes = converter.handle(cidr_ipv6_address)

print("CIDR IPv6:", cidr_ipv6_address)
print("Binary Network Mask:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Binary Network Mask: ['11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000']
```
3. `BinaryIPv6ConverterHandler` - Convert an IPv6 address represented as a list of BinaryClass instances to its processed binary format:
```python
from ttlinks.ipservice.ip_converters import BinaryIPv6ConverterHandler
from ttlinks.common.base_utils import BinaryFlyWeightFactory

binary_ipv6 = [
    BinaryFlyWeightFactory.get_binary_class('00100000'),  # 2001
    BinaryFlyWeightFactory.get_binary_class('00000001'),  # 2001
    BinaryFlyWeightFactory.get_binary_class('00001101'),  # 0db8
    BinaryFlyWeightFactory.get_binary_class('10111000'),  # 0db8
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000000'),  # 0
    BinaryFlyWeightFactory.get_binary_class('00000001')   # 1
]
converter = BinaryIPv6ConverterHandler()
binary_classes = converter.handle(binary_ipv6)

print("Processed Binary IPv6:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Processed Binary IPv6: ['00100000', '00000001', '00001101', '10111000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000001']
```
4. `BinaryDigitsIPv6ConverterHandler` - Convert a list of binary digits (0s and 1s) representing an IPv6 address to BinaryClass instances:
```python
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv6ConverterHandler

binary_digits_ipv6 = [
     0, 0, 1, 0, 0, 0, 0, 0,  # 2001
     0, 0, 0, 0, 0, 0, 0, 1,  # 2001
     0, 0, 0, 0, 1, 1, 0, 1,  # 0db8
     1, 0, 1, 1, 1, 0, 0, 0,  # 0db8
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 1  # 1
]
converter = BinaryDigitsIPv6ConverterHandler()
binary_classes = converter.handle(binary_digits_ipv6)

print("Binary Digits IPv6 as BinaryClass:", [str(bc) for bc in binary_classes])
```
Expected Output:
```
Binary Digits IPv6 as BinaryClass: ['00100000', '00000001', '00001101', '10111000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000001']
```
5. Using a Chain of Handlers to Determine and Process an IPv6 Address:
The chain method can validate multiple formats simultaneously, so users don't need to run handlers individually.
```python
from ttlinks.ipservice.ip_converters import ColonHexIPv6ConverterHandler
from ttlinks.ipservice.ip_converters import CIDRIPv6ConverterHandler
from ttlinks.ipservice.ip_converters import BinaryIPv6ConverterHandler
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv6ConverterHandler

binary_digits_ipv6 = [
     0, 0, 1, 0, 0, 0, 0, 0,  # 2001
     0, 0, 0, 0, 0, 0, 0, 1,  # 2001
     0, 0, 0, 0, 1, 1, 0, 1,  # 0db8
     1, 0, 1, 1, 1, 0, 0, 0,  # 0db8
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 0,  # 0
     0, 0, 0, 0, 0, 0, 0, 1  # 1
 ]
cidr_ipv6 = "/64"
# Initialize handlers
binary_digits_handler = BinaryDigitsIPv6ConverterHandler()
binary_handler = BinaryIPv6ConverterHandler()
colon_hex_handler = ColonHexIPv6ConverterHandler()
cidr_handler = CIDRIPv6ConverterHandler()

# Set up the chain
binary_digits_handler.set_next(binary_handler).set_next(colon_hex_handler).set_next(cidr_handler)

# Process the request through the chain
result_binary_digits = binary_digits_handler.handle(binary_digits_ipv6)
result_cidr = binary_digits_handler.handle(cidr_ipv6)

print("Binary Digits as BinaryClass:", [str(bc) for bc in result_binary_digits])
print("CIDR as BinaryClass:", [str(bc) for bc in result_cidr])
```
Expected Output:
```
Binary Digits as BinaryClass: ['00100000', '00000001', '00001101', '10111000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000001']
CIDR as BinaryClass: ['11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000']
```