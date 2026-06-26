import pytest

from hordekit.crypto.classical.substitution.autokey import Autokey


class TestAutokey:
    # Known vector: key="SECRET", plaintext="ATTACKATDAWN" -> "SXVRGDAMWAYX"
    # Verified by manual calculation and https://en.wikipedia.org/wiki/Autokey_cipher
    def test_encrypt(self) -> None:
        assert Autokey(b"SECRET").encrypt(b"ATTACKATDAWN") == b"SXVRGDAMWAYX"

    def test_decrypt(self) -> None:
        assert Autokey(b"SECRET").decrypt(b"SXVRGDAMWAYX") == b"ATTACKATDAWN"

    def test_roundtrip(self) -> None:
        plaintext = b"The Quick Brown Fox"
        cipher = Autokey(b"KEYWORD")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_roundtrip_long(self) -> None:
        plaintext = b"When the key is exhausted the plaintext extends it"
        cipher = Autokey(b"AB")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_non_alpha_unchanged(self) -> None:
        result = Autokey(b"KEY").encrypt(b"HE LLO, 2024!")
        decrypted = Autokey(b"KEY").decrypt(result.as_bytes())
        assert decrypted.as_str() == "HE LLO, 2024!"
        # Spaces and punctuation pass through unchanged
        assert result.as_bytes()[2] == ord(" ")
        assert result.as_bytes()[6] == ord(",")

    def test_case_preserved(self) -> None:
        result = Autokey(b"KEY").encrypt(b"Hello")
        # Case of each letter must be preserved
        s = result.as_str()
        assert s[0].isupper()
        assert s[1].islower()

    def test_key_case_insensitive(self) -> None:
        assert Autokey(b"secret").encrypt(b"ATTACKATDAWN") == Autokey(b"SECRET").encrypt(b"ATTACKATDAWN")

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Autokey(b"")

    def test_invalid_key_byte_raises(self) -> None:
        with pytest.raises(ValueError, match="ASCII letters"):
            Autokey(b"KEY1")

    def test_invalid_key_space_raises(self) -> None:
        with pytest.raises(ValueError, match="ASCII letters"):
            Autokey(b"MY KEY")
