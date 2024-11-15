import asyncio
import subprocess


class FirewallTools:

    @staticmethod
    async def apply_global_tcp_rst_filter():
        # Add a global rule to drop all outgoing TCP RST packets
        add_rule = ['iptables', '-A', 'OUTPUT', '-p', 'tcp', '--tcp-flags', 'RST', 'RST', '-j', 'DROP']
        await asyncio.create_subprocess_exec(*add_rule, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    async def remove_global_tcp_rst_filter():
        # Remove the global rule to stop dropping TCP RST packets
        remove_rule = ['iptables', '-D', 'OUTPUT', '-p', 'tcp', '--tcp-flags', 'RST', 'RST', '-j', 'DROP']
        await asyncio.create_subprocess_exec(*remove_rule, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
