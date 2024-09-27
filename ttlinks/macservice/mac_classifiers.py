from abc import abstractmethod
from typing import List


from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.macservice import MACType


class MACAddrClassifierHandler(SimpleCoRHandler):
    """
    Abstract base class for handling and classifying MAC addresses.
    This class follows the Chain of Responsibility (CoR) design pattern, allowing requests (MAC addresses)
    to be processed by a chain of handlers. Each handler verifies the type of MAC address and can
    pass the request to the next handler if needed.

    Inherits from:
    - SimpleCoRHandler: A base class for implementing the Chain of Responsibility pattern.

    Methods:
    - handle(request: List[Octet]): Handles the MAC address classification request. If this handler cannot process
      the request, it passes the request to the next handler in the chain.
    - _verify_type(request: List[Octet]) -> bool: Abstract method to verify the MAC address type. This must
      be implemented by subclasses to define the verification logic.
    """
    @abstractmethod
    def handle(self, request: List[Octet]):
        """
        Handles the classification of the provided MAC address. If the current handler cannot classify the MAC address,
        the request is passed to the next handler in the chain.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - The result from the next handler in the chain if this handler cannot process the request. If no further handler exists,
          returns None.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _verify_type(self, request: List[Octet]) -> bool:
        """
        Abstract method to verify if the provided MAC address matches a specific type (e.g., Unicast, Multicast, Broadcast).
        This method must be implemented by subclasses to provide the specific logic for verifying the MAC address type.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - bool: True if the MAC address matches the expected type, False otherwise.
        """
        pass


class BroadcastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    A concrete implementation of MACAddrClassifierHandler that checks if a given MAC address is of Broadcast type.
    It classifies the MAC address as a broadcast address if all bits are set to 1.

    Methods:
    - handle(request: List[Octet]): Processes the request and returns the MACType.BROADCAST if the MAC address is
      identified as a broadcast address, otherwise passes the request to the next handler.
    - _verify_type(request: List[Octet]) -> bool: Verifies if the MAC address is a broadcast address, where all bits are set to 1.
    """
    def handle(self, request: List[Octet]):
        """
        Handles the classification of the provided MAC address. If the MAC address is a broadcast address
        (all bits are set to 1), it returns MACType.BROADCAST. Otherwise, the request is passed to the next handler.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - MACType.BROADCAST if the MAC address is a broadcast address.
        - Calls the next handler if the MAC address is not broadcast.
        """
        if len(request) == 6 and self._verify_type(request):
            return MACType.BROADCAST
        else:
            return super().handle(request)

    def _verify_type(self, request: List[Octet]) -> bool:
        """
        Verifies if the given MAC address is a broadcast address. A broadcast MAC address consists of
        all bits set to 1.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - bool: True if all bits in the MAC address are set to 1, otherwise False.
        """
        all_bit_digits = []
        for binary in request:
            all_bit_digits.extend(binary.binary_digits)
        return all(all_bit_digits)


class UnicastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    A concrete implementation of MACAddrClassifierHandler that checks if a given MAC address is of Unicast type.
    It classifies the MAC address as unicast if the least significant bit (LSB) of the first octet is 0.

    Methods:
    - handle(request: List[Octet]): Processes the request and returns the MACType.UNICAST if the MAC address is
      identified as a unicast address, otherwise passes the request to the next handler.
    - _verify_type(request: List[Octet]) -> bool: Verifies if the MAC address is a unicast address based on the LSB.
    """
    def handle(self, request: List[Octet]):
        """
        Handles the classification of the provided MAC address. If the MAC address is identified as a unicast address
        (LSB of the first octet is 0), it returns MACType.UNICAST. Otherwise, the request is passed to the next handler.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - MACType.UNICAST if the MAC address is a unicast address.
        - Calls the next handler if the MAC address is not unicast.
        """
        if len(request) == 6 and self._verify_type(request):
            return MACType.UNICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: List[Octet]) -> bool:
        """
        Verifies if the given MAC address is a unicast address. A unicast MAC address has the least significant
        bit (LSB) of the first octet set to 0.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - bool: True if the LSB of the first octet is 0 (unicast), otherwise False.
        """
        return request[0].binary_digits[-1] == 0


class MulticastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    A concrete implementation of MACAddrClassifierHandler that checks if a given MAC address is of Multicast type.
    It classifies the MAC address as multicast if the least significant bit (LSB) of the first octet is 1.

    Methods:
    - handle(request: List[Octet]): Processes the request and returns the MACType.MULTICAST if the MAC address is
      identified as a multicast address, otherwise passes the request to the next handler.
    - _verify_type(request: List[Octet]) -> bool: Verifies if the MAC address is a multicast address based on the LSB.
    """
    def handle(self, request: List[Octet]):
        """
        Handles the classification of the provided MAC address. If the MAC address is identified as a multicast address
        (LSB of the first octet is 1), it returns MACType.MULTICAST. Otherwise, the request is passed to the next handler.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - MACType.MULTICAST if the MAC address is a multicast address.
        - Calls the next handler if the MAC address is not multicast.
        """
        if len(request) == 6 and self._verify_type(request):
            return MACType.MULTICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: List[Octet]) -> bool:
        """
        Verifies if the given MAC address is a multicast address. A multicast MAC address has the least significant
        bit (LSB) of the first octet set to 1.

        Parameters:
        - request (List[Octet]): A list of Octet objects representing the MAC address.

        Returns:
        - bool: True if the LSB of the first octet is 1 (multicast), otherwise False.
        """
        return request[0].binary_digits[-1] != 0


class MACAddrClassifier:
    """
    A static class that classifies MAC addresses using a chain of classifier handlers. The handlers follow the Chain
    of Responsibility pattern and classify the MAC address as Unicast, Multicast, or Broadcast.

    Methods:
    - classify_mac(mac: List[Octet], classifiers: List[MACAddrClassifierHandler] = None) -> MACType:
      Classifies the provided MAC address using the provided classifiers. If no classifiers are provided,
      it uses default handlers (Broadcast, Unicast, and Multicast).
    """
    @staticmethod
    def classify_mac(mac: List[Octet], classifiers: List[MACAddrClassifierHandler] = None) -> MACType:
        """
        Classifies the provided MAC address by passing it through a chain of MAC address classifiers.
        By default, the chain includes Broadcast, Unicast, and Multicast classifiers. The MAC address is processed
        by each handler until a classification is made.

        Parameters:
        - mac (List[Octet]): A list of Octet objects representing the MAC address.
        - classifiers (List[MACAddrClassifierHandler], optional): A list of classifier handlers. If not provided,
          the default handlers (Broadcast, Unicast, Multicast) are used.

        Returns:
        - MACType: The classification of the MAC address (UNICAST, MULTICAST, BROADCAST).
        """
        if classifiers is None:
            classifiers = [
                BroadcastMACAddrClassifierHandler(),
                UnicastMACAddrClassifierHandler(),
                MulticastMACAddrClassifierHandler(),
            ]
        classifier_handler = classifiers[0]
        for next_handler in classifiers[1:]:
            classifier_handler.set_next(next_handler)
            classifier_handler = next_handler
        return classifiers[0].handle(mac)
