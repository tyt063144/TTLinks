from enum import Enum


class MACType(Enum):
    """
    Enumeration for MAC (Media Access Control) address types.

    This enum defines three types of MAC addresses: Unicast, Multicast, and Broadcast.
    Each type is associated with a unique integer value to differentiate the behavior or purpose
    of the MAC address in a network.

    Attributes:
    - UNICAST (int): Represents a unicast MAC address, which is used for point-to-point communication between two devices.
    - MULTICAST (int): Represents a multicast MAC address, used to deliver a message to a group of destination devices.
    - BROADCAST (int): Represents a broadcast MAC address, which sends a message to all devices in the network.
    """
    UNICAST = 1
    MULTICAST = 2
    BROADCAST = 3
