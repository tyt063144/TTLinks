from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CoRHandler(ABC):
    """Abstract base class for handlers in the Chain of Responsibility pattern."""

    @abstractmethod
    def set_next(self, h: CoRHandler) -> CoRHandler:
        """Set the next handler in the chain."""
        pass

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        """Handle the request. Concrete handlers must implement this method."""
        pass


class SimpleCoRHandler(CoRHandler, ABC):
    def __init__(self):
        self._next_handler = None  # Reference to the next handler in the chain

    def set_next(self, h: SimpleCoRHandler) -> SimpleCoRHandler:
        """
        Sets the next handler in the chain.

        Args:
            h (SimpleCoRHandler): The next handler to link.

        Returns:
            SimpleCoRHandler: The next handler (for chaining).

        Raises:
            TypeError: If the provided handler is not an instance of SimpleCoRHandler.
        """
        if not isinstance(h, SimpleCoRHandler):
            raise TypeError("The next handler must be an instance of SimpleCoRHandler.")
        self._next_handler = h
        return h

    def get_next(self) -> SimpleCoRHandler:
        """Returns the next handler in the chain."""
        return self._next_handler

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs):
        """
        Handle the request or pass it to the next handler in the chain.
        Subclasses must implement this method.
        """
        pass


class BidirectionalCoRHandler(CoRHandler, ABC):
    _next_handler = None  # Reference to the next handler in the chain
    _previous_handler = None  # Reference to the previous handler in the chain

    def set_next(self, h: BidirectionalCoRHandler) -> BidirectionalCoRHandler:
        """
        Sets the next handler in the chain and links the previous handler.

        Args:
            h (BidirectionalCoRHandler): The next handler to link.

        Returns:
            BidirectionalCoRHandler: The next handler (for chaining).

        Raises:
            TypeError: If the provided handler is not an instance of BidirectionalCoRHandler.
        """
        if not isinstance(h, BidirectionalCoRHandler):
            raise TypeError("The next handler must be an instance of BidirectionalCoRHandler.")
        self._next_handler = h
        h._previous_handler = self
        return h

    def get_next(self) -> BidirectionalCoRHandler:
        """Returns the next handler in the chain."""
        return self._next_handler

    def get_previous(self) -> BidirectionalCoRHandler:
        """Returns the previous handler in the chain."""
        return self._previous_handler

    @abstractmethod
    def handle(self, request, *args, **kwargs):
        """
        Handle the request or pass it to the next handler in the chain.
        Subclasses must implement this method.
        """
        pass

class TrackedCoRHandler(CoRHandler, ABC):
    def __init__(self):
        self._next_handler = None  # Reference to the next handler in the chain
        self._tracker = {}  # Dictionary to track the request and response

    def _set_tracker(self, tracker: dict):
        self._tracker = tracker

    def set_next(self, h: TrackedCoRHandler) -> TrackedCoRHandler:
        if not isinstance(h, TrackedCoRHandler):
            raise TypeError("The next handler must be an instance of TrackedCoRHandler.")
        self._next_handler = h
        self._next_handler._set_tracker(self._tracker)
        return h

    def get_next(self) -> TrackedCoRHandler:
        return self._next_handler

    def get_tracker(self) -> dict:
        return self._tracker

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        pass

class ListBasedCoRHandler(CoRHandler, ABC):
    def __init__(self):
        self._next_handler = None  # Reference to the next handler in the chain
        self._items = []  # List to track the request and response

    def _set_items(self, items: list):
        self._items = items

    def set_next(self, h: ListBasedCoRHandler) -> ListBasedCoRHandler:
        if not isinstance(h, ListBasedCoRHandler):
            raise TypeError("The next handler must be an instance of ListBasedCoRHandler.")
        self._next_handler = h
        self._next_handler._set_items(self._items)
        return h

    def get_next(self) -> ListBasedCoRHandler:
        return self._next_handler

    def get_items(self) -> list:
        return self._items

    @abstractmethod
    def handle(self, request: Any, *args, **kwargs) -> Any:
        pass

class ProtocolUnitSelectorCoRHandler(CoRHandler, ABC):
    def __init__(self, parser: Any = None):
        self._next_handler = None  # Reference to the next handler in the chain
        self._parser = parser  # Reference to the parser object
        self._parsed_data = None  # None if not parsed, dict if parsed

    def _set_parser(self, parser: Any):
        """Sets the parser object."""
        self._parser = parser

    def set_parsed_data(self, parsed_data: dict):
        """Sets the parsed flag."""
        self._parsed_data = parsed_data

    def set_next(self, h: ProtocolUnitSelectorCoRHandler) -> ProtocolUnitSelectorCoRHandler:
        if not isinstance(h, ProtocolUnitSelectorCoRHandler):
            raise TypeError("The next handler must be an instance of ProtocolParserCoRHandler.")
        self._next_handler = h
        self._next_handler._set_parser(self._parser)
        # self._next_handler._set_parsed_data(self._parsed_data)
        return h

    def get_next(self) -> ProtocolUnitSelectorCoRHandler:
        return self._next_handler

    def get_parser(self) -> Any:
        return self._parser

    @abstractmethod
    def handle(self, request: bytes, *args, **kwargs) -> Any:
        pass