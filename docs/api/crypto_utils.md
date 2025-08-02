# Crypto Utils

## AttackMethod

Enumeration of available attack methods for cryptographic algorithms.

```python
from hordekit.crypto.utils import AttackMethod
```

### Values

- `BRUTE_FORCE`: Try all possible keys
- `FREQUENCY_ANALYSIS`: Analyze letter frequency patterns
- `KNOWN_PLAINTEXT`: Use known plaintext-ciphertext pairs

### Usage

```python
from hordekit.crypto.utils import AttackMethod
from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

# Use brute force attack
results = CaesarCipher.attack(AttackMethod.BRUTE_FORCE, ciphertext="KHOOR")

# Use frequency analysis
analysis = CaesarCipher.attack(AttackMethod.FREQUENCY_ANALYSIS, ciphertext="KHOOR")
```

## CryptoAlgorithm

Base class for all cryptographic algorithms.

```python
from hordekit.crypto.utils import CryptoAlgorithm
```

### Abstract Methods

Subclasses must implement:

- `_validate_parameters()`: Validate algorithm-specific parameters
- `_setup_algorithm()`: Initialize the algorithm
- `_encode_raw()`: Perform raw encryption
- `_decode_raw()`: Perform raw decryption
- `generate_key()`: Generate a random key

### Common Methods

#### encode(data)

Encrypt the given data.

**Parameters:**
- `data`: String or bytes to encrypt

**Returns:**
- Encrypted data as bytes

#### decode(data)

Decrypt the given data.

**Parameters:**
- `data`: String or bytes to decrypt

**Returns:**
- Decrypted data as bytes

#### attack(method, **kwargs)

Perform a cryptographic attack.

**Parameters:**
- `method`: AttackMethod enum value
- `**kwargs`: Attack-specific parameters

**Returns:**
- Attack results (format depends on method)

### Example Implementation

```python
from hordekit.crypto.utils import CryptoAlgorithm

class MyCipher(CryptoAlgorithm):
    def _validate_parameters(self, **kwargs):
        # Validate parameters
        pass
    
    def _setup_algorithm(self, **kwargs):
        # Initialize algorithm
        pass
    
    def _encode_raw(self, data, **kwargs):
        # Perform encryption
        return encrypted_data
    
    def _decode_raw(self, data, **kwargs):
        # Perform decryption
        return decrypted_data
    
    @classmethod
    def generate_key(cls):
        # Generate random key
        return cls(**random_params)
``` 