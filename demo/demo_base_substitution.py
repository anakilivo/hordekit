#!/usr/bin/env python3
"""
Demonstration of BaseSubstitutionCipher functionality.

This script shows how to use the BaseSubstitutionCipher class to create
custom substitution ciphers and demonstrates its features.
"""

from hordekit.crypto.symmetric.substitution.base_substitution import BaseSubstitutionCipher
from hordekit.crypto.utils.attack_methods import AttackMethod


class SimpleShiftCipher(BaseSubstitutionCipher):
    """
    Simple shift cipher implementation using BaseSubstitutionCipher.
    
    This is a basic Caesar-like cipher that shifts each character by a fixed amount.
    """
    
    SUPPORTED_ATTACK_METHODS = [AttackMethod.BRUTE_FORCE, AttackMethod.FREQUENCY_ANALYSIS]
    
    def _setup_substitution_algorithm(self, **kwargs):
        """Set up the simple shift cipher."""
        self.shift = kwargs.get('shift', 3)
        print(f"Setting up SimpleShiftCipher with shift={self.shift}")
    
    def _validate_parameters(self, **kwargs):
        """Validate cipher parameters."""
        shift = kwargs.get('shift')
        if shift is not None and not isinstance(shift, int):
            raise ValueError("shift must be an integer")
    
    def _create_mappings(self):
        """Create encryption/decryption translation tables."""
        from_chars = self.alphabet
        to_chars = "".join(chr((ord(c) - ord('A') + self.shift) % 26 + ord('A')) 
                           for c in from_chars)
        
        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)
        
        print(f"Created translation tables for shift={self.shift}")
    
    @classmethod
    def generate_key(cls):
        """Generate a random key for this cipher."""
        import secrets
        return cls(shift=secrets.randbelow(26))
    
    @classmethod
    def _get_possible_keys(cls):
        """Get all possible keys for this cipher."""
        return [{"shift": i} for i in range(26)]
    
    @classmethod
    def _key_to_string(cls, key):
        """Convert key dictionary to string representation."""
        return f"shift_{key.get('shift', 0)}"


