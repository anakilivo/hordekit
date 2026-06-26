# Testing

## Running tests

```bash
make test                                                    # all tests
uv run pytest tests/ -v                                      # verbose
uv run pytest tests/crypto/ -v                               # specific module
uv run pytest -k "caesar" -v                                 # filter by name
uv run pytest tests/ --cov=hordekit --cov-report=html        # with coverage
```

## Structure

Tests mirror the source tree:

```
tests/
├── core/
│   └── test_result.py
└── crypto/
    ├── classical/substitution/
    │   ├── test_caesar.py
    │   ├── test_rot13.py
    │   ├── test_rot47.py
    │   ├── test_atbash.py
    │   ├── test_affine.py
    │   └── test_vigenere.py
    └── attacks/
        └── test_brute_force.py
```

## What to test for each cipher

```python
class TestMyCipher:
    def test_encrypt(self) -> None:
        # known plaintext/ciphertext pair from a verified source
        assert MyCipher(...).encrypt(b"HELLO") == b"XXXXX"

    def test_decrypt(self) -> None:
        assert MyCipher(...).decrypt(b"XXXXX") == b"HELLO"

    def test_roundtrip(self) -> None:
        cipher = MyCipher(...)
        assert cipher.decrypt(cipher.encrypt(b"test data").as_bytes()) == b"test data"

    def test_non_alpha_unchanged(self) -> None:
        result = MyCipher(...).encrypt(b"A1 !z")
        assert result.as_bytes()[1] == ord("1")   # digit unchanged

    def test_invalid_params_raise(self) -> None:
        with pytest.raises(ValueError):
            MyCipher(invalid_param=...)

    def test_possible_keys_count(self) -> None:
        keys = MyCipher.possible_keys()
        assert len(keys) == EXPECTED_COUNT
```
