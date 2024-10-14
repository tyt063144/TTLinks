
from ttlinks.common.design_template.cor import SimpleCoRHandler
from ttlinks.protocol_stack.network_layer.ICMP import icmp_units
from ttlinks.protocol_stack.network_layer.IP.ip_payload_utils import IPPayloadProtocolTypes


class ICMPFactorySelectorHandler(SimpleCoRHandler):
    """
    Handler for selecting the ICMPUnitFactory based on the IP payload protocol type.

    This handler checks if the given protocol is ICMP. If so, it returns the ICMPUnitFactory
    to handle ICMP-related packet creation. If the protocol is not ICMP, it passes the request
    to the next handler in the chain.
    """
    def handle(self, protocol: IPPayloadProtocolTypes, *args, **kwargs):
        """
        Handles the protocol selection based on the type. If the protocol is ICMP,
        it returns the ICMPUnitFactory. Otherwise, it defers to the next handler in the chain.

        Args:
            protocol (IPPayloadProtocolTypes): The protocol type to be handled.
            *args: Additional arguments passed to the handler.
            **kwargs: Additional keyword arguments passed to the handler.

        Returns:
            ICMPUnitFactory: The factory for handling ICMP packets if the protocol is ICMP.
            Otherwise, passes the protocol to the next handler in the chain.
        """
        if protocol == IPPayloadProtocolTypes.ICMP:
            return icmp_units.ICMPUnitFactory
        else:
            return super().handle(protocol)