class CustomAlphabetCipher(BaseSubstitutionCipher):
    """
    Custom alphabet cipher implementation using BaseSubstitutionCipher.
    
    This cipher uses a custom alphabet and reverses it for encryption.
    """
    
    SUPPORTED_ATTACK_METHODS = [AttackMethod.BRUTE_FORCE]
    
    def _setup_substitution_algorithm(self, **kwargs):
        """Set up the custom alphabet cipher."""
        self.custom_alphabet = kwargs.get('alphabet', "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.alphabet = self.custom_alphabet
        self.alphabet_lower = self.alphabet.lower()
        print(f"Setting up CustomAlphabetCipher with alphabet: {self.alphabet}")
    
    def _validate_parameters(self, **kwargs):
        """Validate cipher parameters."""
        alphabet = kwargs.get('alphabet')
        if alphabet is not None and not isinstance(alphabet, str):
            raise ValueError("alphabet must be a string")
    
    def _create_mappings(self):
        """Create encryption/decryption translation tables."""
        from_chars = self.alphabet
        to_chars = self.alphabet[::-1]  # Reverse the alphabet
        
        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)
        
        print(f"Created reverse alphabet mapping")
    
    @classmethod
    def generate_key(cls):
        """Generate a random key for this cipher."""
        return cls(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    @classmethod
    def _get_possible_keys(cls):
        """Get all possible keys for this cipher."""
        return [{"alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}]
    
    @classmethod
    def _key_to_string(cls, key):
        """Convert key dictionary to string representation."""
        return f"alphabet_{key.get('alphabet', 'unknown')}"


def demo_basic_functionality():
    """Demonstrate basic encryption/decryption functionality."""
    print("\n" + "="*60)
    print("DEMO: Basic Functionality")
    print("="*60)
    
    # Create a simple shift cipher
    cipher = SimpleShiftCipher(shift=5)
    
    # Test messages
    messages = [
        "HELLO WORLD",
        "Hello, World!",
        "UPPERCASE TEXT",
        "lowercase text",
        "MiXeD cAsE tExT",
        "Text with numbers: 12345",
        "Special chars: !@#$%^&*()",
    ]
    
    for message in messages:
        print(f"\nOriginal: {message}")
        encrypted = cipher.encode(message)
        print(f"Encrypted: {encrypted}")
        decrypted = cipher.decode(encrypted)
        print(f"Decrypted: {decrypted}")
        print(f"Match: {decrypted == message}")


def demo_case_preservation():
    """Demonstrate case preservation functionality."""
    print("\n" + "="*60)
    print("DEMO: Case Preservation")
    print("="*60)
    
    cipher = SimpleShiftCipher(shift=3)
    
    test_cases = [
        ("A", "D"),
        ("Z", "C"),
        ("a", "a"),  # Lowercase preserved as-is
        ("z", "z"),
        ("Hello World!", "Hello World!"),  # Case preserved
    ]
    
    for original, expected in test_cases:
        encrypted = cipher.encode(original)
        print(f"'{original}' -> '{encrypted}' (expected: '{expected}')")


def demo_non_alphabetic_preservation():
    """Demonstrate non-alphabetic character preservation."""
    print("\n" + "="*60)
    print("DEMO: Non-alphabetic Character Preservation")
    print("="*60)
    
    cipher = SimpleShiftCipher(shift=3)
    
    test_cases = [
        "Hello, World!",
        "Text with numbers: 12345",
        "Special chars: !@#$%^&*()",
        "Spaces   and   tabs\t\t",
        "Unicode: привет мир",
    ]
    
    for message in test_cases:
        encrypted = cipher.encode(message)
        decrypted = cipher.decode(encrypted)
        print(f"Original: {message}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Preserved: {decrypted == message}\n")


def demo_brute_force_attack():
    """Demonstrate brute force attack functionality."""
    print("\n" + "="*60)
    print("DEMO: Brute Force Attack")
    print("="*60)
    
    # Create a message and encrypt it with an unknown shift
    original_message = "ATTACK AT DAWN"
    unknown_shift = 7
    cipher = SimpleShiftCipher(shift=unknown_shift)
    encrypted = cipher.encode(original_message)
    
    print(f"Original message: {original_message}")
    print(f"Encrypted with shift={unknown_shift}: {encrypted}")
    print(f"Unknown shift value to attacker")
    
    # Perform brute force attack
    print("\nPerforming brute force attack...")
    result = SimpleShiftCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)
    
    print(f"Found {len(result['all_results'])} possible decryptions")
    
    # Find the correct decryption
    for key, decrypted in result['all_results'].items():
        if decrypted == original_message:
            print(f"Correct key found: {key}")
            print(f"Correct decryption: {decrypted}")
            break


def demo_brute_force_with_mask():
    """Demonstrate brute force attack with pattern matching."""
    print("\n" + "="*60)
    print("DEMO: Brute Force Attack with Pattern Matching")
    print("="*60)
    
    # Create a message and encrypt it
    original_message = "ATTACK"
    cipher = SimpleShiftCipher(shift=5)
    encrypted = cipher.encode(original_message)
    
    print(f"Original message: {original_message}")
    print(f"Encrypted: {encrypted}")
    
    # Perform brute force attack with mask
    print("\nPerforming brute force attack with pattern matching...")
    result = SimpleShiftCipher.attack(
        AttackMethod.BRUTE_FORCE, 
        ciphertext=encrypted, 
        mask=r"^[A-Z]+$"  # Only uppercase letters
    )
    
    if result.get("mask_matched"):
        print(f"Pattern matched!")
        print(f"Best match: {result['best_match']}")
        print(f"Best key: {result['best_key']}")
    else:
        print("No pattern match found")


def demo_frequency_analysis():
    """Demonstrate frequency analysis attack."""
    print("\n" + "="*60)
    print("DEMO: Frequency Analysis Attack")
    print("="*60)
    
    # Create a longer message for better frequency analysis
    original_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    cipher = SimpleShiftCipher(shift=10)
    encrypted = cipher.encode(original_message)
    
    print(f"Original message: {original_message}")
    print(f"Encrypted with shift=10: {encrypted}")
    
    # Perform frequency analysis attack
    print("\nPerforming frequency analysis attack...")
    result = SimpleShiftCipher.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext=encrypted)
    
    print(f"Most likely key: {result['most_likely_key']}")
    print(f"Decrypted text: {result['decrypted_text']}")
    print(f"Confidence score: {result['confidence_score']:.2f}")
    print(f"Monogram score: {result['monogram_score']:.2f}")
    print(f"Bigram score: {result['bigram_score']:.2f}")
    print(f"Trigram score: {result['trigram_score']:.2f}")
    print(f"Correct: {result['decrypted_text'] == original_message}")


def demo_custom_alphabet_cipher():
    """Demonstrate custom alphabet cipher."""
    print("\n" + "="*60)
    print("DEMO: Custom Alphabet Cipher")
    print("="*60)
    
    # Create a custom alphabet cipher
    cipher = CustomAlphabetCipher(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    test_messages = [
        "HELLO",
        "WORLD",
        "CRYPTOGRAPHY",
    ]
    
    for message in test_messages:
        print(f"\nOriginal: {message}")
        encrypted = cipher.encode(message)
        print(f"Encrypted: {encrypted}")
        decrypted = cipher.decode(encrypted)
        print(f"Decrypted: {decrypted}")
        print(f"Match: {decrypted == message}")


def demo_different_shifts():
    """Demonstrate cipher with different shift values."""
    print("\n" + "="*60)
    print("DEMO: Different Shift Values")
    print("="*60)
    
    message = "HELLO"
    shifts = [1, 5, 13, 25]
    
    for shift in shifts:
        cipher = SimpleShiftCipher(shift=shift)
        encrypted = cipher.encode(message)
        decrypted = cipher.decode(encrypted)
        
        print(f"Shift {shift:2d}: '{message}' -> '{encrypted}' -> '{decrypted}'")


def demo_error_handling():
    """Demonstrate error handling."""
    print("\n" + "="*60)
    print("DEMO: Error Handling")
    print("="*60)
    
    # Test unknown attack method
    try:
        SimpleShiftCipher.attack(AttackMethod.KNOWN_PLAINTEXT, ciphertext="TEST")
    except ValueError as e:
        print(f"Unknown attack method error: {e}")
    
    # Test missing parameters
    try:
        SimpleShiftCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext="")
    except ValueError as e:
        print(f"Missing parameters error: {e}")
    
    # Test empty string
    cipher = SimpleShiftCipher(shift=3)
    empty_result = cipher.encode("")
    print(f"Empty string encryption: '{empty_result}'")


def demo_unicode_handling():
    """Demonstrate Unicode character handling."""
    print("\n" + "="*60)
    print("DEMO: Unicode Character Handling")
    print("="*60)
    
    cipher = SimpleShiftCipher(shift=3)
    
    unicode_messages = [
        "Hello привет мир",
        "Unicode: 你好世界",
        "Mixed: Hello 123 привет!",
    ]
    
    for message in unicode_messages:
        encrypted = cipher.encode(message)
        decrypted = cipher.decode(encrypted)
        print(f"Original: {message}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Preserved: {decrypted == message}\n")


def main():
    """Run all demonstrations."""
    print("BaseSubstitutionCipher Demonstration")
    print("="*60)
    print("This demo shows how to use the BaseSubstitutionCipher class")
    print("to create custom substitution ciphers with built-in features.")
    
    # Run all demos
    demo_basic_functionality()
    demo_case_preservation()
    demo_non_alphabetic_preservation()
    demo_brute_force_attack()
    demo_brute_force_with_mask()
    demo_frequency_analysis()
    demo_custom_alphabet_cipher()
    demo_different_shifts()
    demo_error_handling()
    demo_unicode_handling()
    
    print("\n" + "="*60)
    print("Demonstration Complete!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Basic encryption/decryption")
    print("- Case preservation")
    print("- Non-alphabetic character preservation")
    print("- Brute force attacks")
    print("- Frequency analysis attacks")
    print("- Custom alphabet support")
    print("- Error handling")
    print("- Unicode support")


if __name__ == "__main__":
    main() 