from abc import abstractmethod
from typing import List

from ttlinks.common.base_utils import CoRHandler, BinaryClass
from ttlinks.macservice import MACType


class MACAddrClassifierHandler(CoRHandler):
    _next_handler = None

    def set_next(self, h: CoRHandler) -> CoRHandler:
        if not isinstance(h, CoRHandler):
            raise TypeError("The next handler must be an instance of CoRHandler.")
        self._next_handler = h
        return h

    @abstractmethod
    def handle(self, request: List[BinaryClass]):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def verify_type(self, request: List[BinaryClass]) -> bool:
        pass


class BroadcastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: List[BinaryClass]):
        if len(request) == 6 and self.verify_type(request):
            return MACType.BROADCAST
        else:
            return super().handle(request)

    def verify_type(self, request: List[BinaryClass]) -> bool:
        all_bit_digits = []
        for binary in request:
            all_bit_digits.extend(binary.binary_digits)
        return all(all_bit_digits)


class UnicastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: List[BinaryClass]):
        if len(request) == 6 and self.verify_type(request):
            return MACType.UNICAST
        else:
            return super().handle(request)

    def verify_type(self, request: List[BinaryClass]) -> bool:
        return request[0].binary_digits[-1] == 0


class MulticastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: List[BinaryClass]):
        if len(request) == 6 and self.verify_type(request):
            return MACType.MULTICAST
        else:
            return super().handle(request)

    def verify_type(self, request: List[BinaryClass]) -> bool:
        return request[0].binary_digits[-1] != 0


class MACAddrClassifier:
    @staticmethod
    def classify_mac(mac: List[BinaryClass], classifiers: List[MACAddrClassifierHandler] = None) -> MACType:
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
