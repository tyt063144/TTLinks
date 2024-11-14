import asyncio
import socket

from ttlinks.protocol_stack.base_classes.packet_sender import PacketSender
from ttlinks.protocol_stack.base_classes.protocol_socket import Socket
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit


class TCPSender(PacketSender):
    async def send(self, socket_unit: Socket, destination: str, protocol_unit: ProtocolUnit, *args, **kwargs) -> None:
        loop = asyncio.get_running_loop()
        sock = socket_unit.get_socket
        if kwargs.get('initial'):
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        await loop.run_in_executor(None, sock.sendto, protocol_unit.as_bytes, (destination, 1))