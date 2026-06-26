# Vigenère Cipher

> A polyalphabetic substitution cipher that uses a repeating keyword to shift each letter by a different amount.

## Overview

The Vigenère cipher was described by Giovan Battista Bellaso in 1553 and later misattributed to Blaise de Vigenère. It was considered unbreakable for three centuries — earning the nickname *le chiffre indéchiffrable* — until Charles Babbage and Friedrich Kasiski independently cracked it in the 19th century. Unlike monoalphabetic ciphers, it applies a different shift to each letter based on a repeating keyword, which defeats simple frequency analysis.

## How It Works

The keyword is repeated to match the length of the plaintext (skipping non-letter characters). Each plaintext letter is shifted by the corresponding key letter's position in the alphabet (A=0, B=1, …, Z=25). Decryption subtracts the shift instead.

### Letter-by-letter example (key = "KEY")

```mermaid
flowchart LR
    subgraph plaintext["Plaintext"]
        direction LR
        i1["H\n(x=7)"]
        i2["E\n(x=4)"]
        i3["L\n(x=11)"]
        i4["L\n(x=11)"]
        i5["O\n(x=14)"]
    end
    subgraph key["Key (repeating)"]
        direction LR
        k1["K\n(+10)"]
        k2["E\n(+4)"]
        k3["Y\n(+24)"]
        k4["K\n(+10)"]
        k5["E\n(+4)"]
    end
    subgraph ciphertext["Ciphertext"]
        direction LR
        o1["R\n(y=17)"]
        o2["I\n(y=8)"]
        o3["J\n(y=9)"]
        o4["V\n(y=21)"]
        o5["S\n(y=18)"]
    end
    i1 & k1 -->|"7+10=17"| o1
    i2 & k2 -->|"4+4=8"| o2
    i3 & k3 -->|"11+24=35→9"| o3
    i4 & k4 -->|"11+10=21"| o4
    i5 & k5 -->|"14+4=18"| o5
```

### Per-byte algorithm

```mermaid
flowchart TD
    Start(["Input byte"])
    Check{"Is A–Z\nor a–z?"}
    GetKey["Get next key value\nkey[i mod len(key)]"]
    EncUpper["(byte − 65 + key_val) mod 26 + 65"]
    EncLower["(byte − 97 + key_val) mod 26 + 97"]
    Skip["Pass through unchanged\n(key index not advanced)"]
    Advance["Advance key index"]
    End(["Output byte"])

    Start --> Check
    Check -->|No| Skip
    Check -->|"Yes (A–Z)"| GetKey
    Check -->|"Yes (a–z)"| GetKey
    GetKey --> EncUpper
    GetKey --> EncLower
    EncUpper --> Advance
    EncLower --> Advance
    Advance --> End
    Skip --> End
```

## API

```python
from hordekit.crypto.classical.substitution import Vigenere

cipher = Vigenere(b"KEY")
cipher.encrypt(b"HELLO")   # -> HordeResult → b"RIJVS"
cipher.decrypt(b"RIJVS")   # -> HordeResult → b"HELLO"
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `bytes` | ASCII letters only (upper or lower). Repeated to match plaintext length. |

### Chaining

```python
from hordekit.crypto.classical.substitution import Vigenere

result = (
    Vigenere(b"SECRET").encrypt(b"Attack at dawn")
    .as_base64()
)
```

## Known Attacks

| Attack | When applicable |
|--------|----------------|
| Kasiski test | Identifies key length from repeated ciphertext patterns |
| Index of coincidence | Confirms key length and detects polyalphabetic cipher |
| Frequency analysis per position | Once key length is known, each column is a Caesar cipher |

!!! note
    Vigenere does not implement `possible_keys()` — the key space is too large for brute force. Use Kasiski + per-column frequency analysis instead.

## References

- [Vigenère cipher — Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [Practical Cryptography — Vigenère Cipher](http://practicalcryptography.com/ciphers/vigenere-gronsfeld-and-autokey-cipher/)
- [Cryptanalysis of the Vigenère Cipher](http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/)
