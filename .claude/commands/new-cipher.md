Add a new cipher to hordekit. Arguments: $ARGUMENTS

Format: `cipher-name category`
Examples: `playfair substitution`, `railfence transposition`, `xor`

---

Follow these steps exactly:

## 1. Implementation

Create `hordekit/crypto/classical/{category}/{name}.py`:

```python
from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult

class {ClassName}(BaseCipher):
    def __init__(self, ...) -> None: ...
    def encrypt(self, data: bytes) -> HordeResult: ...
    def decrypt(self, data: bytes) -> HordeResult: ...
    
    # Only if keyspace is enumerable (< ~10^6):
    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]: ...
```

Rules:
- Work with raw `bytes`, never `str` internally
- Return `HordeResult(result_bytes)` — never raw bytes
- Preserve non-target bytes unchanged (letters-only ciphers pass through spaces, digits, etc.)
- `possible_keys()` returns list of kwargs dicts, e.g. `[{"shift": 1}, {"shift": 2}, ...]`

## 2. Register

Add to `hordekit/crypto/classical/{category}/__init__.py`:
```python
from hordekit.crypto.classical.{category}.{name} import {ClassName}
```

Add `{ClassName}` to `__all__`.

Also propagate up to `hordekit/crypto/classical/__init__.py` and `hordekit/crypto/__init__.py`.

## 3. Tests

Create `tests/crypto/classical/{category}/test_{name}.py`. Cover:
- `test_encrypt` — known plaintext/ciphertext pair (use a verified source)
- `test_decrypt` — reverse of above
- `test_roundtrip` — `decrypt(encrypt(data)) == data` with varied input
- `test_non_alpha_unchanged` — spaces, digits, punctuation pass through (if applicable)
- `test_invalid_params_raise` — bad key/params raise `ValueError` with clear message
- `test_possible_keys_count` — if `possible_keys()` is implemented

Run tests after creating them. All must pass before proceeding.

## 4. Documentation

Create `docs/crypto/classical/{category}/{name}.md` following the structure in `docs/cipher-template.md`.

The Mermaid diagram must show:
- The per-byte transformation logic (flowchart)
- A concrete letter-by-letter example (at least 4-5 chars)

## 5. Update mkdocs.yml nav

Add the new page under the correct section in `mkdocs.yml`.

## 6. Run ruff

After all files are created and tests pass, always run:

```bash
uv run ruff format hordekit/ tests/
uv run ruff check --fix hordekit/ tests/
```

Fix any remaining ruff errors before finishing. Do not skip this step.

---

After finishing, report:
- Files created
- Test results (N passed)
- Ruff output (clean or issues fixed)
- Import path: `from hordekit.crypto.classical.{category} import {ClassName}`
