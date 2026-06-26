import pytest

from hordekit.crypto.classical.substitution.beaufort import Beaufort


class TestBeaufort:
    def test_encrypt(self) -> None:
        # KEY=(10,4,24), HELLO=(7,4,11,11,14)
        # (10-7)%26=3=D, (4-4)%26=0=A, (24-11)%26=13=N, (10-11)%26=25=Z, (4-14)%26=16=Q
        assert Beaufort(b"KEY").encrypt(b"HELLO") == b"DANZQ"

    def test_decrypt(self) -> None:
        assert Beaufort(b"KEY").decrypt(b"DANZQ") == b"HELLO"

    def test_reciprocal(self) -> None:
        # Beaufort is a reciprocal cipher: encrypt == decrypt
        cipher = Beaufort(b"LEMON")
        plaintext = b"ATTACKATDAWN"
        ciphertext = cipher.encrypt(plaintext).as_bytes()
        assert cipher.encrypt(ciphertext) == plaintext

    def test_roundtrip(self) -> None:
        plaintext = b"The quick brown fox"
        cipher = Beaufort(b"SECRET")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_key_case_insensitive(self) -> None:
        assert Beaufort(b"key").encrypt(b"HELLO") == Beaufort(b"KEY").encrypt(b"HELLO")

    def test_non_alpha_unchanged(self) -> None:
        result = Beaufort(b"KEY").encrypt(b"HE LLO")
        assert result.as_str() == "DA NZQ"

    def test_digits_and_punctuation_unchanged(self) -> None:
        result = Beaufort(b"KEY").encrypt(b"HE110!")
        assert result.as_str() == "DA110!"

    def test_lowercase_preserved(self) -> None:
        result = Beaufort(b"KEY").encrypt(b"hello")
        assert result.as_str() == "danzq"

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Beaufort(b"")

    def test_invalid_key_byte_raises(self) -> None:
        with pytest.raises(ValueError, match="ASCII letters"):
            Beaufort(b"KEY1")
