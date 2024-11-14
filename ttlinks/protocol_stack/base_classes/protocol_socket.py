from abc import ABC, abstractmethod
import socket
from typing import Any


class Socket:
    """
    Abstract base class representing a network socket.

    This class encapsulates the behavior of a socket and allows adding parameters for socket
    creation. It supports setting the socket's blocking mode, creating a socket instance
    based on specified parameters, and closing the socket.

    Methods:
    - add_param: Adds a parameter to configure the socket.
    - get_socket: Lazily initializes and returns the socket instance.
    - close: Closes the socket and deallocates resources.

    Parameters:
    blocking (bool): Specifies whether the socket should be blocking or non-blocking. Defaults to False.

    Attributes:
    _params: Dictionary storing socket parameters (e.g., family, type, protocol).
    _blocking: Boolean indicating whether the socket operates in blocking mode.
    _sock: The underlying socket instance.

    Returns:
    None
    """
    def __init__(self, blocking: bool = False):
        self._params = {}
        self._blocking = blocking
        self._sock = None

    def add_param(self, name: str, value: Any):
        """
        Adds a parameter for the socket creation.

        Parameters:
        name (str): The name of the parameter (e.g., family, type, proto, fileno).
        value (Any): The value to assign to the parameter.

        Raises:
        ValueError: If an invalid socket parameter name is provided.

        Returns:
        None
        """
        if name not in ['family', 'type', 'proto', 'fileno']:
            raise ValueError(f'Invalid socket parameter')
        self._params[name] = value

    @property
    def get_socket(self) -> socket.socket:
        """
        Lazily initializes and returns the socket instance if not already created.

        If the socket is already initialized, it returns the existing socket object.

        Returns:
        socket.socket: The created socket object.
        """
        if self._sock is None:
            self._sock = socket.socket(**self._params)
            self._sock.setblocking(self._blocking)
            return self._sock
        return self._sock

    def close(self):
        """
        Closes the socket and deallocates resources.

        Raises:
        ValueError: If the socket has not been initialized yet.

        Returns:
        None
        """
        if self._sock is not None:
            self._sock.close()
            self._sock = None
        else:
            raise ValueError('Socket is not initialized yet')

class SocketBuilderInterface(ABC):
    """
    Abstract interface for building a `Socket` object.

    The **Builder** design pattern is applied here, allowing for step-by-step configuration
    of socket parameters such as family, type, protocol, and file descriptor.

    Methods:
    - build_socket_unit (abstract property): Returns the built `Socket` object.
    - set_family (abstract): Configures the socket's family.
    - set_type (abstract): Configures the socket's type.
    - set_proto (abstract): Configures the socket's protocol.
    - set_fileno (abstract): Configures the socket's file descriptor (optional).
    """
    @property
    @abstractmethod
    def build_socket_unit(self) -> Socket:
        """
        Abstract property to build and return the `Socket` object.
        """
        pass

    @abstractmethod
    def set_family(self, family: any):
        pass

    @abstractmethod
    def set_type(self, type: any):
        pass

    @abstractmethod
    def set_proto(self, proto: any):
        pass

    @abstractmethod
    def set_fileno(self, fileno: any = None):
        pass


# ------------------ICMP Socket Builder------------------
class ICMPSocketBuilder(SocketBuilderInterface):
    """
    Concrete builder class for creating an ICMP `Socket` using the **Builder** pattern.

    This class provides default settings for creating a raw ICMP socket, but allows for
    customization of its parameters. It is responsible for setting the family, type, protocol,
    and optional file descriptor.

    Methods:
    - reset: Resets the internal `Socket` object to allow building from scratch.
    - set_family: Configures the socket's family (default: `socket.AF_INET`).
    - set_type: Configures the socket's type (default: `socket.SOCK_RAW`).
    - set_proto: Configures the socket's protocol (default: `socket.IPPROTO_ICMP`).
    - set_fileno: Configures the socket's file descriptor (optional).
    - build_socket_unit: Builds and returns the configured `Socket` object.

    Parameters:
    blocking (bool): Specifies whether the socket should be blocking or non-blocking. Defaults to False.
    """
    def __init__(self, blocking: bool = False):
        self._socket = Socket(blocking)
        self._blocking = blocking

    def reset(self):
        """
        Resets the internal `Socket` object to its initial state, allowing for a new socket build.

        Parameters:
        None

        Returns:
        None
        """
        self._socket = Socket(self._blocking)

    @property
    def build_socket_unit(self) -> Socket:
        """
        Builds and returns the configured `Socket` object.

        Resets the builder to allow reusing the same builder instance for new socket creations.

        Returns:
        Socket: The fully configured socket instance.
        """
        socket_unit = self._socket
        self.reset()
        return socket_unit

    def set_family(self, family: any = socket.AF_INET):
        """
        Sets the socket's address family.

        Parameters:
        family (any): The address family (default: `socket.AF_INET`).

        Returns:
        None
        """
        self._socket.add_param('family', family)

    def set_type(self, type: any = socket.SOCK_RAW):
        """
        Sets the socket's type.

        Parameters:
        type (any): The socket type (default: `socket.SOCK_RAW`).

        Returns:
        None
        """
        self._socket.add_param('type', type)

    def set_proto(self, proto: any = socket.IPPROTO_ICMP):
        """
        Sets the socket's protocol.

        Parameters:
        proto (any): The protocol to use (default: `socket.IPPROTO_ICMP`).

        Returns:
        None
        """
        self._socket.add_param('proto', proto)

    def set_fileno(self, fileno: any = None):
        """
        Sets the socket's file descriptor (optional).

        Parameters:
        fileno (any): The file descriptor (default: None).

        Returns:
        None
        """
        self._socket.add_param('fileno', fileno)

# ------------------IP Socket Builder------------------
class TCPRawSocketBuilder(SocketBuilderInterface):

    def __init__(self, blocking: bool = False):
        self._socket = Socket(blocking)
        self._blocking = blocking

    def reset(self):
        self._socket = Socket(self._blocking)

    @property
    def build_socket_unit(self) -> Socket:
        socket_unit = self._socket
        self.reset()
        return socket_unit

    def set_family(self, family: any = socket.AF_INET):
        self._socket.add_param('family', family)

    def set_type(self, type: any = socket.SOCK_RAW):
        self._socket.add_param('type', type)

    def set_proto(self, proto: any = socket.IPPROTO_TCP):
        self._socket.add_param('proto', proto)

    def set_fileno(self, fileno: any = None):
        self._socket.add_param('fileno', fileno)


# ------------------Socket Builder Director------------------
class SocketBuilderDirector:
    """
    Director class for managing the construction process of a `Socket` object using a builder.

    The **Builder** pattern is used to abstract the step-by-step creation of complex socket objects.
    The director ensures the correct sequence of steps for building the desired socket.

    Methods:
    - build_socket: Directs the builder to create a socket with the appropriate settings.

    Parameters:
    builder (SocketBuilderInterface): The socket builder used to configure the socket.

    Returns:
    None
    """
    def __init__(self, builder):
        self.builder = builder

    def build_socket(self):
        self.builder.set_family()
        self.builder.set_type()
        self.builder.set_proto()
        self.builder.set_fileno()
        return self.builder.build_socket_unit