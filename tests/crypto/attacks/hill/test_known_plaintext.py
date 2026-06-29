import pytest

from hordekit.crypto.attacks.hill.known_plaintext import hill_known_plaintext
from hordekit.crypto.classical.substitution.hill import Hill

_K2 = [[3, 3], [2, 5]]
_K3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]


class TestHillKnownPlaintext:
    def test_recovers_2x2_key(self) -> None:
        pt, ct = b"HELP", b"HIAT"
        result = hill_known_plaintext(pt, ct, n=2)
        assert result.metadata["key_matrix"] == _K2

    def test_recovers_3x3_key(self) -> None:
        # "ACTPOHGHI" → P matrix det ≡ 9 (mod 26), gcd(9,26)=1, so P is invertible
        pt = b"ACTPOHGHI"
        ct = Hill(_K3).encrypt(pt).as_bytes()
        result = hill_known_plaintext(pt, ct, n=3)
        assert result.metadata["key_matrix"] == _K3

    def test_result_bytes_are_flattened_key(self) -> None:
        result = hill_known_plaintext(b"HELP", b"HIAT", n=2)
        flat = bytes(v for row in _K2 for v in row)
        assert result.as_bytes() == flat

    def test_metadata_contains_n(self) -> None:
        result = hill_known_plaintext(b"HELP", b"HIAT", n=2)
        assert result.metadata["n"] == 2

    def test_extra_letters_ignored(self) -> None:
        # More than n² letters → only first n² are used, rest ignored
        pt = b"HELPEXTRA"
        ct = Hill(_K2).encrypt(b"HELPEXTRA").as_bytes()
        result = hill_known_plaintext(pt, ct, n=2)
        assert result.metadata["key_matrix"] == _K2

    def test_non_alpha_in_input_skipped(self) -> None:
        # Spaces in plaintext/ciphertext are ignored
        result = hill_known_plaintext(b"HE LP", b"HI AT", n=2)
        assert result.metadata["key_matrix"] == _K2

    def test_roundtrip_via_recovered_key(self) -> None:
        # "HILL" → P = [[7,11],[8,11]], det = 77-88 = -11 ≡ 15 (mod 26), gcd(15,26)=1 ✓
        message = b"HILLCIPHER"
        ct = Hill(_K2).encrypt(message).as_bytes()
        result = hill_known_plaintext(message, ct, n=2)
        recovered = Hill(result.metadata["key_matrix"])
        assert recovered.decrypt(ct).as_bytes() == message

    def test_insufficient_plaintext_raises(self) -> None:
        with pytest.raises(ValueError, match="plaintext"):
            hill_known_plaintext(b"HEL", b"HIAT", n=2)  # 3 < 4 letters

    def test_insufficient_ciphertext_raises(self) -> None:
        with pytest.raises(ValueError, match="ciphertext"):
            hill_known_plaintext(b"HELP", b"HIA", n=2)  # 3 < 4 letters

    def test_singular_plaintext_matrix_raises(self) -> None:
        # If the chosen plaintext blocks form a singular matrix, the attack fails
        # HH + HH → plaintext matrix [[7,7],[7,7]], det=0
        with pytest.raises(ValueError, match="invertible"):
            hill_known_plaintext(b"HHHH", b"HHHH", n=2)

    def test_n_less_than_2_raises(self) -> None:
        with pytest.raises(ValueError, match="dimension"):
            hill_known_plaintext(b"HELP", b"HIAT", n=1)
