from typing import Any, Dict, List

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


def _rot47_byte(b: int) -> int:
    if 33 <= b <= 126:
        return (b - 33 + 47) % 94 + 33
    return b


class ROT47(BaseCipher):
    def encrypt(self, data: bytes) -> HordeResult:
        return HordeResult(bytes(_rot47_byte(b) for b in data))

    def decrypt(self, data: bytes) -> HordeResult:
        return self.encrypt(data)

    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]:
        return [{}]
