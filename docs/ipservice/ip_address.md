# `ip_address` Module

Create IP address objects for both IPv4 and IPv6 addresses. 

```python
from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr

ipv4_address = IPv4Addr('192.168.1.1')
ipv6_address = IPv6Addr('2001:db8::1')
```

<details>
<summary>Example 1 - Displaying the string representation of an IP address:</summary>

```python
ipv4_address_str = ipv4_address.address
ipv6_address_str = ipv6_address.address
print('%12s: %s' % ('IPv4 Address', ipv4_address_str))
print('%12s: %s' % ('IPv6 Address', ipv6_address_str))
```
Output:
```
IPv4 Address: 192.168.1.1
IPv6 Address: 2001:DB8::1
```
</details>

<details>
<summary>Example 2 - Displaying the IP addresses in binary format:</summary>

```python
ipv4_bin_str = ipv4_address.binary_string
ipv6_bin_str = ipv6_address.binary_string
ipv4_bin_digits = ipv4_address.binary_digits
ipv6_bin_digits = ipv6_address.binary_digits
print('%-12s: %s' % ('IPv4 Binary String', ipv4_bin_str))
print('%-12s: %s' % ('IPv6 Binary String', ipv6_bin_str))
print('%-12s: %s' % ('IPv4 Binary Digits', ipv4_bin_digits))  # 32 bits
print('%-12s: %s' % ('IPv6 Binary Digits', ipv6_bin_digits))  # 128 bits
```
Output:
```
IPv4 Binary String: 11000000101010000000000100000001
IPv6 Binary String: 001000000000000100001101101110000...
IPv4 Binary Digits: [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, ...]
IPv6 Binary Digits: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, ...]
```
</details>

<details>
<summary>Example 3 - Displaying the IP addresses in decimal format:</summary>

```python
ipv4_decimal = ipv4_address.decimal
ipv6_decimal = ipv6_address.decimal
print('%-12s: %s' % ('IPv4 Decimal', ipv4_decimal))
print('%-12s: %s' % ('IPv6 Decimal', ipv6_decimal))
```
Output:
```
IPv4 Decimal: 3232235777
IPv6 Decimal: 42540766411282592856903984951653826561
```
</details>

<details>
<summary>Example 4 - Displaying the IP addresses in bytes format:</summary>

This format can be used in network programming to send and receive IP addresses.
```python
ipv4_bytes = ipv4_address.as_bytes
ipv6_bytes = ipv6_address.as_bytes
print('%-12s: %s' % ('IPv4 Bytes', ipv4_bytes))
print('%-12s: %s' % ('IPv6 Bytes', ipv6_bytes))
```
Output:
```
IPv4 Bytes  : b'\xc0\xa8\x01\x01'
IPv6 Bytes  : b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
```
</details>

<details>
<summary>Example 5 - Displaying the IP addresses in hex format:</summary>

This format can be used in network programming to send and receive IP addresses.
```python
ipv4_hex = ipv4_address.as_hexadecimal
ipv6_hex = ipv6_address.as_hexadecimal
print('%-12s: %s' % ('IPv4 Hex', ipv4_hex))
print('%-12s: %s' % ('IPv6 Hex', ipv6_hex))
```
Output:
```
IPv4 Hex    : C0A80101
IPv6 Hex    : 20010DB8000000000000000000000001
```
</details>

<details>
<summary>Example 6 - IPMask Objects</summary>

IPMask objects are distinct from IPAddr objects as they specifically represent network masks and wildcards, including `IPv4NetMask`, `IPv6NetMask`, `IPv4WildCard`, and `IPv6WildCard`. 

#### Key Differences and Features:
- **Network Masks (`IPv4NetMask` and `IPv6NetMask`):**
  - Include an additional validation step to ensure the input represents a valid netmask.
  - Provide an extra property, `mask_size`, to retrieve the length of the mask in bits.
  - Support other properties and methods similar to IPAddr objects for consistency and usability.

- **Wildcards (`IPv4WildCard` and `IPv6WildCard`):**
  - Used extensively in contexts such as creating `WildCardConfig` objects in the `ip_configs` module, which will be covered in a later section.
  - Support all properties and methods similar to IPAddr objects for consistency and usability.

```python
from ttlinks.ipservice.ip_address import IPv4NetMask, IPv6NetMask

print('IPv4 Netmask'.center(50, '-'))
try:
    incorrect_ipv4_netmask = IPv4NetMask('192.168.1.1')
except ValueError as e:
    print(e)
correct_ipv4_netmask = IPv4NetMask('255.255.255.0')  # Can also be '/24'
ipv4_mask_size = correct_ipv4_netmask.mask_size
print('IPv4 Mask size:', ipv4_mask_size)
print('IPv4 Mask addr:', correct_ipv4_netmask.address)

print('IPv6 Netmask'.center(50, '-'))
try:
    incorrect_ipv6_netmask = IPv6NetMask('2001:db8::1')
except ValueError as e:
    print(e)
correct_ipv6_netmask = IPv6NetMask('/64')  # Can also be 'ffff:ffff:ffff:ffff::'
ipv6_mask_size = correct_ipv6_netmask.mask_size
print('IPv6 Mask size:', ipv6_mask_size)
print('IPv6 Mask addr:', correct_ipv6_netmask.address)
```
Output:
```
-------------------IPv4 Netmask-------------------
192.168.1.1 is not a valid IPv4 netmask.
IPv4 Mask size: 24
IPv4 Mask addr: 255.255.255.0
-------------------IPv6 Netmask-------------------
2001:db8::1 is not a valid IPv6 netmask.
IPv6 Mask size: 64
IPv6 Mask addr: FFFF:FFFF:FFFF:FFFF::
```
</details>