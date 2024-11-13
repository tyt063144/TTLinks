from __future__ import annotations
from abc import ABC
from typing import Any

from ttlinks.common.design_template.cor import TrackedCoRHandler, ListBasedCoRHandler
from ttlinks.protocol_stack.transport_layer.TCP import tcp_options


# ------------------TCP Header Field Parser Handlers------------------
class TCPParserHandler(TrackedCoRHandler, ABC):
    """
    Base handler class for parsing fields of a TCP packet using the **Chain of Responsibility** pattern.
    Each subclass handles a specific part of the TCP header, storing its result in `_tracker`.
    """
    pass

class TCPSourcePortFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the source port from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts the first 2 bytes for the source port field
      and stores it in `_tracker['source_port']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['source_port'] = packet[0:2]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPDestinationPortFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the destination port from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 2-4 for the destination port field
      and stores it in `_tracker['destination_port']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['destination_port'] = packet[2:4]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPSequenceNumberFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the sequence number from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 4-8 for the sequence number field
      and stores it in `_tracker['sequence_number']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['sequence_number'] = packet[4:8]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPAcknowledgmentNumberFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the acknowledgment number from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 8-12 for the acknowledgment number field
      and stores it in `_tracker['acknowledgment_number']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['acknowledgment_number'] = packet[8:12]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPOffsetReservedFlagsFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the offset, reserved bits, and flags from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 12-14 for the offset, reserved bits, and flags,
      and stores it in `_tracker['offset_reserved_flags']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['offset_reserved_flags'] = packet[12:14]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPWindowSizeFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the window size from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 14-16 for the window size field
      and stores it in `_tracker['window_size']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['window_size'] = packet[14:16]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPChecksumFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the checksum from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 16-18 for the checksum field
      and stores it in `_tracker['checksum']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['checksum'] = packet[16:18]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPURGPointerFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the urgent pointer from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts bytes 18-20 for the urgent pointer field
      and stores it in `_tracker['urgent_pointer']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['urgent_pointer'] = packet[18:20]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPOptionsFieldParserHandler(TCPParserHandler):
    """
    Handler to parse TCP options from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Determines the length of the options field based on the header length
      indicated in the offset_reserved_flags, extracts it, and stores it in `_tracker['options']`.
      Updates `kwargs['options_end']` to mark the end of the options field.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            tcp_length_bytes = (self._tracker['offset_reserved_flags'][0] >> 4) * 4
            self._tracker['options'] = packet[20:tcp_length_bytes]
            kwargs['options_end'] = tcp_length_bytes
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

class TCPPayloadFieldParserHandler(TCPParserHandler):
    """
    Handler to parse the payload from a TCP packet.

    Methods:
    - handle(packet: bytes, *args, **kwargs): Extracts the payload from the packet starting at `options_end`,
      as marked in `kwargs`, and stores it in `_tracker['payload']`.
    """
    def handle(self, packet: bytes, *args, **kwargs):
        if isinstance(packet, bytes):
            self._tracker['payload'] = packet[kwargs['options_end']:]
        if self._next_handler:
            return self._next_handler.handle(packet, *args, **kwargs)

# ------------------TCP Options Field Parser Handlers------------------
class TCPOptionsParserHandler(ListBasedCoRHandler, ABC):
    """
    Base handler class for parsing TCP options using the **Chain of Responsibility** pattern.
    Each subclass handles a specific TCP option kind and appends the parsed option unit to `_items`.

    Methods:
    - handle(options: bytes, *args, **kwargs): Passes the `options` bytes to the next handler if no specific
      option is handled in this class.
    """
    def handle(self, options: bytes, *args, **kwargs) -> Any:
        if self._next_handler:
            return self._next_handler.handle(options, *args, **kwargs)
        return self._next_handler

class TCPOption0ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 0 (End of Option List).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 0, creates a TCPOption0Unit,
      and appends it to `_items`. Passes remaining options to the first handler for further parsing.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[0:1] == b'\x00':
            option_params = {'kind': options[:1]}
            self._items.append(tcp_options.TCPOption0Unit(**option_params))
            return kwargs['first_handler'].handle(options[1:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption1ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 1 (No Operation).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 1, creates a TCPOption1Unit,
      and appends it to `_items`. Passes remaining options to the first handler for further parsing.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[0:1] == b'\x01':
            option_params = {'kind': options[:1]}
            self._items.append(tcp_options.TCPOption1Unit(**option_params))
            return kwargs['first_handler'].handle(options[1:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption2ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 2 (Maximum Segment Size).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 2, extracts the option length,
      creates a TCPOption2Unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[:1] == b'\x02':
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPOption2Unit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption3ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 3 (Window Scale).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 3, extracts the option length,
      creates a TCPOption3Unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[:1] == b'\x03':
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPOption3Unit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption4ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 4 (Selective Acknowledgment Permitted).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 4, extracts the option length,
      creates a TCPOption4Unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[:1] == b'\x04':
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPOption4Unit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption5ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 5 (Selective Acknowledgment, or SACK).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 5, extracts the option length,
      creates a TCPOption5Unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[:1] == b'\x05':
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPOption5Unit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOption8ParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing TCP option kind 8 (Timestamp Option).

    Methods:
    - handle(options: bytes, *args, **kwargs): Checks if the option kind is 8, extracts the option length,
      creates a TCPOption8Unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options[:1] == b'\x08':
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPOption8Unit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPUnknownOptionParserHandler(TCPOptionsParserHandler):
    """
    Handler for parsing unknown TCP options.

    Methods:
    - handle(options: bytes, *args, **kwargs): Parses an unrecognized option kind, extracts its length,
      creates a TCPUnknownOption unit, and appends it to `_items`. Passes remaining options to the first handler.
    """
    def handle(self, options: bytes, *args, **kwargs):
        if isinstance(options, bytes) and options:
            length = int.from_bytes(options[1:2], byteorder='big')
            target_option_bytes = options[:length]
            option_params = {
                'kind': target_option_bytes[:1],
                'length': target_option_bytes[1:2],
                'value': target_option_bytes[2:length]
            }
            self._items.append(tcp_options.TCPUnknownOptionUnit(**option_params))
            return kwargs['first_handler'].handle(options[length:], first_handler=kwargs['first_handler'])
        else:
            return super().handle(options, *args, **kwargs)

class TCPOptionParser:
    """
    Parser for handling TCP options using a chain of handlers. The parser resets with a predefined sequence
    of handlers for various known TCP options and a final handler for unknown options.

    Methods:
    - _reset_parser(): Initializes the chain of option handlers in a specific order, including known and unknown option handlers.
    - parse(options: bytes): Initiates the option parsing process on the provided byte sequence.

    Returns:
    - list: Parsed TCP options as a list of option units.
    """
    def _reset_parser(self):
        """
        Sets up the TCP option parser chain by linking specific handlers for each known TCP option
        and an unknown option handler at the end of the chain.

        Returns:
        - TCPOptionsParserHandler: The start of the parser chain.
        """
        self._option_parser = TCPOption1ParserHandler()
        (
            self._option_parser
            .set_next(TCPOption2ParserHandler())
            .set_next(TCPOption3ParserHandler())
            .set_next(TCPOption4ParserHandler())
            .set_next(TCPOption5ParserHandler())
            .set_next(TCPOption8ParserHandler())
            .set_next(TCPOption0ParserHandler())
            .set_next(TCPUnknownOptionParserHandler())
        )
        return self._option_parser

    def parse(self, options: bytes):
        """
        Parses the given TCP options byte sequence by passing it through the chain of handlers.

        Parameters:
        - options (bytes): The byte sequence containing TCP options.

        Returns:
        - list: Parsed options as a list of TCPOption units.
        """
        option_parser = self._reset_parser()
        option_parser.handle(options, first_handler=option_parser)
        return self._option_parser.get_items()


class TCPParser:
    """
    Singleton parser class for parsing a full TCP frame. Uses a chain of handlers to process each
    field of the TCP header and stores results in a tracker.

    Methods:
    - __new__: Ensures only one instance of the parser exists.
    - _reset_parser: Initializes the chain of handlers for each TCP header field in order.
    - parse(frame: bytes): Parses the provided TCP frame byte sequence.

    Returns:
    - dict: Parsed TCP fields stored in the tracker.
    """
    __instance: TCPParser = None

    def __new__(cls):
        """
        Ensures a single instance of the TCPParser class, implementing the Singleton pattern.

        Returns:
        - TCPParser: The single instance of the TCPParser class.
        """
        if cls.__instance is None:
            cls.__instance = super(TCPParser, cls).__new__(cls)
        return cls.__instance

    def _reset_parser(self):
        """
        Sets up the TCP packet parser chain by linking specific handlers for each field in the TCP header.

        Returns:
        - None
        """
        self._packet_parser = TCPSourcePortFieldParserHandler()
        (
            self._packet_parser
            .set_next(TCPDestinationPortFieldParserHandler())
            .set_next(TCPSequenceNumberFieldParserHandler())
            .set_next(TCPAcknowledgmentNumberFieldParserHandler())
            .set_next(TCPOffsetReservedFlagsFieldParserHandler())
            .set_next(TCPWindowSizeFieldParserHandler())
            .set_next(TCPChecksumFieldParserHandler())
            .set_next(TCPURGPointerFieldParserHandler())
            .set_next(TCPOptionsFieldParserHandler())
            .set_next(TCPPayloadFieldParserHandler())
        )

    def parse(self, frame: bytes):
        """
        Parses the given TCP frame byte sequence by passing it through the chain of handlers.

        Parameters:
        - frame (bytes): The byte sequence representing the entire TCP frame.

        Returns:
        - dict: Parsed TCP fields with their respective values stored in the tracker.
        """
        self._reset_parser()
        self._packet_parser.handle(frame)
        return self._packet_parser.get_tracker()

