# Atbash

> A substitution cipher that mirrors the alphabet: A↔Z, B↔Y, C↔X, and so on.

## Overview

Atbash is one of the oldest known ciphers, originating in ancient Hebrew cryptography (the name comes from the first, last, second, and second-to-last letters of the Hebrew alphabet). It maps each letter to its mirror position in the alphabet — A becomes Z, B becomes Y, and so forth. The cipher is its own inverse: applying it twice recovers the original text.

## How It Works

Each letter is replaced by the letter at the symmetric position in the alphabet. Uppercase maps to uppercase, lowercase to lowercase. Non-letter bytes pass through unchanged.

### Letter-by-letter example

```mermaid
flowchart LR
    subgraph plaintext["Plaintext"]
        direction LR
        i1["H\n(72)"]
        i2["E\n(69)"]
        i3["L\n(76)"]
        i4["L\n(76)"]
        i5["O\n(79)"]
    end
    subgraph ciphertext["Ciphertext"]
        direction LR
        o1["S\n(83)"]
        o2["V\n(86)"]
        o3["O\n(79)"]
        o4["O\n(79)"]
        o5["L\n(76)"]
    end
    i1 -->|"A–Z mirror"| o1
    i2 -->|"A–Z mirror"| o2
    i3 -->|"A–Z mirror"| o3
    i4 -->|"A–Z mirror"| o4
    i5 -->|"A–Z mirror"| o5
```

### Per-byte algorithm

```mermaid
flowchart TD
    Start(["Input byte"])
    CheckUpper{"65 ≤ byte ≤ 90\n(A–Z)?"}
    CheckLower{"97 ≤ byte ≤ 122\n(a–z)?"}
    EncUpper["90 − (byte − 65)\n= 155 − byte"]
    EncLower["122 − (byte − 97)\n= 219 − byte"]
    Skip["Pass through unchanged"]
    End(["Output byte"])

    Start --> CheckUpper
    CheckUpper -->|Yes| EncUpper
    CheckUpper -->|No| CheckLower
    CheckLower -->|Yes| EncLower
    CheckLower -->|No| Skip
    EncUpper --> End
    EncLower --> End
    Skip --> End
```

## API

```python
from hordekit.crypto.classical.substitution import Atbash

a = Atbash()
a.encrypt(b"Hello, World!")   # -> HordeResult → b"Svool, Dliow!"
a.decrypt(b"Svool, Dliow!")   # -> HordeResult → b"Hello, World!"

# self-inverse
a.encrypt(a.encrypt(b"Hello")) == b"Hello"  # True
```

### Chaining

```python
from hordekit.crypto.classical.substitution import Atbash, Caesar

result = (
    Atbash().encrypt(b"HELLO")
    .pipe(Caesar, shift=3)
    .as_str()
)
```

## Known Attacks

| Attack | When applicable |
|--------|----------------|
| Trivial — apply Atbash again | Always; there is exactly one key |
| Frequency analysis | Ciphertext > ~100 characters |

## References

- [Atbash — Wikipedia](https://en.wikipedia.org/wiki/Atbash)
