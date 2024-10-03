from __future__ import annotations

import concurrent.futures
import random
from abc import abstractmethod, ABC
from enum import Enum
from multiprocessing import cpu_count
from typing import List, Union, Tuple

from ttlinks.ipservice.ip_addr_type_classifiers import IPv4AddrClassifierPublicHandler
from ttlinks.ipservice.ip_address import IPv4Addr, IPv4NetMask, IPAddr, IPv6NetMask, IPv6Addr
from ttlinks.ipservice.ip_configs import InterfaceIPConfig, IPv4HostConfig, IPv4SubnetConfig, IPv4WildCardConfig, IPv6HostConfig, IPv6SubnetConfig, \
    IPv6WildCardConfig
from ttlinks.ipservice.ip_converters import DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler
from ttlinks.ipservice.ip_utils import IPv4AddrType


class IPv4TypeAddrBlocks(Enum):
    UNSPECIFIED = ['0.0.0.0/32']
    CURRENT_NETWORK = ['0.0.0.0/8']
    PUBLIC = [
            '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
            '172.16.0.0/12', '192.0.0.0/24', '192.0.2.0/24', '192.88.99.0/24', '192.168.0.0/16',
            '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24', '224.0.0.0/4', '233.252.0.0/24',
            '240.0.0.0/4', '255.255.255.255/32'
        ]  # Public IPs generated have to avoid the blocks in the list.
    PRIVATE = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    MULTICAST = ["224.0.0.0/4"]  # For 224.0.0.0/4 and others
    LINK_LOCAL = ["169.254.0.0/16"]  # For 169.254.0.0/16
    LOOPBACK = ["127.0.0.0/8"]  # For 127.0.0.0/8
    DOCUMENTATION = ['192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '233.252.0.0/24']  # For 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, and 233.252.0.0/24
    CARRIER_GRADE_NAT = ['100.64.0.0/10']  # For 100.64.0.0/10
    BENCHMARK_TESTING = ['198.18.0.0/15']  # For 198.18.0.0/15
    IPV6_TO_IPV4_RELAY = ['192.88.99.0/24']  # For 192.88.99.0/24 (formerly used)
    RESERVED = ['240.0.0.0/4']  # For 240.0.0.0/4 and 255.255.255.255/32
    LIMITED_BROADCAST = ['255.255.255.255/32']  # For 255.255.255.255/32, "limited broadcast" destination address
    DS_LITE = ['192.0.0.0/24']  # For 192.0.0.0/24

class IPv6TypeAddrBlocks(Enum):
    UNSPECIFIED = ['::/128']  # ::/128
    SRV6 = ['5f00::/16']  # 5f00::/16, IPv6 Segment Routing
    GLOBAL_UNICAST = ['2000::/3']
    UNIQUE_LOCAL = ['fc00::/7']  # fc00::/7
    MULTICAST = ['ff00::/8']  # ff00::/8
    LINK_LOCAL = ['fe80::/64']  # fe80::/64 from fe80::/10
    LOOPBACK = ['::1/128']  # ::1/128
    DOCUMENTATION = ['2001:db8::/32', '3fff::/20']  # 2001:db8::/32 and 3fff::/20
    IPV4_MAPPED = ['::ffff:0:0/96']  # ::ffff:0:0/96
    IPV4_TRANSLATED = ['::ffff:0:0:0/96']  # ::ffff:0:0:0/96
    IPV4_IPV6_TRANSLATION = ['64:ff9b::/96', '64:ff9b:1::/48']  # 64:ff9b::/96 and 64:ff9b:1::/48
    DISCARD_PREFIX = ['100::/64']  # 100::/64
    IP6_TO4 = ['2002::/16'] # 2002::/16, 6to4 addressing scheme
    TEREDO_TUNNELING = ['2001::/32']  # 2001::/32
    ORCHIDV2 = ['2001:20::/28']  # 2001:20::/28


class IPFactory(ABC):
    """
    Abstract Base Class (ABC) for generating various IP configurations, including host IPs, subnets, and wildcard configurations.
    This class serves as the blueprint for concrete implementations that can generate random or batch configurations for different address types.

    Attributes:
    _subnet_cache (dict): A cache to store pre-generated subnet configurations, reducing the need for redundant calculations.
    """
    def __init__(self):
        """
        Initializes the IPFactory object by setting up a cache to store subnet configurations.
        This cache helps improve performance by reusing subnet data rather than recalculating it.
        """
        self._subnet_cache = {}

    @abstractmethod
    def host(self, host: str) -> InterfaceIPConfig:
        """
        Abstract method to generate a host IP configuration.

        Parameters:
        host (str): The string representation of the host IP.

        Returns:
        InterfaceIPConfig: The configuration object representing the host IP.
        """
        pass

    @abstractmethod
    def subnet(self, subnet: str) -> InterfaceIPConfig:
        """
        Abstract method to generate a subnet configuration.

        Parameters:
        subnet (str): The string representation of the subnet.

        Returns:
        InterfaceIPConfig: The configuration object representing the subnet.
        """
        pass

    @abstractmethod
    def wildcard(self, wildcard: str) -> InterfaceIPConfig:
        """
        Abstract method to generate a wildcard configuration.

        Parameters:
        wildcard (str): The string representation of the wildcard IP.

        Returns:
        InterfaceIPConfig: The configuration object representing the wildcard IP.
        """
        pass

    @abstractmethod
    def batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[InterfaceIPConfig]:
        """
        Abstract method to generate a batch of host configurations.

        Parameters:
        hosts (List[str]): A list of host IP strings.
        max_workers (int): The maximum number of workers to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate host IPs in the batch.

        Returns:
        List[InterfaceIPConfig]: A list of configuration objects representing the host IPs.
        """
        pass

    @abstractmethod
    def batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[InterfaceIPConfig]:
        """
        Abstract method to generate a batch of subnet configurations.

        Parameters:
        subnets (List[str]): A list of subnet IP strings.
        max_workers (int): The maximum number of workers to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate subnet IPs in the batch.

        Returns:
        List[InterfaceIPConfig]: A list of configuration objects representing the subnets.
        """
        pass

    @abstractmethod
    def random_host(self, addr_type=None) -> InterfaceIPConfig:
        """
        Abstract method to generate a random host IP configuration.

        Parameters:
        addr_type (Any): The type of address block for which to generate the random host IP.

        Returns:
        InterfaceIPConfig: The configuration object representing the random host IP.
        """
        pass

    @abstractmethod
    def random_subnet(self, addr_type=None) -> InterfaceIPConfig:
        """
        Abstract method to generate a random subnet configuration.

        Parameters:
        addr_type (Any): The type of address block for which to generate the random subnet.

        Returns:
        InterfaceIPConfig: The configuration object representing the random subnet.
        """
        pass

    @abstractmethod
    def random_hosts_batch(self, addr_type=None, num_ips = 10) -> List[InterfaceIPConfig]:
        """
        Abstract method to generate a batch of random host IP configurations.

        Parameters:
        addr_type (Any): The type of address block for which to generate the random host IPs.
        num_ips (int): The number of random IPs to generate in the batch.

        Returns:
        List[InterfaceIPConfig]: A list of configuration objects representing the random host IPs.
        """
        pass

    @abstractmethod
    def random_subnets_batch(self, addr_type=None, num_ips = 10) -> List[InterfaceIPConfig]:
        """
        Abstract method to generate a batch of random subnet configurations.

        Parameters:
        addr_type (Any): The type of address block for which to generate the random subnets.
        num_ips (int): The number of random subnets to generate in the batch.

        Returns:
        List[InterfaceIPConfig]: A list of configuration objects representing the random subnets.
        """
        pass

    @abstractmethod
    def _random_subnet_for_type(self, addr_type) -> InterfaceIPConfig:
        """
        Abstract method to generate a random subnet configuration for a specific address type.

        Parameters:
        addr_type (Any): The type of address block for which to generate the random subnet.

        Returns:
        InterfaceIPConfig: The configuration object representing the random subnet for the given address type.
        """
        pass



class IPv4Factory(IPFactory):
    """
    Concrete implementation of IPFactory for handling IPv4 addresses.
    This class provides methods to generate and manage IPv4 host, subnet, and wildcard configurations, as well as random IP generation.
    """
    def host(self, host: str) -> IPv4HostConfig:
        """
        Generates an IPv4 host configuration.

        Parameters:
        host (str): The string representation of the host IP.

        Returns:
        IPv4HostConfig: The configuration object representing the host IP.
        """
        return IPv4HostConfig(host)

    def subnet(self, subnet: str) -> IPv4SubnetConfig:
        """
        Generates an IPv4 subnet configuration.

        Parameters:
        subnet (str): The string representation of the subnet.

        Returns:
        IPv4SubnetConfig: The configuration object representing the subnet.
        """
        return IPv4SubnetConfig(subnet)

    def wildcard(self, wildcard: str) -> IPv4WildCardConfig:
        """
        Generates an IPv4 wildcard configuration.

        Parameters:
        wildcard (str): The string representation of the wildcard IP.

        Returns:
        IPv4WildCardConfig: The configuration object representing the wildcard IP.
        """
        return IPv4WildCardConfig(wildcard)

    def batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv4HostConfig]:
        """
        Generates a batch of IPv4 host configurations using multi-threading.

        Parameters:
        hosts (List[str]): A list of host IP strings.
        max_workers (int): The maximum number of threads to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate host IPs in the batch.

        Returns:
        List[IPv4HostConfig]: A list of configuration objects representing the host IPs.
        """
        if keep_dup is False:
            hosts = list(set(hosts))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.host, hosts))
        return results

    def batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv4SubnetConfig]:
        """
        Generates a batch of IPv4 subnet configurations using multi-threading.

        Parameters:
        subnets (List[str]): A list of subnet IP strings.
        max_workers (int): The maximum number of threads to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate subnet IPs in the batch.

        Returns:
        List[IPv4SubnetConfig]: A list of configuration objects representing the subnets.
        """
        if keep_dup is False:
            subnets = list(set(subnets))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.subnet, subnets))
        return results

    def random_host(self, addr_type:IPv4TypeAddrBlocks=None) -> IPv4HostConfig:
        """
        Generates a random IPv4 host configuration based on the specified address type.

        Parameters:
        addr_type (IPv4TypeAddrBlocks): The address block type to use for generating the random host.

        Returns:
        IPv4HostConfig: A randomly generated host configuration.
        """
        subnet = self._random_subnet_for_type(addr_type)
        generated_host = IPv4HostConfigRandomizer(subnet).randomize()
        if addr_type == IPv4TypeAddrBlocks.PUBLIC and IPv4AddrClassifierPublicHandler().handle(generated_host.ip_addr) != IPv4AddrType.PUBLIC:
            return self.random_host(addr_type)
        return generated_host

    def random_subnet(self, addr_type:IPv4TypeAddrBlocks=None) -> IPv4SubnetConfig:
        """
        Generates a random IPv4 subnet configuration based on the specified address type.

        Parameters:
        addr_type (IPv4TypeAddrBlocks): The address block type to use for generating the random subnet.

        Returns:
        IPv4SubnetConfig: A randomly generated subnet configuration.
        """
        subnet = self._random_subnet_for_type(addr_type)
        generated_subnet = IPv4SubnetConfigRandomizer(subnet).randomize()
        if addr_type == IPv4TypeAddrBlocks.PUBLIC and IPv4AddrClassifierPublicHandler().handle(generated_subnet.ip_addr) != IPv4AddrType.PUBLIC:
            return self.random_subnet(addr_type)
        return generated_subnet

    def random_hosts_batch(self, addr_type:IPv4TypeAddrBlocks=None, num_ips = 10) -> List[IPv4HostConfig]:
        """
        Generates a batch of random IPv4 host configurations using multiprocessing.

        Parameters:
        addr_type (IPv4TypeAddrBlocks): The address block type to use for generating the random hosts.
        num_ips (int): The number of random IPs to generate in the batch.

        Returns:
        List[IPv4HostConfig]: A list of randomly generated host configurations.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_host, addr_type) for _ in range(num_ips)]
            random_ips = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_ips

    def random_subnets_batch(self, addr_type:IPv4TypeAddrBlocks=None, num_ips = 10) -> List[IPv4SubnetConfig]:
        """
        Generates a batch of random IPv4 subnet configurations using multiprocessing.

        Parameters:
        addr_type (IPv4TypeAddrBlocks): The address block type to use for generating the random subnets.
        num_ips (int): The number of random subnets to generate in the batch.

        Returns:
        List[IPv4SubnetConfig]: A list of randomly generated subnet configurations.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_subnet, addr_type) for _ in range(num_ips)]
            random_subnets = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_subnets

    def _random_subnet_for_type(self, addr_type:IPv4TypeAddrBlocks) -> IPv4SubnetConfig:
        """
        Retrieves or generates a random subnet configuration for the given address type, utilizing caching for performance.

        Parameters:
        addr_type (IPv4TypeAddrBlocks): The address block type to use for generating the subnet.

        Returns:
        IPv4SubnetConfig: A random subnet configuration.
        """
        if addr_type in self._subnet_cache:
            subnets = self._subnet_cache[addr_type]
        else:
            if addr_type == IPv4TypeAddrBlocks.PUBLIC:
                subnets = self.batch_subnets(['0.0.0.0/0'])
            elif addr_type is None:
                subnets = self.batch_subnets(['0.0.0.0/0'])
            else:
                subnets = self.batch_subnets(addr_type.value)
            self._subnet_cache[addr_type] = subnets
        return random.choice(subnets)

