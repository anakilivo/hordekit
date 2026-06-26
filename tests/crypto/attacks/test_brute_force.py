from hordekit.crypto.attacks.generic.brute_force import brute_force
from hordekit.crypto.classical.substitution.caesar import Caesar


class TestBruteForce:
    def test_finds_correct_shift(self) -> None:
        plaintext = b"The quick brown fox jumps over the lazy dog and then some more text"
        ciphertext = Caesar(shift=13).encrypt(plaintext).as_bytes()
        result = brute_force(Caesar, ciphertext)
        assert result.as_str().lower() == plaintext.decode().lower()

    def test_returns_candidates(self) -> None:
        ciphertext = Caesar(shift=5).encrypt(b"The quick brown fox").as_bytes()
        result = brute_force(Caesar, ciphertext)
        assert "candidates" in result.metadata
        assert len(result.metadata["candidates"]) == 25

    def test_best_candidate_is_first(self) -> None:
        ciphertext = Caesar(shift=3).encrypt(b"Hello World").as_bytes()
        result = brute_force(Caesar, ciphertext)
        candidates = result.metadata["candidates"]
        best_score = candidates[0]["score"]
        assert all(best_score >= c["score"] for c in candidates)

    def test_custom_scorer(self) -> None:
        ciphertext = Caesar(shift=1).encrypt(b"aaa").as_bytes()
        result = brute_force(Caesar, ciphertext, scorer=lambda data: -len(data))
        assert "candidates" in result.metadata
