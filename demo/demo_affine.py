#!/usr/bin/env python3
"""
Demo of Affine Cipher implementation.
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from hordekit.crypto.symmetric.substitution.affine import AffineCipher
from hordekit.crypto.utils import AttackMethod


def demo_basic_usage():
    """Demonstrate basic Affine cipher usage."""
    print("=== Affine Cipher Basic Usage ===\n")
    
    # Create cipher with key a=5, b=8
    affine = AffineCipher(a=5, b=8)
    
    # Test basic encryption/decryption
    plaintext = "HELLO WORLD"
    encrypted = affine.encode(plaintext)
    decrypted = affine.decode(encrypted)
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: a={affine.a}, b={affine.b}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {plaintext == decrypted}")
    print()


def demo_key_generation():
    """Demonstrate key generation."""
    print("=== Affine Cipher Key Generation ===\n")
    
    # Generate random keys
    for i in range(3):
        generated = AffineCipher.generate_key()
        print(f"Generated key {i+1}: a={generated.a}, b={generated.b}")
        
        # Test the generated key
        test_message = "TEST MESSAGE"
        encrypted = generated.encode(test_message)
        decrypted = generated.decode(encrypted)
        print(f"  Test: '{test_message}' -> '{encrypted}' -> '{decrypted}'")
        print(f"  Valid: {test_message == decrypted}")
        print()
    print()


def demo_attack_methods():
    """Demonstrate attack methods."""
    print("=== Affine Cipher Attack Methods ===\n")
    
    # Create a cipher with known key
    affine = AffineCipher(a=9, b=13)
    plaintext = "YUBITSEC{A_FINE_CIPHER}"
    ciphertext = affine.encode(plaintext)
    
    print(f"Original: {plaintext}")
    print(f"Key: a={affine.a}, b={affine.b}")
    print(f"Encrypted: {ciphertext}")
    print()
    
    # Brute force attack with mask
    print("1. Brute Force Attack with Mask:")
    mask = r"YUBITSEC\{.*\}"
    results = AffineCipher.attack(
        AttackMethod.BRUTE_FORCE,
        ciphertext=ciphertext,
        mask=mask
    )
    
    print(f"   Mask: {mask}")
    print(f"   Mask matched: {results['mask_matched']}")
    if results['mask_matched']:
        print(f"   Best match: {results['best_match']}")
        print(f"   Recovered key: a={results['best_a']}, b={results['best_b']}")
    print()
    
    # Frequency analysis attack
    print("2. Frequency Analysis Attack:")
    long_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    affine2 = AffineCipher(a=7, b=11)
    encrypted2 = affine2.encode(long_message)
    
    analysis = AffineCipher.attack(
        AttackMethod.FREQUENCY_ANALYSIS,
        ciphertext=encrypted2
    )
    
    print(f"   Original: {long_message}")
    print(f"   Key: a={affine2.a}, b={affine2.b}")
    print(f"   Encrypted: {encrypted2}")
    print(f"   Recovered key: a={analysis['most_likely_a']}, b={analysis['most_likely_b']}")
    print(f"   Decrypted: {analysis['decrypted_text']}")
    print(f"   Confidence score: {analysis['confidence_score']:.2f}")
    print()
    
    # Known plaintext attack
    print("3. Known Plaintext Attack:")
    known_plain = "HELLO"
    affine3 = AffineCipher(a=3, b=7)
    known_cipher = affine3.encode(known_plain)
    
    recovered_key = AffineCipher.attack(
        AttackMethod.KNOWN_PLAINTEXT,
        plaintext=known_plain,
        ciphertext=known_cipher
    )
    
    print(f"   Known plaintext: {known_plain}")
    print(f"   Known ciphertext: {known_cipher}")
    print(f"   Original key: a={affine3.a}, b={affine3.b}")
    if recovered_key:
        print(f"   Recovered key: a={recovered_key['a']}, b={recovered_key['b']}")
        print(f"   Success: {recovered_key['a'] == affine3.a and recovered_key['b'] == affine3.b}")
    else:
        print("   Attack failed")
    print()


def demo_validation():
    """Demonstrate parameter validation."""
    print("=== Affine Cipher Parameter Validation ===\n")
    
    # Test valid parameters
    print("Valid parameters:")
    try:
        valid = AffineCipher(a=5, b=8)
        print(f"  a=5, b=8: ✓ Valid")
    except ValueError as e:
        print(f"  a=5, b=8: ✗ {e}")
    
    try:
        valid2 = AffineCipher(a=3, b=0)
        print(f"  a=3, b=0: ✓ Valid")
    except ValueError as e:
        print(f"  a=3, b=0: ✗ {e}")
    
    print()
    print("Invalid parameters:")
    
    # Test invalid a values
    try:
        AffineCipher(a=2, b=8)  # Not coprime with 26
        print("  a=2, b=8: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=2, b=8: ✓ {e}")
    
    try:
        AffineCipher(a=0, b=8)  # Invalid range
        print("  a=0, b=8: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=0, b=8: ✓ {e}")
    
    try:
        AffineCipher(a=26, b=8)  # Invalid range
        print("  a=26, b=8: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=26, b=8: ✓ {e}")
    
    # Test invalid b values
    try:
        AffineCipher(a=5, b=-1)  # Invalid range
        print("  a=5, b=-1: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=5, b=-1: ✓ {e}")
    
    try:
        AffineCipher(a=5, b=26)  # Invalid range
        print("  a=5, b=26: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=5, b=26: ✓ {e}")
    
    # Test missing parameters
    try:
        AffineCipher(a=5)  # Missing b
        print("  a=5: ✗ Should have failed")
    except ValueError as e:
        print(f"  a=5: ✓ {e}")
    
    try:
        AffineCipher(b=8)  # Missing a
        print("  b=8: ✗ Should have failed")
    except ValueError as e:
        print(f"  b=8: ✓ {e}")
    
    print()


def demo_case_preservation():
    """Demonstrate case preservation."""
    print("=== Affine Cipher Case Preservation ===\n")
    
    affine = AffineCipher(a=7, b=11)
    mixed_case = "Hello World! 123"
    
    encrypted = affine.encode(mixed_case)
    decrypted = affine.decode(encrypted)
    
    print(f"Original: {mixed_case}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Case preserved: {mixed_case == decrypted}")
    print()


if __name__ == "__main__":
    demo_basic_usage()
    demo_key_generation()
    demo_attack_methods()
    demo_validation()
    demo_case_preservation() 