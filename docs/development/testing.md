# Testing Guide

This guide covers the testing infrastructure and best practices for Hordekit.

## Test Structure

### Base Test Class

All algorithm tests inherit from `BaseCryptoTest`:

```python
from tests.base_crypto_test import BaseCryptoTest

class TestMyAlgorithm(BaseCryptoTest):
    algorithm_class = MyAlgorithm
    valid_parameters = {"param1": "value1"}
    invalid_parameters = [{"invalid": "param"}]
```

### Required Attributes

- `algorithm_class`: The algorithm class to test
- `valid_parameters`: Valid parameters for the algorithm
- `invalid_parameters`: List of invalid parameter sets

### Automatic Tests

The base class provides these tests automatically:

- `test_basic_encryption_decryption`: Tests encode/decode functionality
- `test_parameter_validation`: Tests parameter validation
- `test_attack_methods_availability`: Tests attack method availability
- `test_algorithm_inheritance`: Tests proper inheritance
- `test_abstract_methods_implementation`: Tests required methods
- `test_algorithm_consistency`: Tests deterministic behavior
- `test_error_messages`: Tests error message quality
- `test_algorithm_properties`: Tests basic properties

## Running Tests

### All Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=hordekit --cov-report=html
```

### Specific Tests

```bash
# Run specific test file
uv run pytest tests/crypto/symmetric/substitution/test_caesar.py -v

# Run specific test class
uv run pytest tests/crypto/symmetric/substitution/test_caesar.py::TestCaesarCipher -v

# Run specific test method
uv run pytest tests/crypto/symmetric/substitution/test_caesar.py::TestCaesarCipher::test_basic_encryption_decryption -v
```

### Test Categories

```bash
# Run only unit tests
uv run pytest tests/ -m "not integration"

# Run only integration tests
uv run pytest tests/ -m "integration"

# Run tests with specific markers
uv run pytest tests/ -m "slow"
```

## Writing Tests

### Basic Test Structure

```python
class TestMyAlgorithm(BaseCryptoTest):
    algorithm_class = MyAlgorithm
    valid_parameters = {"key": "value"}
    invalid_parameters = [{"invalid": "param"}]
    
    def test_specific_functionality(self):
        """Test specific algorithm functionality."""
        algorithm = self.algorithm_class(**self.valid_parameters)
        
        # Test encryption
        encrypted = algorithm.encode("test")
        assert encrypted is not None
        
        # Test decryption
        decrypted = algorithm.decode(encrypted)
        assert decrypted == "test"
    
    def test_attack_methods(self):
        """Test attack methods."""
        algorithm = self.algorithm_class(**self.valid_parameters)
        encrypted = algorithm.encode("test")
        
        # Test brute force attack
        results = algorithm.attack(AttackMethod.BRUTE_FORCE, ciphertext=encrypted)
        assert "all_results" in results
```

### Overriding Base Tests

```python
def test_parameter_validation(self):
    """Override parameter validation test for special cases."""
    # Custom validation logic
    algorithm = self.algorithm_class()
    assert algorithm is not None
```

### Custom Test Methods

```python
def test_algorithm_specific_feature(self):
    """Test algorithm-specific features."""
    algorithm = self.algorithm_class(**self.valid_parameters)
    
    # Test specific feature
    result = algorithm.specific_method()
    assert result == expected_value
```

## Test Data

### Using Faker

The base class uses Faker for generating random test data:

```python
def test_with_random_data(self):
    """Test with random strings."""
    fake = Faker()
    
    for _ in range(5):
        random_message = fake.text(max_nb_chars=50).strip()
        if random_message:
            encrypted = self.algorithm.encode(random_message)
            decrypted = self.algorithm.decode(encrypted)
            assert random_message == decrypted
```

### Parametrized Tests

Use `parametrize_from_file` for data-driven tests:

```python
import parametrize_from_file as pff

