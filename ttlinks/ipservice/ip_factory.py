from __future__ import annotations

import concurrent.futures
import random
from abc import abstractmethod, ABC
from multiprocessing import cpu_count
from typing import List, Union, Tuple

from ttlinks.ipservice.ip_addr_type_classifiers import IPv4AddrClassifierPublicHandler
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPAddr, IPv6NetMask, IPv6Addr
from ttlinks.ipservice.ip_configs import InterfaceIPConfig, IPv4HostConfig, IPv4SubnetConfig, IPv4WildCardConfig, IPv6HostConfig, IPv6SubnetConfig, \
    IPv6WildCardConfig
from ttlinks.ipservice.ip_converters import DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler
from ttlinks.ipservice.ip_utils import IPv4AddrType, IPv4TypeAddrBlocks, IPv6TypeAddrBlocks


class IPFactory(ABC):
    def __init__(self):
        self._subnet_cache = {}

    @abstractmethod
    def host(self, host: str) -> InterfaceIPConfig:
        pass

    @abstractmethod
    def subnet(self, subnet: str) -> InterfaceIPConfig:
        pass

    @abstractmethod
    def wildcard(self, wildcard: str) -> InterfaceIPConfig:
        pass

    @abstractmethod
    def batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[InterfaceIPConfig]:
        pass

    @abstractmethod
    def batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[InterfaceIPConfig]:
        pass

    @abstractmethod
    def random_host(self, addr_type=None) -> InterfaceIPConfig:
        pass

    @abstractmethod
    def random_subnet(self, addr_type=None) -> InterfaceIPConfig:
        pass

    @abstractmethod
    def random_hosts_batch(self, addr_type=None, num_ips = 10) -> List[InterfaceIPConfig]:
        pass

    @abstractmethod
    def random_subnets_batch(self, addr_type=None, num_ips = 10) -> List[InterfaceIPConfig]:
        pass

    @abstractmethod
    def _random_subnet_for_type(self, addr_type) -> InterfaceIPConfig:
        pass



class IPv4Factory(IPFactory):
    def host(self, host: str) -> IPv4HostConfig:
        return IPv4HostConfig(host)

    def subnet(self, subnet: str) -> IPv4SubnetConfig:
        return IPv4SubnetConfig(subnet)

    def wildcard(self, wildcard: str) -> IPv4WildCardConfig:
        return IPv4WildCardConfig(wildcard)

    def batch_hosts(self, *hosts: str, max_workers: int = 10, keep_dup = True) -> List[IPv4HostConfig]:
        if keep_dup is False:
            hosts = list(set(hosts))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.host, hosts))
        return results

    def batch_subnets(self, *subnets: str, max_workers: int = 10, keep_dup = True) -> List[IPv4SubnetConfig]:
        if keep_dup is False:
            subnets = list(set(subnets))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.subnet, subnets))
        return results

    def random_host(self, addr_type:IPv4TypeAddrBlocks=None) -> IPv4HostConfig:
        subnet = self._random_subnet_for_type(addr_type)
        generated_host = IPv4HostConfigRandomizer(subnet).randomize()
        if addr_type == IPv4TypeAddrBlocks.PUBLIC and IPv4AddrClassifierPublicHandler().handle(generated_host.addr) != IPv4AddrType.PUBLIC:
            return self.random_host(addr_type)
        return generated_host

    def random_subnet(self, addr_type:IPv4TypeAddrBlocks=None) -> IPv4SubnetConfig:
        subnet = self._random_subnet_for_type(addr_type)
        generated_subnet = IPv4SubnetConfigRandomizer(subnet).randomize()
        if addr_type == IPv4TypeAddrBlocks.PUBLIC and IPv4AddrClassifierPublicHandler().handle(generated_subnet.addr) != IPv4AddrType.PUBLIC:
            return self.random_subnet(addr_type)
        return generated_subnet

    def random_hosts_batch(self, addr_type:IPv4TypeAddrBlocks=None, num_ips = 10) -> List[IPv4HostConfig]:
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_host, addr_type) for _ in range(num_ips)]
            random_ips = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_ips

    def random_subnets_batch(self, addr_type:IPv4TypeAddrBlocks=None, num_ips = 10) -> List[IPv4SubnetConfig]:
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_subnet, addr_type) for _ in range(num_ips)]
            random_subnets = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_subnets

    def _random_subnet_for_type(self, addr_type:IPv4TypeAddrBlocks) -> IPv4SubnetConfig:
        if addr_type in self._subnet_cache:
            subnets = self._subnet_cache[addr_type]
        else:
            if addr_type == IPv4TypeAddrBlocks.PUBLIC:
                subnets = self.batch_subnets('0.0.0.0/0')
            elif addr_type is None:
                subnets = self.batch_subnets('0.0.0.0/0')
            else:
                subnets = self.batch_subnets(*addr_type.value)
            self._subnet_cache[addr_type] = subnets
        return random.choice(subnets)

