from enum import Enum


class IPv4Flags(Enum):
    NO_FLAGS = 0  # Reserved bit (100 in binary, which is 4 in decimal)
    DONT_FRAGMENT = 2  # Don't Fragment bit (010 in binary, which is 2 in decimal)
    MORE_FRAGMENTS = 1  # More Fragments bit (001 in binary, which is 1 in decimal)