class IPv6Factory(IPFactory):
    """
    Concrete implementation of IPFactory for handling IPv6 addresses.
    This class provides methods to generate and manage IPv6 host, subnet, and wildcard configurations, as well as random IP generation.
    """
    def host(self, host: str) -> IPv6HostConfig:
        """
        Generates an IPv6 host configuration.

        Parameters:
        host (str): The string representation of the host IPv6 address.

        Returns:
        IPv6HostConfig: The configuration object representing the host IPv6 address.
        """
        return IPv6HostConfig(host)

    def subnet(self, subnet: str) -> IPv6SubnetConfig:
        """
        Generates an IPv6 subnet configuration.

        Parameters:
        subnet (str): The string representation of the IPv6 subnet.

        Returns:
        IPv6SubnetConfig: The configuration object representing the IPv6 subnet.
        """
        return IPv6SubnetConfig(subnet)

    def wildcard(self, wildcard: str) -> IPv6WildCardConfig:
        """
        Generates an IPv6 wildcard configuration.

        Parameters:
        wildcard (str): The string representation of the wildcard IPv6 address.

        Returns:
        IPv6WildCardConfig: The configuration object representing the wildcard IPv6 address.
        """
        return IPv6WildCardConfig(wildcard)

    def batch_hosts(self, hosts: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6HostConfig]:
        """
        Generates a batch of IPv6 host configurations using multi-threading.

        Parameters:
        hosts (List[str]): A list of IPv6 host strings.
        max_workers (int): The maximum number of threads to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate IPv6 host addresses in the batch.

        Returns:
        List[IPv6HostConfig]: A list of configuration objects representing the host IPv6 addresses.
        """
        if keep_dup is False:
            hosts = list(set(hosts))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.host, hosts))
        return results

    def batch_subnets(self, subnets: List[str], max_workers: int = 10, keep_dup = True) -> List[IPv6SubnetConfig]:
        """
        Generates a batch of IPv6 subnet configurations using multi-threading.

        Parameters:
        subnets (List[str]): A list of IPv6 subnet strings.
        max_workers (int): The maximum number of threads to use for parallel processing.
        keep_dup (bool): Whether to keep duplicate IPv6 subnet addresses in the batch.

        Returns:
        List[IPv6SubnetConfig]: A list of configuration objects representing the IPv6 subnets.
        """
        if keep_dup is False:
            subnets = list(set(subnets))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.subnet, subnets))
        return results

    def random_host(self, addr_type=None) -> IPv6HostConfig:
        """
        Generates a random IPv6 host configuration based on the specified address type.

        Parameters:
        addr_type (Any): The address block type to use for generating the random IPv6 host.

        Returns:
        IPv6HostConfig: A randomly generated IPv6 host configuration.
        """
        subnet = self._random_subnet_for_type(addr_type)
        generated_host = IPv6HostConfigRandomizer(subnet).randomize()
        return generated_host

    def random_subnet(self, addr_type=None) -> IPv6SubnetConfig:
        """
        Generates a random IPv6 subnet configuration based on the specified address type.

        Parameters:
        addr_type (Any): The address block type to use for generating the random IPv6 subnet.

        Returns:
        IPv6SubnetConfig: A randomly generated IPv6 subnet configuration.
        """
        subnet = self._random_subnet_for_type(addr_type)
        generated_subnet = IPv6SubnetConfigRandomizer(subnet).randomize()
        return generated_subnet

    def random_hosts_batch(self, addr_type=None, num_ips = 10) -> List[IPv6HostConfig]:
        """
        Generates a batch of random IPv6 host configurations using multiprocessing.

        Parameters:
        addr_type (Any): The address block type to use for generating the random IPv6 hosts.
        num_ips (int): The number of random IPv6 hosts to generate in the batch.

        Returns:
        List[IPv6HostConfig]: A list of randomly generated IPv6 host configurations.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_host, addr_type) for _ in range(num_ips)]
            random_ips = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_ips

    def random_subnets_batch(self, addr_type=None, num_ips = 10) -> List[IPv6SubnetConfig]:
        """
        Generates a batch of random IPv6 subnet configurations using multiprocessing.

        Parameters:
        addr_type (Any): The address block type to use for generating the random IPv6 subnets.
        num_ips (int): The number of random IPv6 subnets to generate in the batch.

        Returns:
        List[IPv6SubnetConfig]: A list of randomly generated IPv6 subnet configurations.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(self.random_subnet, addr_type) for _ in range(num_ips)]
            random_subnets = [future.result() for future in concurrent.futures.as_completed(futures)]
        return random_subnets

    def _random_subnet_for_type(self, addr_type) -> IPv6SubnetConfig:
        """
        Retrieves or generates a random IPv6 subnet configuration for the given address type, utilizing caching for performance.

        Parameters:
        addr_type (Any): The address block type to use for generating the IPv6 subnet.

        Returns:
        IPv6SubnetConfig: A random IPv6 subnet configuration.
        """
        if addr_type in self._subnet_cache:
            subnets = self._subnet_cache[addr_type]
        elif addr_type is None:
            subnets = self.batch_subnets(['::/0'])
        else:
            subnets = self.batch_subnets(addr_type.value)
            self._subnet_cache[addr_type] = subnets
        return random.choice(subnets)

