import pytest

from hordekit.crypto.classical.substitution.hill import Hill

# 2×2 verified example
# Key K = [[3,3],[2,5]]
# HELP → H=7,E=4 → [3*7+3*4, 2*7+5*4]=[33,34]%26=[7,8]=H,I
#         L=11,P=15 → [3*11+3*15,2*11+5*15]=[78,97]%26=[0,19]=A,T
_K2 = [[3, 3], [2, 5]]
_PT2 = b"HELP"
_CT2 = b"HIAT"

# 3×3 verified example (Wikipedia key)
# Key K = [[6,24,1],[13,16,10],[20,17,15]]
# ACT → POH  (verified against Wikipedia)
# FOO → QNC  (computed manually)
# BAZ → FDF  (computed manually)
_K3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
_PT3 = b"ACTFOOBAZ"
_CT3 = b"POHQNCFDF"


class TestHill:
    # ── encryption ──────────────────────────────────────────────────────────

    def test_encrypt_2x2(self) -> None:
        assert Hill(_K2).encrypt(_PT2).as_bytes() == _CT2

    def test_encrypt_3x3(self) -> None:
        assert Hill(_K3).encrypt(_PT3).as_bytes() == _CT3

    # ── decryption ──────────────────────────────────────────────────────────

    def test_decrypt_2x2(self) -> None:
        assert Hill(_K2).decrypt(_CT2).as_bytes() == _PT2

    def test_decrypt_3x3(self) -> None:
        assert Hill(_K3).decrypt(_CT3).as_bytes() == _PT3

    # ── roundtrip ───────────────────────────────────────────────────────────

    def test_roundtrip_2x2(self) -> None:
        cipher = Hill(_K2)
        for pt in (b"HELLOWORLD", b"ABCDEFGH", b"HORDEKIT"):
            assert cipher.decrypt(cipher.encrypt(pt).as_bytes()) == pt

    def test_roundtrip_3x3(self) -> None:
        # Inputs must be exact multiples of 3 (otherwise X-padding makes roundtrip lossy)
        cipher = Hill(_K3)
        for pt in (b"ACTFOOBAZ", b"ACTPOHGHI", b"CRYPTOSYS"):
            assert cipher.decrypt(cipher.encrypt(pt).as_bytes()) == pt

    def test_roundtrip_lowercase(self) -> None:
        cipher = Hill(_K2)
        assert cipher.decrypt(cipher.encrypt(b"help").as_bytes()) == b"help"

    # ── non-alpha pass-through ───────────────────────────────────────────────

    def test_non_alpha_unchanged(self) -> None:
        # spaces preserved between blocks
        result = Hill(_K2).encrypt(b"HE LP").as_bytes()
        assert result == Hill(_K2).encrypt(b"HE").as_bytes() + b" " + Hill(_K2).encrypt(b"LP").as_bytes()

    def test_digits_punctuation_unchanged(self) -> None:
        result = Hill(_K2).encrypt(b"HE!1LP").as_bytes()
        assert result[2:4] == b"!1"

    def test_case_preserved(self) -> None:
        upper = Hill(_K2).encrypt(b"HELP").as_bytes()
        lower = Hill(_K2).encrypt(b"help").as_bytes()
        assert upper == upper.upper()
        assert lower == lower.lower()

    # ── padding ─────────────────────────────────────────────────────────────

    def test_odd_block_padded_2x2(self) -> None:
        # 3 letters → last block padded with X → 4 letters out
        result = Hill(_K2).encrypt(b"HEL").as_bytes()
        assert len(result) == 4

    def test_odd_block_padded_3x3(self) -> None:
        # 4 letters → last block needs 2 X pads → 6 letters out
        result = Hill(_K3).encrypt(b"ABCD").as_bytes()
        assert len(result) == 6

    # ── invalid parameters ───────────────────────────────────────────────────

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Hill([])

    def test_non_square_key_raises(self) -> None:
        with pytest.raises(ValueError, match="square"):
            Hill([[1, 2, 3], [4, 5, 6]])

    def test_out_of_range_entry_raises(self) -> None:
        with pytest.raises(ValueError, match=r"\[0, 25\]"):
            Hill([[3, 3], [2, 26]])

    def test_singular_key_raises(self) -> None:
        # [[2,4],[3,6]] has det=2*6-4*3=0, gcd(0,26)=26 → not invertible
        with pytest.raises(ValueError, match="invertible"):
            Hill([[2, 4], [3, 6]])

    def test_key_with_gcd_not_1_raises(self) -> None:
        # [[2,0],[0,2]] has det=4, gcd(4,26)=2 → not invertible mod 26
        with pytest.raises(ValueError, match="invertible"):
            Hill([[2, 0], [0, 2]])
