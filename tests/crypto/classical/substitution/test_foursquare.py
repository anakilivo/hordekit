import pytest

from hordekit.crypto.classical.substitution.foursquare import FourSquare

# Four-square with key1="EXAMPLE", key2="KEYWORD" (I=J merged).
#
# Plaintext squares (top-left & bottom-right) — standard alphabet, J shares I:
#   A B C D E
#   F G H I K
#   L M N O P
#   Q R S T U
#   V W X Y Z
#
# Ciphertext square 1 (top-right) — key "EXAMPLE":
#   E X A M P
#   L B C D F
#   G H I K N
#   O Q R S T
#   U V W Y Z
#
# Ciphertext square 2 (bottom-left) — key "KEYWORD":
#   K E Y W O
#   R D A B C
#   F G H I L
#   M N P Q S
#   T U V X Z
#
# Encrypt digraph (a, b): a@(r1,c1) in top-left, b@(r2,c2) in bottom-right;
# ciphertext = (cipher1[r1][c2], cipher2[r2][c1]).
#   HE -> H(1,2) E(0,4) -> cipher1[1][4]=F, cipher2[0][2]=Y -> FY
#   LP -> L(2,0) P(2,4) -> cipher1[2][4]=N, cipher2[2][0]=F -> NF
#   ME -> M(2,1) E(0,4) -> cipher1[2][4]=N, cipher2[0][1]=E -> NE
_KEY1 = b"EXAMPLE"
_KEY2 = b"KEYWORD"
_PLAINTEXT = b"HELPME"
_CIPHERTEXT = b"FYNFNE"


class TestFourSquare:
    def test_encrypt(self) -> None:
        result = FourSquare(_KEY1, _KEY2).encrypt(_PLAINTEXT).as_bytes()
        assert result == _CIPHERTEXT

    def test_decrypt(self) -> None:
        result = FourSquare(_KEY1, _KEY2).decrypt(_CIPHERTEXT).as_bytes()
        assert result == _PLAINTEXT

    def test_roundtrip(self) -> None:
        # Even-length input with no J round-trips exactly
        plaintext = b"ATTACKATDAWN"
        cipher = FourSquare(b"SECRET", b"KEYWORD")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_roundtrip_lowercase(self) -> None:
        plaintext = b"defendtheeast"  # odd length -> X pad survives roundtrip
        cipher = FourSquare(b"alpha", b"bravo")
        decrypted = cipher.decrypt(cipher.encrypt(plaintext).as_bytes()).as_bytes()
        assert decrypted == plaintext + b"x"

    def test_repeated_letters_need_no_filler(self) -> None:
        # Unlike Playfair, "LL" is a valid digraph (each letter in its own square)
        result = FourSquare(_KEY1, _KEY2).encrypt(b"LL").as_bytes()
        letters = bytes(b for b in result if 65 <= b <= 90 or 97 <= b <= 122)
        assert len(letters) == 2

    def test_odd_length_padded(self) -> None:
        # Odd number of letters -> X appended to form the last pair
        result = FourSquare(_KEY1, _KEY2).encrypt(b"ABC").as_bytes()
        letters = bytes(b for b in result if 65 <= b <= 90 or 97 <= b <= 122)
        assert len(letters) == 4

    def test_non_alpha_unchanged(self) -> None:
        # Space preserved between encrypted pairs
        result = FourSquare(_KEY1, _KEY2).encrypt(b"HE LP").as_bytes()
        assert result == b"FY NF"

    def test_non_alpha_roundtrip(self) -> None:
        cipher = FourSquare(_KEY1, _KEY2)
        plaintext = b"HE LP ME"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_digits_and_punctuation_unchanged(self) -> None:
        result = FourSquare(_KEY1, _KEY2).encrypt(b"HE!12LP").as_bytes()
        assert result[2:5] == b"!12"

    def test_case_preserved(self) -> None:
        upper = FourSquare(_KEY1, _KEY2).encrypt(b"HELPME").as_bytes()
        lower = FourSquare(_KEY1, _KEY2).encrypt(b"helpme").as_bytes()
        assert upper == upper.upper()
        assert lower == lower.lower()

    def test_j_treated_as_i(self) -> None:
        # J and I share a cell, so a digraph with J encrypts like one with I
        cipher = FourSquare(_KEY1, _KEY2)
        assert cipher.encrypt(b"JE") == cipher.encrypt(b"IE")

    def test_key_with_j_normalises(self) -> None:
        # A key containing J is equivalent to the same key with I
        assert FourSquare(b"JOHN", b"KEY").encrypt(b"ABCD") == FourSquare(b"IOHN", b"KEY").encrypt(b"ABCD")

    def test_key_spaces_ignored(self) -> None:
        # Non-alpha chars in a key are silently skipped
        assert FourSquare(b"KEY WORD", b"FOO").encrypt(b"ABCD") == FourSquare(b"KEYWORD", b"FOO").encrypt(b"ABCD")

    def test_different_keys_differ(self) -> None:
        assert FourSquare(b"EXAMPLE", b"KEYWORD").encrypt(_PLAINTEXT) != FourSquare(b"OTHER", b"KEYS").encrypt(
            _PLAINTEXT
        )

    def test_invalid_key1_raises(self) -> None:
        with pytest.raises(ValueError, match="key1 must contain at least one ASCII letter"):
            FourSquare(b"123 !", b"KEY")

    def test_invalid_key2_raises(self) -> None:
        with pytest.raises(ValueError, match="key2 must contain at least one ASCII letter"):
            FourSquare(b"KEY", b"")
