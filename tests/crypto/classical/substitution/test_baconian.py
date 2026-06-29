import pytest

from hordekit.crypto.classical.substitution.baconian import Baconian

# Modern 26-letter Baconian: code = letter index in MSB-first 5-bit binary.
#   A=00000=AAAAA ... Z=11001=BBAAB
#
# HELLO:
#   H=7  = 00111 -> AABBB
#   E=4  = 00100 -> AABAA
#   L=11 = 01011 -> ABABB
#   L=11 = 01011 -> ABABB
#   O=14 = 01110 -> ABBBA
_PLAINTEXT = b"HELLO"
_CIPHERTEXT = b"AABBBAABAAABABBABABBABBBA"


class TestBaconian:
    def test_encrypt(self) -> None:
        assert Baconian().encrypt(_PLAINTEXT).as_bytes() == _CIPHERTEXT

    def test_decrypt(self) -> None:
        assert Baconian().decrypt(_CIPHERTEXT).as_bytes() == _PLAINTEXT

    def test_corner_letters(self) -> None:
        assert Baconian().encrypt(b"A").as_bytes() == b"AAAAA"
        assert Baconian().encrypt(b"Z").as_bytes() == b"BBAAB"

    def test_roundtrip(self) -> None:
        plaintext = b"ATTACKATDAWN"
        cipher = Baconian()
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_roundtrip_lowercase_loses_case(self) -> None:
        # Output is a binary code, so case is not preserved
        cipher = Baconian()
        assert cipher.decrypt(cipher.encrypt(b"hello").as_bytes()) == b"HELLO"

    def test_non_alpha_unchanged(self) -> None:
        # Space passes through between encoded groups
        result = Baconian().encrypt(b"HI BYE").as_bytes()
        # H=AABBB I=ABAAA, space, B=AAAAB Y=BBAAA E=AABAA
        assert result == b"AABBBABAAA AAAABBBAAAAABAA"

    def test_non_alpha_roundtrip(self) -> None:
        cipher = Baconian()
        plaintext = b"MEET ME AT DAWN!"
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_digits_and_punctuation_unchanged(self) -> None:
        result = Baconian().encrypt(b"A!12").as_bytes()
        assert result == b"AAAAA!12"

    def test_custom_symbols(self) -> None:
        cipher = Baconian(zero=b"0", one=b"1")
        assert cipher.encrypt(b"A").as_bytes() == b"00000"
        assert cipher.encrypt(b"Z").as_bytes() == b"11001"

    def test_custom_symbols_roundtrip(self) -> None:
        cipher = Baconian(zero=b"0", one=b"1")
        assert cipher.decrypt(cipher.encrypt(b"HELLO").as_bytes()) == b"HELLO"

    def test_dangling_partial_group_preserved(self) -> None:
        # Fewer than 5 code symbols cannot form a letter — emitted unchanged
        assert Baconian().decrypt(b"AABBB" + b"AAB").as_bytes() == b"H" + b"AAB"

    def test_invalid_symbol_length_raises(self) -> None:
        with pytest.raises(ValueError, match="exactly one byte"):
            Baconian(zero=b"AB", one=b"C")

    def test_invalid_symbols_equal_raises(self) -> None:
        with pytest.raises(ValueError, match="different bytes"):
            Baconian(zero=b"A", one=b"A")
