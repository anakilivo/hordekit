"""
Affine Cipher implementation.

The Affine cipher is a type of substitution cipher where each letter is mapped to its
numeric equivalent, transformed using a mathematical function, and converted back to a letter.
The encryption function is: E(x) = (ax + b) mod 26
The decryption function is: D(x) = a^(-1)(x - b) mod 26

Where:
- a and b are the key
- a must be coprime with 26 (gcd(a, 26) = 1)
- a^(-1) is the modular multiplicative inverse of a modulo 26
"""

import math

from typing import Any, Dict, Optional

from ...utils import AttackMethod  # type: ignore
from .base_substitution import BaseSubstitutionCipher


class AffineCipher(BaseSubstitutionCipher):
    """
    Affine Cipher - a substitution cipher that uses a mathematical function.

    The Affine cipher uses the formula: E(x) = (ax + b) mod 26
    Where a and b are the key, and a must be coprime with 26.

    Attributes:
        a (int): Multiplicative key (must be coprime with 26)
        b (int): Additive key (can be any integer)
        alphabet (str): The alphabet used for encryption
        alphabet_lower (str): Lowercase alphabet
        a_inverse (int): Modular multiplicative inverse of a modulo 26
    """

    SUPPORTED_ATTACK_METHODS = [
        AttackMethod.BRUTE_FORCE,
        AttackMethod.FREQUENCY_ANALYSIS,
        AttackMethod.KNOWN_PLAINTEXT,
    ]

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate Affine cipher parameters."""
        a = kwargs.get("a")
        b = kwargs.get("b")

        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")

        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Both 'a' and 'b' must be integers")

        if a <= 0 or a >= 26:
            raise ValueError("'a' must be between 1 and 25")

        if b < 0 or b >= 26:
            raise ValueError("'b' must be between 0 and 25")

        # Check if a is coprime with 26
        if math.gcd(a, 26) != 1:
            raise ValueError("'a' must be coprime with 26 (gcd(a, 26) = 1)")

    def _setup_substitution_algorithm(self, **kwargs: Any) -> None:
        """Set up the Affine cipher algorithm."""
        self.a = kwargs["a"]
        self.b = kwargs["b"]

        # Calculate modular multiplicative inverse of a
        self.a_inverse = pow(self.a, -1, 26)

    def _create_mappings(self) -> None:
        """Create encryption and decryption translation tables."""
        # Create translation tables for both upper and lower case
        from_chars = self.alphabet + self.alphabet_lower
        to_chars = ""

        # Upper case mapping
        for i, _ in enumerate(self.alphabet):
            encrypted_pos = (self.a * i + self.b) % 26
            to_chars += self.alphabet[encrypted_pos]

        # Lower case mapping
        for i, _ in enumerate(self.alphabet_lower):
            encrypted_pos = (self.a * i + self.b) % 26
            to_chars += self.alphabet_lower[encrypted_pos]

        # Create translation tables
        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)

    @classmethod
    def generate_key(cls) -> "AffineCipher":
        """Generate a random Affine cipher key."""
        import secrets

        # Find all numbers coprime with 26
        coprime_with_26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

        a = secrets.choice(coprime_with_26)
        b = secrets.randbelow(26)

        return cls(a=a, b=b)

    @classmethod
    def _get_possible_keys(cls) -> list:
        """Get all possible keys for Affine cipher."""
        # All numbers coprime with 26
        coprime_with_26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

        keys = []
        for a in coprime_with_26:
            for b in range(26):
                keys.append({"a": a, "b": b})
        return keys

    @classmethod
    def _key_to_string(cls, key: Dict[str, Any]) -> str:
        """Convert key dictionary to string representation."""
        return f"a={key['a']},b={key['b']}"

    @classmethod
    def _attack_known_plaintext(cls, **kwargs: Any) -> Optional[Dict[str, int]]:
        """
        Known plaintext attack on Affine cipher.

        Args:
            plaintext (str): Known plaintext
            ciphertext (str): Corresponding ciphertext

        Returns:
            Optional[Dict[str, int]]: Recovered key {a, b}, or None if attack fails
        """
        plaintext = kwargs.get("plaintext", "")
        ciphertext = kwargs.get("ciphertext", "")

        if not plaintext or not ciphertext:
            raise ValueError("Both plaintext and ciphertext required for known plaintext attack")

        # Find two different letters in plaintext and their corresponding ciphertext
        plain_chars = []
        cipher_chars = []

        for i, (p_char, c_char) in enumerate(zip(plaintext, ciphertext)):
            if p_char.isalpha() and c_char.isalpha():
                plain_chars.append(p_char.upper())
                cipher_chars.append(c_char.upper())
                if len(plain_chars) >= 2:
                    break

        if len(plain_chars) < 2:
            return None

        # Convert to numbers
        p1 = ord(plain_chars[0]) - ord("A")
        p2 = ord(plain_chars[1]) - ord("A")
        c1 = ord(cipher_chars[0]) - ord("A")
        c2 = ord(cipher_chars[1]) - ord("A")

        # Solve for a and b
        # c1 = (a * p1 + b) mod 26
        # c2 = (a * p2 + b) mod 26
        # c1 - c2 = a * (p1 - p2) mod 26
        # a = (c1 - c2) * (p1 - p2)^(-1) mod 26

        p_diff = (p1 - p2) % 26
        c_diff = (c1 - c2) % 26

        if p_diff == 0:
            return None

        # Find modular inverse of p_diff
        try:
            p_diff_inv = pow(p_diff, -1, 26)
        except ValueError:
            return None

        a = (c_diff * p_diff_inv) % 26

        # Check if a is coprime with 26
        if math.gcd(a, 26) != 1:
            return None

        # Calculate b
        b = (c1 - a * p1) % 26

        # Verify the solution
        try:
            test_instance = cls(a=a, b=b)
            test_encrypted = test_instance.encode(plaintext)
            if test_encrypted == ciphertext:
                return {"a": a, "b": b}
        except Exception:  # nosec
            pass

        return None
