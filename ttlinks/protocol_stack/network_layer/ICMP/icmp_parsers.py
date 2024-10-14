from __future__ import annotations
from abc import ABC

from ttlinks.common.design_template.cor import TrackedCoRHandler
from ttlinks.protocol_stack.network_layer.ICMP.icmp_parse_routers import ICMPParseRouter


class ICMPFieldParserHandler(TrackedCoRHandler, ABC):
    """
    Abstract base class for parsing ICMP fields using the Chain of Responsibility pattern.

    Inherits from TrackedCoRHandler, which allows tracking parsed fields in the `_tracker` dictionary.
    Subclasses will implement specific field parsing logic, such as ICMP type, code, and checksum.
    """
    pass

class ICMPTypeFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Type field from the packet payload.

    This class extracts the first byte of the ICMP payload, representing the ICMP type, and stores it in the `_tracker`.
    It then passes the remaining payload to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['icmp_type'] = payload[:1]
        if self._next_handler:
            return self._next_handler.handle(payload, index=1, *args, **kwargs)

class ICMPCodeFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Code field from the packet payload.

    This class extracts the ICMP Code (the byte following the ICMP Type) and stores it in the `_tracker`.
    It then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['icmp_code'] = payload[kwargs['index']:kwargs['index']+1]
        if self._next_handler:
            kwargs['index'] += 1
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPChecksumFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Checksum field from the packet payload.

    This class extracts the ICMP Checksum (the two bytes following the ICMP Code) and stores it in the `_tracker`.
    After extracting the checksum, it uses the `ICMPParseRouter` to route the payload to the appropriate
    handlers based on the ICMP type.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['checksum'] = payload[kwargs['index']:kwargs['index']+2]
            icmp_type = int.from_bytes(self._tracker['icmp_type'], 'big')
            ICMPParseRouter.route(self, icmp_type=icmp_type)
        if self._next_handler:
            kwargs['index'] += 2
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPIdentifierFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Identifier field from the packet payload.

    This class extracts the Identifier field (2 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['identifier'] = payload[kwargs['index']:kwargs['index']+2]
        if self._next_handler:
            kwargs['index'] += 2
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPSequenceNumberFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Sequence Number field from the packet payload.

    This class extracts the Sequence Number field (2 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['sequence_number'] = payload[kwargs['index']:kwargs['index']+2]
        if self._next_handler:
            kwargs['index'] += 2
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPGatewayAddressFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Gateway Address field from the packet payload.

    This class extracts the Gateway Address field (4 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['gateway_address'] = payload[kwargs['index']:kwargs['index']+4]
        if self._next_handler:
            kwargs['index'] += 4
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPOriginalTimestampFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Originate Timestamp field from the packet payload.

    This class extracts the Originate Timestamp field (4 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['originate_timestamp'] = payload[kwargs['index']:kwargs['index']+4]
        if self._next_handler:
            kwargs['index'] += 4
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPReceiveTimestampFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Receive Timestamp field from the packet payload.

    This class extracts the Receive Timestamp field (4 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['receive_timestamp'] = payload[kwargs['index']:kwargs['index']+4]
        if self._next_handler:
            kwargs['index'] += 4
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPTransmitTimestampFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Transmit Timestamp field from the packet payload.

    This class extracts the Transmit Timestamp field (4 bytes) from the ICMP packet and stores it in the `_tracker`.
    The handler then passes the remaining payload to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['transmit_timestamp'] = payload[kwargs['index']:kwargs['index']+4]
        if self._next_handler:
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPPointerFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Pointer field from the packet payload.

    This class extracts the Pointer field (1 byte) from the ICMP packet and stores it in the `_tracker`.
    It also sets the `unused_bytes` to 3, which indicates the size of the next unused field in this context.
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['pointer'] = payload[kwargs['index']:kwargs['index']+1]
            kwargs['unused_bytes'] = 3
        if self._next_handler:
            kwargs['index'] += 2
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPUnusedFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Unused field from the packet payload.

    This class extracts the Unused field from the ICMP packet, which can vary in size depending on the context.
    It uses the `unused_bytes` value from the kwargs to determine the length of the unused field (default is 4 bytes).
    The handler then passes the remaining payload and updated index to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            unused_bytes = kwargs.get('unused_bytes', 4)
            self._tracker['unused'] = payload[kwargs['index']:kwargs['index']+unused_bytes]
        if self._next_handler:
            kwargs['index'] += 4
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPPayloadFieldParserHandler(ICMPFieldParserHandler):
    """
    Handler for parsing the ICMP Payload field from the packet payload.

    This class extracts the Payload field, which is the remaining bytes in the packet after the other fields are parsed.
    The handler then passes the remaining payload to the next handler in the chain.
    """
    def handle(self, payload: bytes, *args, **kwargs):
        if isinstance(payload, bytes):
            self._tracker['payload'] = payload[kwargs['index']:]
        if self._next_handler:
            return self._next_handler.handle(payload, *args, **kwargs)

class ICMPParser:
    """
    Singleton class for parsing ICMP packets using the Chain of Responsibility pattern.

    This class ensures that only one instance of ICMPParser exists. It resets the parser chain for each
    new ICMP frame, starting with the Type field handler. The Chain of Responsibility pattern is used to
    delegate the parsing of ICMP fields to various handlers.
    """
    __instance: ICMPParser = None

    def __new__(cls):
        """
        Ensures that only one instance of ICMPParser is created (Singleton pattern).
        """
        if cls.__instance is None:
            cls.__instance = super(ICMPParser, cls).__new__(cls)
        return cls.__instance

    def _reset_parser(self):
        """
        Resets the parser chain by setting up the initial chain of responsibility handlers for ICMP parsing.

        This method starts with the ICMP Type, Code, and Checksum handlers. Additional handlers are dynamically
        added later by the router based on the ICMP type after checksum parsing.
        """
        # Initialize the payload parser chain with ICMP Type, Code, and Checksum fields
        self._payload_parser = ICMPTypeFieldParserHandler()
        (
            self._payload_parser
            .set_next(ICMPCodeFieldParserHandler())
            .set_next(ICMPChecksumFieldParserHandler())
        )

    def parse(self, frame: bytes) -> dict:
        """
        Parses the ICMP frame using the Chain of Responsibility pattern.

        This method resets the parser chain, invokes the chain to parse the frame,
        and returns the parsed fields as a dictionary.

        Parameters:
        - frame (bytes): The raw bytes of the ICMP packet to be parsed.

        Returns:
        - dict: A dictionary containing the parsed ICMP fields, tracked by each handler.
        """
        self._reset_parser()
        self._payload_parser.handle(frame)
        return self._payload_parser.get_tracker()