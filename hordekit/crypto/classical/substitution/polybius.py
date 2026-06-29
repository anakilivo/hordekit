from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Polybius(BaseCipher):
    """Polybius square cipher: each letter maps to a 2-digit (row, column) coordinate.

    Uses a 5×5 grid where I and J share a cell. An optional keyword scrambles the
    grid (mixed square); with no key the standard A–Z layout is used. Coordinates
    are 1-indexed, so each letter becomes a pair of ASCII digits in the range 1–5.
    """

    def __init__(self, key: bytes = b"") -> None:
        if key and not any(65 <= b <= 90 or 97 <= b <= 122 for b in key):
            raise ValueError("Key must contain at least one ASCII letter")
        self._square, self._pos = self._build_square(key)

    def _build_square(self, key: bytes) -> tuple[list[list[int]], dict[int, tuple[int, int]]]:
        seen: set[int] = set()
        order: list[int] = []
        for b in key:
            if 65 <= b <= 90:
                v = b - 65
            elif 97 <= b <= 122:
                v = b - 97
            else:
                continue
            if v == 9:  # J -> I
                v = 8
            if v not in seen:
                seen.add(v)
                order.append(v)
        for v in range(26):
            if v == 9:
                continue  # J shares cell with I
            if v not in seen:
                seen.add(v)
                order.append(v)
        square = [order[r * 5 : r * 5 + 5] for r in range(5)]
        pos: dict[int, tuple[int, int]] = {}
        for r, row in enumerate(square):
            for c, val in enumerate(row):
                pos[val] = (r, c)
        return square, pos

    def encrypt(self, data: bytes) -> HordeResult:
        result: list[int] = []
        for b in data:
            if 65 <= b <= 90:
                val = b - 65
            elif 97 <= b <= 122:
                val = b - 97
            else:
                result.append(b)
                continue
            if val == 9:  # J -> I
                val = 8
            r, c = self._pos[val]
            result.append(49 + r)  # ASCII '1'..'5'
            result.append(49 + c)
        return HordeResult(bytes(result))

    def decrypt(self, data: bytes) -> HordeResult:
        result: list[int] = []
        pending: int | None = None  # row digit awaiting its column digit
        for b in data:
            if 49 <= b <= 53:  # ASCII '1'..'5' — a coordinate digit
                if pending is None:
                    pending = b - 49
                else:
                    val = self._square[pending][b - 49]
                    result.append(65 + val)  # uppercase letter
                    pending = None
            else:
                if pending is not None:
                    # Dangling row digit with no column — emit it unchanged
                    result.append(49 + pending)
                    pending = None
                result.append(b)
        if pending is not None:
            result.append(49 + pending)
        return HordeResult(bytes(result))