class IPConfigRandomizer(ABC):
    """
    Abstract base class for randomizing IP configurations.
    This class provides the structure for generating random IP addresses and netmask configurations based on a given subnet.

    Attributes:
    subnet (IPSubnetConfig): The subnet configuration used as the basis for randomizing IP configurations.
    """
    def __init__(self, subnet):
        """
        Initializes the IPConfigRandomizer with the given subnet.

        Parameters:
        subnet (IPSubnetConfig): The subnet configuration that provides the IP address and netmask for randomization.
        """
        self.subnet = subnet

    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        """
        Abstract method to generate a random IP configuration.

        This method must be implemented by subclasses to produce a specific type of random IP configuration (e.g., host, subnet).

        Returns:
        InterfaceIPConfig: A randomly generated IP configuration based on the implementation.
        """
        pass

    def _prepare(self,
                 longest_mask_size: int,
                 decimal_convert_handler: Union[DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler]
                 ) -> Tuple[IPAddr, IPAddr]:
        """
        Prepares and generates a random IP address and netmask based on the given subnet configuration.

        This helper method handles the bitwise operations needed to create a randomized IP address within the given subnet
        and a random netmask, and it returns both the IP address and the mask in the correct format.

        Parameters:
        longest_mask_size (int): The maximum possible mask size (e.g., 32 for IPv4 or 128 for IPv6).
        decimal_convert_handler (Union[DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler]):
            The handler used to convert the decimal IP and mask values into their respective binary representations.

        Returns:
        Tuple[IPAddr, IPAddr]: A tuple containing the randomly generated IP address and the corresponding netmask.
        """
        # Get original mask size from the subnet configuration
        original_mask_size = self.subnet.mask.get_mask_size()

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
        bitwise_random_host = self.subnet.ip_addr.decimal | random_host

        # Convert the decimal IP and mask to binary using the given handler
        random_host = decimal_convert_handler.handle(bitwise_random_host)
        random_mask = decimal_convert_handler.handle(bitwise_random_mask)

        return random_host, random_mask

