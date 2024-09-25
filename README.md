## TTLinks Network Toolkit Overview

**TTLinks** is a comprehensive toolkit designed for network engineers and administrators. It provides utilities for managing and analyzing IP addresses, MAC addresses, and related network components. The package supports IP and MAC address classification, OUI lookups, and binary data manipulation, streamlining tasks essential to network management.

## Installation
This project is available on PyPI and can be installed using pip:
```bash
pip install ttlinks
```


### IP Services
The IP service module in **TTLinks** offers a variety of tools to classify and work with both IPv4 and IPv6 addresses. These services allow you to:
- Identify address types (public, private, multicast, etc.)
- Perform address calculations, subnetting operations, and wildcard calculation.

For more details, visit:
- [IP Address Services](docs/ipservice/ip_services.md)
- [design diagram](docs/ipservice/Class%20Diagram.pdf)

### MAC Services
**TTLinks** includes a powerful MAC service module for validating MAC addresses, converting between various formats, and performing OUI lookups using a local database. This is especially useful for managing devices across a network.

- Document is coming soon
- [design diagram](docs/macservice/Class%20Diagram-unfinished.pdf)

### Test Cases
If you're interested in seeing how these modules function in practice, check out the test cases. They provide a great way to understand how the different components work together.

For more details, visit:
- [IP Address Services Test Cases](tests/)


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