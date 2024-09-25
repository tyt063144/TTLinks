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
    def handle(self, request: Any):
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
    def handle(self, request: Any):
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
    def handle(self, request):
        """
        Handle the request or pass it to the next handler in the chain.
        Subclasses must implement this method.
        """
        pass