class IPv4ConfigRandomizer(IPConfigRandomizer):
    """
    Concrete implementation of IPConfigRandomizer for generating random IPv4 configurations.

    This class provides the implementation for the randomize method to generate random IPv4 addresses and netmasks.
    """
    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        """
        Generates a random IPv4 configuration based on the given subnet.

        This method must be implemented by subclasses to produce a specific random IPv4 configuration, such as a host or subnet.

        Returns:
        InterfaceIPConfig: A randomly generated IPv4 configuration.
        """
        pass

class IPv4HostConfigRandomizer(IPv4ConfigRandomizer):
    """
    A concrete implementation of IPv4ConfigRandomizer that generates random IPv4 host configurations.

    This class randomizes an IPv4 host address and its corresponding netmask based on a given subnet configuration.
    It utilizes the `DecimalIPv4ConverterHandler` to convert the randomized IP and netmask into the proper binary format.
    """
    def randomize(self) -> IPv4HostConfig:
        """
        Randomizes and generates an IPv4 host configuration.

        This method uses the `_prepare` method to generate a random host IP address and netmask within a given subnet.
        The randomization is based on the longest mask size (32 for IPv4) and converts the IP and netmask using `DecimalIPv4ConverterHandler`.

        Returns:
        IPv4HostConfig: A randomly generated host configuration containing the IP address and the netmask.
        """
        random_host, random_mask = self._prepare(32, DecimalIPv4ConverterHandler())
        ipv4_host = IPv4HostConfig(IPv4Addr(random_host), IPv4NetMask(random_mask))
        return ipv4_host

