# Installation

## Requirements

- Python 3.9 or higher
- pip or uv package manager

## Installation Methods

### Using pip

```bash
pip install hordekit
```

### Using uv (Recommended)

```bash
uv add hordekit
```

### From Source

If you want to install from the latest development version:

```bash
git clone https://github.com/anakilivo/hordekit.git
cd hordekit
pip install -e .
```

Or with uv:

```bash
git clone https://github.com/anakilivo/hordekit.git
cd hordekit
uv sync --dev
```

## Development Installation

For development and contributing:

```bash
git clone https://github.com/anakilivo/hordekit.git
cd hordekit
uv sync --dev
```

This will install all development dependencies including:

- Testing tools (pytest, faker)
- Code quality tools (black, isort, flake8, mypy)
- Security tools (bandit, safety)
- Documentation tools (mkdocs)

## Verification

To verify the installation, run:

```python
from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

caesar = CaesarCipher(shift=3)
result = caesar.encode("HELLO")
print(result)  # Should print: KHOOR
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're using Python 3.9+
2. **Permission Error**: Use `pip install --user` or a virtual environment
3. **uv not found**: Install uv first: `pip install uv`

### Virtual Environment

We recommend using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Install hordekit
pip install hordekit
``` 