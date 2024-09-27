from __future__ import annotations

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