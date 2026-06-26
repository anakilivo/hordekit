import pytest

from hordekit.crypto.classical.substitution.vigenere import Vigenere


class TestVigenere:
    def test_encrypt(self) -> None:
        assert Vigenere(b"KEY").encrypt(b"HELLO") == b"RIJVS"

    def test_decrypt(self) -> None:
        assert Vigenere(b"KEY").decrypt(b"RIJVS") == b"HELLO"

    def test_roundtrip(self) -> None:
        plaintext = b"Attack at dawn"
        cipher = Vigenere(b"LEMON")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_key_case_insensitive(self) -> None:
        assert Vigenere(b"key").encrypt(b"HELLO") == Vigenere(b"KEY").encrypt(b"HELLO")

    def test_non_alpha_skipped(self) -> None:
        result = Vigenere(b"KEY").encrypt(b"HE LLO")
        assert result.as_str() == "RI JVS"

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Vigenere(b"")

    def test_invalid_key_byte_raises(self) -> None:
        with pytest.raises(ValueError, match="ASCII letters"):
            Vigenere(b"KEY1")
