from abc import ABC

from ttlinks.protocol_stack.base_classes.protocol_socket import Socket
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit


class PacketSender(ABC):
    """
    Abstract base class for sending packets over a network socket.

    The `PacketSender` class defines an abstract method `send` that should be
    implemented by subclasses to handle sending packets to a specified
    destination using a provided `Socket`. This class is part of an asynchronous
    system, likely used in conjunction with a protocol stack, where data is sent
    over a network socket.

    Methods:
    - send (abstract): To be implemented by subclasses for handling packet transmission.

    Parameters:
    None

    Methods:
    send:
    - socket_unit (Socket): The network socket object through which the data will be sent.
    - destination (str): The destination address or identifier where the packet will be sent.
    - protocol_unit (ProtocolUnit): The protocol unit that encapsulates the data to be sent.
    - *args: Additional positional arguments for custom implementation.
    - **kwargs: Additional keyword arguments for custom implementation.

    Returns:
    None
    """
    async def send(self, socket_unit: Socket, destination: str, protocol_unit: ProtocolUnit, *args, **kwargs):
        """
        Asynchronously sends a packet to the specified destination using the given socket.

        This is an abstract method that must be implemented by a subclass.
        The method should define the logic for sending packets over the `socket_unit`
        to the specified `destination` while encapsulating the data in the `protocol_unit`.

        Parameters:
        socket_unit (Socket): The network socket object through which the data will be sent.
        destination (str): The destination address or identifier where the packet will be sent.
        protocol_unit (ProtocolUnit): The protocol unit encapsulating the data to be sent.
        *args: Additional positional arguments for further customization.
        **kwargs: Additional keyword arguments for further customization.

        Returns:
        None
        """
        pass