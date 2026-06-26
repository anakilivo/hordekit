import base64
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

if TYPE_CHECKING:
    from hordekit.core.base import BaseTool


class HordeResult:
    def __init__(self, data: bytes, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._data = data
        self.metadata: Dict[str, Any] = metadata or {}

    def as_bytes(self) -> bytes:
        return self._data

    def as_str(self, encoding: str = "utf-8") -> str:
        return self._data.decode(encoding)

    def as_hex(self) -> str:
        return self._data.hex()

    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("ascii")

    def as_int(self, byteorder: str = "big") -> int:
        return int.from_bytes(self._data, byteorder=byteorder)

    def pipe(self, tool_cls: "Type[BaseTool]", **kwargs: Any) -> "HordeResult":
        tool = tool_cls(**kwargs)
        return tool.run(self._data)

    def __bytes__(self) -> bytes:
        return self._data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HordeResult):
            return self._data == other._data
        if isinstance(other, bytes):
            return self._data == other
        return NotImplemented

    def __repr__(self) -> str:
        preview = self._data[:32]
        suffix = "..." if len(self._data) > 32 else ""
        return f"HordeResult({preview!r}{suffix})"
