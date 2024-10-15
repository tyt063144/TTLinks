## TTLinks Network Toolkit Overview

**TTLinks** is a comprehensive toolkit designed for network engineers and administrators. It provides utilities for managing and analyzing IP addresses, MAC addresses, and related network components. The package supports IP and MAC address classification, OUI lookups, and binary data manipulation, streamlining tasks essential to network management.

## Installation
This project is available on PyPI and can be installed using pip:
```bash
pip install ttlinks
```

### Common Utilities
**TTLinks** includes a set of common utilities that provide essential functionality for network management tasks. These utilities are designed to be reusable and extensible, offering a foundation for building more complex network tools.
For more details, visit:
- [Common Utilities](docs/common/common_utilities.md)

### IP Services
The IP service module in **TTLinks** offers a variety of tools to classify and work with both IPv4 and IPv6 addresses. These services allow you to:
- Identify address types (public, private, multicast, etc.)
- Perform address calculations, subnetting operations, and wildcard calculation.

For more details, visit:
- [IP Address Services](docs/ipservice/ip_services.md)
- [design diagram](docs/ipservice/Class%20Diagram.pdf)

### MAC Services
**TTLinks** includes a powerful MAC service module for validating MAC addresses, converting between various formats, and performing OUI lookups using a local database. This is especially useful for managing devices across a network.

For more details, visit:
- [MAC Address Services](docs/macservice/mac_services.md)
- [design diagram](docs/macservice/Class%20Diagram.pdf)

### Protocol Stack
The protocol stack module in **TTLinks** provides a framework for working with network protocol data units (PDUs) at different layers of the TCP/IP model. This module allows you to create, parse, and manipulate protocol headers, making it easier to analyze network traffic and build custom network tools. The protocol stack currently supports Ethernet, IPv4, and ICMP headers. Example applications include packet crafting, network monitoring, port scanning, and more.

For more details, visit:
- [Protocol Stack](docs/protocol_stack/protocol_stack.md)


### Test Cases
If you're interested in seeing how these modules function in practice, check out the test cases. They provide a great way to understand how the different components work together.

For more details, visit:
- [IP Address Services Test Cases](ttlinks/tests/)


### Future Updates
**TTLinks** will be continuously evolving, with planned updates to include additional features aimed at expanding its utility for network monitoring, diagnostics and automation. Upcoming features will include:
- **Reachability (Ping) Checks**: Test the reachability of hosts over the network using ICMP ping.
- **Port Checks**: Check the availability of specific ports on a given host to verify service access.
- **DNS Lookup**: Query DNS records (A, AAAA, CNAME, MX, etc.) for a domain to assist with DNS-related issues.
- **WHOIS Check**: Retrieve domain registration and ownership information.
- **AS Number Lookup**: Look up Autonomous System (AS) numbers for specific IPs to analyze routing information.
- **Public IP Geolocation**: Tools for determining the geographic location of public IPs.
- **SSL/TLS Certificate Checker**: A service to validate SSL/TLS certificates, including expiration checks and cipher strength evaluation.

These future features will further enhance **TTLinks** as a versatile toolkit for network management and diagnostics.


## Contributing
Contributions to this project are welcome! Please feel free to submit issues or pull requests on <a href='https://github.com/tyt063144/TTLinks'>GitHub</a>.

## License
**TTLinks** is licensed under the MIT License. You are free to use, modify, and distribute the software with appropriate attribution.

## Contact
For further information, please contact Yantao Tao at tytccie@gmail.com.