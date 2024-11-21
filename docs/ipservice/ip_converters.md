# `ip_converters` Module

`ip_converters` provides functions to convert IP addresses from different formats to bytes. In this module, most of the time you will only need to use the utility functions other than the specific converter handlers. However, if you know the specific IP address format, you can use the corresponding converter handler directly. Module is designed by implementing the Chain of Responsibility pattern.


<details>
<summary>Example 1 - Utility function to convert IPv4 addresses:</summary>

```python
from ttlinks.ipservice.ip_converters import IPConverter

ip_converter = IPConverter
ipv4_bytes_1 = ip_converter.convert_to_ipv4_bytes('192.168.1.1')
ipv4_bytes_2 = ip_converter.convert_to_ipv4_bytes(65535)
ipv4_bytes_3 = ip_converter.convert_to_ipv4_bytes('/24')
ipv4_bytes_4 = ip_converter.convert_to_ipv4_bytes(
    [
        1, 1, 0, 0, 0, 0, 0, 0, 
        1, 0, 1, 0, 1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 1, 
        0, 0, 0, 0, 1, 0, 1, 0
    ])
ipv4_bytes_5 = ip_converter.convert_to_ipv4_bytes('11111111111111110000000000000000')

print('IPv4 bytes 1:', ' -> ', '%-20s'%ipv4_bytes_1, ' -> ', [octet for octet in ipv4_bytes_1])
print('IPv4 bytes 2:', ' -> ', '%-20s'%ipv4_bytes_2, ' -> ', [octet for octet in ipv4_bytes_2])
print('IPv4 bytes 3:', ' -> ', '%-20s'%ipv4_bytes_3, ' -> ', [octet for octet in ipv4_bytes_3])
print('IPv4 bytes 4:', ' -> ', '%-20s'%ipv4_bytes_4, ' -> ', [octet for octet in ipv4_bytes_4])
print('IPv4 bytes 5:', ' -> ', '%-20s'%ipv4_bytes_5, ' -> ', [octet for octet in ipv4_bytes_5])
```
Example output:
```
IPv4 bytes 1:  ->  b'\xc0\xa8\x01\x01'   ->  [192, 168, 1, 1]
IPv4 bytes 2:  ->  b'\x00\x00\xff\xff'   ->  [0, 0, 255, 255]
IPv4 bytes 3:  ->  b'\xff\xff\xff\x00'   ->  [255, 255, 255, 0]
IPv4 bytes 4:  ->  b'\xc0\xa8\x01\n'     ->  [192, 168, 1, 10]
IPv4 bytes 5:  ->  b'\xff\xff\x00\x00'   ->  [255, 255, 0, 0]
```
</details>

<details>
<summary>Example 2 - Utility function to convert IPv6 addresses:</summary>

```python
from ttlinks.ipservice.ip_address import IPv6Addr
from ttlinks.ipservice.ip_converters import IPConverter

ip_converter = IPConverter
ipv6_bytes_1 = ip_converter.convert_to_ipv6_bytes('2003:0db8:0000:0042:0000:8a2e:0370:7334')
ipv6_bytes_2 = ip_converter.convert_to_ipv6_bytes(5412213248541258421)
ipv6_bytes_3 = ip_converter.convert_to_ipv6_bytes('/96')
ipv6_bytes_4 = ip_converter.convert_to_ipv6_bytes(
    [
        1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
        1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ])
ipv6_bytes_5 = ip_converter.convert_to_ipv6_bytes(
    '11111111111111111111111111111111'
    '11111111111111111111111111111111'
    '00000000000000000000000000000000'
    '00000000000000000000000000000000'
)

print('IPv6 bytes 1:', ' -> ', '%-70s'%ipv6_bytes_1, ' -> ', IPv6Addr(ipv6_bytes_1))
print('IPv6 bytes 2:', ' -> ', '%-70s'%ipv6_bytes_2, ' -> ', IPv6Addr(ipv6_bytes_2))
print('IPv6 bytes 3:', ' -> ', '%-70s'%ipv6_bytes_3, ' -> ', IPv6Addr(ipv6_bytes_3))
print('IPv6 bytes 4:', ' -> ', '%-70s'%ipv6_bytes_4, ' -> ', IPv6Addr(ipv6_bytes_4))
print('IPv6 bytes 5:', ' -> ', '%-70s'%ipv6_bytes_5, ' -> ', IPv6Addr(ipv6_bytes_5))

```
Example output:
```
IPv6 bytes 1:  ->  b' \x03\r\xb8\x00\x00\x00B\x00\x00\x8a.\x03ps4'                         ->  2003:DB8:0:42:0:8A2E:370:7334
IPv6 bytes 2:  ->  b'\x00\x00\x00\x00\x00\x00\x00\x00K\x1c\x0bF?\xf6\xf2\xb5'              ->  ::4B1C:B46:3FF6:F2B5
IPv6 bytes 3:  ->  b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00'     ->  FFFF:FFFF:FFFF:FFFF:FFFF:FFFF::
IPv6 bytes 4:  ->  b'\xc0\xc0\xa8\xa8\x01\x01\n\n\x00\x00\x00\x00\x00\x00\x00\x00'         ->  C0C0:A8A8:101:A0A::
IPv6 bytes 5:  ->  b'\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'     ->  FFFF:FFFF:FFFF:FFFF::
```
</details>

