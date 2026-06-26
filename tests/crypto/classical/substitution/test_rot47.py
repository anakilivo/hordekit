from hordekit.crypto.classical.substitution.rot47 import ROT47


class TestROT47:
    def test_encrypt(self) -> None:
        assert ROT47().encrypt(b"Hello") == b"w6==@"

    def test_self_inverse(self) -> None:
        plaintext = b"Hello, World! 123"
        r = ROT47()
        assert r.decrypt(r.encrypt(plaintext).as_bytes()) == plaintext

    def test_non_printable_unchanged(self) -> None:
        result = ROT47().encrypt(b"\x00\x1f\x7f")
        assert result.as_bytes() == b"\x00\x1f\x7f"
