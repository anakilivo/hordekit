# ROT13

> A special case of the Caesar cipher with a fixed shift of 13 — applying it twice returns the original text.

## Overview

ROT13 ("rotate by 13") became popular in the early 1980s as a simple way to obscure text in Usenet posts — spoilers, punchlines, offensive content — without any intent of real security. Because the Latin alphabet has 26 letters, shifting by 13 is self-inverse: encrypting and decrypting are the same operation. ROT13 is implemented as `Caesar(shift=13)`.

## How It Works

Every letter is shifted 13 positions forward in the alphabet, wrapping around. Non-letter bytes pass through unchanged. Applying ROT13 to already-encrypted text always recovers the original.

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
        o1["U\n(85)"]
        o2["R\n(82)"]
        o3["Y\n(89)"]
        o4["Y\n(89)"]
        o5["B\n(66)"]
    end
    i1 -->|"+13"| o1
    i2 -->|"+13"| o2
    i3 -->|"+13"| o3
    i4 -->|"+13"| o4
    i5 -->|"+13"| o5
```

### Per-byte algorithm

```mermaid
flowchart TD
    Start(["Input byte"])
    CheckUpper{"65 ≤ byte ≤ 90\n(A–Z)?"}
    CheckLower{"97 ≤ byte ≤ 122\n(a–z)?"}
    EncUpper["(byte − 65 + 13) mod 26 + 65"]
    EncLower["(byte − 97 + 13) mod 26 + 97"]
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
from hordekit.crypto.classical.substitution import ROT13

r = ROT13()
r.encrypt(b"Hello, World!")   # -> HordeResult → b"Uryyb, Jbeyq!"
r.decrypt(b"Uryyb, Jbeyq!")   # -> HordeResult → b"Hello, World!"

# encrypt == decrypt
r.encrypt(r.encrypt(b"Hello")) == b"Hello"  # True
```

### Chaining

```python
from hordekit.crypto.classical.substitution import ROT13, Caesar

result = (
    Caesar(shift=3).encrypt(b"Hello")
    .pipe(ROT13)
    .as_str()
)
```

## Known Attacks

| Attack | When applicable |
|--------|----------------|
| Trivial — apply ROT13 again (`ROT13().decrypt(ct)`) | Always; there is exactly one key |
| [Brute Force](../../attacks/generic/brute_force.md) | Automated version of the trivial case |
| [Frequency Analysis](../../attacks/substitution/frequency.md) | Ciphertext > ~100 characters |

## References

- [ROT13 — Wikipedia](https://en.wikipedia.org/wiki/ROT13)
