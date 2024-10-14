import concurrent.futures
import random
from abc import abstractmethod, ABC
from typing import List, Any

from ttlinks.macservice import MACType
from ttlinks.macservice.mac_address import InterfaceMACAddr, MACAddr
from ttlinks.macservice.mac_converters import MACConverter


class InterfaceMACFactory(ABC):
    """
    Abstract base class for generating and managing MAC (Media Access Control) addresses.
    Provides methods for single or batch MAC address operations, including the ability to
    generate random MAC addresses and manage lists of MACs with optional parallel processing.

    Methods:
        mac(mac: str) -> InterfaceMACAddr:
            Abstract method to get or create a MAC address from a given string.

        batch_macs(macs: list[str], max_workers: int = 10, keep_dup: bool = True) -> List[InterfaceMACAddr]:
            Abstract method to process a batch of MAC addresses, allowing for parallel processing with a
            specified number of workers. Optionally keeps duplicates.

        random_mac(mac_type=None) -> InterfaceMACAddr:
            Abstract method to generate a random MAC address. The type of the MAC can be optionally specified.

        random_macs_batch(mac_type=None, num_macs: int = 10) -> List[InterfaceMACAddr]:
            Abstract method to generate a batch of random MAC addresses, with the number of MACs specified.
    """
    @abstractmethod
    def mac(self, mac: Any) -> MACAddr:
        """
        Get or create a MAC address from the given string.

        Parameters:
        mac (str): The MAC address as a string.

        Returns:
        InterfaceMACAddr: An object representing the processed or validated MAC address.
        """
        pass

    @abstractmethod
    def batch_macs(self, macs: list[str], max_workers:int=10, keep_dup:bool=True) -> List[MACAddr]:
        """
        Process a batch of MAC addresses with optional parallelism and duplicate handling.

        Parameters:
        macs (list[str]): A list of MAC addresses to process.
        max_workers (int, optional): The maximum number of workers for parallel processing. Defaults to 10.
        keep_dup (bool, optional): Whether to keep duplicate MAC addresses. Defaults to True.

        Returns:
        List[InterfaceMACAddr]: A list of processed or validated MAC addresses.
        """
        pass

    @abstractmethod
    def random_mac(self, mac_type=None) -> MACAddr:
        """
        Generate a random MAC address, optionally of a specified type.

        Parameters:
        mac_type (optional): The type of MAC address to generate. Can be specified if needed.

        Returns:
        InterfaceMACAddr: A randomly generated MAC address.
        """
        pass

    @abstractmethod
    def random_macs_batch(self, mac_type=None, num_macs=10) -> List[MACAddr]:
        """
        Generate a batch of random MAC addresses.

        Parameters:
        mac_type (optional): The type of MAC addresses to generate. Can be specified if needed.
        num_macs (int, optional): The number of random MAC addresses to generate. Defaults to 10.

        Returns:
        List[InterfaceMACAddr]: A list of randomly generated MAC addresses.
        """
        pass

class MACFactory(InterfaceMACFactory):
    """
    A concrete implementation of the InterfaceMACFactory for handling MAC addresses.
    Provides methods to generate and manage single or batch MAC addresses, including
    generating random MACs and processing MAC batches with multi-threading.

    Attributes:
        randomizer (MACRandomizer): A utility to generate random MAC addresses.

    Methods:
        mac(mac: str) -> InterfaceMACAddr:
            Converts a given string into a MAC address object.

        batch_macs(macs: list[str], max_workers: int = 10, keep_dup: bool = True) -> List[InterfaceMACAddr]:
            Processes a list of MAC addresses, optionally removing duplicates and using multi-threading
            to increase performance.

        random_mac(mac_type=None) -> InterfaceMACAddr:
            Generates a single random MAC address, with an optional type.

        random_macs_batch(mac_type=None, num_macs: int = 10) -> List[InterfaceMACAddr]:
            Generates a batch of random MAC addresses.
    """
    def __init__(self):
        """
        Initializes the MACFactory with a MACRandomizer for generating random MAC addresses.
        """
        self.randomizer = MACRandomizer()

    def mac(self, mac) -> MACAddr:
        """
        Converts a given MAC address string into a MAC address object.

        Parameters:
        mac (str): The MAC address as a string.

        Returns:
        InterfaceMACAddr: An object representing the validated or created MAC address.
        """
        return MACAddr(MACConverter.convert_mac(mac))

    def batch_macs(self, macs: list[str], max_workers:int=10, keep_dup:bool=True) -> List[MACAddr]:
        """
        Processes a batch of MAC addresses with optional parallel processing and duplicate removal.

        Parameters:
        macs (list[str]): A list of MAC address strings to process.
        max_workers (int, optional): The maximum number of worker threads to use for processing. Defaults to 10.
        keep_dup (bool, optional): Whether to keep duplicate MAC addresses in the result. Defaults to True.

        Returns:
        List[InterfaceMACAddr]: A list of processed MAC address objects.
        """
        if not keep_dup:
            macs = list(set(macs))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.mac, macs))
        return results

    def random_mac(self, mac_type=None) -> MACAddr:
        """
        Generates a single random MAC address.

        Parameters:
        mac_type (optional): The type of MAC address to generate. Can be specified if needed.

        Returns:
        InterfaceMACAddr: A randomly generated MAC address object.
        """
        generated_mac = self.randomizer.randomize(mac_type)
        return MACAddr(generated_mac)

    def random_macs_batch(self, mac_type=None, num_macs=10) -> List[MACAddr]:
        """
        Generates a batch of random MAC addresses.

        Parameters:
        mac_type (optional): The type of MAC addresses to generate. Can be specified if needed.
        num_macs (int, optional): The number of random MAC addresses to generate. Defaults to 10.

        Returns:
        List[InterfaceMACAddr]: A list of randomly generated MAC address objects.
        """
        macs = [self.randomizer.randomize(mac_type) for _ in range(num_macs)]
        return [MACAddr(mac) for mac in macs]


class MACRandomizer:
    """
    A class responsible for generating random MAC addresses with support for different MAC types
    such as unicast, multicast, and broadcast.

    Methods:
        randomize(mac_type: MACType = None) -> int:
            Generates a random MAC address, optionally conforming to the specified MAC type.

    Static Methods:
        _prepare(mac_type: MACType = None) -> int:
            Helper function that generates a random 48-bit integer and modifies it according
            to the provided MAC type (unicast, multicast, or broadcast).
    """

    def randomize(self, mac_type:MACType=None) -> int:
        """
        Generates a random MAC address of the specified type.

        Parameters:
        mac_type (MACType, optional): The type of MAC address to generate (unicast, multicast, or broadcast).
        Defaults to None for a generic MAC address.

        Returns:
        int: A randomly generated MAC address as a 48-bit integer.
        """
        return self._prepare(mac_type)

    @staticmethod
    def _prepare(mac_type:MACType=None) -> int:
        """
        Prepares a random MAC address based on the provided MAC type.

        Parameters:
        mac_type (MACType, optional): The type of MAC address to generate.
        Can be UNICAST, MULTICAST, or BROADCAST. Defaults to None for a generic MAC address.

        Returns:
        int: A 48-bit integer representing the generated MAC address.
        """
        # Generate a random 48-bit integer
        mac_int = random.getrandbits(48)
        if mac_type == MACType.UNICAST:
            mac_int &= ~(1 << 40)  # Clear bit 40
        elif mac_type == MACType.MULTICAST:
            mac_int |= (1 << 40)  # Set bit 40
        elif mac_type == MACType.BROADCAST:
            mac_int = 0xFFFFFFFFFFFF  # All bits set to 1
        return mac_int
