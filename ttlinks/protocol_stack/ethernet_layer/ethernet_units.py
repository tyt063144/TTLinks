from ttlinks.common.design_template.cor import ProtocolUnitSelectorCoRHandler
from ttlinks.macservice.mac_address import MACAddr
from ttlinks.macservice.mac_factory import MACFactory
from ttlinks.macservice.oui_db import OUI_DATABASE
from ttlinks.macservice.oui_utils import OUIUnit
from ttlinks.protocol_stack.base_classes.stack_utils import ProtocolUnit
from ttlinks.protocol_stack.ethernet_layer.ethernet_parsers import EthernetFrameParser
from ttlinks.protocol_stack.ethernet_layer.ethernet_payload_unit_factory import EthernetPayloadUnitFactory
from ttlinks.protocol_stack.ethernet_layer.ethernet_utils import EthernetPayloadProtocolTypes, LSAP, EthernetTypes


class EthernetII(ProtocolUnit):
    """
    Represents an Ethernet II frame.

    This class encapsulates an Ethernet II frame, which consists of a destination MAC address,
    source MAC address, EtherType, and payload. It provides properties to access the frame
    components and converts the entire frame to bytes.

    The class also supports parsing the payload based on the EtherType field, using the
    `EthernetPayloadUnitFactory` to create appropriate higher-layer protocol units.

    Attributes:
    - _dst (bytes): The destination MAC address (6 bytes).
    - _src (bytes): The source MAC address (6 bytes).
    - _type (bytes): The EtherType field (2 bytes), indicating the network protocol in the payload.
    - _payload (bytes): The payload (remaining bytes after the EtherType).

    Properties:
    - as_bytes: Returns the entire frame as a sequence of bytes.
    - summary: Provides a dictionary summary of the frame, including MAC addresses and payload.
    - attributes: Returns a dictionary containing the raw frame attributes (dst, src, type, payload).
    - frame_type: Returns the frame type (Ethernet II).
    - dst: Returns the parsed destination MAC address as a `MACAddr` object.
    - src: Returns the parsed source MAC address as a `MACAddr` object.
    - type: Returns the EtherType as an `EthernetPayloadProtocolTypes` enum.
    - payload: Attempts to parse the payload based on the EtherType and returns the parsed payload or raw payload.

    Methods:
    None
    """
    def __init__(
            self,
            dst: bytes,
            src: bytes,
            type: bytes,
            payload: bytes
    ):
        """
        Initializes an Ethernet II frame with the destination MAC, source MAC, EtherType, and payload.

        Parameters:
        - dst (bytes): Destination MAC address (6 bytes).
        - src (bytes): Source MAC address (6 bytes).
        - type (bytes): EtherType field (2 bytes), indicating the network protocol in the payload.
        - payload (bytes): The payload (the data carried by the Ethernet frame).
        """
        self._dst = dst
        self._src = src
        self._type = type
        self._payload = payload

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the entire Ethernet II frame as a sequence of bytes.

        This concatenates the destination MAC, source MAC, EtherType, and payload into a single byte sequence.

        Returns:
        bytes: The byte representation of the Ethernet II frame.
        """
        return self._dst + self._src + self._type + self._payload

    @property
    def summary(self) -> dict:
        """
        Provides a summary of the Ethernet II frame as a dictionary.

        The summary includes:
        - frame_type: The type of Ethernet frame (Ethernet II).
        - destination_mac: The parsed destination MAC address.
        - source_mac: The parsed source MAC address.
        - network_layer: The network protocol indicated by the EtherType.
        - next_layer_payload: The payload data or parsed network layer unit.

        Returns:
        dict: A summary of the frame fields.
        """
        return {
            'frame_type': self.frame_type,
            'destination_mac': self.dst,
            'source_mac': self.src,
            'next_layer': self.type,
            'next_layer_payload': self.payload,
        }

    @property
    def attributes(self) -> dict:
        """
        Returns the raw attributes of the Ethernet II frame as a dictionary.

        The dictionary includes the destination MAC, source MAC, EtherType, and payload in their raw byte forms.

        Returns:
        dict: The raw frame attributes.
        """
        return {
            'dst': self._dst,
            'src': self._src,
            'type': self._type,
            'payload': self._payload,
        }

    @property
    def frame_type(self) -> EthernetTypes:
        """
        Returns the Ethernet frame type (Ethernet II).

        This property returns a constant indicating the type of the frame.

        Returns:
        EthernetTypes: The Ethernet frame type (Ethernet II).
        """
        return EthernetTypes.Ethernet_II

    @property
    def dst(self) -> MACAddr:
        """
        Returns the destination MAC address as a `MACAddr` object.

        Uses the `MACFactory` to parse the raw destination MAC address.

        Returns:
        MACAddr: The parsed destination MAC address.
        """
        return MACFactory().mac(self._dst)

    @property
    def src(self) -> MACAddr:
        """
        Returns the source MAC address as a `MACAddr` object.

        Uses the `MACFactory` to parse the raw source MAC address.

        Returns:
        MACAddr: The parsed source MAC address.
        """
        return MACFactory().mac(self._src)

    @property
    def type(self) -> EthernetPayloadProtocolTypes:
        """
        Returns the EtherType field as an `EthernetPayloadProtocolTypes` enum.

        The EtherType field indicates the protocol in the network layer (e.g., IPv4, ARP).

        Returns:
        EthernetPayloadProtocolTypes: The parsed EtherType as an enum.
        """
        return EthernetPayloadProtocolTypes(int.from_bytes(self._type, byteorder='big'))

    @property
    def payload(self) -> bytes:
        """
        Returns the payload of the Ethernet II frame.

        This method attempts to parse the payload based on the EtherType using the `EthernetPayloadUnitFactory`.
        If parsing is successful, the parsed payload (higher-layer protocol unit) is returned. Otherwise, the
        raw payload bytes are returned.

        Returns:
        bytes: The parsed network layer payload or the raw payload if parsing fails.
        """
        parsed_payload = EthernetPayloadUnitFactory.create_unit(self._payload, self.type)
        if parsed_payload:
            return parsed_payload
        return self._payload

class IEEE8023(ProtocolUnit):
    """
    A class representing an IEEE 802.3 frame.

    This class handles the parsing and representation of IEEE 802.3 Ethernet frames,
    which include the LLC (Logical Link Control) and SNAP (Subnetwork Access Protocol) headers.
    The class also supports extracting and interpreting fields from the frame,
    such as the destination MAC, source MAC, length, DSAP, SSAP, and control fields,
    along with the payload and optional padding.

    Methods:
    - as_bytes: Returns the full frame as a sequence of bytes.
    - summary: Returns a summary of key fields in the frame for logging or inspection.
    - attributes: Returns a dictionary containing raw values of the frame fields.
    - frame_type: Returns the frame type (IEEE 802.3).
    - dst: Returns the destination MAC address as a MACAddr object.
    - src: Returns the source MAC address as a MACAddr object.
    - length: Returns the length of the frame.
    - dsap: Returns the DSAP (Destination Service Access Point) from the LLC header.
    - ssap: Returns the SSAP (Source Service Access Point) from the LLC header.
    - control: Returns the control field from the LLC header.
    - oui: Returns the Organizationally Unique Identifier (OUI) from the SNAP header.
    - pid: Returns the Protocol Identifier (PID) from the SNAP header.
    - payload: Attempts to parse the payload based on the PID or returns the raw payload.
    - padding: Returns any padding required to meet the minimum Ethernet frame size.

    Parameters:
    - dst (bytes): The destination MAC address.
    - src (bytes): The source MAC address.
    - length (bytes): The length of the Ethernet frame.
    - llc (bytes): The Logical Link Control (LLC) header.
    - snap (bytes): The Subnetwork Access Protocol (SNAP) header.
    - payload (bytes): The payload of the Ethernet frame.
    """
    def __init__(
            self,
            dst: bytes,
            src: bytes,
            length: bytes,
            llc: bytes,
            snap: bytes,
            payload: bytes
    ):
        self._dst = dst
        self._src = src
        self._length = length
        self._llc = llc
        self._snap = snap
        self._payload = payload

    @property
    def as_bytes(self) -> bytes:
        """
        Returns the full frame as a sequence of bytes by concatenating
        destination MAC, source MAC, length, LLC, SNAP, and payload fields.

        Returns:
        bytes: The entire Ethernet frame as bytes.
        """
        return self._dst + self._src + self._length + self._llc + self._snap + self._payload

    @property
    def summary(self) -> dict:
        """
        Provides a summary of the key fields in the IEEE 802.3 frame.

        Returns:
        dict: A dictionary summarizing the frame's fields, including frame type,
        destination and source MAC addresses, length, DSAP, SSAP, OUI, PID, payload, and padding.
        """
        return {
            'frame_type': self.frame_type,
            'destination_mac': self.dst,
            'source_mac': self.src,
            'length': self.length,
            'dsap': self.dsap,
            'ssap': self.ssap,
            'control': self.control,
            'oui': self.oui,
            'next_layer': self.pid,
            'next_layer_payload': self.payload,
            'padding': self.padding
        }

    @property
    def attributes(self) -> dict:
        """
        Provides the raw values of the frame's fields.

        Returns:
        dict: A dictionary containing the raw destination MAC, source MAC, length, LLC, SNAP, and payload fields.
        """
        return {
            'dst': self._dst,
            'src': self._src,
            'length': self._length,
            'llc': self._llc,
            'snap': self._snap,
            'payload': self._payload
        }

    @property
    def frame_type(self) -> EthernetTypes:
        """
        Returns the frame type, indicating that this is an IEEE 802.3 frame.

        Returns:
        EthernetTypes: Enum value representing the IEEE 802.3 frame type.
        """
        return EthernetTypes.IEEE802_3

    @property
    def dst(self) -> MACAddr:
        """
        Returns the destination MAC address.

        Returns:
        MACAddr: The destination MAC address as a MACAddr object.
        """
        return MACAddr(self._dst)

    @property
    def src(self) -> MACAddr:
        """
        Returns the source MAC address.

        Returns:
        MACAddr: The source MAC address as a MACAddr object.
        """
        return MACAddr(self._src)

    @property
    def length(self) -> int:
        """
        Returns the length of the frame by converting the length bytes.

        Returns:
        int: The length of the Ethernet frame.
        """
        return int.from_bytes(self._length, byteorder='big')

    @property
    def dsap(self) -> LSAP:
        """
        Returns the Destination Service Access Point (DSAP) from the LLC header.

        Returns:
        LSAP: The DSAP value.
        """
        return LSAP(self._llc[0])

    @property
    def ssap(self) -> LSAP:
        """
        Returns the Source Service Access Point (SSAP) from the LLC header.

        Returns:
        LSAP: The SSAP value.
        """
        return LSAP(self._llc[1])

    @property
    def control(self) -> bytes:
        """
        Returns the control field from the LLC header.

        Returns:
        bytes: The control field (the third byte of the LLC header).
        """
        return self._llc[2:3]

    @property
    def oui(self) -> OUIUnit:
        """
        Returns the Organizationally Unique Identifier (OUI) from the SNAP header, if present.

        Returns:
        OUIUnit: The OUI value based on the first three bytes of the SNAP header.
        """
        if self._snap:
            return OUI_DATABASE.search(self._snap[:3])

    @property
    def pid(self) -> EthernetPayloadProtocolTypes:
        """
        Returns the Protocol Identifier (PID) from the SNAP header, if present.

        Returns:
        EthernetPayloadProtocolTypes: Enum representing the protocol identifier from the SNAP header.
        """
        if self._snap:
            return EthernetPayloadProtocolTypes(int.from_bytes(self._snap[3:5], byteorder='big'))

    @property
    def payload(self) -> bytes:
        """
        Attempts to parse the payload based on the protocol identifier (PID), or returns the raw payload if parsing is not possible.

        Returns:
        bytes: The parsed payload or raw payload.
        """
        parsed_payload = EthernetPayloadUnitFactory.create_unit(self._payload, self.pid)
        if parsed_payload:
            return parsed_payload
        return self._payload

    @property
    def padding(self) -> bytes:
        """
        Calculates and returns the padding required to meet the minimum Ethernet frame size.

        Returns:
        bytes: Padding bytes (if needed), ensuring the frame meets the 46-byte minimum payload requirement.
        """
        return max(0, 46 - self.length) * b'\x00'


class EthernetIIUnitSelectorHandler(ProtocolUnitSelectorCoRHandler):
    """
    Handler for selecting and creating Ethernet II units based on the parsed frame.

    This class is part of a **Chain of Responsibility** pattern and attempts to parse
    the provided frame as an Ethernet II frame. If the parsed frame contains the expected
    fields (destination, source, type, payload), it constructs and returns an `EthernetII` object.

    Methods:
    - _parse: Parses the raw frame into a dictionary of fields.
    - handle: Handles the frame parsing and attempts to create an `EthernetII` object.

    Parameters:
    - frame (bytes): The raw Ethernet frame to be parsed.

    Returns:
    - EthernetII: If the frame matches the Ethernet II format.
    - Otherwise, forwards the request to the next handler in the chain.
    """
    def _parse(self, frame: bytes):
        """
        Parses the raw Ethernet frame into a dictionary of fields, if not already parsed.

        Parameters:
        - frame (bytes): The raw Ethernet frame.

        Returns:
        None
        """
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(frame)
    def handle(self, frame: bytes, *args, **kwargs):
        """
        Handles the frame parsing and attempts to create an `EthernetII` object if the frame
        contains the expected Ethernet II fields.

        If the frame does not match the Ethernet II format, it forwards the request
        to the next handler in the chain.

        Parameters:
        - frame (bytes): The raw Ethernet frame.
        - *args, **kwargs: Additional arguments for custom handling.

        Returns:
        - EthernetII: The constructed Ethernet II object if the frame is valid.
        - Otherwise, forwards the request to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(frame)
        if isinstance(self._parsed_data, dict) and ['dst', 'src', 'type', 'payload'] == list(self._parsed_data.keys()):
            return EthernetII(**self._parsed_data)
        else:
            return self._next_handler.handle(frame, *args, **kwargs)


