from hordekit.core.result import HordeResult
from hordekit.crypto.classical.substitution.caesar import Caesar


class TestHordeResult:
    def test_as_bytes(self) -> None:
        r = HordeResult(b"hello")
        assert r.as_bytes() == b"hello"

    def test_as_str(self) -> None:
        r = HordeResult(b"hello")
        assert r.as_str() == "hello"

    def test_as_hex(self) -> None:
        r = HordeResult(b"\x00\xff")
        assert r.as_hex() == "00ff"

    def test_as_base64(self) -> None:
        r = HordeResult(b"hello")
        assert r.as_base64() == "aGVsbG8="

    def test_as_int(self) -> None:
        r = HordeResult(b"\x01\x00")
        assert r.as_int() == 256

    def test_as_int_little_endian(self) -> None:
        r = HordeResult(b"\x01\x00")
        assert r.as_int(byteorder="little") == 1

    def test_equality_with_result(self) -> None:
        assert HordeResult(b"abc") == HordeResult(b"abc")
        assert HordeResult(b"abc") != HordeResult(b"xyz")

    def test_equality_with_bytes(self) -> None:
        assert HordeResult(b"abc") == b"abc"

    def test_bytes_conversion(self) -> None:
        r = HordeResult(b"data")
        assert bytes(r) == b"data"

    def test_metadata(self) -> None:
        r = HordeResult(b"data", metadata={"key": "value"})
        assert r.metadata["key"] == "value"

    def test_metadata_defaults_empty(self) -> None:
        r = HordeResult(b"data")
        assert r.metadata == {}

    def test_pipe(self) -> None:
        # pipe calls run() which is encrypt; shift=23 is the inverse of shift=3
        result = HordeResult(b"Khoor").pipe(Caesar, shift=23)
        assert result.as_str() == "Hello"

    def test_repr(self) -> None:
        r = HordeResult(b"hi")
        assert "HordeResult" in repr(r)
