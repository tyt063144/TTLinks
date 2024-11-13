from enum import Enum


class TCPFlags(Enum):
    """
    Enum class representing TCP flags, used in TCP packet headers to control various behaviors in
    TCP connections. Each flag is associated with a specific bit position in a TCP header.

    Flags:
    - FIN (0x0001): Indicates the end of data from the sender.
    - SYN (0x0002): Synchronize sequence numbers to initiate a connection.
    - RST (0x0004): Reset the connection.
    - PSH (0x0008): Push function to send data immediately.
    - ACK (0x0010): Acknowledges received data.
    - URG (0x0020): Marks urgent data.
    - ECE (0x0040): Indicates ECN-Echo, used for congestion control.
    - CWR (0x0080): Congestion Window Reduced flag, part of ECN.
    - NS (0x0100): ECN-nonce concealment protection.

    Methods:
    - __repr__: Returns a string representation of the flag with its name and hexadecimal value.
    - __str__: Returns the name of the flag as a string.
    """
    FIN = 0x0001
    SYN = 0x0002
    RST = 0x0004
    PSH = 0x0008
    ACK = 0x0010
    URG = 0x0020
    ECE = 0x0040
    CWR = 0x0080
    NS = 0x0100

    def __repr__(self):
        """
         Returns a string representation of the TCP flag, showing its name and hexadecimal value.

         Returns:
         - str: The name of the flag and its value in hexadecimal format.
         """
        return f"{self.name} ({hex(self.value)})"

    def __str__(self):
        """
        Returns the name of the TCP flag as a string.

        Returns:
        - str: The name of the TCP flag.
        """
        return self.name

