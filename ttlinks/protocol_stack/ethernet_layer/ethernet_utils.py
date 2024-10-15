from enum import Enum


class EthernetTypes(Enum):
    UNKNOWN = -1  # Unknown
    Ethernet_II = 0  # Ethernet II
    IEEE802_3 = 1  # IEEE 802.3

class EthernetPayloadProtocolTypes(Enum):
    UNKNOWN = -1  # Unknown
    IPv4 = 0x0800  # Internet Protocol version 4 (IPv4)
    ARP = 0x0806  # Address Resolution Protocol (ARP)
    WAKE_ON_LAN = 0x0842  # Wake-on-LAN
    CDP = 0x2000  # Cisco Discovery Protocol
    SRP = 0x22EA  # Stream Reservation Protocol
    AVTP = 0x22F0  # Audio Video Transport Protocol (AVTP)
    TRILL = 0x22F3  # IETF TRILL Protocol
    DEC_MOP_RC = 0x6002  # DEC MOP RC
    DECNET_PHASE_IV = 0x6003  # DECnet Phase IV, DNA Routing
    DEC_LAT = 0x6004  # DEC LAT
    RARP = 0x8035  # Reverse Address Resolution Protocol (RARP)
    APPLETALK = 0x809B  # AppleTalk (EtherTalk)
    LLC_PDU = 0x80D5  # LLC PDU, particularly IBM SNA
    AARP = 0x80F3  # AppleTalk Address Resolution Protocol (AARP)
    VLAN = 0x8100  # VLAN-tagged frame (IEEE 802.1Q)
    SLPP = 0x8102  # Simple Loop Prevention Protocol (SLPP)
    VLACP = 0x8103  # Virtual Link Aggregation Control Protocol (VLACP)
    IPX = 0x8137  # IPX
    QNX_QNET = 0x8204  # QNX Qnet
    IPv6 = 0x86DD  # Internet Protocol Version 6 (IPv6)
    ETHERNET_FLOW_CONTROL = 0x8808  # Ethernet flow control
    ETHERNET_SLOW_PROTOCOLS = 0x8809  # Ethernet Slow Protocols (e.g., LACP)
    COBRANET = 0x8819  # CobraNet
    MPLS_UNICAST = 0x8847  # MPLS unicast
    MPLS_MULTICAST = 0x8848  # MPLS multicast
    PPPOE_DISCOVERY = 0x8863  # PPPoE Discovery Stage
    PPPOE_SESSION = 0x8864  # PPPoE Session Stage
    HOMEPLUG_1_0 = 0x887B  # HomePlug 1.0 MME
    EAP_OVER_LAN = 0x888E  # EAP over LAN (IEEE 802.1X)
    PROFINET = 0x8892  # PROFINET Protocol
    HYPERSCSI = 0x889A  # HyperSCSI (SCSI over Ethernet)
    ATA_OVER_ETHERNET = 0x88A2  # ATA over Ethernet
    ETHERCAT = 0x88A4  # EtherCAT Protocol
    S_TAG = 0x88A8  # Service VLAN tag identifier (S-Tag) on Q-in-Q tunnel
    ETHERNET_POWERLINK = 0x88AB  # Ethernet Powerlink
    GOOSE = 0x88B8  # GOOSE (Generic Object Oriented Substation event)
    GSE_MANAGEMENT = 0x88B9  # GSE (Generic Substation Events) Management Services
    SV = 0x88BA  # SV (Sampled Value Transmission)
    MIKROTIK_ROMON = 0x88BF  # MikroTik RoMON (unofficial)
    LLDP = 0x88CC  # Link Layer Discovery Protocol (LLDP)
    SERCOS_III = 0x88CD  # SERCOS III
    HOMEPLUG_GREEN_PHY = 0x88E1  # HomePlug Green PHY
    MEDIA_REDUNDANCY_PROTOCOL = 0x88E3  # Media Redundancy Protocol (IEC62439-2)
    MACSEC = 0x88E5  # IEEE 802.1AE MAC security (MACsec)
    PBB = 0x88E7  # Provider Backbone Bridges (PBB) (IEEE 802.1ah)
    PTP = 0x88F7  # Precision Time Protocol (PTP) over IEEE 802.3 Ethernet
    NC_SI = 0x88F8  # NC-SI
    PRP = 0x88FB  # Parallel Redundancy Protocol (PRP)
    CFM = 0x8902  # IEEE 802.1ag Connectivity Fault Management (CFM) / ITU-T Y.1731
    FCOE = 0x8906  # Fibre Channel over Ethernet (FCoE)
    FIP = 0x8914  # FCoE Initialization Protocol
    ROCE = 0x8915  # RDMA over Converged Ethernet (RoCE)
    TTE = 0x891D  # TTEthernet Protocol Control Frame
    IEEE_1905_1 = 0x893A  # IEEE 1905.1 Protocol
    HSR = 0x892F  # High-availability Seamless Redundancy (HSR)
    ETHERNET_TESTING = 0x9000  # Ethernet Configuration Testing Protocol
    REDUNDANCY_TAG = 0xF1C1  # Redundancy Tag (IEEE 802.1CB Frame Replication and Elimination)


class LSAP(Enum):
    UNKNOWN = -1  # Unknown
    NULL_LSAP = 0x00  # Null LSAP
    INDIVIDUAL_LLC_MGMT = 0x02  # Individual LLC Sublayer Mgt
    SNA_PATH_CONTROL_INDIVIDUAL = 0x04  # SNA Path Control (individual)
    RESERVED_IP = 0x06  # Reserved for DoD IP
    PROWAY_LAN = 0x0E  # ProWay-LAN
    TEXAS_INSTRUMENTS = 0x18  # Texas Instruments
    BRIDGE_SPANNING_TREE = 0x42  # IEEE 802.1 Bridge Spanning Tree Protocol
    EIA_RS511 = 0x4E  # EIA-RS 511
    ISI_IP = 0x5E  # ISI IP
    ISO_8208_X25 = 0x7E  # ISO 8208 (X.25 over IEEE 802.2 Type LLC)
    XNS = 0x80  # Xerox Network Systems (XNS)
    BACNET_ETHERNET = 0x82  # BACnet/Ethernet
    NESTAR = 0x86  # Nestar
    PROWAY_LAN_IEC_955 = 0x8E  # ProWay-LAN (IEC 955)
    ARP = 0x98  # ARPANET Address Resolution Protocol (ARP)
    RDE = 0xA6  # Route Determination Entity
    SNAP_EXTENSION = 0xAA  # SNAP Extension Used
    BANYAN_VINES = 0xBC  # Banyan VINES
    NOVELL_NETWARE = 0xE0  # Novell NetWare
    NETBIOS = 0xF0  # IBM NetBIOS
    LAN_MGMT_INDIVIDUAL = 0xF4  # IBM LAN Management (individual)
    RPL = 0xF8  # IBM Remote Program Load (RPL)
    UNGERMANN_BASS = 0xFA  # Ungermann-Bass
    OSI_CLNS = 0xFE  # OSI Connectionless-mode Network Service (CLNP, ISIS, ESIS)
    GROUP_LLC_MGMT = 0x03  # Group LLC Sublayer Mgt (Group DSAP)
    SNA_PATH_CONTROL_GROUP = 0x05  # SNA Path Control (Group DSAP)
    IBM_LAN_MGMT_GROUP = 0xF5  # IBM LAN Management (Group DSAP)
    GLOBAL_DSAP = 0xFF  # Global DSAP (Group DSAP)