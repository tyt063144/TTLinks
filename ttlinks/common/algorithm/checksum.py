from abc import ABC, abstractmethod


class ChecksumAlgorithm(ABC):
    @abstractmethod
    def calculate(self, data: bytes) -> int:
        """
        Calculates the checksum of the given data.

        This is an abstract method that must be implemented by subclasses
        to compute the checksum for the provided byte data. The checksum
        is generally used to verify the integrity of the data by producing
        a fixed-size integer result based on the contents of the input.

        Parameters:
        data (bytes): The data for which the checksum needs to be calculated.

        Returns:
        int: The calculated checksum as an integer.
        """
        pass

class InternetChecksum(ChecksumAlgorithm):
    def calculate(self, data: bytes) -> int:
        """
        Calculates the checksum of the given data using the Internet Checksum algorithm.

        This algorithm sums 16-bit words, adds any carry-over bits, and returns the
        one's complement of the final sum. If the data length is odd, a padding byte
        of zero is appended to the end of the data to make it even-length for processing.

        Parameters:
        data (bytes): The data for which the checksum needs to be calculated.
                      If the data length is odd, it will be padded with a zero byte.

        Returns:
        int: The calculated 16-bit checksum as an integer.
        """
        checksum = 0
        if len(data) % 2 != 0:
            data += b'\0'
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]
        while checksum >> 16:
            checksum = (checksum >> 16) + (checksum & 0xffff)
        return ~checksum & 0xffff


class ChecksumCalculator:
    def __init__(self, algorithm: ChecksumAlgorithm):
        """
        Initializes the ChecksumCalculator with the specified checksum algorithm.

        This class implements the Strategy Design Pattern by allowing the user
        to dynamically choose which checksum algorithm to use for calculation.
        The algorithm must be a subclass of ChecksumAlgorithm.

        Parameters:
        algorithm (ChecksumAlgorithm): An instance of a class implementing the
                                       ChecksumAlgorithm interface.
        """
        self._algorithm = algorithm

    def calculate(self, data: bytes) -> int:
        """
        Calculates the checksum of the given data using the provided checksum algorithm.

        This method delegates the actual checksum calculation to the algorithm instance,
        demonstrating the Strategy Design Pattern, where different algorithms can be
        applied to the same task (in this case, calculating a checksum) without changing
        the client code.

        Parameters:
        data (bytes): The data for which the checksum needs to be calculated.

        Returns:
        int: The calculated checksum as an integer.
        """
        return self._algorithm.calculate(data)
