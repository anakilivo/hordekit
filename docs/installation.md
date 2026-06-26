# Installation

## Requirements

- Python 3.11 or higher
- pip or uv

## Install

=== "pip"

    ```bash
    pip install hordekit
    ```

=== "uv"

    ```bash
    uv add hordekit
    ```

## From source

```bash
git clone https://github.com/anakilivo/hordekit.git
cd hordekit
uv sync --dev
```

## Verify

```python
from hordekit.crypto.classical.substitution import Caesar

result = Caesar(shift=3).encrypt(b"Hello")
print(result.as_str())   # Khoor
```

## Dev dependencies

```bash
uv sync --dev
```

Includes:

| Tool | Purpose |
|------|---------|
| `ruff` | Linting + formatting |
| `mypy` | Type checking |
| `bandit` | Security scanning |
| `pytest` + `pytest-cov` | Tests |
| `mkdocs` + `mkdocs-material` | Documentation |

## Troubleshooting

**Import error** — check Python version: `python --version` (must be 3.11+)

**uv not found** — install it first: `pip install uv`
