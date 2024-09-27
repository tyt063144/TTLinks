Here's the markdown documentation for the `mac_utils.py` module based on the file you uploaded:

---

# `mac_utils.py` Module Documentation

## Overview

The `mac_utils.py` module provides utilities related to MAC (Media Access Control) addresses, specifically for categorizing and managing different types of MAC addresses. This module defines an enumeration for the three main types of MAC addresses: unicast, multicast, and broadcast.

## Classes

### 1. `MACType`

- **Description**: An enumeration that categorizes the different types of MAC addresses. MAC addresses are used for network communication to ensure data is sent to the correct recipient on a local network.
  
#### Categories:

- **UNICAST**: A MAC address that identifies a single unique device on a network. Unicast addresses are used for one-to-one communication.
  
- **MULTICAST**: A MAC address that identifies a group of devices on a network. Multicast addresses are used for one-to-many communication, where data is sent to multiple devices simultaneously.

- **BROADCAST**: A MAC address used to send data to all devices on a network. Broadcast communication is used for one-to-all communication on the network.

---

## Dependencies

This module does not have any external dependencies.
