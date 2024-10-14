from __future__ import annotations
from abc import ABC

from ttlinks.common.design_template.cor import TrackedCoRHandler


class EtherFrameFieldParserHandler(TrackedCoRHandler, ABC):
    """
    Abstract base class for parsing Ethernet frame fields in a Chain of Responsibility (CoR) pattern.

    This class extends the `TrackedCoRHandler` to track parsed fields of an Ethernet frame
    while allowing different handlers to be chained together. Subclasses must implement the
    `handle` method to parse specific fields of the frame.

    Methods:
    - handle: To be implemented by subclasses to parse a specific section of the Ethernet frame.

    Parameters:
    None

    Returns:
    None
    """
    pass

class FrameDstFieldParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the destination MAC address from an Ethernet frame.

    This handler extracts the first 6 bytes of the frame (which represent the destination MAC address)
    and stores them in the `_tracker` dictionary under the key 'dst'. It then passes the frame to the next handler
    in the chain, if any.

    Methods:
    - handle: Parses the destination MAC address and invokes the next handler if available.

    Parameters:
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            self._tracker['dst'] = frame[:6]
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)


class FrameSrcFieldParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the source MAC address from an Ethernet frame.

    This handler extracts bytes 6 to 12 of the frame (which represent the source MAC address)
    and stores them in the `_tracker` dictionary under the key 'src'. It then passes the frame to the next handler
    in the chain, if any.

    Methods:
    - handle: Parses the source MAC address and invokes the next handler if available.

    Parameters:
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            self._tracker['src'] = frame[6:12]
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)

class EthernetTypeFieldParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the EtherType or Length field from an Ethernet frame.

    This handler extracts bytes 12 to 14, which could represent either the EtherType or the length of
    the payload depending on the value. If the value is greater than or equal to 1536, it is interpreted
    as EtherType, otherwise as length. Based on the result, the appropriate next handler is set.

    Methods:
    - handle: Parses the EtherType/Length field and invokes the next handler based on the field value.

    Parameters:
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            type_or_length = int.from_bytes(frame[12:14], 'big')
            if type_or_length >= 1536:
                self._tracker['type'] = frame[12:14]
                self.set_next(EthernetPayloadParserHandler(payload_start_offset=14))
            else:
                self._tracker['length'] = frame[12:14]
                self.set_next(IEEE8023LLCFieldParserHandler())
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)


class IEEE8023LLCFieldParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the IEEE 802.3 LLC (Logical Link Control) field from an Ethernet frame.

    This handler extracts bytes 14 to 17, which represent the LLC field. If the first two bytes of the
    LLC field are `0xAA` (indicating the presence of a SNAP header), the handler passes the frame to
    the `IEEE8023SNAPFieldParserHandler`. Otherwise, it passes the frame to the `EthernetPayloadParserHandler`.

    Methods:
    - handle: Parses the LLC field and invokes the next handler based on the LLC field content.

    Parameters:
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            self._tracker['llc'] = frame[14:17]
            if frame[14:15] == b'\xAA' and frame[15:16] == b'\xAA':
                self.set_next(IEEE8023SNAPFieldParserHandler())
            else:
                self._tracker['snap'] = b''
                self.set_next(EthernetPayloadParserHandler(payload_start_offset=17))
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)

class IEEE8023SNAPFieldParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the IEEE 802.3 SNAP (Subnetwork Access Protocol) field from an Ethernet frame.

    This handler extracts bytes 17 to 22, which represent the SNAP field. Once the SNAP field is parsed,
    the frame is passed to the `EthernetPayloadParserHandler`.

    Methods:
    - handle: Parses the SNAP field and invokes the next handler to process the Ethernet payload.

    Parameters:
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            self._tracker['snap'] = frame[17:22]
            self.set_next(EthernetPayloadParserHandler(payload_start_offset=22))
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)

class EthernetPayloadParserHandler(EtherFrameFieldParserHandler):
    """
    Handler for parsing the payload section of an Ethernet frame.

    This handler extracts the payload starting from a specified offset in the frame. The payload is
    stored in the `_tracker` dictionary under the key 'payload'. After extracting the payload, the frame
    can be passed to the next handler in the chain, if any.

    Methods:
    - handle: Parses the payload starting from the given offset.

    Parameters:
    - payload_start_offset (int): The offset in the frame where the payload begins.
    - frame (bytes): The Ethernet frame to be parsed.
    - *args, **kwargs: Additional arguments for custom handling.

    Returns:
    The result of the next handler in the chain, if applicable.
    """
    def __init__(self, payload_start_offset: int = 0):
        super().__init__()
        self._payload_start_offset = payload_start_offset

    def handle(self, frame: bytes, *args, **kwargs):
        if isinstance(frame, bytes):
            self._tracker['payload'] = frame[self._payload_start_offset:]
        if self._next_handler:
            return self._next_handler.handle(frame, *args, **kwargs)


class EthernetFrameParser:
    """
    A Singleton class responsible for parsing Ethernet frames.

    This class implements the **Singleton** design pattern, ensuring that only one instance of
    `EthernetFrameParser` can exist. It utilizes a chain of responsibility for parsing different fields
    in the Ethernet frame, starting with the destination MAC address, followed by the source MAC address,
    and finally the EtherType/Length field.

    Methods:
    - parse: Resets the parser and initiates the chain of responsibility to parse the Ethernet frame.
    - _reset_parser: Initializes and chains together the frame field handlers (destination, source, EtherType).

    Attributes:
    __instance (EthernetFrameParser): Holds the single instance of the class (Singleton pattern).
    _frame_parser: The first handler in the chain of responsibility for parsing the Ethernet frame.
    """
    __instance: EthernetFrameParser = None

    def __new__(cls):
        """
        Ensures that only one instance of EthernetFrameParser is created (Singleton pattern).

        Returns:
        EthernetFrameParser: The single instance of the class.
        """
        if cls.__instance is None:
            cls.__instance = super(EthernetFrameParser, cls).__new__(cls)
        return cls.__instance

    def _reset_parser(self):
        """
        Resets the parser by setting up the chain of responsibility.

        The parsing chain starts with the destination MAC address handler, followed by the source MAC
        address handler, and ends with the EtherType/Length field handler. Each handler is responsible
        for a specific part of the Ethernet frame.

        Returns:
        None
        """
        self._frame_parser = FrameDstFieldParserHandler()
        self._frame_parser.set_next(FrameSrcFieldParserHandler()).set_next(EthernetTypeFieldParserHandler())

    def parse(self, frame: bytes) -> dict:
        """
        Parses an Ethernet frame by passing it through the chain of handlers.

        This method resets the parser to its initial state and initiates the chain of responsibility
        for parsing the frame fields. After parsing, it returns the tracking information from the handlers.

        Parameters:
        frame (bytes): The raw Ethernet frame to be parsed.

        Returns:
        dict: A dictionary containing the parsed fields of the Ethernet frame (e.g., destination MAC, source MAC, EtherType).
        """
        self._reset_parser()
        self._frame_parser.handle(frame)
        return self._frame_parser.get_tracker()