class IPv4SubnetConfigRandomizer(IPv4ConfigRandomizer):
    """
    A concrete implementation of IPv4ConfigRandomizer that generates random IPv4 subnet configurations.

    This class randomizes an IPv4 subnet address and its corresponding netmask based on a given subnet configuration.
    It utilizes the `DecimalIPv4ConverterHandler` to convert the randomized IP and netmask into the proper binary format.
    """
    def randomize(self) -> IPv4SubnetConfig:
        """
        Randomizes and generates an IPv4 subnet configuration.

        This method uses the `_prepare` method to generate a random subnet IP address and netmask within a given subnet.
        The randomization is based on the longest mask size (32 for IPv4) and converts the IP and netmask using `DecimalIPv4ConverterHandler`.

        Returns:
        IPv4SubnetConfig: A randomly generated subnet configuration containing the IP address and the netmask.
        """
        random_host, random_mask = self._prepare(32, DecimalIPv4ConverterHandler())
        ipv4_subnet = IPv4SubnetConfig(IPv4Addr(random_host), IPv4NetMask(random_mask))
        return ipv4_subnet

class IPv6ConfigRandomizer(IPConfigRandomizer):
    """
    Abstract class for generating random IPv6 configurations.

    This class provides the structure for generating random IPv6 addresses and netmask configurations based on a given subnet.
    Subclasses must implement the `randomize` method to generate specific IPv6 configurations (e.g., host, subnet).
    """
    @abstractmethod
    def randomize(self) -> InterfaceIPConfig:
        """
        Abstract method to generate a random IPv6 configuration.

        This method must be implemented by subclasses to produce a specific random IPv6 configuration (such as a host or subnet).

        Returns:
        InterfaceIPConfig: A randomly generated IPv6 configuration.
        """
        pass

