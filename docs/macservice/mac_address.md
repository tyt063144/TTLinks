# `mac_address` Module  

## 1. Create a `MACAddr` Object  

This example demonstrates how to create a `MACAddr` object using the **TTLinks** `macservice` library. The accepted formats include **dashed**, **dotted**, **colon-separated**, and **pure string** representations.  

```python
from ttlinks.macservice.mac_address import MACAddr

mac1 = MACAddr("08-BF-B8-34-b0-03")
mac2 = MACAddr("08:BF:B8:34:b0:03")
mac3 = MACAddr("08.BF.B8.34.b0.03")
mac4 = MACAddr("08BFB834b003")

print(str(mac1))
print(str(mac2))
print(str(mac3))
print(str(mac4))
```

### Example Output:
```
08:BF:B8:34:B0:03
08:BF:B8:34:B0:03
08:BF:B8:34:B0:03
08:BF:B8:34:B0:03
```

## 2. Show MAC Address in Bit-Level Representation  

The `.binary_string` property provides the bit-level representation of a given MAC address.  

```python
mac1.binary_string
```

### Example Output:
```
000010001011111110111000001101001011000000000011
```

## 3. Convert MAC Address to Decimal  

The `.as_decimal` property converts a MAC address to its decimal format.  

```python
mac1.as_decimal
```

### Example Output:
```
9619522236419
```

## 4. Check OUI Information  

When a `MACAddr` object is created, **TTLinks** automatically searches the **OUI database** and links any corresponding **OUI information** to the MAC address.  

- The result is returned as a **list**.  
- Typically, the list contains **one OUI entry**, which can be accessed using `[0]`.  
- If no OUI is found, an **empty list** is returned.  

```python
if mac1.oui:
    print(mac1.oui[0].record)
else:
    print("No OUI record for mac1")

if mac2.oui:
    print(mac2.oui[0].record)
else:
    print("No OUI record for mac2")
```

### Example Output:
```
mac1:  {
    'oui_id': '08BFB8', 
    'start_hex': '000000', 
    'end_hex': 'FFFFFF', 
    'start_decimal': 9619518783488, 
    'end_decimal': 9619535560703, 
    'block_size': 16777215, 
    'oui_type': 'MA_L', 
    'organization': 'ASUSTek COMPUTER INC.', 
    'address': 'No.15, Lide Rd., Beitou Dist., Taipei 112, Taiwan Taipei Taiwan TW 112'
}
No OUI record for mac2
```
