from typing import Any

from hordekit.core.result import HordeResult
from hordekit.crypto.classical.substitution.caesar import Caesar


class ROT13(Caesar):
    def __init__(self) -> None:
        super().__init__(shift=13)

    def decrypt(self, data: bytes) -> HordeResult:
        return self.encrypt(data)

    @classmethod
    def possible_keys(cls) -> list[dict[str, Any]]:
        return [{}]
