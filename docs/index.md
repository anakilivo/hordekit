# Hordekit - Cryptographic Toolkit

A comprehensive Python library for cryptographic algorithms and analysis tools, designed for educational and research purposes.

## Overview

Hordekit provides implementations of various cryptographic algorithms, focusing on classical and modern cryptographic techniques. The library includes comprehensive documentation, analysis tools, and educational resources for understanding cryptography.

## Key Features

- **Classical Ciphers**: Caesar, Affine, Atbash, and more
- **Attack Methods**: Brute force, frequency analysis, known plaintext attacks
- **Educational Focus**: Designed for learning cryptography concepts
- **Comprehensive Testing**: Extensive test coverage with real-world examples
- **Modern Python**: Type hints, async support, and modern Python features

## Quick Start

```python
from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

# Create a Caesar cipher with shift 3
caesar = CaesarCipher(shift=3)

# Encrypt a message
encrypted = caesar.encode("HELLO WORLD")
print(encrypted)  # Output: KHOOR ZRUOG

# Decrypt the message
decrypted = caesar.decode(encrypted)
print(decrypted)  # Output: HELLO WORLD
```

## Installation

```bash
pip install hordekit
```

Or using uv:

```bash
uv add hordekit
```

## Available Algorithms

### Symmetric Ciphers

#### Substitution Ciphers

- **Caesar Cipher**: Simple shift cipher
- **Affine Cipher**: Mathematical substitution cipher
- **Atbash Cipher**: Alphabet mirroring cipher
- **ROT13 Cipher**: Fixed 13-position shift cipher
- **ROT47 Cipher**: Extended ASCII shift cipher

### Attack Methods

- **Brute Force**: Try all possible keys
- **Frequency Analysis**: Analyze letter patterns
- **Known Plaintext**: Use known text-cipher pairs

## Documentation

Explore the documentation to learn about:

- [Installation Guide](installation.md)
- [Quick Start Tutorial](quickstart.md)
- [Algorithm Documentation](crypto/symmetric/substitution/)
- [API Reference](api/)

## Contributing

We welcome contributions! See our [Contributing Guide](development/contributing.md) for details.

## Security Notice

⚠️ **Important**: This library is designed for educational purposes only. The implemented algorithms are not suitable for secure communication. For real-world applications, use established cryptographic libraries like `cryptography` or `pycryptodome`.

## License

This project is licensed under the MIT License. 