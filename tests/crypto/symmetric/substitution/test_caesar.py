#!/usr/bin/env python3
"""
Tests for Caesar Cipher implementation.
"""
import parametrize_from_file as pff  # type: ignore

from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher
from hordekit.crypto.utils import AttackMethod
from tests.base_crypto_test import BaseCryptoTest


class TestCaesarCipher(BaseCryptoTest):
    """Test cases for Caesar Cipher implementation."""

    algorithm_class = CaesarCipher
    valid_parameters = {"shift": 3}
    invalid_parameters = [
        {},  # Missing shift
        {"shift": "invalid"},  # Invalid shift type
        {"shift": 0},  # Invalid shift value
        {"shift": 26},  # Invalid shift value
    ]

    def test_brute_force_attack(self):
        """Test brute force attack method."""
        message = "ATTACK AT DAWN"
        encrypted = self.algorithm.encode(message)

        results = self.algorithm_class.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)

        assert "all_results" in results
        assert len(results["all_results"]) == 25
        assert results["all_results"][self.algorithm.shift] == message

    def test_brute_force_attack_with_mask(self):
        """Test brute force attack method with mask."""
        message = "testMask{tEsT1ng}"
        encrypted = self.algorithm.encode(message)
        mask = r"testMask\{.*\}"

        results = self.algorithm_class.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted, mask=mask)

        assert "all_results" in results
        assert "best_match" in results
        assert "best_shift" in results
        assert "mask_matched" in results
        assert results["mask_matched"] is True
        assert results["best_match"] == message
        assert results["best_shift"] == self.algorithm.shift

    def test_frequency_analysis_attack(self):
        """Test frequency analysis attack method."""
        # Use a longer text for better frequency analysis
        long_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        encrypted = self.algorithm.encode(long_message)

        analysis = self.algorithm_class.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext=encrypted)

        assert "most_likely_shift" in analysis
        assert "decrypted_text" in analysis
        assert "confidence_score" in analysis
        assert "monogram_score" in analysis
        assert "bigram_score" in analysis
        assert "trigram_score" in analysis

        assert analysis["most_likely_shift"] == self.algorithm.shift

    def test_known_plaintext_attack(self):
        """Test known plaintext attack method."""
        plaintext = "HELLO"
        ciphertext = self.algorithm.encode(plaintext)

        recovered_shift = self.algorithm_class.attack(
            AttackMethod.KNOWN_PLAINTEXT,
            plaintext=plaintext,
            ciphertext=ciphertext,
        )

        assert recovered_shift == self.algorithm.shift

    @pff.parametrize(path="test_caesar.yml")
    def test_caesar_with_mask(self, plaintext: str, shift: int, ciphertext: str, mask: str):
        """Test Caesar cipher with mask-based brute force attack."""
        caesar = CaesarCipher(shift=shift)

        # Test basic encryption/decryption
        assert caesar.encode(plaintext) == ciphertext
        assert caesar.decode(ciphertext) == plaintext

        # Test brute force attack with mask
        attack_results = CaesarCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext=ciphertext, mask=mask)

        assert attack_results["mask_matched"] is True
        assert attack_results["best_match"] == plaintext
        assert attack_results["best_shift"] == shift
