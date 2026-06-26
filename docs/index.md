# hordekit

A modular CTF toolkit for Python. Each module is independent but shares the same `HordeResult` interface and `.pipe()` chaining.

## Modules

| Module | Status | Description |
|--------|--------|-------------|
| `crypto` | ✅ Active | Classical and modern ciphers + cryptanalysis |
| `web` | 🔜 Planned | Web vulnerability tools (SQLi, XSS, SSTI, ...) |
| `osint` | 🔜 Planned | OSINT tools (username lookup, DNS, dorks, ...) |
| `forensics` | 🔜 Planned | File analysis, steganography, PCAP |

## Core concept

Every tool returns a `HordeResult` that can be converted to any format or piped into the next tool:

```python
from hordekit.crypto.classical.substitution import Caesar, ROT13

result = (
    Caesar(shift=3).encrypt(b"Hello, World!")
    .pipe(ROT13)
    .as_base64()
)
```

## Installation

```bash
pip install hordekit
```

## Links

- [Quick Start](quickstart.md)
- [Roadmap](roadmap.md)
- [GitHub](https://github.com/anakilivo/hordekit)
