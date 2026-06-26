from typing import Any, Dict, List

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult

_TABLE = bytes.maketrans(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    b"ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba",
)


class Atbash(BaseCipher):
    def encrypt(self, data: bytes) -> HordeResult:
        return HordeResult(data.translate(_TABLE))

    def decrypt(self, data: bytes) -> HordeResult:
        return self.encrypt(data)

    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]:
        return [{}]
