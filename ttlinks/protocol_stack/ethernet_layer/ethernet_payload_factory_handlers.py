
from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import EthernetPayloadProtocolTypes
from ttlinks.protocol_stack.network_layer.IPv4.ipv4_packet_units import IPv4UnitFactory


class IPv4FactorySelectorHandler(SimpleCoRHandler):
    """
    A handler for selecting the IPv4 unit factory based on the Ethernet payload protocol type.

    This class is part of a **Chain of Responsibility** pattern, where it handles the protocol type
    and returns the appropriate factory if the protocol is IPv4. If the protocol does not match IPv4,
    it passes the request to the next handler in the chain (if available).

    Methods:
    - handle: Checks if the protocol matches IPv4. If it does, returns the `IPv4UnitFactory`.
              Otherwise, it forwards the request to the next handler in the chain.

    Parameters:
    - protocol (EthernetPayloadProtocolTypes): The protocol type of the Ethernet payload.

    Returns:
    - IPv4UnitFactory: If the protocol is IPv4, returns the IPv4 factory for constructing IPv4 units.
    - Otherwise, forwards the request to the next handler in the chain.
    """
    def handle(self, protocol: EthernetPayloadProtocolTypes, *args, **kwargs):
        if protocol == EthernetPayloadProtocolTypes.IPv4:
            return IPv4UnitFactory
        else:
            return super().handle(protocol)

