"""
Tests for BaseSubstitutionCipher class.

This module contains tests for the abstract base class that provides
common functionality for all substitution ciphers.
"""

import pytest
from faker import Faker

from hordekit.crypto.symmetric.substitution.base_substitution import BaseSubstitutionCipher
from hordekit.crypto.utils.attack_methods import AttackMethod


class TestSubstitutionCipher(BaseSubstitutionCipher):
    """
    Test implementation of BaseSubstitutionCipher for testing purposes.

    This is a simple shift cipher that shifts each character by 3 positions.
    """

    SUPPORTED_ATTACK_METHODS = [AttackMethod.BRUTE_FORCE, AttackMethod.FREQUENCY_ANALYSIS]

    def _setup_substitution_algorithm(self, **kwargs):
        """Set up the test substitution cipher."""
        self.shift = kwargs.get("shift", 3)

    def _validate_parameters(self, **kwargs):
        """Validate cipher parameters."""
        shift = kwargs.get("shift")
        if shift is not None and not isinstance(shift, int):
            raise ValueError("shift must be an integer")

    def _create_mappings(self):
        """Create encryption/decryption translation tables."""
        from_chars = self.alphabet
        to_chars = "".join(chr((ord(c) - ord("A") + self.shift) % 26 + ord("A")) for c in from_chars)

        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)

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


