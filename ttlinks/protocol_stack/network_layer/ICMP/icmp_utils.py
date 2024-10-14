from enum import Enum

# detail of ICMP types refer to https://notes.shichao.io/tcpv1/ch8/
class ICMPTypes(Enum):
    UNKNOWN = -1
    ECHO_REPLY = 0
    DESTINATION_UNREACHABLE = 3
    REDIRECT = 5
    ECHO = 8
    TIME_EXCEEDED = 11
    PARAMETER_PROBLEM = 12
    TIMESTAMP = 13
    TIMESTAMP_REPLY = 14
    @staticmethod
    def get_type(type_code, code):
        for icmp_type in ICMPTypes:
            if icmp_type.value == (type_code, code):
                return icmp_type
        return ICMPTypes.UNKNOWN

class ICMPResponseDescription:
    @staticmethod
    def get_description(icmp_type, code):
        if icmp_type == ICMPTypes.ECHO_REPLY and code == 0:
            return 'Echo reply'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 0:
            return 'Network unreachable'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 1:
            return 'Host unreachable'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 2:
            return 'Protocol unreachable'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 3:
            return 'Port unreachable'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 4:
            return 'Fragmentation needed and DF set'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 5:
            return 'Source route failed'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 6:
            return 'Destination network unknown'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 7:
            return 'Destination host unknown'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 8:
            return 'Source host isolated'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 9:
            return 'Network administratively prohibited'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 10:
            return 'Host administratively prohibited'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 11:
            return 'Network unreachable for TOS'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 12:
            return 'Host unreachable for TOS'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 13:
            return 'Communication administratively prohibited'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 14:
            return 'Host Precedence Violation'
        if icmp_type == ICMPTypes.DESTINATION_UNREACHABLE and code == 15:
            return 'Precedence cutoff in effect'
        if icmp_type == ICMPTypes.REDIRECT and code == 0:
            return 'Redirect for network'
        if icmp_type == ICMPTypes.REDIRECT and code == 1:
            return 'Redirect for host'
        if icmp_type == ICMPTypes.REDIRECT and code == 2:
            return 'Redirect for TOS and network'
        if icmp_type == ICMPTypes.REDIRECT and code == 3:
            return 'Redirect for TOS and host'
        if icmp_type == ICMPTypes.ECHO and code == 0:
            return 'Echo request'
        if icmp_type == ICMPTypes.TIME_EXCEEDED and code == 0:
            return 'TTL expired in transit'
        if icmp_type == ICMPTypes.TIME_EXCEEDED and code == 1:
            return 'Fragment reassembly time exceeded'
        if icmp_type == ICMPTypes.PARAMETER_PROBLEM and code == 0:
            return 'Pointer indicates the error'
        if icmp_type == ICMPTypes.PARAMETER_PROBLEM and code == 1:
            return 'Missing a required option'
        if icmp_type == ICMPTypes.PARAMETER_PROBLEM and code == 2:
            return 'Bad length'