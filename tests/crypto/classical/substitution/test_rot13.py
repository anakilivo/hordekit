from hordekit.crypto.classical.substitution.rot13 import ROT13


class TestROT13:
    def test_encrypt(self) -> None:
        assert ROT13().encrypt(b"Hello") == b"Uryyb"

    def test_self_inverse(self) -> None:
        plaintext = b"Hello, World!"
        r = ROT13()
        assert r.decrypt(r.encrypt(plaintext).as_bytes()) == plaintext
        assert r.encrypt(r.encrypt(plaintext).as_bytes()) == plaintext

    def test_possible_keys(self) -> None:
        assert ROT13.possible_keys() == [{}]
