#!/usr/bin/env python3
"""
Tests for ROT13 Cipher implementation.
"""

import pytest

from hordekit.crypto.symmetric.substitution.rot13 import ROT13Cipher
from tests.base_crypto_test import BaseCryptoTest


class TestROT13Cipher(BaseCryptoTest):
    """Test cases for ROT13 Cipher implementation."""

    algorithm_class = ROT13Cipher
    valid_parameters = {}
    invalid_parameters = [
        {"invalid_param": "value"},  # Invalid parameter
    ]

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        message = "ROT13"
        rot13 = ROT13Cipher()

        encrypted = rot13.encode(message)
        decrypted = rot13.decode(encrypted)

        assert decrypted == message
        assert encrypted == "EBG13"

    def test_case_preservation(self):
        """Test that case is preserved during encryption/decryption."""
        message = "RoT13"
        rot13 = ROT13Cipher()

        encrypted = rot13.encode(message)
        decrypted = rot13.decode(encrypted)

        assert decrypted == message
        assert encrypted == "EbG13"

    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        message = "ROT13!@#"
        rot13 = ROT13Cipher()

        encrypted = rot13.encode(message)
        decrypted = rot13.decode(encrypted)

        assert decrypted == message
        assert encrypted == "EBG13!@#"

    def test_rot13_symmetry(self):
        """Test that ROT13 is its own inverse."""
        message = "CRYPTOGRAPHY"
        rot13 = ROT13Cipher()

        # Apply ROT13 twice should return the original
        once = rot13.encode(message)
        twice = rot13.encode(once)

        assert twice == message

    def test_alphabet_mapping(self):
        """Test the complete alphabet mapping."""
        rot13 = ROT13Cipher()

        # Test uppercase alphabet
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        expected_uppercase = "NOPQRSTUVWXYZABCDEFGHIJKLM"

        encrypted = rot13.encode(uppercase)
        assert encrypted == expected_uppercase

        decrypted = rot13.decode(encrypted)
        assert decrypted == uppercase

    def test_lowercase_alphabet_mapping(self):
        """Test the complete lowercase alphabet mapping."""
        rot13 = ROT13Cipher()

        # Test lowercase alphabet
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        expected_lowercase = "nopqrstuvwxyzabcdefghijklm"

        encrypted = rot13.encode(lowercase)
        assert encrypted == expected_lowercase

        decrypted = rot13.decode(encrypted)
        assert decrypted == lowercase

    def test_parameter_validation(self):
        """Test parameter validation for ROT13 cipher."""
        # ROT13 cipher doesn't require any parameters
        # It should work with no parameters
        rot13 = ROT13Cipher()
        assert rot13 is not None

        # It should also work with any parameters (they will be ignored)
        rot132 = ROT13Cipher(invalid_param="value")
        assert rot132 is not None

    def test_error_messages(self):
        """Test error messages for ROT13 cipher."""
        # ROT13 cipher doesn't raise errors for invalid parameters
        # It ignores them instead
        rot13 = ROT13Cipher(invalid_param="value")
        assert rot13 is not None

    def test_attack_methods_availability(self):
        """Test that ROT13 cipher has no attack methods."""
        # ROT13 has no variability, so no attack methods should be available
        methods = self.algorithm_class.SUPPORTED_ATTACK_METHODS
        assert len(methods) == 0

    def test_unknown_attack_method(self):
        """Test that ROT13 cipher doesn't support any attack methods."""
        # ROT13 has no attack methods, so any attack method should fail
        from hordekit.crypto.utils import AttackMethod

        with pytest.raises(ValueError):
            self.algorithm.attack(AttackMethod.BRUTE_FORCE)  # type: ignore

    def test_missing_attack_parameters(self):
        """Test that ROT13 cipher doesn't support attack methods."""
        # ROT13 has no attack methods, so this test doesn't apply

    def test_inheritance_from_caesar(self):
        """Test that ROT13 inherits from CaesarCipher."""
        from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

        rot13 = ROT13Cipher()
        assert isinstance(rot13, CaesarCipher)
        assert rot13.shift == 13

    def test_fixed_shift_value(self):
        """Test that ROT13 always uses shift=13."""
        rot13 = ROT13Cipher()
        assert rot13.shift == 13

        # Even if we try to pass a different shift, it should be ignored
        rot13_ignored = ROT13Cipher(shift=5)
        assert rot13_ignored.shift == 13
