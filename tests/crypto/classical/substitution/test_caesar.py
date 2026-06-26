from hordekit.crypto.classical.substitution.caesar import Caesar


class TestCaesar:
    def test_encrypt_basic(self) -> None:
        assert Caesar(shift=3).encrypt(b"Hello") == b"Khoor"

    def test_decrypt_basic(self) -> None:
        assert Caesar(shift=3).decrypt(b"Khoor") == b"Hello"

    def test_roundtrip(self) -> None:
        plaintext = b"The quick brown fox"
        cipher = Caesar(shift=7)
        assert cipher.decrypt(cipher.encrypt(plaintext).as_bytes()) == plaintext

    def test_preserves_case(self) -> None:
        result = Caesar(shift=1).encrypt(b"aAbBzZ")
        assert result.as_str() == "bBcCaA"

    def test_non_alpha_unchanged(self) -> None:
        result = Caesar(shift=3).encrypt(b"Hello, World! 123")
        assert result.as_str() == "Khoor, Zruog! 123"

    def test_shift_wraps(self) -> None:
        assert Caesar(shift=26).encrypt(b"abc") == b"abc"
        assert Caesar(shift=27).encrypt(b"abc") == Caesar(shift=1).encrypt(b"abc")

    def test_possible_keys_count(self) -> None:
        keys = Caesar.possible_keys()
        assert len(keys) == 25
        assert all("shift" in k for k in keys)

    def test_pipe_chaining(self) -> None:
        from hordekit.crypto.classical.substitution.caesar import Caesar as C

        result = Caesar(shift=3).encrypt(b"Hello").pipe(C, shift=23)
        assert result.as_str() == "Hello"
