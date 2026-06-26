from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Playfair(BaseCipher):
    """Playfair digraph substitution cipher using a 5×5 key square (I=J)."""

    def __init__(self, key: bytes) -> None:
        if not any(65 <= b <= 90 or 97 <= b <= 122 for b in key):
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

    def _encrypt_pair(self, a: int, b: int) -> tuple[int, int]:
        ar, ac = self._pos[a]
        br, bc = self._pos[b]
        if ar == br:  # same row: shift right
            return self._square[ar][(ac + 1) % 5], self._square[br][(bc + 1) % 5]
        if ac == bc:  # same column: shift down
            return self._square[(ar + 1) % 5][ac], self._square[(br + 1) % 5][bc]
        # rectangle: swap columns
        return self._square[ar][bc], self._square[br][ac]

    def _decrypt_pair(self, a: int, b: int) -> tuple[int, int]:
        ar, ac = self._pos[a]
        br, bc = self._pos[b]
        if ar == br:  # same row: shift left
            return self._square[ar][(ac - 1) % 5], self._square[br][(bc - 1) % 5]
        if ac == bc:  # same column: shift up
            return self._square[(ar - 1) % 5][ac], self._square[(br - 1) % 5][bc]
        # rectangle: swap columns (same as encrypt)
        return self._square[ar][bc], self._square[br][ac]

    def _process(self, data: bytes, encrypt: bool) -> HordeResult:
        transform = self._encrypt_pair if encrypt else self._decrypt_pair
        result: list[int] = []
        pending: tuple[int, bool] | None = None  # (letter_val, is_upper)

        for b in data:
            if 65 <= b <= 90:
                is_upper, val = True, b - 65
            elif 97 <= b <= 122:
                is_upper, val = False, b - 97
            else:
                result.append(b)
                continue

            if val == 9:  # J -> I
                val = 8

            if pending is None:
                pending = (val, is_upper)
            else:
                prev_val, prev_upper = pending
                if prev_val == val and encrypt:
                    # Repeated letter: insert filler X (or Q if letter is X), keep current
                    filler = 23 if prev_val != 23 else 16  # X=23, Q=16
                    ea, eb = transform(prev_val, filler)
                    result.append(ea + (65 if prev_upper else 97))
                    result.append(eb + (65 if prev_upper else 97))
                    pending = (val, is_upper)
                else:
                    ea, eb = transform(prev_val, val)
                    result.append(ea + (65 if prev_upper else 97))
                    result.append(eb + (65 if is_upper else 97))
                    pending = None

        if pending is not None:
            val, is_upper = pending
            if encrypt:
                # Pad odd-length input with X (or Q if last letter is X)
                filler = 23 if val != 23 else 16
                ea, eb = transform(val, filler)
                result.append(ea + (65 if is_upper else 97))
                result.append(eb + (65 if is_upper else 97))
            else:
                # Valid ciphertext always has even letter count; emit as-is
                result.append(val + (65 if is_upper else 97))

        return HordeResult(bytes(result))

    def encrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=True)

    def decrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=False)
