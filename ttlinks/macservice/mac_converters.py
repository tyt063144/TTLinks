from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any, List, Union

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.common.tools.converters import NumeralConverter


class MACConverterHandler(SimpleCoRHandler):
    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        if self._next_handler:
            return self._next_handler.handle(request)
        return self._next_handler

    @abstractmethod
    def _to_bytes(self, request: Any) -> bytes:
        pass

class BinaryDigitsMAC48ConverterHandler(MACConverterHandler):

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and len(request) == 48 and set(request) == {0, 1}:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 6)


class DashedHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('-', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace('-', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class ColonHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace(':', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace(':', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class DotHexMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{12}$', request.replace('.', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace('.', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list)


class DecimalMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, int) and request.bit_length() <= 48 and request > 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: int) -> bytes:
        return NumeralConverter.decimal_to_bytes(request, 6)

class BytesMAC48ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 6 and max(request) <= 255 and min(request) >= 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        return request


class BinaryDigitsOUI24ConverterHandler(MACConverterHandler):

    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, list) and len(request) == 24 and set(request) == {0, 1}:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        return NumeralConverter.binary_to_bytes(''.join(map(str, request)), 3) + b'\x00' * 3


class DashedHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('-', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace('-', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3


class ColonHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace(':', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace(':', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3

class DotHexOUI24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, str) and re.match(r'^[0-9A-F]{6}$', request.replace('.', '').upper()):
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: Any) -> bytes:
        raw_mac = request.replace('.', '').upper()
        bytes_list = [
            NumeralConverter.hexadecimal_to_bytes(raw_mac[octet_i: octet_i + 2], 1)
            for octet_i in range(0, len(raw_mac), 2)
        ]
        return b''.join(bytes_list) + b'\x00' * 3


class BytesMAC24ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 3 and max(request) <= 255 and min(request) >= 0:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        return request + b'\x00' * 3


class OctetEUI64ConverterHandler(MACConverterHandler):
    def handle(self, request: Any, *args, **kwargs):
        if isinstance(request, bytes) and len(request) == 6:
            return self._to_bytes(request)
        else:
            return super().handle(request)

    def _to_bytes(self, request: bytes) -> bytes:
        left_binary_digits = request[0:3]
        right_binary_digits = request[3:]
        return b''.join([left_binary_digits, b'\xFF\xFE', right_binary_digits])


class MACConverter:
    @staticmethod
    def convert_mac(mac: Any, converters: List[MACConverterHandler] = None) -> bytes:
        if converters is None:
            converters = [
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                DecimalMAC48ConverterHandler(),
                BytesMAC48ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_oui(mac: Any, converters: List[MACConverterHandler] = None) -> bytes:
        if converters is None:
            converters = [
                BinaryDigitsMAC48ConverterHandler(),
                DashedHexMAC48ConverterHandler(),
                ColonHexMAC48ConverterHandler(),
                DotHexMAC48ConverterHandler(),
                DecimalMAC48ConverterHandler(),
                BytesMAC48ConverterHandler(),
                BinaryDigitsOUI24ConverterHandler(),
                DashedHexOUI24ConverterHandler(),
                ColonHexOUI24ConverterHandler(),
                DotHexOUI24ConverterHandler(),
                BytesMAC24ConverterHandler(),
            ]
        converter_handler = converters[0]
        for next_handler in converters[1:]:
            converter_handler.set_next(next_handler)
            converter_handler = next_handler
        return converters[0].handle(mac)

    @staticmethod
    def convert_to_eui64(mac: Any) -> Union[bytes, None]:
        mac_address = MACConverter.convert_mac(mac)
        if mac_address is not None:
            converter_handler = OctetEUI64ConverterHandler()
            return converter_handler.handle(mac_address)
        return None
