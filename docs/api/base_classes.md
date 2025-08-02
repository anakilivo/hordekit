# Base Classes

## BaseSubstitutionCipher

Base class for all substitution ciphers that provides common functionality.

```python
from hordekit.crypto.symmetric.substitution.base_substitution import BaseSubstitutionCipher
```

### Features

- **Case Preservation**: Maintains original case of letters
- **Non-alphabetic Handling**: Preserves numbers, punctuation, and spaces
- **Efficient Translation**: Uses `str.translate()` for fast character mapping
- **Common Attack Methods**: Built-in brute force and frequency analysis

### Abstract Methods

Subclasses must implement:

- `_create_mappings()`: Create encryption/decryption translation tables
- `_get_possible_keys()`: Get all possible keys for this cipher
- `_key_to_string()`: Convert key dictionary to string representation

### Common Methods

#### _attack_brute_force(**kwargs)

Perform brute force attack on substitution cipher.

**Parameters:**
- `ciphertext`: Encrypted text to decrypt
- `mask`: Regular expression pattern to match successful decryption (optional)

**Returns:**
- Dictionary with all results and best match if mask provided

#### _attack_frequency_analysis(**kwargs)

Perform frequency analysis attack using n-gram scoring.

**Parameters:**
- `ciphertext`: Encrypted text to analyze

**Returns:**
- Dictionary with most likely key and confidence scores

### Example Implementation

```python
from hordekit.crypto.symmetric.substitution.base_substitution import BaseSubstitutionCipher

class MySubstitutionCipher(BaseSubstitutionCipher):
    def _create_mappings(self):
        # Create translation tables
        self.encrypt_table = str.maketrans(from_chars, to_chars)
        self.decrypt_table = str.maketrans(to_chars, from_chars)
    
    @classmethod
    def _get_possible_keys(cls):
        # Return all possible keys
        return [{"key1": value1}, {"key2": value2}]
    
    @classmethod
    def _key_to_string(cls, key):
        # Convert key to string
        return f"key={key['key1']}"
```

## Algorithm Hierarchy

```
CryptoAlgorithm (abstract base)
├── BaseSubstitutionCipher (abstract)
│   ├── CaesarCipher
│   ├── AffineCipher
│   └── AtbashCipher (inherits from AffineCipher)
└── [Future algorithm types]
```

### Inheritance Benefits

- **Code Reuse**: Common functionality shared across algorithms
- **Consistent API**: All algorithms follow the same interface
- **Easy Testing**: Common test infrastructure
- **Extensibility**: Easy to add new algorithms

### Translation Table Creation

The base class handles efficient character mapping:

```python
# Example: Caesar cipher with shift 3
from_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
to_chars = "DEFGHIJKLMNOPQRSTUVWXYZABCdefghijklmnopqrstuvwxyzabc"

encrypt_table = str.maketrans(from_chars, to_chars)
decrypt_table = str.maketrans(to_chars, from_chars)

# Usage
encrypted = text.translate(encrypt_table)
decrypted = text.translate(decrypt_table)
```

### Attack Method Implementation

The base class provides common attack implementations:

```python
# Brute force attack
results = cipher._attack_brute_force(ciphertext="KHOOR", mask=r"HELLO.*")

# Frequency analysis attack
analysis = cipher._attack_frequency_analysis(ciphertext="KHOOR ZRUOG")
```

### Key Management

Each algorithm defines its own key space:

```python
# Caesar cipher: 25 possible keys (shifts 1-25)
keys = CaesarCipher._get_possible_keys()  # [{"shift": 1}, {"shift": 2}, ...]

# Affine cipher: 312 possible keys (12 coprime a values × 26 b values)
keys = AffineCipher._get_possible_keys()  # [{"a": 1, "b": 0}, ...]

# Atbash cipher: 1 possible key (no variability)
keys = AtbashCipher._get_possible_keys()  # [{"a": 25, "b": 25}]
``` 