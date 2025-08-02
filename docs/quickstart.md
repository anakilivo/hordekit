# Quick Start

This guide will help you get started with Hordekit in just a few minutes.

## Basic Usage

### Caesar Cipher

The Caesar cipher is the simplest substitution cipher:

```python
from hordekit.crypto.symmetric.substitution.caesar import CaesarCipher

# Create a Caesar cipher with shift 3
caesar = CaesarCipher(shift=3)

# Encrypt a message
message = "HELLO WORLD"
encrypted = caesar.encode(message)
print(encrypted)  # Output: KHOOR ZRUOG

# Decrypt the message
decrypted = caesar.decode(encrypted)
print(decrypted)  # Output: HELLO WORLD
```

### Affine Cipher

The Affine cipher uses a mathematical function:

```python
from hordekit.crypto.symmetric.substitution.affine import AffineCipher

# Create an Affine cipher with parameters a=5, b=8
affine = AffineCipher(a=5, b=8)

# Encrypt a message
message = "CRYPTO"
encrypted = affine.encode(message)
print(encrypted)  # Output: WZQJLA

# Decrypt the message
decrypted = affine.decode(encrypted)
print(decrypted)  # Output: CRYPTO
```

### Atbash Cipher

The Atbash cipher mirrors the alphabet:

```python
from hordekit.crypto.symmetric.substitution.atbash import AtbashCipher

# Create an Atbash cipher (no parameters needed)
atbash = AtbashCipher()

# Encrypt a message
message = "ATBASH"
encrypted = atbash.encode(message)
print(encrypted)  # Output: ZGYZHS

# Decrypt the message
decrypted = atbash.decode(encrypted)
print(decrypted)  # Output: ATBASH
```

## Attack Methods

### Brute Force Attack

Try all possible keys to decrypt a message:

```python
from hordekit.crypto.utils import AttackMethod

# Try to decrypt a Caesar cipher message
results = CaesarCipher.attack(
    AttackMethod.BRUTE_FORCE,
    ciphertext="KHOOR ZRUOG"
)

print("All possible decryptions:")
for key, decrypted in results["all_results"].items():
    print(f"Shift {key}: {decrypted}")
```

### Frequency Analysis

Use letter frequency patterns to find the most likely key:

```python
# Analyze a longer text
analysis = CaesarCipher.attack(
    AttackMethod.FREQUENCY_ANALYSIS,
    ciphertext="KHOOR ZRUOG VKXOG"
)

print(f"Most likely key: {analysis['most_likely_key']}")
print(f"Decrypted text: {analysis['decrypted_text']}")
print(f"Confidence score: {analysis['confidence_score']}")
```

### Known Plaintext Attack

Use known plaintext-ciphertext pairs:

```python
# Known plaintext attack on Affine cipher
result = AffineCipher.attack(
    AttackMethod.KNOWN_PLAINTEXT,
    plaintext="HELLO",
    ciphertext="WZQJLA"
)

if result:
    print(f"Recovered key: a={result['a']}, b={result['b']}")
else:
    print("Attack failed")
```

## Key Generation

Generate random keys for algorithms:

```python
# Generate random Caesar cipher
random_caesar = CaesarCipher.generate_key()
print(f"Random shift: {random_caesar.shift}")

# Generate random Affine cipher
random_affine = AffineCipher.generate_key()
print(f"Random parameters: a={random_affine.a}, b={random_affine.b}")
```

## Error Handling

All algorithms include proper error handling:

```python
try:
    # Invalid parameters
    caesar = CaesarCipher(shift=0)  # Should raise ValueError
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid attack method
    CaesarCipher.attack("invalid_method", ciphertext="test")
except ValueError as e:
    print(f"Error: {e}")
```

## Case Preservation

All algorithms preserve the original case:

```python
caesar = CaesarCipher(shift=3)

# Mixed case
message = "Hello World!"
encrypted = caesar.encode(message)
print(encrypted)  # Output: Khoor Zruog!

decrypted = caesar.decode(encrypted)
print(decrypted)  # Output: Hello World!
```

## Non-Alphabetic Characters

Numbers, punctuation, and spaces are preserved:

```python
caesar = CaesarCipher(shift=3)

message = "Hello, World! 123"
encrypted = caesar.encode(message)
print(encrypted)  # Output: Khoor, Zruog! 123
```

## Next Steps

Now that you've learned the basics, explore:

- [Algorithm Documentation](crypto/symmetric/substitution/) for detailed explanations
- [API Reference](api/) for complete API documentation
- [Development Guide](development/) for contributing to the project 