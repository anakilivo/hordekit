#!/usr/bin/env python3
"""
Demo of Atbash Cipher implementation.
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hordekit.crypto.symmetric.substitution.atbash import AtbashCipher


def demo_basic_usage():
    """Demo basic Atbash cipher usage."""
    print("=== Atbash Cipher Basic Usage ===")
    
    atbash = AtbashCipher()
    message = "ATBASH CIPHER"
    
    encrypted = atbash.encode(message)
    decrypted = atbash.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_case_preservation():
    """Demo case preservation."""
    print("=== Case Preservation ===")
    
    atbash = AtbashCipher()
    message = "AtBaSh CiPhEr"
    
    encrypted = atbash.encode(message)
    decrypted = atbash.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_symmetry():
    """Demo that Atbash is its own inverse."""
    print("=== Atbash Symmetry ===")
    
    atbash = AtbashCipher()
    message = "CRYPTOGRAPHY"
    
    # Apply Atbash twice
    once = atbash.encode(message)
    twice = atbash.encode(once)
    
    print(f"Original: {message}")
    print(f"First application: {once}")
    print(f"Second application: {twice}")
    print(f"Symmetry holds: {message == twice}")
    print()


def demo_no_attack_methods():
    """Demo that Atbash has no attack methods."""
    print("=== No Attack Methods ===")
    
    print("Atbash cipher has no attack methods because it has no variability.")
    print("It's a fixed algorithm without a key.")
    print(f"Supported attack methods: {AtbashCipher.SUPPORTED_ATTACK_METHODS}")
    print()


def demo_non_alphabetic():
    """Demo handling of non-alphabetic characters."""
    print("=== Non-Alphabetic Characters ===")
    
    atbash = AtbashCipher()
    message = "ATBASH123!@#"
    
    encrypted = atbash.encode(message)
    decrypted = atbash.decode(encrypted)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}")
    print()


def demo_inheritance():
    """Demo inheritance from AffineCipher."""
    print("=== Inheritance from AffineCipher ===")
    
    from hordekit.crypto.symmetric.substitution.affine import AffineCipher
    
    atbash = AtbashCipher()
    
    print(f"Is instance of AffineCipher: {isinstance(atbash, AffineCipher)}")
    print(f"Atbash parameters: a={atbash.a}, b={atbash.b}")
    print("Atbash is a special case of Affine cipher with a=25, b=25")
    print()


if __name__ == "__main__":
    demo_basic_usage()
    demo_case_preservation()
    demo_symmetry()
    demo_no_attack_methods()
    demo_non_alphabetic()
    demo_inheritance() 