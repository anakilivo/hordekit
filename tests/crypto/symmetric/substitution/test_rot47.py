#!/usr/bin/env python3
"""
Tests for ROT47 Cipher implementation.
"""

import pytest

from hordekit.crypto.symmetric.substitution.rot47 import ROT47Cipher
from tests.base_crypto_test import BaseCryptoTest


class TestROT47Cipher(BaseCryptoTest):
    """Test cases for ROT47 Cipher implementation."""

    algorithm_class = ROT47Cipher
    valid_parameters = {}
    invalid_parameters = [
        {"invalid_param": "value"},  # Invalid parameter
    ]

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        message = "ROT47!@#"
        rot47 = ROT47Cipher()

        encrypted = rot47.encode(message)
        decrypted = rot47.decode(encrypted)

        assert decrypted == message
        # ROT47 transforms: R→+, O→~, T→%, 4→c, 7→f, !→P, @→o, #→R
        assert encrypted == "#~%cfPoR"

    def test_ascii_character_mapping(self):
        """Test that all printable ASCII characters are mapped correctly."""
        rot47 = ROT47Cipher()

        # Test some key ASCII mappings
        test_cases = [
            ("!", "P"),
            ("A", "p"),
            ("Z", "+"),
            ("a", "2"),
            ("z", "K"),
            ("0", "_"),
            ("9", "h"),
            ("~", "O"),
        ]

        for original, expected in test_cases:
            encrypted = rot47.encode(original)
            assert encrypted == expected, f"Failed for '{original}' -> expected '{expected}', got '{encrypted}'"

            decrypted = rot47.decode(encrypted)
            assert decrypted == original, f"Failed for '{encrypted}' -> expected '{original}', got '{decrypted}'"

    def test_rot47_symmetry(self):
        """Test that ROT47 is its own inverse."""
        message = "CRYPTOGRAPHY!@#"
        rot47 = ROT47Cipher()

        # Apply ROT47 twice should return the original
        once = rot47.encode(message)
        twice = rot47.encode(once)

        assert twice == message

    def test_full_ascii_range(self):
        """Test the complete printable ASCII range (33-126)."""
        rot47 = ROT47Cipher()

        # Test the full range
        for i in range(33, 127):
            char = chr(i)
            encrypted = rot47.encode(char)
            decrypted = rot47.decode(encrypted)

            assert decrypted == char, f"Failed for ASCII {i} ('{char}')"

    def test_mixed_content(self):
        """Test mixed content with letters, numbers, and symbols."""
        rot47 = ROT47Cipher()

        message = "Hello, World! 123 @#$%"
        encrypted = rot47.encode(message)
        decrypted = rot47.decode(encrypted)

        assert decrypted == message
        # Verify some specific transformations
        assert encrypted != message  # Should be different

    def test_parameter_validation(self):
        """Test parameter validation for ROT47 cipher."""
        # ROT47 cipher doesn't require any parameters
        # It should work with no parameters
        rot47 = ROT47Cipher()
        assert rot47 is not None

        # It should also work with any parameters (they will be ignored)
        rot472 = ROT47Cipher(invalid_param="value")
        assert rot472 is not None

    def test_error_messages(self):
        """Test error messages for ROT47 cipher."""
        # ROT47 cipher doesn't raise errors for invalid parameters
        # It ignores them instead
        rot47 = ROT47Cipher(invalid_param="value")
        assert rot47 is not None

    def test_attack_methods_availability(self):
        """Test that ROT47 cipher has no attack methods."""
        # ROT47 has no variability, so no attack methods should be available
        methods = self.algorithm_class.SUPPORTED_ATTACK_METHODS
        assert len(methods) == 0

    def test_unknown_attack_method(self):
        """Test that ROT47 cipher doesn't support any attack methods."""
        # ROT47 has no attack methods, so any attack method should fail
        from hordekit.crypto.utils import AttackMethod

        with pytest.raises(ValueError):
            self.algorithm.attack(AttackMethod.BRUTE_FORCE)  # type: ignore

    def test_missing_attack_parameters(self):
        """Test that ROT47 cipher doesn't support attack methods."""
        # ROT47 has no attack methods, so this test doesn't apply

    def test_inheritance_from_caesar(self):
        """Test that ROT47 inherits from CryptoAlgorithm."""
        from hordekit.crypto.utils import CryptoAlgorithm

        rot47 = ROT47Cipher()
        assert isinstance(rot47, CryptoAlgorithm)
        # ROT47 no longer inherits from CaesarCipher, it's a standalone implementation

    def test_fixed_shift_value(self):
        """Test that ROT47 is a fixed algorithm without shift."""
        rot47 = ROT47Cipher()
        # ROT47 doesn't have a shift attribute anymore
        assert hasattr(rot47, "alphabet")
        assert len(rot47.alphabet) == 94  # 94 printable ASCII characters

    def test_ascii_alphabet(self):
        """Test that ROT47 uses the correct ASCII alphabet."""
        rot47 = ROT47Cipher()

        # Should contain all printable ASCII characters (33-126)
        expected_length = 126 - 33 + 1  # 94 characters
        assert len(rot47.alphabet) == expected_length

        # Should start with '!' (ASCII 33) and end with '~' (ASCII 126)
        assert rot47.alphabet[0] == "!"
        assert rot47.alphabet[-1] == "~"

    def test_non_printable_ascii(self):
        """Test that non-printable ASCII characters are preserved."""
        rot47 = ROT47Cipher()

        # Test control characters (should be preserved)
        message = "Hello\x00\x01\x02World"
        encrypted = rot47.encode(message)
        decrypted = rot47.decode(encrypted)

        assert decrypted == message

    def test_unicode_characters(self):
        """Test that Unicode characters are preserved."""
        rot47 = ROT47Cipher()

        # Test Unicode characters (should be preserved)
        message = "Hello 世界 🌍"
        encrypted = rot47.encode(message)
        decrypted = rot47.decode(encrypted)

        assert decrypted == message
