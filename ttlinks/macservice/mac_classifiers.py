from abc import abstractmethod
from typing import List


from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter
from ttlinks.macservice import MACType

class MACAddrClassifierHandler(SimpleCoRHandler):
    @abstractmethod
    def handle(self, request: bytes, *args, **kwargs):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _verify_type(self, request: bytes) -> bool:
        pass

class BroadcastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.BROADCAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return all(char == '1' for char in NumeralConverter.bytes_to_binary(request, 48))


class UnicastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.UNICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return request[0] & 1 == 0


class MulticastMACAddrClassifierHandler(MACAddrClassifierHandler):
    def handle(self, request: bytes, *args, **kwargs):
        if len(request) == 6 and self._verify_type(request):
            return MACType.MULTICAST
        else:
            return super().handle(request)

    def _verify_type(self, request: bytes) -> bool:
        return request[0] & 1 == 1


class MACAddrClassifier:
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
