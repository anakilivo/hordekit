"""
Caesar Cipher implementation.

The Caesar cipher is a type of substitution cipher where each letter in the plaintext
is shifted a certain number of positions down the alphabet.
"""

from typing import Any, Dict, Optional

from ...utils import AttackMethod  # type: ignore
from .base_substitution import BaseSubstitutionCipher


class CaesarCipher(BaseSubstitutionCipher):
    """
    Caesar Cipher - a simple substitution cipher that shifts letters by a fixed amount.

    The Caesar cipher shifts each letter in the plaintext by a fixed number of positions
    down the alphabet. For example, with a shift of 3, 'A' becomes 'D', 'B' becomes 'E', etc.

    Attributes:
        shift (int): The number of positions to shift each letter
        alphabet (str): The alphabet used for encryption
        alphabet_lower (str): Lowercase alphabet
        encrypt_table (dict): Translation table for encryption
        decrypt_table (dict): Translation table for decryption
    """

    SUPPORTED_ATTACK_METHODS = [
        AttackMethod.BRUTE_FORCE,
        AttackMethod.FREQUENCY_ANALYSIS,
        AttackMethod.KNOWN_PLAINTEXT,
    ]

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate Caesar cipher parameters."""
        shift = kwargs.get("shift")

        if shift is None:
            raise ValueError("shift parameter is required")

        if not isinstance(shift, int):
            raise ValueError("shift must be an integer")

        if shift < 1 or shift > 25:
            raise ValueError("shift must be between 1 and 25")

    def _setup_substitution_algorithm(self, **kwargs: Any) -> None:
        """Set up the Caesar cipher algorithm."""
        self.shift = kwargs["shift"]

    def _create_mappings(self) -> None:
        """Create encryption and decryption translation tables."""
        # Create translation tables for both upper and lower case
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

    @classmethod
    def generate_key(cls) -> "CaesarCipher":
        """Generate a random Caesar cipher key."""
        import secrets

        shift = secrets.randbelow(25) + 1
        return cls(shift=shift)

    @classmethod
    def _get_possible_keys(cls) -> list:
        """Get all possible keys for Caesar cipher."""
        return [{"shift": i} for i in range(1, 26)]

    @classmethod
    def _key_to_string(cls, key: Dict[str, Any]) -> str:
        """Convert key dictionary to string representation."""
        return str(key["shift"])

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