<details>

<summary>Example 3 - Use the specific converter handler:</summary>

Here is an example of using the decimal converter handler to convert an IPv4 and IPv6 addresses to bytes.

```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr
from ttlinks.ipservice.ip_converters import DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler

ipv4_decimal_handler = DecimalIPv4ConverterHandler()
ipv4_in_bytes = ipv4_decimal_handler.handle(3232235826)

ipv6_decimal_handler = DecimalIPv6ConverterHandler()
ipv6_in_bytes = ipv6_decimal_handler.handle(42540766411282592856903984951653826731)

print('IPv4 in bytes:', ipv4_in_bytes, '| Address:', IPv4Addr(ipv4_in_bytes).address)
print('IPv6 in bytes:', ipv6_in_bytes, '| Address:', IPv6Addr(ipv6_in_bytes).address)
```
Example output:
```
IPv4 in bytes: b'\xc0\xa8\x012' | Address: 192.168.1.50
IPv6 in bytes: b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xab' | Address: 2001:DB8::AB
```

Other converter handlers are doing the same thing but for different formats.
Supported handlers are:

- `BytesIPv4ConverterHandler` - If the input is bytes, it returns the same bytes.
- `BinaryDigitsIPv4ConverterHandler` - Expects a list of 32 binary digits.
- `BinaryStringIPv4ConverterHandler` - Expects a string of 32 binary digits.
- `CIDRIPv4ConverterHandler` - Expects a string in CIDR notation.
- `DotIPv4ConverterHandler` - Expects a string in dot-decimal notation.
- `DecimalIPv4ConverterHandler` - Expects an integer.
- `BytesIPv6ConverterHandler` - If the input is bytes, it returns the same bytes.
- `BinaryDigitsIPv6ConverterHandler` - Expects a list of 128 binary digits.
- `BinaryStringIPv6ConverterHandler` - Expects a string of 128 binary digits.
- `CIDRIPv6ConverterHandler` - Expects a string in CIDR notation.
- `ColonIPv6ConverterHandler` - Expects a string in colon-hexadecimal notation.
- `DecimalIPv6ConverterHandler` - Expects an integer.

</details>

<details>
<summary>Example 4 - Define a custom converter chain:</summary>

The chain processes the input based on the handlers included in it. As demonstrated in the example, the chain initially converts the input to bytes according to the specified formats: Colon-Hex, Dot-Decimal, and Decimal. However, it fails to recognize IPv6's CIDR notation, which is why the conversion process for `example4` failed. After adding the `CIDRIPv6ConverterHandler` to the chain, the conversion process for `example4` succeeded.


```python
from ttlinks.ipservice.ip_converters import DotIPv4ConverterHandler, ColonIPv6ConverterHandler, DecimalIPv6ConverterHandler, CIDRIPv6ConverterHandler

handler = DotIPv4ConverterHandler()
last_in_chain = handler.set_next(ColonIPv6ConverterHandler()).set_next(DecimalIPv6ConverterHandler())
example1 = '192.168.1.0'
example2 = '2001:0db8:85a3::'
example3 = 885511225
example4 = '/96'
print('Input1:', '%-25s'%example1, '->', 'Output1:', handler.handle(example1))
print('Input2:', '%-25s'%example2, '->', 'Output2:', handler.handle(example2))
print('Input3:', '%-25s'%example3, '->', 'Output3:', handler.handle(example3))
print('Input4:', '%-25s'%example4, '->', 'Output4:', handler.handle(example4))


print('\nPut CIDRIPv6ConverterHandler in the chain..')
last_in_chain.set_next(CIDRIPv6ConverterHandler())
print('Input4:', '%-25s'%example4, '->', 'Output4:', handler.handle(example4))
```
Example output:
```
Input1: 192.168.1.0               -> Output1: b'\xc0\xa8\x01\x00'
Input2: 2001:0db8:85a3::          -> Output2: b' \x01\r\xb8\x85\xa3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
Input3: 885511225                 -> Output3: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x004\xc7\xd49'
Input4: /96                       -> Output4: None

Put CIDRIPv6ConverterHandler in the chain..
Input4: /96                       -> Output4: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00'
```

> [!NOTE]  The process follows the order of the handlers in the chain. If the input is not recognized by a handler, it is passed to the next handler. However, once the input is processed by a handler, it will not proceed to subsequent handlers. Therefore, it is crucial to carefully define the order of handlers in the chain. A poor example is including both `CIDRIPv4NetmaskClassifierHandler` and `CIDRIPv6NetmaskClassifierHandler` in the same chain. If `CIDRIPv4NetmaskClassifierHandler` is placed first, it will process inputs like `/24`, even if the input is intended for IPv6. This prevents the input from being correctly handled by `CIDRIPv6NetmaskClassifierHandler`, causing inaccurate results.

</details>

> [!TIP]  test

> [!WARNING]\
> test