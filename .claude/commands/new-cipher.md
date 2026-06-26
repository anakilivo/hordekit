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

The **Known Attacks** section must use Markdown links to the attack docs — not just module names:

```markdown
## Known Attacks

| Attack | When applicable |
|--------|----------------|
| [Brute Force](../../attacks/generic/brute_force.md) | Always — N possible keys |
| [Frequency Analysis](../../attacks/substitution/frequency.md) | Ciphertext > ~100 characters |
```

Relative path from `docs/crypto/classical/{category}/` to attacks:
- `../../attacks/generic/brute_force.md`
- `../../attacks/generic/dictionary.md`
- `../../attacks/substitution/frequency.md`
- `../../attacks/substitution/ioc.md`
- `../../attacks/vigenere/kasiski.md`

## 5. Update mkdocs.yml nav

Add the cipher page under the correct section in `mkdocs.yml`.

If a **new attack** was created in step 6, also add it under the `Attacks:` section of the nav.

## 6. Attacks (if applicable)

If the cipher has a brute-forceable keyspace (`possible_keys()` implemented), it is automatically supported by `brute_force`. No extra work needed.

If the cipher is a **substitution cipher**, consider adding or verifying coverage in `hordekit/crypto/attacks/substitution/`:
- `frequency.py` — already covers monogram frequency analysis (works for any monoalphabetic cipher)
- `ioc.py` — already covers Index of Coincidence (detects poly vs. mono and estimates key length)

If the cipher is a **polyalphabetic substitution cipher** (like Vigenère-family):
- `hordekit/crypto/attacks/vigenere/kasiski.py` — Kasiski test already covers key-length estimation

If the cipher requires a **new** dedicated attack:
1. Create `hordekit/crypto/attacks/{category}/{attack_name}.py`
2. Export it from `hordekit/crypto/attacks/{category}/__init__.py`
3. Add to top-level `hordekit/crypto/attacks/__init__.py`
4. Write tests in `tests/crypto/attacks/test_{attack_name}.py`
5. Write docs in `docs/crypto/attacks/{category}/{attack_name}.md` — include:
   - Overview (what it detects/recovers, when to use)
   - Mermaid flowchart of the algorithm
   - API section with full example
   - "See also" links back to the cipher docs that are vulnerable to it
6. Add the doc to `mkdocs.yml` under `Attacks:`

## 7. Run ruff

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
- Attack coverage: which attacks apply (brute_force / frequency / ioc / kasiski / new)
