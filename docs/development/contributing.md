# Contributing to Hordekit

Thank you for your interest in contributing to Hordekit! This guide will help you get started.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anakilivo/hordekit.git
   cd hordekit
   ```

2. **Install development dependencies:**
   ```bash
   uv sync --dev
   ```

3. **Run tests to ensure everything works:**
   ```bash
   make check
   ```

## Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks with:
```bash
make check
```

## Adding New Algorithms

### 1. Create the Algorithm Class

Create a new file in the appropriate directory:

```python
# hordekit/crypto/symmetric/substitution/my_cipher.py
from hordekit.crypto.symmetric.substitution.base_substitution import BaseSubstitutionCipher

class MyCipher(BaseSubstitutionCipher):
    """My custom substitution cipher."""
    
    SUPPORTED_ATTACK_METHODS = [
        AttackMethod.BRUTE_FORCE,
        AttackMethod.FREQUENCY_ANALYSIS,
    ]
    
    def _validate_parameters(self, **kwargs):
        # Validate your parameters
        pass
    
    def _create_mappings(self):
        # Create translation tables
        pass
    
    @classmethod
    def _get_possible_keys(cls):
        # Return all possible keys
        return [{"key": value}]
    
    @classmethod
    def _key_to_string(cls, key):
        # Convert key to string
        return str(key["key"])
```

### 2. Add Tests

Create comprehensive tests:

```python
# tests/crypto/symmetric/substitution/test_my_cipher.py
from tests.base_crypto_test import BaseCryptoTest
from hordekit.crypto.symmetric.substitution.my_cipher import MyCipher

class TestMyCipher(BaseCryptoTest):
    algorithm_class = MyCipher
    valid_parameters = {"key": "value"}
    invalid_parameters = [{"invalid": "param"}]
    
    def test_basic_encryption_decryption(self):
        # Test basic functionality
        pass
    
    def test_attack_methods(self):
        # Test attack methods
        pass
```

### 3. Add Documentation

Create detailed documentation:

```markdown
# docs/crypto/symmetric/substitution/my_cipher.md
# My Cipher

## History
...

## Concept
...

## Implementation
...
```

### 4. Add Demo

Create a demonstration script:

```python
# demo/demo_my_cipher.py
#!/usr/bin/env python3
"""Demo of My Cipher implementation."""

from hordekit.crypto.symmetric.substitution.my_cipher import MyCipher

def demo_basic_usage():
    # Basic usage demo
    pass

if __name__ == "__main__":
    demo_basic_usage()
```

## Testing Guidelines

### Test Structure

- Inherit from `BaseCryptoTest`
- Define `algorithm_class`, `valid_parameters`, `invalid_parameters`
- Override specific tests as needed

### Test Coverage

- Basic encryption/decryption
- Parameter validation
- Error handling
- Attack methods
- Edge cases (empty strings, non-alphabetic characters)
- Case preservation

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/crypto/symmetric/substitution/test_my_cipher.py -v

# Run with coverage
uv run pytest tests/ --cov=hordekit --cov-report=html
```

## Documentation Guidelines

### Algorithm Documentation

Each algorithm should have:

1. **History**: Historical context and background
2. **Concept**: Mathematical foundation
3. **Implementation**: How it works
4. **Security Analysis**: Strengths and weaknesses
5. **Code Examples**: Practical usage

### API Documentation

- Clear parameter descriptions
- Return value explanations
- Usage examples
- Error conditions

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-cipher
   ```

2. **Make your changes:**
   - Add the algorithm implementation
   - Add comprehensive tests
   - Add documentation
   - Add demo script

3. **Run quality checks:**
   ```bash
   make check
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add My Cipher algorithm"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/my-cipher
   ```

## Code Review Guidelines

### What We Look For

- **Correctness**: Algorithm implementation is mathematically sound
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear and complete documentation
- **Code Quality**: Follows style guidelines
- **Security**: Proper handling of sensitive operations

### Review Checklist

- [ ] Algorithm implementation is correct
- [ ] Tests cover all functionality
- [ ] Documentation is complete and accurate
- [ ] Code follows style guidelines
- [ ] No security issues (bandit passes)
- [ ] Type hints are correct (mypy passes)

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Code Review**: Ask questions in PR comments

## License

By contributing to Hordekit, you agree that your contributions will be licensed under the MIT License. 