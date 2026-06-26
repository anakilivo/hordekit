# Contributing

## Setup

```bash
git clone https://github.com/anakilivo/hordekit.git
cd hordekit
uv sync --dev
```

## Adding a new cipher

Use the `/new-cipher` slash command in Claude Code:

```
/new-cipher playfair substitution
```

It will create the implementation, tests, docs, and register everything automatically.

If you prefer doing it manually, follow the structure of an existing cipher like `hordekit/crypto/classical/substitution/caesar.py`.

**Rules:**
- Extend `BaseCipher` from `hordekit.core`
- Return `HordeResult` from `encrypt()` and `decrypt()`
- Work with raw `bytes`, never `str` internally
- Pass non-target bytes through unchanged
- Implement `possible_keys()` if the keyspace is enumerable

## Quality checks

```bash
make check        # format + lint + type-check + security + tests
make format       # ruff format + fix
make lint         # ruff check (no autofix)
make type-check   # mypy
make security     # bandit
make test         # pytest
```

All checks must pass before submitting a PR.

## Pull request checklist

- [ ] Implementation follows `BaseCipher` interface
- [ ] Tests cover encrypt, decrypt, roundtrip, edge cases
- [ ] Documentation has Mermaid diagrams (see `docs/cipher-template.md`)
- [ ] `ruff`, `mypy`, `bandit` all pass
- [ ] Added to `mkdocs.yml` nav
