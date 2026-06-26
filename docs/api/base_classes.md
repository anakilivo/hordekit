# Core API

## HordeResult

The universal return type for all tools. Wraps `bytes` and provides format conversion and chaining.

```python
from hordekit.core import HordeResult
```

### Conversions

| Method | Returns | Description |
|--------|---------|-------------|
| `.as_bytes()` | `bytes` | Raw bytes |
| `.as_str(encoding="utf-8")` | `str` | Decoded string |
| `.as_hex()` | `str` | Hex string, e.g. `"4a6f"` |
| `.as_base64()` | `str` | Base64-encoded string |
| `.as_int(byteorder="big")` | `int` | Integer representation |

### Chaining

```python
result.pipe(ToolClass, **init_kwargs) -> HordeResult
```

Creates an instance of `ToolClass(**init_kwargs)` and calls `.run()` on the current bytes.

```python
Caesar(shift=3).encrypt(b"Hello").pipe(ROT13).as_hex()
```

### Metadata

Attacks and other multi-result tools store extra data in `.metadata`:

```python
result = brute_force(Caesar, ciphertext=b"Khoor")
result.metadata["candidates"]  # list of {key, result, score}
```

---

## BaseTool

Abstract base class for all hordekit tools.

```python
from hordekit.core import BaseTool
```

```python
class BaseTool(ABC):
    def run(self, data: bytes) -> HordeResult: ...
```

All tools implement `.run()`. For ciphers, `run()` defaults to `encrypt()`.

---

## BaseCipher

Abstract base class for all ciphers. Extends `BaseTool`.

```python
from hordekit.core import BaseCipher
```

```python
class BaseCipher(BaseTool, ABC):
    def encrypt(self, data: bytes) -> HordeResult: ...
    def decrypt(self, data: bytes) -> HordeResult: ...
    def run(self, data: bytes) -> HordeResult: ...          # calls encrypt()

    @classmethod
    def possible_keys(cls) -> list[dict[str, Any]]: ...    # raises if not implemented
```

### Implementing a custom cipher

```python
from hordekit.core import BaseCipher
from hordekit.core.result import HordeResult

class XORCipher(BaseCipher):
    def __init__(self, key: int) -> None:
        self.key = key

    def encrypt(self, data: bytes) -> HordeResult:
        return HordeResult(bytes(b ^ self.key for b in data))

    def decrypt(self, data: bytes) -> HordeResult:
        return self.encrypt(data)  # XOR is self-inverse

    @classmethod
    def possible_keys(cls) -> list[dict[str, Any]]:
        return [{"key": k} for k in range(256)]
```
