# Hordekit

A comprehensive cryptographic library for Python, providing various encryption algorithms, attack methods, and educational tools.

## Features

- **Multiple Cipher Types**: Substitution, transposition, and modern ciphers
- **Attack Methods**: Brute force, frequency analysis, known plaintext attacks
- **Educational Focus**: Perfect for learning cryptography concepts
- **Well Documented**: Comprehensive documentation and examples
- **Type Safe**: Full type hints and mypy support
- **Tested**: Extensive test coverage

## Available Ciphers

### Substitution Ciphers

- **Caesar Cipher**: Simple shift cipher with configurable offset
- **Affine Cipher**: Mathematical substitution using linear transformation
- **Atbash Cipher**: Alphabet mirroring cipher
- **ROT13**: Special case of Caesar cipher with 13-position shift
- **ROT47**: Extended ROT cipher for printable ASCII characters
- **Vigenère Cipher**: Polyalphabetic substitution cipher with keyword

### Transposition Ciphers

*Coming soon...*

### Modern Ciphers

*Coming soon...*

## Quick Start

The library provides a simple interface for creating and using various cryptographic ciphers. You can start with basic substitution ciphers like the Caesar cipher, which uses a simple shift operation to encrypt and decrypt messages.

## Attack Methods

The library includes various attack methods for analyzing and breaking ciphers, including brute force attacks, frequency analysis, and known plaintext attacks. These methods are designed for educational purposes to understand cryptographic weaknesses.

## Installation

The library can be installed using pip or other Python package managers.

## Development

The project uses modern Python development tools including uv for dependency management and comprehensive testing frameworks.

## Documentation

- [Installation Guide](installation.md)
- [Quick Start](quickstart.md)
- [Substitution Ciphers](crypto/symmetric/substitution/base_substitution.md)
- [API Reference](api/)

## Contributing

See [Contributing Guide](development/contributing.md) for details.

## License

MIT License - see LICENSE file for details. 