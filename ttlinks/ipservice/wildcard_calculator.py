from ttlinks.ipservice.ip_address import IPv4Addr, IPv4WildCard, IPv6Addr, IPv6WildCard
from ttlinks.ipservice.ip_configs import IPv4WildCardConfig, IPv4SubnetConfig, IPv6WildCardConfig, IPv6SubnetConfig
from ttlinks.ipservice.ip_converters import BinaryDigitsIPv4ConverterHandler, BinaryDigitsIPv6ConverterHandler


def calculate_minimum_ipv4_wildcard(*subnets: str) -> IPv4WildCardConfig:
    """
    Calculates the minimal IPv4 wildcard configuration that encompasses all the provided subnets.

    Parameters:
    *subnets: str
        - A variable number of IPv4 subnets to be consolidated into a wildcard configuration.

    Returns:
    IPv4WildCardConfig: The minimal wildcard configuration covering the given IPv4 subnets.

    Steps:
    1. Converts the input subnets into `IPv4SubnetConfig` objects.
    2. Extracts network ID and mask bit lists for each subnet.
    3. Determines the maximum number of host bits across all subnets.
    4. Generates the wildcard address and mask by comparing bits across all subnets.
    """
    ipv4_subnets = [IPv4SubnetConfig(subnet) for subnet in subnets]
    network_id_bits_list = [list(subnet.network_id.binary_digits) for subnet in ipv4_subnets]
    netmask_bits_list = [list(subnet.mask.binary_digits) for subnet in ipv4_subnets]
    max_host_bits = max([netmask_bits.count(0) for netmask_bits in netmask_bits_list])
    wildcard_address_bits = []
    wildcard_mask_bits = []
    for network_id_bits in zip(*network_id_bits_list):
        if len(set(network_id_bits)) == 1:
            wildcard_address_bits.append(network_id_bits[0])
            wildcard_mask_bits.append(0)
        else:
            wildcard_address_bits.append(0)
            wildcard_mask_bits.append(1)
    wildcard_mask_bits[-max_host_bits:] = [1] * max_host_bits
    return IPv4WildCardConfig(
        IPv4Addr(BinaryDigitsIPv4ConverterHandler().handle(wildcard_address_bits)),
        IPv4WildCard(BinaryDigitsIPv4ConverterHandler().handle(wildcard_mask_bits))
    )


def calculate_minimum_ipv6_wildcard(*subnets: str) -> IPv6WildCardConfig:
    """
    Calculates the minimal IPv6 wildcard configuration that encompasses all the provided subnets.

    Parameters:
    *subnets: str
        - A variable number of IPv6 subnets to be consolidated into a wildcard configuration.

    Returns:
    IPv6WildCardConfig: The minimal wildcard configuration covering the given IPv6 subnets.

    Steps:
    1. Converts the input subnets into `IPv6SubnetConfig` objects.
    2. Extracts network ID and mask bit lists for each subnet.
    3. Determines the maximum number of host bits across all subnets.
    4. Generates the wildcard address and mask by comparing bits across all subnets.
    """
    ipv6_subnets = [IPv6SubnetConfig(subnet) for subnet in subnets]
    network_id_bits_list = [list(subnet.network_id.binary_digits) for subnet in ipv6_subnets]
    netmask_bits_list = [list(subnet.mask.binary_digits) for subnet in ipv6_subnets]
    max_host_bits = max([netmask_bits.count(0) for netmask_bits in netmask_bits_list])
    wildcard_address_bits = []
    wildcard_mask_bits = []
    for network_id_bits in zip(*network_id_bits_list):
        if len(set(network_id_bits)) == 1:
            wildcard_address_bits.append(network_id_bits[0])
            wildcard_mask_bits.append(0)
        else:
            wildcard_address_bits.append(0)
            wildcard_mask_bits.append(1)
    wildcard_mask_bits[-max_host_bits:] = [1] * max_host_bits
    return IPv6WildCardConfig(
        IPv6Addr(BinaryDigitsIPv6ConverterHandler().handle(wildcard_address_bits)),
        IPv6WildCard(BinaryDigitsIPv6ConverterHandler().handle(wildcard_mask_bits))
    )