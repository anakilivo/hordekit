from typing import Any

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
    def possible_keys(cls) -> list[dict[str, Any]]:
        return [{}]
