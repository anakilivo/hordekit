# Substitution Ciphers

## Introduction

Substitution ciphers are a fundamental class of cryptographic algorithms that work by replacing each character in the plaintext with another character according to a specific rule or mapping. The HordeKit library provides a comprehensive framework for implementing and using substitution ciphers through the `BaseSubstitutionCipher` class.

## What are Substitution Ciphers?

Substitution ciphers are cryptographic algorithms that:
- **Replace characters**: Each plaintext character is substituted with a corresponding ciphertext character
- **Use fixed mappings**: The substitution follows a predetermined rule or pattern
- **Preserve structure**: The overall structure and length of the message remain unchanged
- **Maintain readability**: The encrypted text often remains readable, just with different characters

## Available Substitution Ciphers

HordeKit currently supports the following substitution ciphers:

### 1. [Caesar Cipher](caesar.md)
The simplest substitution cipher that shifts each letter by a fixed number of positions in the alphabet.

**Key Features:**
- Simple shift operation
- 26 possible keys (shifts 0-25)
- Easy to implement and understand
- Vulnerable to frequency analysis

### 2. [Affine Cipher](affine.md)
A mathematical substitution cipher that uses linear algebra operations.

**Key Features:**
- Uses formula: `E(x) = (ax + b) mod 26`
- Requires coprime key pairs
- More secure than Caesar cipher
- Supports mathematical attacks

### 3. [Atbash Cipher](atbash.md)
A simple substitution cipher that reverses the alphabet.

**Key Features:**
- Maps A→Z, B→Y, C→X, etc.
- Self-inverse (applying twice returns original)
- No key required
- Historical significance

### 4. [ROT13 Cipher](rot13.md)
A special case of Caesar cipher with a fixed shift of 13 positions.

**Key Features:**
- Fixed 13-position shift
- Self-inverse operation
- Commonly used for simple obfuscation
- No key management required

### 5. [ROT47 Cipher](rot47.md)
An extension of ROT13 that works with the entire printable ASCII character set.

**Key Features:**
- Works with ASCII characters 33-126
- 47-position shift
- Self-inverse operation
- Handles special characters and numbers

## Overview

The `BaseSubstitutionCipher` is an abstract base class that provides common functionality for all substitution ciphers in the HordeKit library. It serves as a foundation for implementing various character substitution algorithms while ensuring consistent behavior and attack methods.

## Conclusion

The `BaseSubstitutionCipher` provides a robust foundation for implementing substitution ciphers. By inheriting from this class, you get:

- **Consistent API**: Same interface across all substitution ciphers
- **Built-in Features**: Case preservation, attack methods, translation tables
- **Extensibility**: Easy to add new ciphers and attack methods
- **Performance**: Optimized translation table operations
- **Security**: Built-in attack methods for testing

This base class makes it easy to implement new substitution ciphers while ensuring they integrate seamlessly with the HordeKit ecosystem. 