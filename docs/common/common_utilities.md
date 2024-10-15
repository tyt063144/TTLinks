## Algorithm

### 1. **`checksum.py`**
This module provides a robust and extensible framework for calculating checksums in Python. By leveraging the Strategy Design Pattern, it allows users to switch between different checksum algorithms seamlessly without altering the client code. The primary components include an abstract base class defining the checksum interface, a concrete implementation of the Internet Checksum algorithm, and a calculator class that utilizes the chosen checksum strategy.

- [Checksum Module](/docs/common/algorithm/checksum.md)

### 2. **`converters.py`**
The `converters.py` module currently provides a utility class, `NumeralConverter`, for converting between binary, decimal, and hexadecimal numeral systems. This module is designed to offer efficient and reliable numeral system conversions, and while it currently contains only the `NumeralConverter` class, it is structured to accommodate additional converters in the future.

- [Converters Module](/docs/common/tools/converters.md)

