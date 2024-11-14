import asyncio

from ttlinks.protocol_stack.base_classes.packet_receiver import PacketReceiver
from ttlinks.protocol_stack.base_classes.protocol_socket import Socket
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_parsers import IPv4PacketParser
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_units import IPv4Unit
from ttlinks.protocol_stack.transport_layer.TCP.tcp_parsers import TCPParser
from ttlinks.protocol_stack.transport_layer.TCP.tcp_units import TCPUnit


class TCPReceiver(PacketReceiver):
    async def listen(self, socket_unit: Socket, *args, **kwargs):
        loop = asyncio.get_running_loop()
        sock = socket_unit.get_socket
        initial_packet = kwargs['initial_packet']
        while True:
            fut = loop.sock_recv(sock, 65535)
            response = await fut
            ip_parser = IPv4PacketParser()
            ip_unit = IPv4Unit(**ip_parser.parse(response))
            tcp_parser = TCPParser()
            tcp_unit = TCPUnit(**tcp_parser.parse(ip_unit.payload))
            if (
                    initial_packet.tcp_unit.destination_port == tcp_unit.source_port
                    and str(initial_packet.ip_unit.destination_address) == str(ip_unit.source_address)
                    and str(initial_packet.ip_unit.source_address) == str(ip_unit.destination_address)
            ):
                kwargs['return_packets'].append((ip_unit, tcp_unit))
                await asyncio.sleep(0)
            else:
                await asyncio.sleep(0.1)
