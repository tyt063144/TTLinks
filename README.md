## TTLLinks IP and MAC Address Management and Conversion Toolkit
### Overview
This project provides a comprehensive toolkit for managing, validating, and converting IP addresses in both IPv4 and IPv6 formats, with planned support for MAC address management. Leveraging design patterns such as Chain of Responsibility and Flyweight, this toolkit ensures efficient and flexible handling of IP and MAC-related operations. The modular design allows for easy integration and extension within larger networking and automation systems.

### Installation
This project is available on PyPI and can be installed using pip:
```bash
pip install ttlinks
```

### Usage
After installation, you can import the necessary classes and utilities from the ttlinks package:
```python
from ttlinks.common.base_utils import BinaryClass
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr, IPv4NetMask, IPv6NetMask
from ttlinks.ipservice.converters import NumeralConverter
from ttlinks.ipservice.ip_utils import NetToolsSuite, IPType
# ...more
```

### Features
#### Common
1. Binary Management
* The `BinaryClass` offers robust management of binary strings, ensuring that the string contains only '0's and '1's through validation. It also supports conversion to lists of integers and provides string representations that are useful for debugging and display. Additionally, BinaryClass serves as a foundational layer in the `ipservice` and `macservice` modules, underpinning all IP and MAC address operations.
* Create BinaryClass
  ```python
  from ttlinks.common.base_utils import BinaryClass
  binary_class = BinaryClass('11111110')
  print(binary_class)
  print(binary_class.binary_digits())
  ```
  Expected Output:
  ```
  11111110
  [1, 1, 1, 1, 1, 1, 1, 0]
  ```
2. Flyweight Pattern for Memory Optimization:
* The `BinaryFlyWeightFactory` and `BinaryFlyWeight` classes implement the Flyweight pattern to manage instances of `BinaryClass`. This pattern minimizes memory usage by sharing instances of `BinaryClass` with identical binary strings across the application.
* Memory-Efficient Management of Binary Strings:
  ```python
  from ttlinks.common.base_utils import BinaryFlyWeightFactory
  binary1 = BinaryFlyWeightFactory.get_binary_class("101010")
  binary2 = BinaryFlyWeightFactory.get_binary_class("101010")
  print(binary1 is binary2)  
  ```
  Expected Output:
  ```
  True  # since they share the same instance
  ```
3. Chain of Responsibility Pattern:
   * The `CoRHandler` abstract base class sets up the framework for building a chain of responsibility, allowing different handlers to process requests in a sequence. This pattern is extensively used for IP/MAC validation and conversion tasks, enabling modular and flexible processing.

#### Converters
1. The `NumeralConverter` class in the `converters` module allows you to convert between binary, decimal, and hexadecimal formats easily.
   1. Binary to Decimal Conversion
   * Convert a binary string to its decimal representation:
     ```python
     from ttlinks.ipservice.converters import NumeralConverter
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
   2. Decimal to Binary Conversion
   * Convert a decimal number to a binary string, right-justified to 8 bits by default:
     ```python
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
   3. Binary to Hexadecimal Conversion
   * Convert a binary string to its hexadecimal representation:
     ```python
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
   4. Hexadecimal to Binary Conversion
   * Convert a binary string to its hexadecimal representation:
     ```python
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
2. IP Converters<br>
The IP converters in the converters module allow you to handle different IP address formats using the Chain of Responsibility pattern. Below are examples demonstrating how to convert IP addresses in various formats.
   1. `DotDecimalIPv4ConverterHandler`
   * Convert a standard dot-decimal IPv4 address to its binary representation:
    ```python
    from ttlinks.ipservice.converters import DotDecimalIPv4ConverterHandler
    
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
   2. `CIDRIPv4ConverterHandler`
   * Convert a CIDR notation IPv4 address to its binary representation:
    ```python
    from ttlinks.ipservice.converters import CIDRIPv4ConverterHandler

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
   3. `BinaryIPv4ConverterHandler`
   * Convert an IPv4 address represented as a list of `BinaryClass` instances to its processed binary format:
    ```python
    from ttlinks.ipservice.converters import BinaryIPv4ConverterHandler
    from ttlinks.common.base_utils import BinaryClass

    binary_ipv4 = [
        BinaryClass('11000000'),  # 192
        BinaryClass('10101000'),  # 168
        BinaryClass('00000001'),  # 1
        BinaryClass('00000001')   # 1
    ]
    converter = BinaryIPv4ConverterHandler()
    binary_classes = converter.handle(binary_ipv4)
    
    print("Processed Binary IPv4:", [str(bc) for bc in binary_classes])
    ```
    Expected Output:
    ```
    Processed Binary IPv4: ['11000000', '10101000', '00000001', '00000001']
    ```
   4. `BinaryDigitsIPv4ConverterHandler`
   * Convert a list of binary digits (0s and 1s) representing an IPv4 address to `BinaryClass` instances:
    ```python
    from ttlinks.ipservice.converters import BinaryDigitsIPv4ConverterHandler

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
    ```python
    Binary Digits as BinaryClass: ['11000000', '10101000', '00000001', '00000001']
    CIDR as BinaryClass: ['11111111', '11111111', '11111111', '10000000']
    ```


### Contributing
Contributions to this project are welcome! Please feel free to submit issues or pull requests on <a href='https://github.com/tyt063144/TTLinks'>GitHub</a>. Ensure your code follows the established style and passes all tests.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Contact
For further information, please contact Yantao at tyt063144@gmail.com.