"""
Base class for substitution ciphers.

This class provides common functionality for all substitution ciphers:
- Translation table creation
- Case preservation
- Non-alphabetic character handling
- Common attack methods
"""

from typing import Any, Dict

from ...utils import CryptoAlgorithm  # type: ignore


class BaseSubstitutionCipher(CryptoAlgorithm):
    """
    Base class for substitution ciphers.

    Provides common functionality for ciphers that substitute one character for another.
    Subclasses should implement:
    - _create_mappings(): Create encryption/decryption translation tables
    - _validate_parameters(): Validate cipher-specific parameters
    """

    def _setup_algorithm(self, **kwargs: Any) -> None:
        """Set up the substitution cipher algorithm."""
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet_lower = self.alphabet.lower()

        # Call subclass-specific setup
        self._setup_substitution_algorithm(**kwargs)

        # Create translation tables
        self._create_mappings()

    def _setup_substitution_algorithm(self, **kwargs: Any) -> None:
        """Subclass-specific algorithm setup. Override in subclasses."""

    def _create_mappings(self) -> None:
        """Create encryption and decryption translation tables. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement _create_mappings")

    def _encode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Encode data using substitution cipher."""
        text = data.decode("utf-8")
        encrypted = text.translate(self.encrypt_table)
        return encrypted.encode("utf-8")

    def _decode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Decode data using substitution cipher."""
        text = data.decode("utf-8")
        decrypted = text.translate(self.decrypt_table)
        return decrypted.encode("utf-8")

    @classmethod
    def _attack_brute_force(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Brute force attack on substitution cipher.

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

        # Get all possible keys for this cipher
        possible_keys = cls._get_possible_keys()

        results = {}
        best_match = None
        best_key = None

        for key in possible_keys:
            try:
                instance = cls(**key)
                decrypted = instance.decode(ciphertext)
                key_str = cls._key_to_string(key)
                results[key_str] = decrypted

                # Check if this decryption matches the mask
                if mask and re.search(mask, decrypted):
                    best_match = decrypted
                    best_key = key_str
            except Exception:  # nosec
                continue

        result: Dict[str, Any] = {"all_results": results}

        if best_match:
            result["best_match"] = best_match
            result["best_key"] = best_key
            result["mask_matched"] = True
        elif mask:
            result["mask_matched"] = False

        return result

    @classmethod
    def _attack_frequency_analysis(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Frequency analysis attack on substitution cipher using n-gram scoring.

        Returns:
            Dict[str, Any]: Analysis results with most likely key
        """
        ciphertext = kwargs.get("ciphertext", "")
        if not ciphertext:
            raise ValueError("ciphertext parameter required for frequency analysis")

        from ...cryptoanalysis.ngram_score import BigramScore, MonogramScore, TrigramScore  # type: ignore

        # Initialize n-gram scorers
        monogram_scorer = MonogramScore()
        bigram_scorer = BigramScore()
        trigram_scorer = TrigramScore()

        # Get all possible keys for this cipher
        possible_keys = cls._get_possible_keys()

        # Find best key by testing all possibilities
        best_key = possible_keys[0] if possible_keys else None
        best_score: float = float("-inf")

        for key in possible_keys:
            try:
                instance = cls(**key)
                decrypted = instance.decode(ciphertext)

                # Calculate score using multiple n-gram methods
                try:
                    mono_score = monogram_scorer.score(decrypted)
                    bi_score = bigram_scorer.score(decrypted)
                    tri_score = trigram_scorer.score(decrypted)

                    # Combined score (weighted average)
                    combined_score = mono_score * 0.3 + bi_score * 0.4 + tri_score * 0.3

                    if combined_score > best_score:
                        best_score = combined_score
                        best_key = key

                except Exception:  # nosec
                    continue

            except Exception:  # nosec
                continue

        if best_key is None:
            raise ValueError("No valid keys found for frequency analysis")

        # Decrypt with best key
        instance = cls(**best_key)
        decrypted = instance.decode(ciphertext)

        return {
            "most_likely_key": cls._key_to_string(best_key),
            "confidence_score": best_score,
            "decrypted_text": decrypted,
            "monogram_score": monogram_scorer.score(decrypted.encode("utf-8")),
            "bigram_score": bigram_scorer.score(decrypted.encode("utf-8")),
            "trigram_score": trigram_scorer.score(decrypted.encode("utf-8")),
        }

    @classmethod
    def _get_possible_keys(cls) -> list:
        """Get all possible keys for this cipher. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement _get_possible_keys")

    @classmethod
    def _key_to_string(cls, key: Dict[str, Any]) -> str:
        """Convert key dictionary to string representation. Override in subclasses."""
        return str(key)
