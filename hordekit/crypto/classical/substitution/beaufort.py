from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Beaufort(BaseCipher):
    def __init__(self, key: bytes) -> None:
        values: list[int] = []
        for b in key:
            if 65 <= b <= 90:
                values.append(b - 65)
            elif 97 <= b <= 122:
                values.append(b - 97)
            else:
                raise ValueError(f"Key must contain only ASCII letters, got byte {b!r}")
        if not values:
            raise ValueError("Key must not be empty")
        self._key = values

    def _transform(self, data: bytes) -> HordeResult:
        # Beaufort is reciprocal: C = (K - P) mod 26, P = (K - C) mod 26
        result = []
        key_idx = 0
        for b in data:
            if 65 <= b <= 90:
                result.append((self._key[key_idx % len(self._key)] - (b - 65)) % 26 + 65)
                key_idx += 1
            elif 97 <= b <= 122:
                result.append((self._key[key_idx % len(self._key)] - (b - 97)) % 26 + 97)
                key_idx += 1
            else:
                result.append(b)
        return HordeResult(bytes(result))

    def encrypt(self, data: bytes) -> HordeResult:
        return self._transform(data)

    def decrypt(self, data: bytes) -> HordeResult:
        return self._transform(data)
