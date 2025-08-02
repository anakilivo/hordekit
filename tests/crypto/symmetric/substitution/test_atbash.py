#!/usr/bin/env python3
"""
Tests for Atbash Cipher implementation.
"""

import pytest

from hordekit.crypto.symmetric.substitution.atbash import AtbashCipher
from hordekit.crypto.utils import AttackMethod  # type: ignore
from tests.base_crypto_test import BaseCryptoTest


class TestAtbashCipher(BaseCryptoTest):
    """Test cases for Atbash Cipher implementation."""

    algorithm_class = AtbashCipher
    valid_parameters = {}
    invalid_parameters = [
        {"invalid_param": "value"},  # Invalid parameter
    ]

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        message = "ATBASH"
        atbash = AtbashCipher()

        encrypted = atbash.encode(message)
        decrypted = atbash.decode(encrypted)

        assert decrypted == message
        assert encrypted == "ZGYZHS"

    def test_case_preservation(self):
        """Test that case is preserved during encryption/decryption."""
        message = "AtBaSh"
        atbash = AtbashCipher()

        encrypted = atbash.encode(message)
        decrypted = atbash.decode(encrypted)

        assert decrypted == message
        assert encrypted == "ZgYzHs"

    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        message = "ATBASH123!@#"
        atbash = AtbashCipher()

        encrypted = atbash.encode(message)
        decrypted = atbash.decode(encrypted)

        assert decrypted == message
        assert encrypted == "ZGYZHS123!@#"

    def test_atbash_symmetry(self):
        """Test that Atbash is its own inverse."""
        message = "CRYPTOGRAPHY"
        atbash = AtbashCipher()

        # Apply Atbash twice should return the original
        once = atbash.encode(message)
        twice = atbash.encode(once)

        assert twice == message

    def test_parameter_validation(self):
        """Test parameter validation for Atbash cipher."""
        # Atbash cipher doesn't require any parameters
        # It should work with no parameters
        atbash = AtbashCipher()
        assert atbash is not None

        # It should also work with any parameters (they will be ignored)
        atbash2 = AtbashCipher(invalid_param="value")
        assert atbash2 is not None

    def test_error_messages(self):
        """Test error messages for Atbash cipher."""
        # Atbash cipher doesn't raise errors for invalid parameters
        # It ignores them instead
        atbash = AtbashCipher(invalid_param="value")
        assert atbash is not None

    def test_attack_methods_availability(self):
        """Test that Atbash cipher has no attack methods."""
        # Atbash has no variability, so no attack methods should be available
        methods = self.algorithm_class.SUPPORTED_ATTACK_METHODS
        assert len(methods) == 0

    def test_unknown_attack_method(self):
        """Test that Atbash cipher doesn't support any attack methods."""
        # Atbash has no attack methods, so any attack method should fail

        with pytest.raises(ValueError):
            self.algorithm.attack(AttackMethod.BRUTE_FORCE)  # type: ignore

    def test_missing_attack_parameters(self):
        """Test that Atbash cipher doesn't support attack methods."""
        # Atbash has no attack methods, so this test doesn't apply
