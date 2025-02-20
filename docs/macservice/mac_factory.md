# `mac_factory` Module  

The **`mac_factory`** module extends the functionality of the standard **`MACAddr`** class by providing additional features, including:  
- Creating **MACAddr** objects from different formats.  
- **Batch processing** of MAC addresses with optional parallel execution.  
- Generating **random MAC addresses**, either individually or in bulk.  

Internally, all MAC addresses are instantiated as `MACAddr` objects based on user requests.  

---

## 1. Create a `MACAddr` Object  

The `MACFactory` class allows the creation of `MACAddr` objects from various MAC address formats.  

```python
from ttlinks.macservice.mac_factory import MACFactory

factory = MACFactory()
mac = factory.mac("70-1A-B8-20-0F-12")
print(mac)
```

### Example Output:
```
70:1A:B8:20:0F:12
```

---

## 2. Process a Batch of MAC Addresses  

The **`batch_macs`** method processes a list of MAC addresses, with optional **multi-threading** and **duplicate filtering**.  

```python
mac_list = [
    "08-BF-B8-34-B0-03",
    "70-1A-B8-20-0F-12",
    "08-BF-B8-34-B0-03",  # Duplicate for testing
]

# Process batch with 5 worker threads and remove duplicates
batch_result = factory.batch_macs(mac_list, max_workers=5, keep_dup=False)

for mac in batch_result:
    print(mac)
```

### Example Output:
```
08:BF:B8:34:B0:03
70:1A:B8:20:0F:12
```

---

## 3. Generate a Random MAC Address  

The **`random_mac`** method generates a **random MAC address**. You can optionally specify a **MAC type** (Unicast, Multicast, or Broadcast).  

```python
random_mac = factory.random_mac()
print(random_mac)
```

### Example Output:
```
A2:B3:C4:D5:E6:F7
```

To generate a **specific MAC type**:  
```python
from ttlinks.macservice import MACType

unicast_mac = factory.random_mac(MACType.UNICAST)
multicast_mac = factory.random_mac(MACType.MULTICAST)
broadcast_mac = factory.random_mac(MACType.BROADCAST)

print(unicast_mac)   # Expected Output: A Unicast MAC Address
print(multicast_mac) # Expected Output: A Multicast MAC Address
print(broadcast_mac) # Expected Output: FF:FF:FF:FF:FF:FF
```

---

## 4. Generate a Batch of Random MAC Addresses  

The **`random_macs_batch`** method generates multiple random MAC addresses. The number of MACs to generate can be specified (default: `10`).  

```python
random_macs = factory.random_macs_batch(num_macs=5)

for mac in random_macs:
    print(mac)
```

### Example Output:
```
A3:B4:C5:D6:E7:F8
F1:E2:D3:C4:B5:A6
12:34:56:78:9A:BC
98:76:54:32:10:FE
1A:2B:3C:4D:5E:6F
```

For a **specific MAC type** (e.g., **Multicast**):  
```python
multicast_macs = factory.random_macs_batch(mac_type=MACType.MULTICAST, num_macs=3)

for mac in multicast_macs:
    print(mac)
```
