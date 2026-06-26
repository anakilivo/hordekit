# Quick Start

## Installation

```bash
pip install hordekit
```

## Encrypting and decrypting

```python
from hordekit.crypto.classical.substitution import Caesar, Vigenere

# Caesar cipher
c = Caesar(shift=13)
encrypted = c.encrypt(b"Hello, World!")
print(encrypted.as_str())                        # Uryyb, Jbeyq!
print(c.decrypt(encrypted.as_bytes()).as_str())  # Hello, World!

# Vigenere
v = Vigenere(b"KEY")
enc = v.encrypt(b"ATTACK AT DAWN")
print(v.decrypt(enc.as_bytes()).as_str())        # ATTACK AT DAWN
```

## Result formats

Every operation returns a `HordeResult` you can convert on the fly:

```python
result = Caesar(shift=3).encrypt(b"Hello")

result.as_bytes()   # b'Khoor'
result.as_str()     # 'Khoor'
result.as_hex()     # '4b686f6f72'
result.as_base64()  # 'S2hvb3I='
result.as_int()     # 334794610
```

## Chaining with .pipe()

`.pipe(Tool, **kwargs)` passes the current bytes into the next tool's `run()` (which calls `encrypt` by default):

```python
from hordekit.crypto.classical.substitution import Caesar, ROT13

result = (
    Caesar(shift=3).encrypt(b"Hello")
    .pipe(ROT13)
    .as_hex()
)
```

## Attacking ciphers

```python
from hordekit.crypto.attacks.generic import brute_force
from hordekit.crypto.classical.substitution import Caesar

result = brute_force(Caesar, ciphertext=b"Uryyb Jbeyq")

print(result.as_str())                          # Hello World
print(result.metadata["candidates"][0]["key"])  # {'shift': 13}
```

## Available ciphers

```python
from hordekit.crypto.classical.substitution import (
    Caesar,    # Caesar(shift=N)
    ROT13,     # ROT13()
    ROT47,     # ROT47()
    Atbash,    # Atbash()
    Affine,    # Affine(a=N, b=N)
    Vigenere,  # Vigenere(b"KEY")
)
```
