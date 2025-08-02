#!/usr/bin/env python3
"""
Tests for Affine Cipher implementation.
"""

import parametrize_from_file as pff  # type: ignore

from hordekit.crypto.symmetric.substitution.affine import AffineCipher
from hordekit.crypto.utils import AttackMethod
from tests.base_crypto_test import BaseCryptoTest


class TestAffineCipher(BaseCryptoTest):
    """Test cases for Affine Cipher implementation."""

    algorithm_class = AffineCipher
    valid_parameters = {"a": 5, "b": 8}
    invalid_parameters = [
        {},  # Missing parameters
        {"a": 5},  # Missing b
        {"b": 8},  # Missing a
        {"a": "invalid", "b": 8},  # Invalid a type
        {"a": 5, "b": "invalid"},  # Invalid b type
        {"a": 0, "b": 8},  # Invalid a value
        {"a": 26, "b": 8},  # Invalid a value
        {"a": 5, "b": -1},  # Invalid b value
        {"a": 5, "b": 26},  # Invalid b value
        {"a": 2, "b": 8},  # a not coprime with 26
        {"a": 4, "b": 8},  # a not coprime with 26
        {"a": 13, "b": 8},  # a not coprime with 26
    ]

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption."""
        message = "AFFINECIPHER"
        affine = AffineCipher(a=5, b=8)

        encrypted = affine.encode(message)
        decrypted = affine.decode(encrypted)

        assert decrypted == message
        assert encrypted == "IHHWVCSWFRCP"

    def test_case_preservation(self):
        """Test that case is preserved."""
        message = "Hello World"
        affine = AffineCipher(a=3, b=7)

        encrypted = affine.encode(message)
        decrypted = affine.decode(encrypted)

        assert decrypted == message

    def test_non_alphabetic_characters(self):
        """Test that non-alphabetic characters are preserved."""
        message = "HELLO, WORLD! 123"
        affine = AffineCipher(a=7, b=11)

        encrypted = affine.encode(message)
        decrypted = affine.decode(encrypted)

        assert decrypted == message

    def test_brute_force_attack(self):
        """Test brute force attack method."""
        message = "ATTACK AT DAWN"
        affine = AffineCipher(a=9, b=13)
        encrypted = affine.encode(message)

        results = AffineCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)

        assert "all_results" in results
        assert len(results["all_results"]) > 0
        # Should find the correct key
        correct_key = f"a={affine.a},b={affine.b}"
        assert correct_key in results["all_results"]
        assert results["all_results"][correct_key] == message

    def test_brute_force_attack_with_mask(self):
        """Test brute force attack method with mask."""
        message = "YUBITSEC{A_FINE_CIPHER}"
        affine = AffineCipher(a=9, b=13)
        encrypted = affine.encode(message)
        mask = r"YUBITSEC\{.*\}"

        results = AffineCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted, mask=mask)

        assert "all_results" in results
        assert "best_match" in results
        assert "best_key" in results
        assert "mask_matched" in results
        assert results["mask_matched"] is True
        assert results["best_match"] == message
        assert results["best_key"] == f"a={affine.a},b={affine.b}"

    def test_frequency_analysis_attack(self):
        """Test frequency analysis attack method."""
        long_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        affine = AffineCipher(a=7, b=11)
        encrypted = affine.encode(long_message)

        analysis = AffineCipher.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext=encrypted)

        assert "most_likely_key" in analysis
        assert "confidence_score" in analysis
        assert "decrypted_text" in analysis
        assert "monogram_score" in analysis
        assert "bigram_score" in analysis
        assert "trigram_score" in analysis

        # The analysis should find the correct key
        assert analysis["most_likely_key"] == f"a={affine.a},b={affine.b}"

    def test_known_plaintext_attack(self):
        """Test known plaintext attack method."""
        plaintext = "HELLO"
        affine = AffineCipher(a=3, b=7)
        ciphertext = affine.encode(plaintext)

        recovered_key = AffineCipher.attack(
            AttackMethod.KNOWN_PLAINTEXT,
            plaintext=plaintext,
            ciphertext=ciphertext,
        )

        assert recovered_key is not None
        assert recovered_key["a"] == affine.a
        assert recovered_key["b"] == affine.b

    def test_known_plaintext_attack_failure(self):
        """Test known plaintext attack with insufficient data."""
        plaintext = "A"  # Only one letter
        affine = AffineCipher(a=3, b=7)
        ciphertext = affine.encode(plaintext)

        recovered_key = AffineCipher.attack(
            AttackMethod.KNOWN_PLAINTEXT,
            plaintext=plaintext,
            ciphertext=ciphertext,
        )

        assert recovered_key is None

    @pff.parametrize(path="test_affine.yml", key="test_affine_examples")
    def test_affine_with_mask(self, plaintext: str, a: int, b: int, ciphertext: str, mask: str):
        """Test Affine cipher with mask-based brute force attack."""
        affine = AffineCipher(a=a, b=b)

        # Test basic encryption/decryption
        assert affine.encode(plaintext) == ciphertext
        assert affine.decode(ciphertext) == plaintext

        # Test brute force attack with mask
        attack_results = AffineCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=ciphertext, mask=mask)

        assert attack_results["mask_matched"] is True
        assert attack_results["best_match"] == plaintext
        assert attack_results["best_key"] == f"a={a},b={b}"
