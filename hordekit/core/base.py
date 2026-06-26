from abc import ABC, abstractmethod
from typing import Any, Dict, List

from hordekit.core.result import HordeResult


class BaseTool(ABC):
    @abstractmethod
    def run(self, data: bytes) -> HordeResult: ...


class BaseCipher(BaseTool, ABC):
    @abstractmethod
    def encrypt(self, data: bytes) -> HordeResult: ...

    @abstractmethod
    def decrypt(self, data: bytes) -> HordeResult: ...

    def run(self, data: bytes) -> HordeResult:
        return self.encrypt(data)

    @classmethod
    def possible_keys(cls) -> List[Dict[str, Any]]:
        raise NotImplementedError(f"{cls.__name__} does not support key enumeration")