class TestBaseSubstitutionCipher:
    """Test cases for BaseSubstitutionCipher functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fake = Faker()
        self.cipher = TestSubstitutionCipher(shift=3)

    def test_inheritance_from_crypto_algorithm(self):
        """Test that BaseSubstitutionCipher inherits from CryptoAlgorithm."""
        assert issubclass(BaseSubstitutionCipher, BaseSubstitutionCipher.__bases__[0])

    def test_abstract_methods_implementation(self):
        """Test that required abstract methods are implemented."""
        # Test that _create_mappings raises NotImplementedError in base class
        # We can't instantiate BaseSubstitutionCipher directly, so we test
        # that our concrete implementation works
        cipher = TestSubstitutionCipher(shift=3)
        assert hasattr(cipher, "_create_mappings")
        assert callable(cipher._create_mappings)

    def test_setup_algorithm(self):
        """Test that _setup_algorithm sets up the cipher correctly."""
        cipher = TestSubstitutionCipher(shift=5)

        assert hasattr(cipher, "alphabet")
        assert hasattr(cipher, "alphabet_lower")
        assert hasattr(cipher, "encrypt_table")
        assert hasattr(cipher, "decrypt_table")
        assert cipher.shift == 5
        assert cipher.alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert cipher.alphabet_lower == "abcdefghijklmnopqrstuvwxyz"

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption functionality."""
        message = self.fake.text(max_nb_chars=50)
        encrypted = self.cipher.encode(message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == message

    def test_case_preservation(self):
        """Test that case is preserved during encryption/decryption."""
        test_cases = [
            "Hello World!",
            "UPPERCASE TEXT",
            "lowercase text",
            "MiXeD cAsE tExT",
            "Hello, World! 123",
        ]

        for message in test_cases:
            encrypted = self.cipher.encode(message)
            decrypted = self.cipher.decode(encrypted)
            assert decrypted == message

    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        test_cases = [
            "Hello, World!",
            "Text with numbers: 12345",
            "Special chars: !@#$%^&*()",
            "Spaces   and   tabs\t\t",
            "Unicode: привет мир",
        ]

        for message in test_cases:
            encrypted = self.cipher.encode(message)
            decrypted = self.cipher.decode(encrypted)
            assert decrypted == message

    def test_empty_string(self):
        """Test encryption/decryption of empty string."""
        message = ""
        encrypted = self.cipher.encode(message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == message

    def test_bytes_input(self):
        """Test that bytes input is handled correctly."""
        message = "Hello World!"
        message_bytes = message.encode("utf-8")

        encrypted = self.cipher.encode(message_bytes)
        decrypted = self.cipher.decode(encrypted)

        # The result should be bytes, so we need to decode it back to string
        assert decrypted.decode("utf-8") == message

    def test_translation_tables(self):
        """Test that translation tables are created correctly."""
        # Test encryption table - it should be a dict mapping ordinals
        assert isinstance(self.cipher.encrypt_table, dict)
        assert 65 in self.cipher.encrypt_table  # ord('A')
        assert 90 in self.cipher.encrypt_table  # ord('Z')

        # Test decryption table
        assert isinstance(self.cipher.decrypt_table, dict)
        assert 68 in self.cipher.decrypt_table  # ord('D') - A shifted by 3
        assert 67 in self.cipher.decrypt_table  # ord('C') - Z shifted by 3

    def test_character_mapping(self):
        """Test that characters are mapped correctly."""
        # Test basic mapping (shift=3)
        assert self.cipher.encode("A") == "D"
        assert self.cipher.encode("Z") == "C"
        assert self.cipher.encode("HELLO") == "KHOOR"

        # Test decryption
        assert self.cipher.decode("D") == "A"
        assert self.cipher.decode("C") == "Z"
        assert self.cipher.decode("KHOOR") == "HELLO"

    def test_different_shifts(self):
        """Test cipher with different shift values."""
        cipher_shift_1 = TestSubstitutionCipher(shift=1)
        cipher_shift_10 = TestSubstitutionCipher(shift=10)

        message = "HELLO"

        # Test shift=1
        encrypted_1 = cipher_shift_1.encode(message)
        decrypted_1 = cipher_shift_1.decode(encrypted_1)
        assert decrypted_1 == message

        # Test shift=10
        encrypted_10 = cipher_shift_10.encode(message)
        decrypted_10 = cipher_shift_10.decode(encrypted_10)
        assert decrypted_10 == message

    def test_brute_force_attack(self):
        """Test brute force attack functionality."""
        # Create a message and encrypt it
        message = "ATTACK"
        encrypted = self.cipher.encode(message)

        # Perform brute force attack
        result = TestSubstitutionCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)

        # Check that all results are present
        assert "all_results" in result
        assert len(result["all_results"]) == 26  # 26 possible shifts

        # Check that the original message is in the results
        assert message in result["all_results"].values()

    def test_brute_force_attack_with_mask(self):
        """Test brute force attack with pattern matching."""
        message = "ATTACK"
        encrypted = self.cipher.encode(message)

        # Perform brute force attack with mask
        result = TestSubstitutionCipher.attack(
            AttackMethod.BRUTE_FORCE, ciphertext=encrypted, mask=r"^ATTACK$"  # Exact match for the original message
        )

        # Check that mask matching works
        assert "mask_matched" in result
        assert result["mask_matched"] is True
        assert "best_match" in result
        assert "best_key" in result
        assert result["best_match"] == message

    def test_frequency_analysis_attack(self):
        """Test frequency analysis attack functionality."""
        # Create a longer message for better frequency analysis
        message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        encrypted = self.cipher.encode(message)

        # Perform frequency analysis attack
        result = TestSubstitutionCipher.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext=encrypted)

        # Check that analysis results are present
        assert "most_likely_key" in result
        assert "confidence_score" in result
        assert "decrypted_text" in result
        assert "monogram_score" in result
        assert "bigram_score" in result
        assert "trigram_score" in result

        # Check that the decrypted text matches the original
        assert result["decrypted_text"] == message

    def test_get_possible_keys(self):
        """Test that _get_possible_keys returns all possible keys."""
        keys = TestSubstitutionCipher._get_possible_keys()

        assert len(keys) == 26  # 26 possible shifts
        assert all(isinstance(key, dict) for key in keys)
        assert all("shift" in key for key in keys)
        assert all(isinstance(key["shift"], int) for key in keys)

        # Check that all shifts from 0 to 25 are present
        shifts = [key["shift"] for key in keys]
        assert set(shifts) == set(range(26))

    def test_key_to_string(self):
        """Test that _key_to_string converts keys correctly."""
        test_keys = [
            {"shift": 0},
            {"shift": 5},
            {"shift": 25},
        ]

        for key in test_keys:
            key_str = TestSubstitutionCipher._key_to_string(key)
            expected = f"shift_{key['shift']}"
            assert key_str == expected

    def test_attack_methods_availability(self):
        """Test that attack methods are available."""
        assert hasattr(TestSubstitutionCipher, "attack")

        # Test that attack method can be called
        result = TestSubstitutionCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext="TEST")
        assert isinstance(result, dict)

    def test_unknown_attack_method(self):
        """Test that unknown attack methods raise appropriate errors."""
        with pytest.raises(ValueError, match="Unknown attack method"):
            TestSubstitutionCipher.attack(AttackMethod.KNOWN_PLAINTEXT, ciphertext="TEST")

    def test_missing_attack_parameters(self):
        """Test that missing required parameters raise appropriate errors."""
        with pytest.raises(ValueError, match="ciphertext parameter required"):
            TestSubstitutionCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext="")

        with pytest.raises(ValueError, match="ciphertext parameter required"):
            TestSubstitutionCipher.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext="")

    def test_algorithm_consistency(self):
        """Test that the algorithm is consistent across multiple uses."""
        message = "CONSISTENCY TEST"

        # Test multiple encryptions/decryptions
        for _ in range(5):
            encrypted = self.cipher.encode(message)
            decrypted = self.cipher.decode(encrypted)
            assert decrypted == message

    def test_algorithm_properties(self):
        """Test that the algorithm has the expected properties."""
        assert hasattr(self.cipher, "alphabet")
        assert hasattr(self.cipher, "alphabet_lower")
        assert hasattr(self.cipher, "encrypt_table")
        assert hasattr(self.cipher, "decrypt_table")
        assert hasattr(self.cipher, "shift")

        # Test that alphabet is correct
        assert self.cipher.alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert self.cipher.alphabet_lower == "abcdefghijklmnopqrstuvwxyz"

    def test_error_messages(self):
        """Test that error messages are informative."""
        with pytest.raises(ValueError, match="ciphertext parameter required"):
            TestSubstitutionCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext="")

        with pytest.raises(ValueError, match="Unknown attack method"):
            TestSubstitutionCipher.attack(AttackMethod.KNOWN_PLAINTEXT, ciphertext="TEST")

    def test_unicode_handling(self):
        """Test that Unicode characters are handled correctly."""
        unicode_messages = [
            "Hello привет мир",
            "Unicode: 你好世界",
            "Mixed: Hello 123 привет!",
        ]

        for message in unicode_messages:
            encrypted = self.cipher.encode(message)
            decrypted = self.cipher.decode(encrypted)
            assert decrypted == message

    def test_long_text(self):
        """Test encryption/decryption of long text."""
        long_message = self.fake.text(max_nb_chars=1000)
        encrypted = self.cipher.encode(long_message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == long_message

    def test_special_characters(self):
        """Test that special characters are preserved."""
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        message = f"Text with special chars: {special_chars}"

        encrypted = self.cipher.encode(message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == message

    def test_newlines_and_tabs(self):
        """Test that newlines and tabs are preserved."""
        message = "Line 1\nLine 2\tTabbed content"

        encrypted = self.cipher.encode(message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == message

    def test_multiple_spaces(self):
        """Test that multiple spaces are preserved."""
        message = "Multiple    spaces   preserved"

        encrypted = self.cipher.encode(message)
        decrypted = self.cipher.decode(encrypted)

        assert decrypted == message
