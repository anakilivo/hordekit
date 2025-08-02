"""
Caesar Cipher implementation.
A simple substitution cipher that shifts each letter by a fixed number of positions.
"""

from typing import Any, Dict, Optional

from ...utils import AttackMethod, CryptoAlgorithm  # type: ignore


class CaesarCipher(CryptoAlgorithm):
    SUPPORTED_ATTACK_METHODS = [
        AttackMethod.BRUTE_FORCE,
        AttackMethod.FREQUENCY_ANALYSIS,
        AttackMethod.KNOWN_PLAINTEXT,
    ]

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate Caesar cipher parameters"""
        shift = kwargs.get("shift")
        if shift is None:
            raise ValueError("Shift parameter is required")
        if not isinstance(shift, int):
            raise ValueError("Shift must be an integer")
        if shift < 1 or shift > 25:
            raise ValueError("Shift must be between 1 and 25")

        alphabet = kwargs.get("alphabet", None)
        if alphabet is not None and not isinstance(alphabet, str):
            raise ValueError("Alphabet must be a string")

    def _setup_algorithm(self, **kwargs: Any) -> None:
        """Configure Caesar cipher with validated parameters"""
        shift_value = kwargs.get("shift")
        if shift_value is None:
            raise ValueError("Shift parameter is required")
        self.shift: int = shift_value
        self.alphabet: str = kwargs.get("alphabet", "ABCDEFGHIJKLMNOPQRSTUVWXYZ").upper()
        self.alphabet_lower: str = self.alphabet.lower()

        # Create shift mappings
        self._create_mappings()

    def _create_mappings(self) -> None:
        """Create encryption and decryption translation tables"""
        # Create combined tables for both upper and lower case
        from_chars = self.alphabet + self.alphabet_lower
        to_chars_encrypt = (
            self.alphabet[self.shift :]
            + self.alphabet[: self.shift]
            + self.alphabet_lower[self.shift :]
            + self.alphabet_lower[: self.shift]
        )
        to_chars_decrypt = (
            self.alphabet[-self.shift :]
            + self.alphabet[: -self.shift]
            + self.alphabet_lower[-self.shift :]
            + self.alphabet_lower[: -self.shift]
        )

        self.encrypt_table = str.maketrans(from_chars, to_chars_encrypt)
        self.decrypt_table = str.maketrans(from_chars, to_chars_decrypt)

    def _encode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Encrypt data using Caesar cipher"""
        text = data.decode("utf-8")

        # Use single translation table for both cases
        encrypted = text.translate(self.encrypt_table)

        return encrypted.encode("utf-8")

    def _decode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Decrypt data using Caesar cipher"""
        text = data.decode("utf-8")

        # Use single translation table for both cases
        decrypted = text.translate(self.decrypt_table)

        return decrypted.encode("utf-8")

    @classmethod
    def get_attack_methods(cls) -> Dict[AttackMethod, str]:
        """Return available attack methods for Caesar cipher"""
        return {
            AttackMethod.BRUTE_FORCE: "Try all possible shift values (1-25)",
            AttackMethod.FREQUENCY_ANALYSIS: "Analyze letter frequency patterns",
            AttackMethod.KNOWN_PLAINTEXT: "Use known plaintext-ciphertext pairs",
        }

    @classmethod
    def generate_key(cls) -> "CaesarCipher":
        """
        Generate a Caesar cipher with random shift value.

        Returns:
            CaesarCipher: New instance with random shift value
        """
        import random

        shift = random.randint(1, 25)
        return cls(shift=shift)

    @classmethod
    def _attack_brute_force(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Brute force attack - try all possible shift values.

        Args:
            ciphertext (str): Encrypted text to decrypt
            mask (str, optional): Regular expression pattern to match successful decryption

        Returns:
            Dict[str, Any]: Attack results with all decryptions and best match if mask provided
        """
        ciphertext = kwargs.get("ciphertext", "")
        mask = kwargs.get("mask", None)

        if not ciphertext:
            raise ValueError("ciphertext parameter required for brute force attack")

        import re

        results = {}
        best_match = None
        best_shift = None

        for shift in range(1, 26):
            instance = cls(shift=shift)
            decrypted = instance.decode(ciphertext)
            results[shift] = decrypted

            # Check if this decryption matches the mask
            if mask and re.search(mask, decrypted):
                best_match = decrypted
                best_shift = shift

        result: Dict[str, Any] = {"all_results": results}

        if best_match:
            result["best_match"] = best_match
            result["best_shift"] = best_shift
            result["mask_matched"] = True
        elif mask:
            result["mask_matched"] = False

        return result

    @classmethod
    def _attack_frequency_analysis(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Frequency analysis attack on Caesar cipher using n-gram scoring.

        Returns:
            Dict[str, Any]: Analysis results with most likely shift
        """
        ciphertext = kwargs.get("ciphertext", "")
        if not ciphertext:
            raise ValueError("ciphertext parameter required for frequency analysis")

        from ...cryptoanalysis.ngram_score import BigramScore, MonogramScore, TrigramScore  # type: ignore

        # Initialize n-gram scorers
        monogram_scorer = MonogramScore()
        bigram_scorer = BigramScore()
        trigram_scorer = TrigramScore()

        # Find best shift by testing all possibilities
        best_shift: int = 1
        best_score: float = float("-inf")  # Higher score is better for n-gram scoring

        for shift in range(1, 26):
            # Temporarily set shift and create mappings
            instance = cls(shift=shift)

            # Decrypt with current shift
            decrypted = instance.decode(ciphertext)

            # Calculate score using multiple n-gram methods
            try:
                # Get scores from different n-gram methods
                mono_score = monogram_scorer.score(decrypted)
                bi_score = bigram_scorer.score(decrypted)
                tri_score = trigram_scorer.score(decrypted)

                # Combined score (weighted average)
                combined_score = mono_score * 0.3 + bi_score * 0.4 + tri_score * 0.3

                if combined_score > best_score:
                    best_score = combined_score
                    best_shift = shift

            except Exception:
                # Skip this shift if scoring fails
                continue

        # Decrypt with best shift
        instance = cls(shift=best_shift)
        decrypted = instance.decode(ciphertext)

        return {
            "most_likely_shift": best_shift,
            "confidence_score": best_score,
            "decrypted_text": decrypted,
            "monogram_score": monogram_scorer.score(decrypted.encode("utf-8")),
            "bigram_score": bigram_scorer.score(decrypted.encode("utf-8")),
            "trigram_score": trigram_scorer.score(decrypted.encode("utf-8")),
        }

    @classmethod
    def _attack_known_plaintext(cls, **kwargs: Any) -> Optional[int]:
        """
        Known plaintext attack on Caesar cipher.

        Args:
            plaintext (str): Known plaintext
            ciphertext (str): Corresponding ciphertext

        Returns:
            Optional[int]: Recovered shift value, or None if attack fails
        """
        plaintext = kwargs.get("plaintext", "")
        ciphertext = kwargs.get("ciphertext", "")

        if not plaintext or not ciphertext:
            raise ValueError("Both plaintext and ciphertext required for known plaintext attack")

        # Find first letter that appears in both plaintext and ciphertext
        plaintext_upper = plaintext.upper()
        ciphertext_upper = ciphertext.upper()

        # Create instance to access alphabet
        instance = cls(shift=1)
        alphabet = instance.alphabet

        for i, plain_char in enumerate(plaintext_upper):
            if plain_char in alphabet and i < len(ciphertext_upper):
                cipher_char = ciphertext_upper[i]
                if cipher_char in alphabet:
                    # Calculate shift
                    plain_idx = alphabet.find(plain_char)
                    cipher_idx = alphabet.find(cipher_char)
                    shift = (cipher_idx - plain_idx) % 26
                    return shift

        return None
