# `mac_converters` Module  

The **`mac_converters`** module is used to convert **MAC addresses** from different formats into **byte representations**. This standardization helps ensure compatibility when passing MAC addresses as parameters to other classes and functions.  

## 1. `BinaryDigitsMAC48ConverterHandler`  

Converts a **list of 48 binary bits** into the **byte representation** of a MAC address.  

```python
from ttlinks.macservice.mac_converters import BinaryDigitsMAC48ConverterHandler

handler = BinaryDigitsMAC48ConverterHandler()
print(handler.handle([
    0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1,
    1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0,
    1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1
]))
```

### Example Output:
```
b'\x08\xbf\xb84\xb0\x03'
```

## 2. `DashedHexMAC48ConverterHandler`  

Converts a **dashed hexadecimal MAC address** (e.g., `"70-1A-B8-20-0F-12"`) into its **byte representation**.  

```python
from ttlinks.macservice.mac_converters import DashedHexMAC48ConverterHandler

handler = DashedHexMAC48ConverterHandler()
print(handler.handle("70-1A-B8-20-0F-12"))
```

### Example Output:
```
b'p\x1a\xb8 \x0f\x12'
```

## 3. `ColonHexMAC48ConverterHandler`  

Converts a **colon-separated hexadecimal MAC address** into its **byte representation**.  

```python
from ttlinks.macservice.mac_converters import ColonHexMAC48ConverterHandler

handler = ColonHexMAC48ConverterHandler()
print(handler.handle("70:1A:B8:20:0F:12"))
```

### Example Output:
```
b'p\x1a\xb8 \x0f\x12'
```

## 4. `DotHexMAC48ConverterHandler`  

Converts a **dot-separated hexadecimal MAC address** into its **byte representation**.  

```python
from ttlinks.macservice.mac_converters import DotHexMAC48ConverterHandler

handler = DotHexMAC48ConverterHandler()
print(handler.handle("701A.B820.0F12"))
```

### Example Output:
```
b'p\x1a\xb8 \x0f\x12'
```

## 5. `DecimalMAC48ConverterHandler`  

Converts a **decimal representation of a MAC address** into its **byte representation**.  

```python
from ttlinks.macservice.mac_converters import DecimalMAC48ConverterHandler

handler = DecimalMAC48ConverterHandler()
print(handler.handle(123456789012345))
```

### Example Output:
```
b'pH\x86\r\xdfy'
```

## 6. `BytesMAC48ConverterHandler`  

Converts a **raw bytes MAC address** into a **byte representation**.  

```python
from ttlinks.macservice.mac_converters import BytesMAC48ConverterHandler

handler = BytesMAC48ConverterHandler()
print(handler.handle(b'\x70\x1A\xB8\x20\x0F\x12'))
```

### Example Output:
```
b'p\x1a\xb8 \x0f\x12'
```

## 7. Other OUI24 Converters  

The following converters are used to **extend OUI-24 identifiers** to **6 bytes** by appending three `00` bytes at the end. This ensures compatibility when passing the result to `MACAddr`, allowing seamless integration with the **OUI lookup method**.  

These converters function similarly to the MAC-48 converters but specifically handle **OUI-24 formats**:  

- `BinaryDigitsOUI24ConverterHandler`  
- `DashedHexOUI24ConverterHandler`  
- `ColonHexOUI24ConverterHandler`  
- `DotHexOUI24ConverterHandler`  
- `BytesOUI24ConverterHandler`  

### Example Usage (`DashedHexOUI24ConverterHandler`)  

```python
from ttlinks.macservice.mac_converters import DashedHexOUI24ConverterHandler

handler = DashedHexOUI24ConverterHandler()
print(handler.handle("DB-AA-EE"))
```

### Example Output:
```
b'\xdb\xaa\xee\x00\x00\x00'
```