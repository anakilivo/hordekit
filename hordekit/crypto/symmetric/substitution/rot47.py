"""
ROT47 Cipher implementation.

ROT47 is a simple character substitution cipher that replaces a character with the 47th character
after it in the ASCII table (from position 33 to 126). It is an extension of ROT13 that works
with the entire printable ASCII character set.

ROT47 is its own inverse - applying ROT47 twice returns the original text.
"""

from typing import Any, List

from ...utils import CryptoAlgorithm  # type: ignore


class ROT47Cipher(CryptoAlgorithm):
    """
    ROT47 Cipher - an extension of Caesar cipher that works with printable ASCII.

    ROT47 replaces each character with the 47th character after it in the ASCII table
    (from position 33 to 126). For example: !→P, "→Q, #→R, ..., ~→}

    ROT47 is its own inverse - the same operation is used for both
    encryption and decryption.

    ROT47 is a special case of the Caesar cipher with shift=47, but works
    with the entire printable ASCII character set (33-126) instead of just letters.

    Note: ROT47 has no variability, so attack methods are not applicable.

    Attributes:
        alphabet (str): The printable ASCII character set (33-126)
        encrypt_table (dict): Translation table for encryption
        decrypt_table (dict): Translation table for decryption
    """

    SUPPORTED_ATTACK_METHODS: List[str] = []  # No attack methods - no variability

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize ROT47 cipher.

        ROT47 is a fixed algorithm without parameters.
        """
        super().__init__(**kwargs)

    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate ROT47 cipher parameters."""
        # ROT47 cipher doesn't require any parameters

    def _setup_algorithm(self, **kwargs: Any) -> None:
        """Set up the ROT47 cipher algorithm."""
        # ROT47 uses the entire printable ASCII character set (33-126)
        self.alphabet = "".join(chr(i) for i in range(33, 127))
        self.alphabet_lower = self.alphabet  # ROT47 doesn't distinguish case

        # Create translation tables
        self._create_mappings()

    def _create_mappings(self) -> None:
        """Create encryption and decryption translation tables for ROT47."""
        # Create the full ASCII mapping for ROT47
        # Map each character to the character 47 positions later
        from_chars = self.alphabet
        to_chars = "".join(chr((ord(c) - 33 + 47) % 94 + 33) for c in from_chars)

        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)

    def _encode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Encode data using ROT47 cipher."""
        text = data.decode("utf-8")
        encrypted = text.translate(self.encrypt_table)
        return encrypted.encode("utf-8")

    def _decode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Decode data using ROT47 cipher."""
        text = data.decode("utf-8")
        decrypted = text.translate(self.decrypt_table)
        return decrypted.encode("utf-8")

    @classmethod
    def generate_key(cls) -> "ROT47Cipher":
        """Generate a ROT47 cipher key."""
        # ROT47 cipher doesn't have a key, but we return an instance
        return cls()

    @classmethod
    def _get_possible_keys(cls) -> list:
        """Get all possible keys for ROT47 cipher."""
        # ROT47 cipher only has one possible configuration
        return [{}]

    @classmethod
    def _key_to_string(cls, key: dict) -> str:
        """Convert key dictionary to string representation."""
        return "rot47"
