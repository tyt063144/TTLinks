from abc import ABC

from ttlinks.protocol_stack.base_classes.protocol_socket import Socket


class PacketReceiver(ABC):
    """
    Abstract base class for receiving packets over a network socket.

    The `PacketReceiver` class defines an abstract method `listen` that should be
    implemented by subclasses to handle the reception of packets from a given
    network socket. This class could be part of an asynchronous networking system
    where data is received over a `Socket` object.

    Methods:
    - listen (abstract): To be implemented by subclasses for handling incoming packets.

    Parameters:
    None

    Methods:
    listen:
    - socket_unit (Socket): The network socket object used to receive data.
    - destination (str): The destination address or identifier to listen to.
    - *args: Additional positional arguments for custom implementation.
    - **kwargs: Additional keyword arguments for custom implementation.

    Returns:
    None
    """
    async def listen(self, socket_unit: Socket, *args, **kwargs):
        """
        Asynchronously listens for incoming packets on the given socket.

        This is an abstract method that must be implemented by a subclass.
        The method should define the logic for receiving packets from the specified
        `socket_unit` and `destination`.

        Parameters:
        socket_unit (Socket): The network socket object to listen on.
        destination (str): The destination address or identifier to listen to.
        *args: Additional positional arguments for further customization.
        **kwargs: Additional keyword arguments for further customization.

        Returns:
        None
        """
        pass