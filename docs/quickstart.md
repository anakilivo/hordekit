# Quick Start

This guide will help you get started with Hordekit in just a few minutes.

## Basic Usage

### Caesar Cipher

The Caesar cipher is the simplest substitution cipher, using a fixed shift to encrypt and decrypt messages. It's perfect for learning basic cryptographic concepts.

### Affine Cipher

The Affine cipher uses a mathematical function with two parameters to perform encryption and decryption. It provides more complexity than the Caesar cipher while remaining educational.

### Atbash Cipher

The Atbash cipher mirrors the alphabet, providing a simple but effective substitution method. It's self-reciprocal, meaning the same operation is used for both encryption and decryption.

## Attack Methods

### Brute Force Attack

The brute force attack tries all possible keys to decrypt a message. This method is exhaustive but guaranteed to find the correct key if the key space is small enough.

### Frequency Analysis

Frequency analysis uses letter frequency patterns to find the most likely key. This method is particularly effective against simple substitution ciphers where letter frequencies are preserved.

### Known Plaintext Attack

The known plaintext attack uses known plaintext-ciphertext pairs to derive the encryption key. This method is powerful when you have partial knowledge of the encrypted content.

## Key Generation

The library supports automatic key generation for various algorithms, creating cryptographically secure random keys of appropriate length and format for each cipher type.

## Error Handling

All algorithms include proper error handling for invalid parameters, ensuring robust operation and clear error messages when something goes wrong.

## Case Preservation

All algorithms preserve the original case of letters during encryption and decryption, maintaining the formatting and readability of the original text.

## Non-Alphabetic Characters

Numbers, punctuation, and spaces are preserved during encryption and decryption, ensuring that the structure and meaning of the original text are maintained.

## Next Steps

Now that you've learned the basics, explore:

- [Algorithm Documentation](crypto/symmetric/substitution/) for detailed explanations
- [API Reference](api/) for complete API documentation
- [Development Guide](development/) for contributing to the project 