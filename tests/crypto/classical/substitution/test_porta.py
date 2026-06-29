import pytest

from hordekit.crypto.classical.substitution.porta import Porta

# Della Porta tableau (key letters paired; row = key_letter // 2):
#   KEY | A B C D E F G H I J K L M
#   ----+---------------------------
#   A,B | N O P Q R S T U V W X Y Z
#   C,D | O P Q R S T U V W X Y Z N
#   E,F | P Q R S T U V W X Y Z N O   (row 2)
#   ...
#   K,L | S T U V W X Y Z N O P Q R   (row 5)
#   ...
#   Y,Z | Z N O P Q R S T U V W X Y   (row 12)
# Each row is reciprocal: A–M map to N–Z and vice versa.
#
# Plaintext "HELLO" with key "KEY" (rows: K->5, E->2, Y->12, K->5, E->2):
#   H(7)  row 5  -> (7+5)%13+13  = 25 -> Z
#   E(4)  row 2  -> (4+2)%13+13  = 19 -> T
#   L(11) row 12 -> (11+12)%13+13= 23 -> X
#   L(11) row 5  -> (11+5)%13+13 = 16 -> Q
#   O(14) row 2  -> (14-13-2)%13 = 12 -> M
_KEY = b"KEY"
_PLAINTEXT = b"HELLO"
_CIPHERTEXT = b"ZTXQM"


class TestPorta:
    def test_encrypt(self) -> None:
        assert Porta(_KEY).encrypt(_PLAINTEXT).as_bytes() == _CIPHERTEXT

    def test_decrypt(self) -> None:
        # Reciprocal cipher: decrypting the ciphertext restores the plaintext
        assert Porta(_KEY).decrypt(_CIPHERTEXT).as_bytes() == _PLAINTEXT

    def test_encrypt_equals_decrypt(self) -> None:
        # Porta is an involution — encrypt and decrypt are the same operation
        assert Porta(_KEY).encrypt(_PLAINTEXT) == Porta(_KEY).decrypt(_PLAINTEXT)

    def test_roundtrip(self) -> None:
        plaintext = b"ATTACKATDAWN"
        cipher = Porta(b"LEMON")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_roundtrip_lowercase(self) -> None:
        plaintext = b"attackatdawn"
        cipher = Porta(b"lemon")
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_paired_key_letters_share_row(self) -> None:
        # A and B select the same alphabet, as do C and D, etc.
        assert Porta(b"A").encrypt(_PLAINTEXT) == Porta(b"B").encrypt(_PLAINTEXT)
        assert Porta(b"C").encrypt(_PLAINTEXT) == Porta(b"D").encrypt(_PLAINTEXT)

    def test_first_half_maps_to_second_half(self) -> None:
        # A–M always encrypt to N–Z and N–Z encrypt to A–M (any key)
        enc = Porta(b"A").encrypt(b"ABCM").as_bytes()
        assert all(78 <= b <= 90 for b in enc)  # all in N..Z
        enc2 = Porta(b"A").encrypt(b"NOPZ").as_bytes()
        assert all(65 <= b <= 77 for b in enc2)  # all in A..M

    def test_case_preserved(self) -> None:
        assert Porta(_KEY).encrypt(b"hello").as_bytes() == _CIPHERTEXT.lower()

    def test_non_alpha_unchanged(self) -> None:
        # Spaces/punctuation pass through; key only advances on letters
        result = Porta(_KEY).encrypt(b"HE LL O").as_bytes()
        assert result == b"ZT XQ M"

    def test_non_alpha_roundtrip(self) -> None:
        cipher = Porta(b"SECRET")
        plaintext = b"MEET ME AT DAWN!"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_digits_and_punctuation_unchanged(self) -> None:
        result = Porta(_KEY).encrypt(b"HE!12LL").as_bytes()
        assert result[2:5] == b"!12"

    def test_invalid_key_non_letter_raises(self) -> None:
        with pytest.raises(ValueError, match="only ASCII letters"):
            Porta(b"KE9Y")

    def test_invalid_key_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            Porta(b"")
