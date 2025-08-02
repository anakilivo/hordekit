"""
Atbash Cipher implementation.

The Atbash cipher is a substitution cipher where each letter is replaced by the letter
that is symmetric to it about the center of the alphabet.
For example: A→Z, B→Y, C→X, ..., M→N, N→M, ..., X→C, Y→B, Z→A

Atbash is a special case of the Affine cipher where a=25 and b=25.
"""

from typing import Any

from .affine import AffineCipher


class AtbashCipher(AffineCipher):
    """
    Atbash Cipher - a substitution cipher that mirrors the alphabet.

    The Atbash cipher replaces each letter with the letter that is symmetric
    about the center of the alphabet. For example:
    - A becomes Z, B becomes Y, C becomes X, etc.
    - M becomes N, N becomes M (they are symmetric about the center)
    - Z becomes A, Y becomes B, X becomes C, etc.

    This cipher is its own inverse - the same operation is used for both
    encryption and decryption.

    Atbash is a special case of the Affine cipher where a=25 and b=25.
    The transformation is: E(x) = (25x + 25) mod 26

    Note: Atbash has no key or variability, so attack methods are not applicable.

    Attributes:
        alphabet (str): The alphabet used for encryption
        alphabet_lower (str): Lowercase alphabet
        encrypt_table (dict): Translation table for encryption
        decrypt_table (dict): Translation table for decryption
        a (int): Affine parameter a (fixed at 25 for Atbash)
        b (int): Affine parameter b (fixed at 25 for Atbash)
    """

    SUPPORTED_ATTACK_METHODS = []  # No attack methods - no variability

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize Atbash cipher.

        Atbash is a special case of Affine cipher with a=25 and b=25.
        No parameters are needed as these values are fixed.
        """
        # Remove any a or b parameters from kwargs to avoid conflicts
        kwargs.pop("a", None)
        kwargs.pop("b", None)

        # Atbash is Affine cipher with a=25, b=25
        super().__init__(a=25, b=25, **kwargs)

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate Atbash cipher parameters."""
        # Atbash cipher doesn't require any parameters
        # All validation is handled by the parent AffineCipher class

    @classmethod
    def generate_key(cls) -> "AtbashCipher":
        """Generate an Atbash cipher key."""
        # Atbash cipher doesn't have a key, but we return an instance
        return cls()
