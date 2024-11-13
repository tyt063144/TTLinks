from __future__ import annotations

import random
import socket
from itertools import product
from typing import List, Tuple, Any

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory


class BinaryTools:

    @staticmethod
    def expand_by_mask(digits: List[int], mask: List[int]) -> list[tuple[Any, ...]]:
        """
        Expands the given digits based on the mask to generate all possible combinations.

        This method takes a list of digits (which can represent an IP address, MAC address, etc.)
        and a corresponding list of mask digits. The mask determines which bits of the digits are
        fixed and which bits can vary. If a bit in the mask is 1, the corresponding digit bit is fixed.
        If the mask bit is 0, the corresponding digit bit can take multiple values.

        Args:
            digits (List[int]): A list of digits representing an address (IP, MAC, etc.).
            mask (List[int]): A list of mask digits. A 1 indicates the bit is fixed, and a 0 indicates
                              the bit can vary.

        Returns:
            List[Tuple[int]]: A list of tuples, where each tuple represents a possible combination
                              of digits generated based on the mask.

        Example:
            digits = [0, 1, 0]
            mask = [1, 1, 0]
            result = IPUtils.expand_by_mask(digits, mask)
            # result will be [(0, 1, 0), (0, 1, 1)]
        """
        expanded_digits = {}
        index = 0
        for mask_bit in mask:
            if mask_bit == 1:
                expanded_digits[index] = [digits[index]]
            elif mask_bit == 0:
                expanded_digits[index] = [0, 1]  # Example values, adjust as needed
            index += 1
        # Generate all combinations using itertools.product
        combinations = list(product(*expanded_digits.values()))
        return combinations

    @staticmethod
    def is_binary_in_range(id_digits: List[int], mask_digits: List[int], compared_digits: List[int]) -> bool:
        """
        Determines if a given set of compared digits falls within the range defined by the id digits and mask digits.

        This method compares the `id_digits` and `compared_digits` up to the number of bits specified by the `mask_digits`.
        The method checks if the `compared_digits` match the `id_digits` for the positions where the `mask_digits` are set to 1.

        Args:
            id_digits (List[int]): A list of binary digits representing the ID.
            mask_digits (List[int]): A list of binary digits representing the mask, where 1s indicate the positions to be compared.
            compared_digits (List[int]): A list of binary digits representing the values to compare against the ID.

        Returns:
            bool: True if the `compared_digits` are within the range defined by the `id_digits` and `mask_digits`, False otherwise.

        Raises:
            ValueError: If the lengths of `id_digits`, `mask_digits`, and `compared_digits` are not the same.
        """
        if len(id_digits) != len(mask_digits) != len(compared_digits):
            raise ValueError("The lengths of id_digits, mask_digits, and compared_digits must be the same.")

        matching_count = mask_digits.count(1)
        return id_digits[:matching_count] == compared_digits[:matching_count]

    @staticmethod
    def apply_mask_variations(address: List[Octet], mask : List[Octet]):
        address_string = ''.join([str(address_bit) for address_bit in address])
        mask_string = ''.join([str(mask_bit) for mask_bit in mask])
        adjusted_address = ''
        for address_bit, mask_bit in zip(address_string, mask_string):
            if mask_bit == '0':
                adjusted_address += '0'
            else:
                adjusted_address += address_bit
        return [OctetFlyWeightFactory.get_octet(adjusted_address[i:i+8]) for i in range(0, len(adjusted_address), 8)]

class NetTools:
    """
    NetTools is a utility class providing essential network-related methods for:
    - Retrieving the outgoing IP address of the local network interface.
    - Finding an available TCP port on the local machine.
    - Generating a random 32-bit TCP sequence number.
    - Generating a random 16-bit IPv4 identification number.

    Each method within this class is static, allowing direct access without instantiating the class.
    """
    @staticmethod
    def get_outgoing_interface_ip(destination="8.8.8.8", port=80, timeout=0.002):
        """
        Retrieves the IP address of the local interface used to reach a specified destination.

        Parameters:
        - destination (str, default="8.8.8.8"): The IP address to simulate a connection to (default is Google's DNS).
        - port (int, default=80): Port number for the simulated connection.
        - timeout (float, default=0.002): Timeout duration for the connection attempt.

        Returns:
        - str: The IP address of the outgoing interface if successful.
        - None: If there's a timeout or socket error.
        """
        try:
            # Create a socket and set a timeout
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)  # Set the timeout in seconds
                s.connect((destination, port))
                local_ip = s.getsockname()[0]  # Get the IP address of the outgoing interface
            return local_ip
        except (socket.timeout, socket.error) as e:
            print(f"An error occurred or timeout reached: {e}")
            return None

    @staticmethod
    def get_unused_port() -> int:
        """
        Finds and returns an available random port between 1025 and 65535 for TCP connections.

        Returns:
        - int: A free TCP port number.
        """
        while True:
            random_port = random.randint(1025, 65535)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("localhost", random_port))
                except OSError:
                    continue # get next random port that is not in use
                return random_port  # Port is free
    @staticmethod
    def get_tcp_sequence_number() -> int:
        """
        Generates a random 32-bit TCP sequence number with a small offset to simulate non-deterministic sequences.

        Returns:
        - int: A random 32-bit TCP sequence number.
        """
        sequence_number = random.getrandbits(32)
        offset = random.randint(1, 1000)
        sequence_number = (sequence_number + offset) % (2**32)
        return sequence_number
    @staticmethod
    def get_ipv4_id() -> int:
        """
        Generates a random 16-bit IPv4 identification number with a small offset for uniqueness in packet identification.

        Returns:
        - int: A random 16-bit IPv4 identification number.
        """
        identification = random.getrandbits(16)
        offset = random.randint(1, 1000)
        identification = (identification + offset) % (2**16)
        return identification