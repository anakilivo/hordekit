import pytest

from hordekit.crypto.attacks.generic import dictionary_attack
from hordekit.crypto.classical.substitution import Caesar, Vigenere


def test_finds_correct_caesar_key() -> None:
    plaintext = b"the quick brown fox jumps over the lazy dog and we kept going for longer"
    ct = Caesar(shift=7).encrypt(plaintext).as_bytes()

    wordlist = [{"shift": s} for s in range(1, 26)]
    result = dictionary_attack(Caesar, ct, wordlist)

    best = result.metadata["candidates"][0]
    assert best["key"] == {"shift": 7}
    assert result.as_str().lower() == plaintext.decode().lower()


def test_finds_correct_vigenere_key() -> None:
    plaintext = b"the quick brown fox jumps over the lazy dog and the fox ran away quickly"
    ct = Vigenere(key=b"lemon").encrypt(plaintext).as_bytes()

    wordlist = [{"key": b"apple"}, {"key": b"lemon"}, {"key": b"secret"}]
    result = dictionary_attack(Vigenere, ct, wordlist)

    assert result.as_str() == plaintext.decode()
    assert result.metadata["candidates"][0]["key"] == {"key": b"lemon"}


def test_candidates_sorted_by_score() -> None:
    plaintext = b"the quick brown fox jumps over the lazy dog and the fox ran away"
    ct = Caesar(shift=3).encrypt(plaintext).as_bytes()

    wordlist = [{"shift": s} for s in range(1, 26)]
    result = dictionary_attack(Caesar, ct, wordlist)

    scores = [c["score"] for c in result.metadata["candidates"]]
    assert scores == sorted(scores, reverse=True)


def test_empty_wordlist_raises() -> None:
    with pytest.raises(ValueError, match="No valid candidates found"):
        dictionary_attack(Caesar, b"hello", [])


def test_invalid_keys_skipped() -> None:
    ct = Caesar(shift=3).encrypt(b"hello world this is a longer text for testing").as_bytes()
    wordlist = [{"shift": 3}, {"invalid_kwarg": 99}]
    result = dictionary_attack(Caesar, ct, wordlist)
    assert len(result.metadata["candidates"]) == 1
