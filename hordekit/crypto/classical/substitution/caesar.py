from typing import Any, Dict, List

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


def _shift_byte(b: int, shift: int) -> int:
    if 65 <= b <= 90:
        return (b - 65 + shift) % 26 + 65
    if 97 <= b <= 122:
        return (b - 97 + shift) % 26 + 97
    return b


class Caesar(BaseCipher):
    def __init__(self, shift: int) -> None:
        self.shift = shift % 26

    def encrypt(self, data: bytes) -> HordeResult:
        return HordeResult(bytes(_shift_byte(b, self.shift) for b in data))

    def decrypt(self, data: bytes) -> HordeResult:
        return HordeResult(bytes(_shift_byte(b, -self.shift) for b in data))

    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]:
        return [{"shift": i} for i in range(1, 26)]
