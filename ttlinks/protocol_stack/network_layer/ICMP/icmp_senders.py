from __future__ import annotations
import asyncio
import time
from ttlinks.ipservice.ip_configs import IPv4SubnetConfig
from ttlinks.protocol_stack.base_classes.packet_sender import PacketSender
from ttlinks.protocol_stack.base_classes.protocol_socket import ICMPSocketBuilder, SocketBuilderDirector, Socket
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.network_layer.ICMP.icmp_builder import ICMPEchoRequestHeaderBuilder, ICMPEchoRequestHeader, ICMPHeaderBuilderDirector


# ----------------- ICMP Echo Request Senders -----------------

class ICMPEchoRequestSender(PacketSender):
    """
    Asynchronous ICMP Echo Request sender.

    This class is responsible for sending ICMP Echo Request packets (used in ping operations) to the specified
    destination IP address. It sends the ICMP packet over the provided socket and records the time the request was sent.
    """
    async def send(
            self,
            socket_unit: Socket,
            destination: str,
            protocol_unit: ProtocolUnit,
            *args, **kwargs
    ):
        # kwargs must include icmp_unit
        loop = asyncio.get_running_loop()
        sock = socket_unit.get_socket
        kwargs['time_record']['start_time'] = time.perf_counter()
        await loop.run_in_executor(None, sock.sendto, protocol_unit.as_bytes, (destination, 1))
