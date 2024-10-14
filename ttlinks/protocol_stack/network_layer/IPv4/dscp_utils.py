from enum import Enum

class DSCP(Enum):
    CS0 = 0
    CS1 = 8
    CS2 = 16
    CS3 = 24
    CS4 = 32
    CS5 = 40
    CS6 = 48
    CS7 = 56
    EF = 46
    AF11 = 10
    AF12 = 12
    AF13 = 14
    AF21 = 18
    AF22 = 20
    AF23 = 22
    AF31 = 26
    AF32 = 28
    AF33 = 30
    AF41 = 34
    AF42 = 36
    AF43 = 38

    @staticmethod
    def get_name_or_value(value):
        """
        Return the DSCP name if it exists, otherwise return the value itself.
        """
        try:
            return DSCP(value)
        except ValueError:
            return value  # Return the number if no matching DSCP name