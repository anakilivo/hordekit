from hordekit.crypto.attacks.vigenere import kasiski
from hordekit.crypto.classical.substitution import Vigenere


def test_finds_key_length() -> None:
    plaintext = b"the quick brown fox jumps over the lazy dog and it jumped again over the fence " * 3
    ct = Vigenere(key=b"lemon").encrypt(plaintext).as_bytes()
    result = kasiski(ct)
    assert 5 in result.metadata["likely_key_lengths"]


def test_metadata_keys_present() -> None:
    ct = Vigenere(key=b"key").encrypt(b"hello world foo bar baz qux " * 10).as_bytes()
    result = kasiski(ct)
    assert "likely_key_lengths" in result.metadata
    assert "factor_counts" in result.metadata
    assert "spacings" in result.metadata


def test_returns_original_ciphertext() -> None:
    ct = b"VIGENERE CIPHER TEST " * 5
    result = kasiski(ct)
    assert result.as_bytes() == ct


def test_short_text_returns_error() -> None:
    result = kasiski(b"AB")
    assert "error" in result.metadata
    assert result.metadata["likely_key_lengths"] == []


def test_spacings_are_positive() -> None:
    ct = Vigenere(key=b"crypto").encrypt(b"the quick brown fox jumps over the lazy dog the quick " * 3).as_bytes()
    result = kasiski(ct)
    for spacing in result.metadata["spacings"]:
        assert spacing > 0
