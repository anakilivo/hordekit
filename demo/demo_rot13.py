#!/usr/bin/env python3
"""
Demo of ROT13 Cipher implementation.
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hordekit.crypto.symmetric.substitution.rot13 import ROT13Cipher


def demo_basic_usage():
    """Demo basic ROT13 cipher usage."""
    print("=== ROT13 Cipher Basic Usage ===")
    
    rot13 = ROT13Cipher()
    message = "ROT13 CIPHER"
    
    encrypted = rot13.encode(message)
    decrypted = rot13.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_case_preservation():
    """Demo case preservation."""
    print("=== Case Preservation ===")
    
    rot13 = ROT13Cipher()
    message = "RoT13 CiPhEr"
    
    encrypted = rot13.encode(message)
    decrypted = rot13.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_symmetry():
    """Demo that ROT13 is its own inverse."""
    print("=== ROT13 Symmetry ===")
    
    rot13 = ROT13Cipher()
    message = "CRYPTOGRAPHY"
    
    # Apply ROT13 twice
    once = rot13.encode(message)
    twice = rot13.encode(once)
    
    print(f"Original: {message}")
    print(f"First application: {once}")
    print(f"Second application: {twice}")
    print(f"Symmetry holds: {message == twice}")
    print()


def demo_no_attack_methods():
    """Demo that ROT13 has no attack methods."""
    print("=== No Attack Methods ===")
    
    print("ROT13 cipher has no attack methods because it has no variability.")
    print("It's a fixed algorithm without a key.")
    print(f"Supported attack methods: {ROT13Cipher.SUPPORTED_ATTACK_METHODS}")
    print()


def demo_non_alphabetic():
    """Demo handling of non-alphabetic characters."""
    print("=== Non-Alphabetic Characters ===")
    
    rot13 = ROT13Cipher()
    message = "ROT13!@#123"
    
    encrypted = rot13.encode(message)
    decrypted = rot13.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_inheritance():
    """Demo inheritance from CaesarCipher."""
    print("=== Inheritance from CaesarCipher ===")
    
    from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher
    
    rot13 = ROT13Cipher()
    
    print(f"Is instance of CaesarCipher: {isinstance(rot13, CaesarCipher)}")
    print(f"ROT13 shift value: {rot13.shift}")
    print("ROT13 is a special case of Caesar cipher with shift=13")
    print()


def demo_alphabet_mapping():
    """Demo complete alphabet mapping."""
    print("=== Complete Alphabet Mapping ===")
    
    rot13 = ROT13Cipher()
    
    # Uppercase alphabet
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    expected_uppercase = "NOPQRSTUVWXYZABCDEFGHIJKLM"
    
    encrypted_upper = rot13.encode(uppercase)
    print(f"Uppercase alphabet: {uppercase}")
    print(f"ROT13 encrypted:   {encrypted_upper}")
    print(f"Expected:          {expected_uppercase}")
    print(f"Correct: {encrypted_upper == expected_uppercase}")
    print()
    
    # Lowercase alphabet
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    expected_lowercase = "nopqrstuvwxyzabcdefghijklm"
    
    encrypted_lower = rot13.encode(lowercase)
    print(f"Lowercase alphabet: {lowercase}")
    print(f"ROT13 encrypted:    {encrypted_lower}")
    print(f"Expected:           {expected_lowercase}")
    print(f"Correct: {encrypted_lower == expected_lowercase}")
    print()


def demo_real_world_examples():
    """Demo real-world ROT13 examples."""
    print("=== Real-World Examples ===")
    
    rot13 = ROT13Cipher()
    
    examples = [
        "HELLO WORLD",
        "CRYPTOGRAPHY",
        "PYTHON PROGRAMMING",
        "SECRET MESSAGE",
        "ROT13 IS SIMPLE"
    ]
    
    for example in examples:
        encrypted = rot13.encode(example)
        decrypted = rot13.decode(encrypted)
        
        print(f"Original:  {example}")
        print(f"ROT13:     {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Success: {example == decrypted}")
        print()


if __name__ == "__main__":
    demo_basic_usage()
    demo_case_preservation()
    demo_symmetry()
    demo_no_attack_methods()
    demo_non_alphabetic()
    demo_inheritance()
    demo_alphabet_mapping()
    demo_real_world_examples()