@pff.parametrize(path="test_data.yml", key="test_cases")
def test_with_data(self, plaintext: str, ciphertext: str, key: str):
    """Test with predefined data."""
    algorithm = self.algorithm_class(key=key)
    encrypted = algorithm.encode(plaintext)
    assert encrypted == ciphertext
```

### Test Data Files

Create YAML files for test data:

```yaml
# tests/data/test_my_algorithm.yml
test_cases:
  - plaintext: "HELLO"
    ciphertext: "KHOOR"
    key: "3"
  - plaintext: "WORLD"
    ciphertext: "ZRUOG"
    key: "3"
```

## Test Coverage

### Coverage Requirements

- **Unit Tests**: 90%+ line coverage
- **Integration Tests**: All public APIs
- **Edge Cases**: Empty strings, invalid parameters, etc.

### Coverage Report

```bash
# Generate HTML coverage report
uv run pytest tests/ --cov=hordekit --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Coverage Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=hordekit --cov-report=term-missing"
testpaths = ["tests"]
```

## Mocking and Stubbing

### Mocking External Dependencies

```python
from unittest.mock import patch

def test_with_mocked_dependency(self):
    """Test with mocked external dependency."""
    with patch('hordekit.crypto.utils.some_external_function') as mock_func:
        mock_func.return_value = "mocked_result"
        
        algorithm = self.algorithm_class()
        result = algorithm.method_that_uses_external_function()
        
        assert result == "expected_result"
        mock_func.assert_called_once()
```

### Stubbing Random Functions

```python
def test_deterministic_behavior(self):
    """Test deterministic behavior by stubbing random functions."""
    with patch('hordekit.crypto.symmetric.substitution.caesar.secrets.randbelow') as mock_rand:
        mock_rand.return_value = 2
        
        algorithm = CaesarCipher.generate_key()
        assert algorithm.shift == 3  # randbelow(25) + 1 = 3
```

## Performance Testing

### Benchmark Tests

```python
import time

def test_encryption_performance(self):
    """Test encryption performance."""
    algorithm = self.algorithm_class(**self.valid_parameters)
    test_data = "A" * 10000  # 10KB of data
    
    start_time = time.time()
    encrypted = algorithm.encode(test_data)
    end_time = time.time()
    
    duration = end_time - start_time
    assert duration < 1.0  # Should complete within 1 second
```

### Memory Usage Tests

```python
import psutil
import os

def test_memory_usage(self):
    """Test memory usage during encryption."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    algorithm = self.algorithm_class(**self.valid_parameters)
    large_data = "A" * 100000  # 100KB of data
    
    encrypted = algorithm.encode(large_data)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    assert memory_increase < 1024 * 1024  # Less than 1MB increase
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:

- Push to main/develop branches
- Pull requests
- Release tags

### Pre-commit Hooks

Install pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Local Testing

Before committing, run:

```bash
# Run all quality checks
make check

# Run tests with coverage
uv run pytest tests/ --cov=hordekit --cov-report=html

# Run security checks
uv run bandit -r hordekit/
uv run safety scan
```

## Debugging Tests

### Verbose Output

```bash
# Run with verbose output
uv run pytest tests/ -v -s

# Run with maximum verbosity
uv run pytest tests/ -vvv -s
```

### Debugging Specific Tests

```python
def test_debug_example(self):
    """Example of debugging a test."""
    algorithm = self.algorithm_class(**self.valid_parameters)
    
    # Add debug prints
    print(f"Algorithm: {algorithm}")
    print(f"Parameters: {self.valid_parameters}")
    
    encrypted = algorithm.encode("test")
    print(f"Encrypted: {encrypted}")
    
    # Use pdb for interactive debugging
    import pdb; pdb.set_trace()
    
    decrypted = algorithm.decode(encrypted)
    assert decrypted == "test"
```

### Test Isolation

```python
@pytest.fixture(autouse=True)
def setup_and_teardown(self):
    """Setup and teardown for each test."""
    # Setup
    yield
    # Teardown
    pass
``` 