class IEEE8023UnitSelectorHandler(ProtocolUnitSelectorCoRHandler):
    """
    Handler for selecting and creating IEEE 802.3 units based on the parsed frame.

    This class is part of a **Chain of Responsibility** pattern and attempts to parse
    the provided frame as an IEEE 802.3 frame. If the parsed frame contains the expected
    fields (destination, source, length, LLC, SNAP, payload), it constructs and returns
    an `IEEE8023` object.

    Methods:
    - _parse: Parses the raw frame into a dictionary of fields.
    - handle: Handles the frame parsing and attempts to create an `IEEE8023` object.

    Parameters:
    - frame (bytes): The raw Ethernet frame to be parsed.

    Returns:
    - IEEE8023: If the frame matches the IEEE 802.3 format.
    - Otherwise, forwards the request to the next handler in the chain.
    """
    def _parse(self, frame: bytes):
        """
        Parses the raw Ethernet frame into a dictionary of fields, if not already parsed.

        Parameters:
        - frame (bytes): The raw Ethernet frame.

        Returns:
        None
        """
        if self._parsed_data is None:
            self._parsed_data = self._parser.parse(frame)
    def handle(self, frame: bytes, *args, **kwargs):
        """
        Handles the frame parsing and attempts to create an `IEEE8023` object if the frame
        contains the expected IEEE 802.3 fields.

        If the frame does not match the IEEE 802.3 format, it forwards the request
        to the next handler in the chain.

        Parameters:
        - frame (bytes): The raw Ethernet frame.
        - *args, **kwargs: Additional arguments for custom handling.

        Returns:
        - IEEE8023: The constructed IEEE 802.3 object if the frame is valid.
        - Otherwise, forwards the request to the next handler in the chain.
        """
        if self._parsed_data is None:
            self._parse(frame)
        if isinstance(self._parsed_data, dict) and ['dst', 'src', 'length', 'llc', 'snap', 'payload'] == list(self._parsed_data.keys()):
            return IEEE8023(**self._parsed_data)
        else:
            return self._next_handler.handle(frame, *args, **kwargs)


