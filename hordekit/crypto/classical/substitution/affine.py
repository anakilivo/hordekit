from typing import Any

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult

_VALID_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]


class Affine(BaseCipher):
    def __init__(self, a: int, b: int) -> None:
        if a not in _VALID_A:
            raise ValueError(f"'a' must be coprime with 26, got {a}. Valid values: {_VALID_A}")
        self.a = a
        self.b = b % 26
        self._a_inv = pow(a, -1, 26)

    def encrypt(self, data: bytes) -> HordeResult:
        def _enc(byte: int) -> int:
            if 65 <= byte <= 90:
                return (self.a * (byte - 65) + self.b) % 26 + 65
            if 97 <= byte <= 122:
                return (self.a * (byte - 97) + self.b) % 26 + 97
            return byte

        return HordeResult(bytes(_enc(b) for b in data))

    def decrypt(self, data: bytes) -> HordeResult:
        def _dec(byte: int) -> int:
            if 65 <= byte <= 90:
                return (self._a_inv * ((byte - 65) - self.b)) % 26 + 65
            if 97 <= byte <= 122:
                return (self._a_inv * ((byte - 97) - self.b)) % 26 + 97
            return byte

        return HordeResult(bytes(_dec(b) for b in data))

    @classmethod
    def possible_keys(cls) -> list[dict[str, Any]]:
        return [{"a": a, "b": b} for a in _VALID_A for b in range(26)]
