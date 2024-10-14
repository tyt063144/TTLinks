from ttlinks.protocol_stack.network_layer.IP.ip_payload_factory_handlers import ICMPFactorySelectorHandler
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes


class IPv4PayloadUnitFactory:
    """
    Factory for creating IPv4 payload units based on the protocol type.

    This factory uses a Chain of Responsibility pattern to select the appropriate factory
    for creating protocol-specific units, such as ICMP, TCP, UDP, etc.
    """
    @staticmethod
    def create_unit(packet: bytes, protocol: IPPayloadProtocolTypes):
        """
        Creates the appropriate protocol-specific payload unit based on the given protocol type.

        Args:
            packet (bytes): The raw packet data to be processed.
            protocol (IPPayloadProtocolTypes): The protocol type (e.g., ICMP, TCP, UDP).

        Returns:
            ProtocolUnit: A protocol-specific unit (e.g., ICMP, TCP) created by the appropriate factory.
                          If no matching factory is found, returns None.
        """
        factory_selector = ICMPFactorySelectorHandler()
        factory = factory_selector.handle(protocol)
        if factory:
            return factory.create_unit(packet)