class EthernetUnitFactory:
    """
    A factory class for creating Ethernet frame units from raw network data.

    This class uses the **Chain of Responsibility** pattern to select the correct
    frame type (either Ethernet II or IEEE 802.3) based on the frame's content and
    structure. It cannot be used to create Ethernet frames from scratch but is designed
    to process raw frames received from the network.

    Methods:
    - create_unit: Creates and returns an appropriate Ethernet frame unit (Ethernet II or IEEE 802.3).

    Returns:
    - Ethernet frame unit (EthernetII or IEEE8023) based on the parsed frame content.
    """
    @staticmethod
    def create_unit(frame: bytes):
        """
        Creates and returns an appropriate Ethernet frame unit (Ethernet II or IEEE 802.3)
        based on the content of the raw frame. It starts with the `EthernetIIUnitSelectorHandler`
        and falls back to `IEEE8023UnitSelectorHandler` if necessary.

        Parameters:
        - frame (bytes): The raw Ethernet frame.

        Returns:
        - Ethernet frame unit: An instance of `EthernetII` or `IEEE8023` based on the parsed frame content.
        """
        frame_selector = EthernetIIUnitSelectorHandler(EthernetFrameParser())
        frame_selector.set_next(IEEE8023UnitSelectorHandler())
        return frame_selector.handle(frame)
