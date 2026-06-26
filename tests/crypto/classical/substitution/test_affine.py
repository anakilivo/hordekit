import pytest

from hordekit.crypto.classical.substitution.affine import Affine


class TestAffine:
    def test_encrypt(self) -> None:
        assert Affine(a=5, b=8).encrypt(b"AFFINECIPHER") == b"IHHWVCSWFRCP"

    def test_decrypt(self) -> None:
        assert Affine(a=5, b=8).decrypt(b"IHHWVCSWFRCP") == b"AFFINECIPHER"

    def test_roundtrip(self) -> None:
        plaintext = b"Hello World"
        cipher = Affine(a=7, b=3)
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_invalid_a_raises(self) -> None:
        with pytest.raises(ValueError, match="coprime"):
            Affine(a=2, b=0)

    def test_possible_keys_count(self) -> None:
        keys = Affine.possible_keys()
        assert len(keys) == 12 * 26

    def test_a1_b0_is_identity(self) -> None:
        assert Affine(a=1, b=0).encrypt(b"Hello") == b"Hello"
