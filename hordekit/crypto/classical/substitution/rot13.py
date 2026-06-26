from typing import Any, Dict, List

from hordekit.core.result import HordeResult
from hordekit.crypto.classical.substitution.caesar import Caesar


class ROT13(Caesar):
    def __init__(self) -> None:
        super().__init__(shift=13)

    def decrypt(self, data: bytes) -> HordeResult:
        return self.encrypt(data)

    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]:
        return [{}]
