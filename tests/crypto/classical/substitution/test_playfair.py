import pytest

from hordekit.crypto.classical.substitution.playfair import Playfair

# Wikipedia Playfair example — key "PLAYFAIR EXAMPLE", verified square:
#   P L A Y F
#   I R E X M
#   B C D G H
#   K N O Q S
#   T U V W Z
_WIKI_KEY = b"PLAYFAIR EXAMPLE"

# HIDETHEGOLD (11 letters, odd) -> pairs HI DE TH EG OL D(X-pad)
#   HI -> BM  (rectangle)
#   DE -> OD  (same column ↓)
#   TH -> ZB  (rectangle)
#   EG -> XD  (rectangle)
#   OL -> NA  (rectangle)
#   DX -> GE  (rectangle)
_PLAINTEXT = b"HIDETHEGOLD"
_CIPHERTEXT = b"BM" + b"OD" + b"ZB" + b"XD" + b"NA" + b"GE"
_PLAINTEXT_WITH_PAD = b"HIDETHEGOLDX"


class TestPlayfair:
    def test_encrypt(self) -> None:
        result = Playfair(_WIKI_KEY).encrypt(_PLAINTEXT).as_bytes()
        assert result == _CIPHERTEXT

    def test_decrypt(self) -> None:
        # Decrypting the ciphertext reveals the padded plaintext (X appended)
        result = Playfair(_WIKI_KEY).decrypt(_CIPHERTEXT).as_bytes()
        assert result == _PLAINTEXT_WITH_PAD

    def test_roundtrip(self) -> None:
        # Even-length input with no adjacent duplicate letters and no J
        plaintext = b"HORDEKIT"
        cipher = Playfair(b"KEY")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_roundtrip_lowercase(self) -> None:
        plaintext = b"hordekit"
        cipher = Playfair(b"KEY")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_non_alpha_unchanged(self) -> None:
        # Space preserved between encrypted pairs
        result = Playfair(_WIKI_KEY).encrypt(b"HI DE").as_bytes()
        assert result == b"BM OD"

    def test_non_alpha_roundtrip(self) -> None:
        cipher = Playfair(b"KEY")
        plaintext = b"HI DE"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_digits_and_punctuation_unchanged(self) -> None:
        result = Playfair(b"KEY").encrypt(b"AB!12CD").as_bytes()
        assert result[2:5] == b"!12"

    def test_j_treated_as_i(self) -> None:
        # J and I are identical in Playfair — same encrypted output
        cipher = Playfair(_WIKI_KEY)
        assert cipher.encrypt(b"HI") == cipher.encrypt(b"HJ")

    def test_key_with_j_normalises(self) -> None:
        # Key containing J is equivalent to key with I in same position
        assert Playfair(b"JOHN").encrypt(b"ABCD") == Playfair(b"IOHN").encrypt(b"ABCD")

    def test_key_spaces_ignored(self) -> None:
        # Non-alpha chars in the key are silently skipped
        assert Playfair(b"KEY WORD").encrypt(b"ABCD") == Playfair(b"KEYWORD").encrypt(b"ABCD")

    def test_repeated_pair_inserts_filler(self) -> None:
        # "LL" gets X inserted: encrypt(L, X), then encrypt(L, ...)
        result = Playfair(b"KEY").encrypt(b"BALLOON").as_bytes()
        # Output has 8 letters (7 input + 1 inserted X → 4 pairs)
        letters = bytes(b for b in result if 65 <= b <= 90 or 97 <= b <= 122)
        assert len(letters) == 8

    def test_odd_length_padded(self) -> None:
        # Odd number of letters → X appended to form last pair
        result = Playfair(b"KEY").encrypt(b"ABC").as_bytes()
        letters = bytes(b for b in result if 65 <= b <= 90 or 97 <= b <= 122)
        assert len(letters) == 4

    def test_case_preserved(self) -> None:
        upper = Playfair(_WIKI_KEY).encrypt(b"HIDETHEGOLD").as_bytes()
        lower = Playfair(_WIKI_KEY).encrypt(b"hidethegold").as_bytes()
        assert upper == upper.upper()
        assert lower == lower.lower()

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValueError, match="letter"):
            Playfair(b"")

    def test_non_alpha_only_key_raises(self) -> None:
        with pytest.raises(ValueError, match="letter"):
            Playfair(b"123 !")
