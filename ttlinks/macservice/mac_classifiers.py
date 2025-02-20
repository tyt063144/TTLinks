from abc import abstractmethod
from typing import List


from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.macservice import MACType

class MACAddrClassifierHandler(SimpleCoRHandler):
    """
    Base abstract handler class for classifying MAC addresses using the Chain of Responsibility pattern.
    
    This class provides a framework for implementing specific MAC address classification logic,
    where each concrete handler will verify the type of a MAC address and either handle it or
    pass it to the next handler in the chain.
    """
    @abstractmethod
    def handle(self, request: bytes, *args, **kwargs):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _verify_type(self, request: bytes) -> bool:
        pass

class BroadcastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    Handles MAC address classification for broadcast addresses.

    This handler checks if a given MAC address matches the broadcast address 
    (i.e., a specific bytes sequence) and classifies it as such. If the address 
    doesn't match, it passes the request to the next handler in the chain.
    """
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.BROADCAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return request == b'\xff\xff\xff\xff\xff\xff'


class UnicastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    Handles MAC address classification for unicast addresses.
    
    A unicast MAC address is identified by checking the least significant bit 
    (LSB) of the first byte. According to the IEEE 802 MAC address conventions, 
    if the LSB of the first byte is `0`, the address is an unicast address.
    
    The expression `request[0] & 1 == 0` effectively isolates the LSB by performing 
    a bitwise AND operation with `1` (binary: `00000001`) and checks if it is `0`.
    
    Example:
    For the MAC address `b'\x02\x11\x22\x33\x44\x55`:
      - The first byte is `0x02` (binary: `00000010`).
      - Performing the operation `0x02 & 1` results in `0`:
        - `00000010`  (binary representation of `0x02`)
        - `00000001`  (binary representation of `1`)
        - `--------`  (bitwise AND operation)
        - `00000000`
      - Since the result is `0`, this indicates an unicast MAC address.
    """
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.UNICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return request[0] & 1 == 0


class MulticastMACAddrClassifierHandler(MACAddrClassifierHandler):
    """
    Handles MAC address classification for multicast addresses.
    
    A multicast MAC address is identified by checking the least significant bit (LSB)
    of the first byte. According to the IEEE 802 MAC address conventions, if the LSB 
    of the first byte is `1`, the address is a multicast address.

    The expression `request[0] & 1 == 1` effectively isolates the LSB by performing 
    a bitwise AND operation with `1` (binary: `00000001`) and checks if it is `1`.
    
    Example:
    For the MAC address `b'\x01\x11\x22\x33\x44\x55`:
      - The first byte is `0x01` (binary: `00000001`).
      - Performing the operation `0x01 & 1` results in `1`:
        - `00000001`  (binary representation of `0x01`)
        - `00000001`  (binary representation of `1`)
        - `--------`  (bitwise AND operation)
        - `00000001`
      - Since the result is `1`, this indicates a multicast MAC address.
    """
    
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.MULTICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return request[0] & 1 == 1


class MACAddrClassifier:
    """
    The MACAddrClassifier class provides a utility to classify MAC addresses 
    into broadcast, unicast, or multicast types using a chain of responsibility 
    pattern. This class orchestrates the classification process by creating a 
    chain of handlers and using the `classify_mac` static method to process the 
    given MAC address.
    """
    
    @staticmethod
    def classify_mac(mac: bytes, classifiers: List[MACAddrClassifierHandler] = None) -> MACType:
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
