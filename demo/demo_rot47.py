#!/usr/bin/env python3
"""
Demo of ROT47 Cipher implementation.
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hordekit.crypto.symmetric.substitution.rot47 import ROT47Cipher


def demo_basic_usage():
    """Demo basic ROT47 cipher usage."""
    print("=== ROT47 Cipher Basic Usage ===")
    
    rot47 = ROT47Cipher()
    message = "ROT47!@#"
    
    encrypted = rot47.encode(message)
    decrypted = rot47.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_ascii_mapping():
    """Demo ASCII character mapping."""
    print("=== ASCII Character Mapping ===")
    
    rot47 = ROT47Cipher()
    
    # Show some key mappings
    test_chars = ["!", "A", "Z", "a", "z", "0", "9", "~"]
    
    print("Character mappings:")
    for char in test_chars:
        encrypted = rot47.encode(char)
        decrypted = rot47.decode(encrypted)
        print(f"'{char}' (ASCII {ord(char):3d}) → '{encrypted}' (ASCII {ord(encrypted):3d}) → '{decrypted}'")
    
    print()


def demo_symmetry():
    """Demo that ROT47 is its own inverse."""
    print("=== ROT47 Symmetry ===")
    
    rot47 = ROT47Cipher()
    message = "CRYPTOGRAPHY!@#"
    
    # Apply ROT47 twice
    once = rot47.encode(message)
    twice = rot47.encode(once)
    
    print(f"Original: {message}")
    print(f"First application: {once}")
    print(f"Second application: {twice}")
    print(f"Symmetry holds: {message == twice}")
    print()


def demo_no_attack_methods():
    """Demo that ROT47 has no attack methods."""
    print("=== No Attack Methods ===")
    
    print("ROT47 cipher has no attack methods because it has no variability.")
    print("It's a fixed algorithm without a key.")
    print(f"Supported attack methods: {ROT47Cipher.SUPPORTED_ATTACK_METHODS}")
    print()


def demo_mixed_content():
    """Demo handling of mixed content."""
    print("=== Mixed Content ===")
    
    rot47 = ROT47Cipher()
    message = "Hello, World! 123 @#$%"
    
    encrypted = rot47.encode(message)
    decrypted = rot47.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_inheritance():
    """Demo inheritance from CaesarCipher."""
    print("=== Inheritance from CaesarCipher ===")
    
    from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher
    
    rot47 = ROT47Cipher()
    
    print(f"Is instance of CaesarCipher: {isinstance(rot47, CaesarCipher)}")
    print(f"ROT47 shift value: {rot47.shift}")
    print("ROT47 is a special case of Caesar cipher with shift=47")
    print()


def demo_ascii_range():
    """Demo the complete ASCII range."""
    print("=== Complete ASCII Range ===")
    
    rot47 = ROT47Cipher()
    
    # Show the alphabet used by ROT47
    print(f"ROT47 alphabet length: {len(rot47.alphabet)}")
    print(f"First character: '{rot47.alphabet[0]}' (ASCII {ord(rot47.alphabet[0])})")
    print(f"Last character: '{rot47.alphabet[-1]}' (ASCII {ord(rot47.alphabet[-1])})")
    print()
    
    # Show a sample of the alphabet
    print("Sample of ROT47 alphabet:")
    sample = rot47.alphabet[:20] + "..." + rot47.alphabet[-20:]
    print(f"'{sample}'")
    print()


def demo_real_world_examples():
    """Demo real-world ROT47 examples."""
    print("=== Real-World Examples ===")
    
    rot47 = ROT47Cipher()
    
    examples = [
        "Hello, World!",
        "Password123!@#",
        "Email: user@example.com",
        "URL: https://example.com",
        "JSON: {\"key\": \"value\"}"
    ]
    
    for example in examples:
        encrypted = rot47.encode(example)
        decrypted = rot47.decode(encrypted)
        
        print(f"Original: {example}")
        print(f"ROT47:    {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Success: {example == decrypted}")
        print()


def demo_comparison_with_rot13():
    """Demo comparison with ROT13."""
    print("=== Comparison with ROT13 ===")
    
    from hordekit.crypto.symmetric.substitution.rot13 import ROT13Cipher
    
    rot13 = ROT13Cipher()
    rot47 = ROT47Cipher()
    
    message = "Hello, World! 123"
    
    rot13_encrypted = rot13.encode(message)
    rot47_encrypted = rot47.encode(message)
    
    print(f"Original: {message}")
    print(f"ROT13:    {rot13_encrypted}")
    print(f"ROT47:    {rot47_encrypted}")
    print()
    
    print("ROT13 only transforms letters (A-Z, a-z)")
    print("ROT47 transforms all printable ASCII characters (33-126)")
    print()


if __name__ == "__main__":
    demo_basic_usage()
    demo_ascii_mapping()
    demo_symmetry()
    demo_no_attack_methods()
    demo_mixed_content()
    demo_inheritance()
    demo_ascii_range()
    demo_real_world_examples()
    demo_comparison_with_rot13() 