import asyncio
from abc import ABC, abstractmethod
from typing import List

from ttlinks.common.tools.systems import FirewallTools
from ttlinks.ipservice.ip_address import IPAddr, IPv4Addr
from ttlinks.protocol_stack.ip_packets.tcp import IPv4TCP
from ttlinks.protocol_stack.network_layer.IPv4.flags_utils import IPv4Flags
from ttlinks.protocol_stack.traffic_flows.TCP.tcp_flow import IPv4TCPFlowController
from ttlinks.protocol_stack.transport_layer.TCP.tcp_utils import TCPFlags


class TCPScanner(ABC):
    _ports: List[int] = None
    _destination_addresses: List[IPAddr] = None
    _report: dict = None

    def _validate(self):
        if len(self._ports) != 2:
            raise ValueError("Ports must be a list of two integers")
        if self._ports[0] > self._ports[1]:
            raise ValueError("The first port must be less than the second port")
        if max(self._ports) > 65535:
            raise ValueError("Port number must be less than 65536")
        if min(self._ports) < 1:
            raise ValueError("Port number must be greater than 0")

    def _initialize_report(self):
        for address in self._destination_addresses:
            self._report[str(address)] = {}

    @property
    def report(self):
        return self._report

    @abstractmethod
    def _build_initial_packet(self, destination_address: str, port: int):
        pass

    @abstractmethod
    async def scan_a_port(self, destination_address: str, port: int) -> bool:
        pass

    @abstractmethod
    async def complete_scan(self):
        pass


class IPv4TCPScanner(TCPScanner):
    def __init__(self, destination_addresses: List[IPAddr], ports=None, timeout=5, semaphore=255):
        self._semaphore = asyncio.Semaphore(semaphore)  # Store the semaphore limit as an integer
        if ports is None:
            ports = [1, 1024]
        self._destination_addresses = destination_addresses
        self._ports = ports
        self._timeout = timeout
        self._report = {}
        self._source_ports = []
        self._validate()
        self._initialize_report()

    def _build_initial_packet(self, destination_address: str, port: int):
        init_tcp_packet = IPv4TCP(
            ipv4_flags=IPv4Flags.DONT_FRAGMENT,
            destination_address=destination_address,
            destination_port=port,
            tcp_flags=[TCPFlags.SYN],
        )
        self._source_ports.append(init_tcp_packet.tcp_unit.source_port)
        return init_tcp_packet

    async def _scan_and_record(self, destination_address: str, port: int):
        """
        Helper coroutine that scans a port and records the result in the report.
        """
        result = await self.scan_a_port(destination_address, port)
        if result is True:
            self._report[destination_address][port] = result  # Record the result in the report

    async def scan_a_port(self, destination_address: str, port: int) -> bool:
        async with self._semaphore:
            tcp_flow = IPv4TCPFlowController(self._build_initial_packet(destination_address, port), timeout=self._timeout)
            await tcp_flow.handshake()
            await tcp_flow.close(close_socket=False)
            return tcp_flow.is_handshake_completed

    async def complete_scan(self):
        await FirewallTools.apply_global_tcp_rst_filter()
        try:
            tasks = []
            for address in self._destination_addresses:
                for port in range(self._ports[0], self._ports[1] + 1):
                    tasks.append(self._scan_and_record(str(address), port))
            await asyncio.gather(*tasks)
        finally:
            # Remove the global firewall rule after the scan is complete
            await FirewallTools.remove_global_tcp_rst_filter()

if __name__ == '__main__':
    ipv4_destinations = [
        IPv4Addr('192.168.1.20'),
        IPv4Addr('192.168.1.30')
    ]
    scanner = IPv4TCPScanner(
        ipv4_destinations,
        ports=[1, 1024],
        timeout=10,
    )
    asyncio.run(scanner.complete_scan())
    print('Scan Report:', scanner.report)