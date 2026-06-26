# {Cipher Name}

> {One-line description, e.g. "A monoalphabetic substitution cipher that shifts each letter by a fixed amount."}

## Overview

{2-3 sentences: what it is, when developed, historical context and use.}

## How It Works

{2-4 sentences explaining the algorithm in plain language, no code.}

```mermaid
flowchart LR
    subgraph plaintext["Plaintext"]
        direction LR
        i1["{char1}\n({byte1})"]
        i2["{char2}\n({byte2})"]
        i3["..."]
    end
    subgraph ciphertext["Ciphertext"]
        direction LR
        o1["{enc1}\n({enc_byte1})"]
        o2["{enc2}\n({enc_byte2})"]
        o3["..."]
    end
    i1 -->|"{operation}"| o1
    i2 -->|"{operation}"| o2
    i3 --> o3
```

### Algorithm

```mermaid
flowchart TD
    Start(["Input byte"])
    Check{"{Is target byte?\ne.g. A-Z or a-z}"}
    Transform["{transformation formula}"]
    Skip["Pass through unchanged"]
    End(["Output byte"])

    Start --> Check
    Check -->|Yes| Transform
    Check -->|No| Skip
    Transform --> End
    Skip --> End
```

## API

```python
from hordekit.crypto.classical.{category} import {ClassName}

cipher = {ClassName}({params})
cipher.encrypt(b"{example}")   # -> HordeResult
cipher.decrypt(b"{encrypted}") # -> HordeResult
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `{param}` | `{type}` | {description} |

### Chaining

```python
result = (
    {ClassName}({params}).encrypt(b"{example}")
    .pipe(AnotherTool, ...)
    .as_hex()
)
```

## Known Attacks

| Attack | When applicable |
|--------|----------------|
| [Brute force](../../attacks/generic/brute_force.md) | Key space is small and enumerable |
| {Other attack} | {condition} |

## References

- [{Source name}]({url})
