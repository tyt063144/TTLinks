from __future__ import annotations

from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.protocol_stack.network_layer.ICMP import icmp_parsers
from ttlinks.protocol_stack.network_layer.ICMP.icmp_utils import ICMPTypes


class ICMPParseRouterHandler(SimpleCoRHandler):
    """
    Base class for routing ICMP parsing logic based on the ICMP type.

    This class forms part of the Chain of Responsibility (CoR) pattern, forwarding requests
    down the chain if no specific handler is responsible for the ICMP type. Subclasses are
    expected to implement specialized behavior for specific ICMP message types.
    """
    def handle(self, handler, *args, **kwargs):
        """
        Forwards the request to the next handler in the chain if available.

        Parameters:
        - handler: The current handler instance responsible for processing ICMP fields.
        - *args, **kwargs: Additional arguments passed to the handler.

        Returns:
        The next handler in the chain if available, or None if no next handler exists.
        """
        if self._next_handler:
            return self._next_handler.handle(handler, *args, **kwargs)
        return self._next_handler

class ICMPEchoAndRequestParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Echo Request and Echo Reply messages.

    This class checks if the ICMP type is either Echo Request or Echo Reply. If it is,
    it chains together handlers responsible for parsing ICMP fields specific to Echo messages,
    such as the identifier, sequence number, and payload.

    Methods:
    - handle: Processes ICMP Echo messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        """
        Handles ICMP Echo Request and Echo Reply types by chaining specific field parsers.

        Parameters:
        - handler: The current handler instance responsible for processing ICMP fields.
        - *args, **kwargs: Additional arguments, including 'icmp_type' for determining ICMP message type.

        Returns:
        The next handler in the chain or None if the ICMP type does not match.
        """
        if kwargs['icmp_type'] in [ICMPTypes.ECHO.value, ICMPTypes.ECHO_REPLY.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPIdentifierFieldParserHandler())
                .set_next(icmp_parsers.ICMPSequenceNumberFieldParserHandler())
                .set_next(icmp_parsers.ICMPPayloadFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)


class ICMPDestinationUnreachableParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Destination Unreachable messages.

    This class checks if the ICMP type is Destination Unreachable. If it is, it chains
    together handlers responsible for parsing ICMP fields specific to this message type,
    such as the unused field and payload.

    Methods:
    - handle: Processes ICMP Destination Unreachable messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        """
        Handles ICMP Destination Unreachable type by chaining specific field parsers.

        Parameters:
        - handler: The current handler instance responsible for processing ICMP fields.
        - *args, **kwargs: Additional arguments, including 'icmp_type' for determining ICMP message type.

        Returns:
        The next handler in the chain or None if the ICMP type does not match.
        """
        if kwargs['icmp_type'] in [ICMPTypes.DESTINATION_UNREACHABLE.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPUnusedFieldParserHandler())
                .set_next(icmp_parsers.ICMPPayloadFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)

class ICMPRedirectMessageParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Redirect messages.

    This class checks if the ICMP type is Redirect and chains the appropriate field
    parsers for parsing the Gateway Address and Payload fields in the ICMP Redirect message.

    Methods:
    - handle: Processes ICMP Redirect messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        if kwargs['icmp_type'] in [ICMPTypes.REDIRECT.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPGatewayAddressFieldParserHandler())
                .set_next(icmp_parsers.ICMPPayloadFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)

class ICMPTimeExceededParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Time Exceeded messages.

    This class checks if the ICMP type is Time Exceeded and chains the appropriate field
    parsers for parsing the Unused and Payload fields in the ICMP Time Exceeded message.

    Methods:
    - handle: Processes ICMP Time Exceeded messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        if kwargs['icmp_type'] in [ICMPTypes.TIME_EXCEEDED.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPUnusedFieldParserHandler())
                .set_next(icmp_parsers.ICMPPayloadFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)

class ICMPParameterProblemParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Parameter Problem messages.

    This class checks if the ICMP type is Parameter Problem and chains the appropriate
    field parsers for parsing the Pointer, Unused, and Payload fields in the ICMP Parameter Problem message.

    Methods:
    - handle: Processes ICMP Parameter Problem messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        if kwargs['icmp_type'] in [ICMPTypes.PARAMETER_PROBLEM.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPPointerFieldParserHandler())
                .set_next(icmp_parsers.ICMPUnusedFieldParserHandler())
                .set_next(icmp_parsers.ICMPPayloadFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)

class ICMPTimestampAndReplyParseRouterHandler(ICMPParseRouterHandler):
    """
    Handler for parsing ICMP Timestamp and Timestamp Reply messages.

    This class checks if the ICMP type is Timestamp or Timestamp Reply and chains the appropriate field
    parsers for parsing the Identifier, Sequence Number, Original Timestamp, Receive Timestamp,
    and Transmit Timestamp fields.

    Methods:
    - handle: Processes ICMP Timestamp and Timestamp Reply messages and forwards other ICMP types to the next handler.
    """
    def handle(self, handler, *args, **kwargs):
        if kwargs['icmp_type'] in [ICMPTypes.TIMESTAMP.value, ICMPTypes.TIMESTAMP_REPLY.value]:
            (
                handler
                .set_next(icmp_parsers.ICMPIdentifierFieldParserHandler())
                .set_next(icmp_parsers.ICMPSequenceNumberFieldParserHandler())
                .set_next(icmp_parsers.ICMPOriginalTimestampFieldParserHandler())
                .set_next(icmp_parsers.ICMPReceiveTimestampFieldParserHandler())
                .set_next(icmp_parsers.ICMPTransmitTimestampFieldParserHandler())
            )
        else:
            return super().handle(handler, *args, **kwargs)


class ICMPParseRouter:
    """
    A singleton class that routes ICMP message types to the appropriate handlers.

    The class follows the Singleton pattern to ensure that only one instance exists. It sets up the
    Chain of Responsibility for parsing different ICMP message types by linking together the appropriate
    handlers and passing the request to them.

    Methods:
    - route: Sets up the chain of handlers and routes the request to the appropriate ICMP handler.
    """
    __instance: ICMPParseRouter = None

    def __new__(cls):
        """
        Ensures that only one instance of ICMPParseRouter is created (Singleton pattern).
        """
        if cls.__instance is None:
            cls.__instance = super(ICMPParseRouter, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def route(handler, *args, **kwargs):
        """
        Sets up the chain of ICMP handlers and routes the request to the appropriate handler.

        Parameters:
        - handler: The handler that will process the ICMP fields.
        - *args, **kwargs: Additional arguments including 'icmp_type' for determining ICMP message type.
        """
        router = ICMPEchoAndRequestParseRouterHandler()
        (
            router
            .set_next(ICMPDestinationUnreachableParseRouterHandler())
            .set_next(ICMPTimeExceededParseRouterHandler())
            .set_next(ICMPRedirectMessageParseRouterHandler())
            .set_next(ICMPParameterProblemParseRouterHandler())
            .set_next(ICMPTimestampAndReplyParseRouterHandler())
        )
        router.handle(handler, *args, **kwargs)