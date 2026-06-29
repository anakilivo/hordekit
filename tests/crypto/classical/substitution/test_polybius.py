import pytest

from hordekit.crypto.classical.substitution.polybius import Polybius

# Standard 5×5 Polybius square (I/J merged), 1-indexed coordinates:
#      1  2  3  4  5
#   1  A  B  C  D  E
#   2  F  G  H  I  K      (J shares I's cell)
#   3  L  M  N  O  P
#   4  Q  R  S  T  U
#   5  V  W  X  Y  Z
#
# HELLO -> H=23 E=15 L=31 L=31 O=34
_PLAINTEXT = b"HELLO"
_CIPHERTEXT = b"2315313134"


class TestPolybius:
    def test_encrypt(self) -> None:
        result = Polybius().encrypt(_PLAINTEXT).as_bytes()
        assert result == _CIPHERTEXT

    def test_decrypt(self) -> None:
        result = Polybius().decrypt(_CIPHERTEXT).as_bytes()
        assert result == _PLAINTEXT

    def test_roundtrip(self) -> None:
        plaintext = b"ATTACKATDAWN"
        cipher = Polybius()
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_lowercase_maps_to_same_coordinates(self) -> None:
        # Case is lost on encryption — both cases yield identical digits
        assert Polybius().encrypt(b"hello") == Polybius().encrypt(b"HELLO")

    def test_decrypt_outputs_uppercase(self) -> None:
        assert Polybius().decrypt(Polybius().encrypt(b"hello").as_bytes()) == b"HELLO"

    def test_j_treated_as_i(self) -> None:
        # J and I share a cell, so they encode identically
        assert Polybius().encrypt(b"J") == Polybius().encrypt(b"I")
        assert Polybius().encrypt(b"I").as_bytes() == b"24"

    def test_corner_letters(self) -> None:
        assert Polybius().encrypt(b"A").as_bytes() == b"11"
        assert Polybius().encrypt(b"E").as_bytes() == b"15"
        assert Polybius().encrypt(b"V").as_bytes() == b"51"
        assert Polybius().encrypt(b"Z").as_bytes() == b"55"

    def test_non_alpha_unchanged(self) -> None:
        # Spaces and punctuation pass through, preserving relative position
        result = Polybius().encrypt(b"A B").as_bytes()
        assert result == b"11 12"

    def test_non_alpha_roundtrip(self) -> None:
        cipher = Polybius()
        plaintext = b"HI THERE!"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_keyed_square_differs_from_standard(self) -> None:
        keyed = Polybius(b"KEYWORD").encrypt(_PLAINTEXT)
        assert keyed != Polybius().encrypt(_PLAINTEXT)

    def test_keyed_roundtrip(self) -> None:
        cipher = Polybius(b"SECRET KEY")
        plaintext = b"DEFENDTHEEASTWALL"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_keyed_square_layout(self) -> None:
        # Key "PLAYFAIR" fills first cells: P L A Y F I R, then remaining alphabet.
        # P -> row 0, col 0 -> "11"
        assert Polybius(b"PLAYFAIR").encrypt(b"P").as_bytes() == b"11"

    def test_empty_key_is_standard_square(self) -> None:
        assert Polybius(b"").encrypt(_PLAINTEXT) == Polybius().encrypt(_PLAINTEXT)

    def test_dangling_coordinate_digit_preserved(self) -> None:
        # A lone trailing row digit has no column — it is emitted unchanged
        assert Polybius().decrypt(b"23" + b"1").as_bytes() == b"H1"

    def test_invalid_params_raise(self) -> None:
        with pytest.raises(ValueError, match="letter"):
            Polybius(b"123 !")