class IPv6Factory(IPFactory):
    def host(self, host: str) -> IPv6HostConfig:
        return IPv6HostConfig(host)

    def subnet(self, subnet: str) -> IPv6SubnetConfig:
        return IPv6SubnetConfig(subnet)

    def wildcard(self, wildcard: str) -> IPv6WildCardConfig:
        return IPv6WildCardConfig(wildcard)

    def batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6HostConfig]:
        if keep_dup is False:
            hosts = list(set(hosts))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.host, hosts))
        return results

    def batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6SubnetConfig]:
        if keep_dup is False:
            subnets = list(set(subnets))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.subnet, subnets))
        return results

    def random_host(self, addr_type: IPv6TypeAddrBlocks=None) -> IPv6HostConfig:
        subnet = self._random_subnet_for_type(addr_type)
        generated_host = IPv6HostConfigRandomizer(subnet).randomize()
        return generated_host

    def random_subnet(self, addr_type: IPv6TypeAddrBlocks=None) -> IPv6SubnetConfig:
        subnet = self._random_subnet_for_type(addr_type)
        generated_subnet = IPv6SubnetConfigRandomizer(subnet).randomize()
        return generated_subnet

    def random_hosts_batch(self, addr_type: IPv6TypeAddrBlocks=None, num_ips = 10) -> List[IPv6HostConfig]:
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_host, addr_type) for _ in range(num_ips)]
            random_ips = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_ips

    def random_subnets_batch(self, addr_type: IPv6TypeAddrBlocks=None, num_ips = 10) -> List[IPv6SubnetConfig]:
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_subnet, addr_type) for _ in range(num_ips)]
            random_subnets = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_subnets

    def _random_subnet_for_type(self, addr_type: IPv6TypeAddrBlocks) -> IPv6SubnetConfig:
        if addr_type in self._subnet_cache:
            subnets = self._subnet_cache[addr_type]
        elif addr_type is None:
            subnets = self.batch_subnets(['::/0'])
        else:
            subnets = self.batch_subnets(addr_type.value)
            self._subnet_cache[addr_type] = subnets
        return random.choice(subnets)

class IPConfigRandomizer(ABC):
    def __init__(self, subnet):
        self.subnet = subnet

    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        pass

    def _prepare(self,
                 longest_mask_size: int,
                 decimal_convert_handler: Union[DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler]
                 ) -> Tuple[IPAddr, IPAddr]:
        # Get original mask size from the subnet configuration
        original_mask_size = self.subnet.mask.mask_size

        # Choose a random mask size between the original and the longest mask size (e.g., /32 for IPv4)
        random_mask_size = random.randint(original_mask_size, longest_mask_size)

        # Create a mask with all 1s for the chosen random mask size
        ones_for_mask = (1 << random_mask_size) - 1

        # Shift the mask to align it correctly with the number of bits (longest_mask_size - random_mask_size)
        bitwise_random_mask = ones_for_mask << (longest_mask_size - random_mask_size)

        # Calculate the number of host bits by subtracting the original mask size from the total mask size
        host_bits = longest_mask_size - original_mask_size

        # Generate random host bits within the given subnet
        random_host = random.getrandbits(host_bits)

        # Combine the original subnet IP with the randomly generated host bits using a bitwise OR operation
        bitwise_random_host = self.subnet.addr.as_decimal | random_host

        # Convert the decimal IP and mask to binary using the given handler
        random_host = decimal_convert_handler.handle(bitwise_random_host)
        random_mask = decimal_convert_handler.handle(bitwise_random_mask)

        return random_host, random_mask

class IPv4ConfigRandomizer(IPConfigRandomizer):
    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        pass

class IPv4HostConfigRandomizer(IPv4ConfigRandomizer):
    def randomize(self) -> IPv4HostConfig:
        random_host, random_mask = self._prepare(32, DecimalIPv4ConverterHandler())
        ipv4_host = IPv4HostConfig(IPv4Addr(random_host), IPv4NetMask(random_mask))
        return ipv4_host

class IPv4SubnetConfigRandomizer(IPv4ConfigRandomizer):
    def randomize(self) -> IPv4SubnetConfig:
        random_host, random_mask = self._prepare(32, DecimalIPv4ConverterHandler())
        ipv4_subnet = IPv4SubnetConfig(IPv4Addr(random_host), IPv4NetMask(random_mask))
        return ipv4_subnet

class IPv6ConfigRandomizer(IPConfigRandomizer):
    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        pass

class IPv6HostConfigRandomizer(IPv6ConfigRandomizer):
    def randomize(self) -> IPv6HostConfig:
        random_host, random_mask = self._prepare(128, DecimalIPv6ConverterHandler())
        ipv6_host = IPv6HostConfig(IPv6Addr(random_host), IPv6NetMask(random_mask))
        return ipv6_host

class IPv6SubnetConfigRandomizer(IPv6ConfigRandomizer):
    def randomize(self) -> IPv6SubnetConfig:
        random_host, random_mask = self._prepare(128, DecimalIPv6ConverterHandler())
        ipv6_subnet = IPv6SubnetConfig(IPv6Addr(random_host), IPv6NetMask(random_mask))
        return ipv6_subnet
