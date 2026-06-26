from hordekit.crypto.classical.substitution.atbash import Atbash


class TestAtbash:
    def test_encrypt(self) -> None:
        assert Atbash().encrypt(b"Hello") == b"Svool"

    def test_self_inverse(self) -> None:
        plaintext = b"Hello, World!"
        a = Atbash()
        assert a.decrypt(a.encrypt(plaintext).as_bytes()) == plaintext

    def test_non_alpha_unchanged(self) -> None:
        result = Atbash().encrypt(b"A1z!")
        assert result.as_str() == "Z1a!"
