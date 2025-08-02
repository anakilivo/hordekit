#!/usr/bin/env python3
"""
Demo script for Caesar Cipher implementation.
Shows basic usage and attack methods.
"""

import sys

from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher
from hordekit.crypto.utils import AttackMethod


def demo_basic_usage():
    """Demonstrate basic Caesar cipher usage."""
    print("=== Caesar Cipher Demo ===\n")

    # Create cipher with shift 3
    caesar = CaesarCipher(shift=3)

    # Test message
    message = "Hello World"
    print(f"Original message: {message}")

    # Encrypt
    encrypted = caesar.encode(message)
    print(f"Encrypted (shift=3): {encrypted}")

    # Decrypt
    decrypted = caesar.decode(encrypted)
    print(f"Decrypted: {decrypted}")

    print(f"Success: {message == decrypted}")
    print()


def demo_custom_shift():
    """Demonstrate custom shift values."""
    print("=== Custom Shift Demo ===\n")

    # Test different shift values
    shifts = [5, 10, 15, 20]
    message = "CRYPTOGRAPHY"

    for shift in shifts:
        caesar = CaesarCipher(shift=shift)
        encrypted = caesar.encode(message)
        print(f"Shift {shift:2d}: {encrypted}")

    print()


def demo_attacks():
    """Demonstrate attack methods."""
    print("=== Attack Methods Demo ===\n")

    # Create cipher and encrypt a message
    caesar = CaesarCipher(shift=12)
    message = "ATTACK AT DAWN"
    encrypted = caesar.encode(message)

    print(f"Original: {message}")
    print(f"Encrypted (shift=12): {encrypted}")
    print()

    # Brute force attack
    print("--- Brute Force Attack ---")
    results = caesar.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)

    # Show results for shifts around the correct one
    print("Results for shifts 10-15:")
    for shift in range(10, 16):
        if shift in results:
            print(f"  Shift {shift:2d}: {results[shift]}")

    print()

    # Frequency analysis attack
    print("--- Frequency Analysis Attack ---")
    long_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    long_encrypted = caesar.encode(long_message)

    analysis = caesar.attack(
        AttackMethod.FREQUENCY_ANALYSIS,
        ciphertext=long_encrypted,
    )
    print(f"Most likely shift: {analysis['most_likely_shift']}")
    print(f"Decrypted text: {analysis['decrypted_text']}")
    print(f"Confidence score: {analysis['confidence_score']:.2f}")
    print()

    # Known plaintext attack
    print("--- Known Plaintext Attack ---")
    known_shift = caesar.attack(
        AttackMethod.KNOWN_PLAINTEXT,
        plaintext="HELLO",
        ciphertext=caesar.encode("HELLO"),
    )
    print(f"Recovered shift: {known_shift}")
    print()


def demo_key_generation():
    """Demonstrate key generation."""
    print("=== Key Generation Demo ===\n")

    # Generate multiple random ciphers
    print("Generated ciphers:")
    for i in range(5):
        caesar = CaesarCipher.generate_key()
        print(f"  Cipher {i+1}: shift={caesar.shift}")

    print()


def demo_formats():
    """Demonstrate different input/output formats."""
    print("=== Format Support Demo ===\n")

    caesar = CaesarCipher(shift=5)

    # Test with bytes
    message_bytes = b"Hello World"
    encrypted_bytes = caesar.encode(message_bytes)
    decrypted_bytes = caesar.decode(encrypted_bytes)
    print(f"Bytes test: {message_bytes == decrypted_bytes}")

    # Test with JSON
    data = {"message": "Hello World", "number": 42}
    encrypted_json = caesar.encode(data)
    decrypted_json = caesar.decode(encrypted_json)
    print(f"JSON test: {data == decrypted_json}")

    print()


def demo_case_preservation():
    """Demonstrate case preservation functionality."""
    print("=== Case Preservation Demo ===\n")

    caesar = CaesarCipher(shift=3)

    # Test mixed case
    messages = ["Hello World", "PYTHON PROGRAMMING", "cryptography", "MiXeD cAsE TeXt", "Hello, World! 123"]

    for message in messages:
        encrypted = caesar.encode(message)
        decrypted = caesar.decode(encrypted)
        success = message == decrypted
        status = "✓" if success else "✗"
        print(f"'{message}' -> '{encrypted}' -> '{decrypted}' {status}")

    print()


if __name__ == "__main__":
    demo_basic_usage()
    demo_custom_shift()
    demo_attacks()
    demo_key_generation()
    demo_formats()
    demo_case_preservation()

    print("Demo completed!")
