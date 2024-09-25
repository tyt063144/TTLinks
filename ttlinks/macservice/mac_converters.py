from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any, List

from ttlinks.common.binary_utils.binary import Octet
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class MACConverterHandler(SimpleCoRHandler):
    def __init__(self, padding: bool = True):
        super().__init__()
        self._padding = padding  # padding 0 from left to right to fill total of 48

    def set_padding(self, padding: bool):
        self._padding = padding

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _to_octets(self, request: Any) -> List[Octet]:
        pass


class OctetMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 6 and all(isinstance(item, Octet) for item in request):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: List[Octet]) -> List[Octet]:
        return request


class BinaryDigitsMAC48ConverterHandler(MACConverterHandler):

    def handle(self, request: Any):
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 48:
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        return [
            OctetFlyWeightFactory.get_octet(binary_string)
            for binary_string in binary_string_list
        ]


class DashedHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('-', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace('-', '').upper()
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class ColonHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace(':', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace(':', '').upper()
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class DotHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('.', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace('.', '').upper()
        return [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]


class OctetOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 3 and all(isinstance(item, Octet) for item in request):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: List[Octet]) -> List[Octet]:
        result = request
        if self._padding:
            result.extend([OctetFlyWeightFactory.get_octet('00000000')] * 3)
        return result


class BinaryDigitsOUI24ConverterHandler(MACConverterHandler):

    def handle(self, request: Any):
        if isinstance(request, list) and all(isinstance(item, int) for item in request) and len(request) == 24:
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        binary_string_list = [
            ''.join(map(str, request[bit_index: bit_index + 8]))
            for bit_index in range(0, len(request), 8)
        ]
        result = [OctetFlyWeightFactory.get_octet(binary_string) for binary_string in binary_string_list]
        if self._padding:
            result.extend([OctetFlyWeightFactory.get_octet('00000000')] * 3)
        return result


class DashedHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('-', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace('-', '').upper()
        result = [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([OctetFlyWeightFactory.get_octet('00000000')] * 3)
        return result


class ColonHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace(':', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace(':', '').upper()
        result = [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([OctetFlyWeightFactory.get_octet('00000000')] * 3)
        return result


class DotHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('.', '').upper()):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: Any) -> List[Octet]:
        raw_mac = request.replace('.', '').upper()
        result = [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(raw_mac[octet_i: octet_i + 2]))
            for octet_i in range(0, len(raw_mac), 2)
        ]
        if self._padding:
            result.extend([OctetFlyWeightFactory.get_octet('00000000')] * 3)
        return result


class OctetEUI64ConverterHandler(MACConverterHandler):
    def handle(self, request: Any):
        if len(request) == 6 and all(isinstance(item, Octet) for item in request):
            return self._to_octets(request)
        else:
            return super().handle(request)

    def _to_octets(self, request: List[Octet]) -> List[Octet]:
        left_binary_digits = [octet.binary_digits for octet in request[0:3]]
        right_binary_digits = [octet.binary_digits for octet in request[3:]]
        middle = [
            OctetFlyWeightFactory.get_octet(NumeralConverter.hexadecimal_to_binary(hexadecimal)).binary_digits
            for hexadecimal in ['ff', 'fe']
        ]
        left_binary_digits[0][6] = 1 if int(left_binary_digits[0][6]) == 0 else 0
        eui64_binary_digits = left_binary_digits + middle + right_binary_digits
        return [
            OctetFlyWeightFactory.get_octet(''.join(map(str, binary_digit)))
            for binary_digit in eui64_binary_digits
        ]


class MACConverter:
    @staticmethod
    def convert_mac(mac: Any, converters: List[MACConverterHandler] = None) -> List[Octet]:
        if converters is None:
            converters = [
                OctetMAC48ConverterHandler(),
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler()
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_oui(mac: Any, converters: List[MACConverterHandler] = None) -> List[Octet]:
        if converters is None:
            converters = [
                OctetMAC48ConverterHandler(),
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                OctetOUI24ConverterHandler(),
                BinaryDigitsOUI24ConverterHandler(),
                DashedHexOUI24ConverterHandler(),
                ColonHexOUI24ConverterHandler(),
                DotHexOUI24ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_to_eui64(mac: Any) -> List[Octet] | None:
        mac_address = MACConverter.convert_mac(mac)
        if mac_address is not None:
            converter_handler = OctetEUI64ConverterHandler()
            return converter_handler.handle(mac_address)
        return None
