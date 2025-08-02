"""
ROT13 Cipher implementation.

ROT13 is a simple letter substitution cipher that replaces a letter with the 13th letter
after it in the alphabet. It is a special case of the Caesar cipher with a fixed shift of 13.

ROT13 is its own inverse - applying ROT13 twice returns the original text.
"""

from typing import Any

from .caesar import CaesarCipher


class ROT13Cipher(CaesarCipher):
    """
    ROT13 Cipher - a special case of Caesar cipher with shift 13.

    ROT13 replaces each letter with the 13th letter after it in the alphabet.
    For example: A→N, B→O, C→P, ..., M→Z, N→A, O→B, ..., Z→M

    ROT13 is its own inverse - the same operation is used for both
    encryption and decryption.

    ROT13 is a special case of the Caesar cipher with shift=13.
    The transformation is: E(x) = (x + 13) mod 26

    Note: ROT13 has no variability, so attack methods are not applicable.

    Attributes:
        alphabet (str): The alphabet used for encryption
        alphabet_lower (str): Lowercase alphabet
        encrypt_table (dict): Translation table for encryption
        decrypt_table (dict): Translation table for decryption
        shift (int): Fixed shift value of 13
    """

    SUPPORTED_ATTACK_METHODS = []  # No attack methods - no variability

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize ROT13 cipher.

        ROT13 is a special case of Caesar cipher with shift=13.
        No parameters are needed as this value is fixed.
        """
        # Remove any shift parameter from kwargs to avoid conflicts
        kwargs.pop("shift", None)

        # ROT13 is Caesar cipher with shift=13
        super().__init__(shift=13, **kwargs)

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate ROT13 cipher parameters."""
        # ROT13 cipher doesn't require any parameters
        # All validation is handled by the parent CaesarCipher class

    @classmethod
    def generate_key(cls) -> "ROT13Cipher":
        """Generate a ROT13 cipher key."""
        # ROT13 cipher doesn't have a key, but we return an instance
        return cls()