class IPv6HostConfigRandomizer(IPv6ConfigRandomizer):
    """
    A concrete implementation of IPv6ConfigRandomizer that generates random IPv6 host configurations.

    This class randomizes an IPv6 host address and its corresponding netmask based on a given subnet configuration.
    It uses the `DecimalIPv6ConverterHandler` to convert the randomized IP and netmask into their binary format.
    """
    def randomize(self) -> IPv6HostConfig:
        """
        Randomizes and generates an IPv6 host configuration.

        This method uses the `_prepare` method to generate a random host IP address and netmask within a given IPv6 subnet.
        The randomization is based on the longest mask size (128 for IPv6) and converts the IP and netmask using `DecimalIPv6ConverterHandler`.

        Returns:
        IPv6HostConfig: A randomly generated IPv6 host configuration containing the IP address and the netmask.
        """
        random_host, random_mask = self._prepare(128, DecimalIPv6ConverterHandler())
        ipv6_host = IPv6HostConfig(IPv6Addr(random_host), IPv6NetMask(random_mask))
        return ipv6_host

class IPv6SubnetConfigRandomizer(IPv6ConfigRandomizer):
    """
    A concrete implementation of IPv6ConfigRandomizer that generates random IPv6 subnet configurations.

    This class randomizes an IPv6 subnet address and its corresponding netmask based on a given subnet configuration.
    It uses the `DecimalIPv6ConverterHandler` to convert the randomized IP and netmask into their binary format.
    """
    def randomize(self) -> IPv6SubnetConfig:
        """
        Randomizes and generates an IPv6 subnet configuration.

        This method uses the `_prepare` method to generate a random subnet IP address and netmask within a given IPv6 subnet.
        The randomization is based on the longest mask size (128 for IPv6) and converts the IP and netmask using `DecimalIPv6ConverterHandler`.

        Returns:
        IPv6SubnetConfig: A randomly generated IPv6 subnet configuration containing the IP address and the netmask.
        """
        random_host, random_mask = self._prepare(128, DecimalIPv6ConverterHandler())
        ipv6_subnet = IPv6SubnetConfig(IPv6Addr(random_host), IPv6NetMask(random_mask))
        return ipv6_subnet
