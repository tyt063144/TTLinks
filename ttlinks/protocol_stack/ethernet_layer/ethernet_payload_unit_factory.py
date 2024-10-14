from ttlinks.protocol_stack.ethernet_layer.ethernet_payload_factory_handlers import IPv4FactorySelectorHandler
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import EthernetPayloadProtocolTypes


class EthernetPayloadUnitFactory:
    """
    A factory class for creating Ethernet payload units from received network data.

    This class is responsible for creating Ethernet payload units from bytes received
    from the network, based on the specified protocol. It leverages a chain of handlers
    (starting with `IPv4FactorySelectorHandler`) to determine the correct factory for creating
    the appropriate protocol unit (e.g., IPv4).

    Note:
    - This class cannot be used to create Ethernet frames from scratch. It only processes
      packets received from the network.

    Methods:
    - create_unit: Selects the appropriate factory based on the protocol and creates an Ethernet payload unit.
    """
    @staticmethod
    def create_unit(packet: bytes, protocol: EthernetPayloadProtocolTypes):
        factory_selector = IPv4FactorySelectorHandler()
        factory = factory_selector.handle(protocol)
        if factory:
            return factory.create_unit(packet)