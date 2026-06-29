from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class FourSquare(BaseCipher):
    """Four-square digraph substitution cipher using four 5×5 squares (I=J).

    Two *plaintext* squares (top-left, bottom-right) hold the standard alphabet,
    while two *ciphertext* squares (top-right keyed with ``key1``, bottom-left
    keyed with ``key2``) hold mixed alphabets. Plaintext is split into letter
    pairs: the first letter is located in the top-left square and the second in
    the bottom-right square; the two letters form a rectangle whose other two
    corners — read from the ciphertext squares — give the encrypted pair. Unlike
    Playfair, a digraph of two identical letters needs no filler, since each
    letter is looked up in a different square.
    """

    def __init__(self, key1: bytes, key2: bytes) -> None:
        if not any(65 <= b <= 90 or 97 <= b <= 122 for b in key1):
            raise ValueError("key1 must contain at least one ASCII letter")
        if not any(65 <= b <= 90 or 97 <= b <= 122 for b in key2):
            raise ValueError("key2 must contain at least one ASCII letter")
        self._plain, self._plain_pos = self._build_square(b"")
        self._cipher1, self._cipher1_pos = self._build_square(key1)
        self._cipher2, self._cipher2_pos = self._build_square(key2)

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
        # a from top-left (plain), b from bottom-right (plain); read the
        # rectangle's other corners from the two ciphertext squares.
        r1, c1 = self._plain_pos[a]
        r2, c2 = self._plain_pos[b]
        return self._cipher1[r1][c2], self._cipher2[r2][c1]

    def _decrypt_pair(self, a: int, b: int) -> tuple[int, int]:
        # a from top-right (cipher1), b from bottom-left (cipher2); read the
        # rectangle's other corners from the two plaintext squares.
        r1, c2 = self._cipher1_pos[a]
        r2, c1 = self._cipher2_pos[b]
        return self._plain[r1][c1], self._plain[r2][c2]

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
                c, d = transform(prev_val, val)
                result.append(c + (65 if prev_upper else 97))
                result.append(d + (65 if is_upper else 97))
                pending = None

        if pending is not None:
            val, is_upper = pending
            if encrypt:
                # Pad odd-length input with a trailing X to complete the pair
                c, d = transform(val, 23)  # X = 23
                result.append(c + (65 if is_upper else 97))
                result.append(d + (65 if is_upper else 97))
            else:
                # Valid ciphertext always has an even letter count; emit as-is
                result.append(val + (65 if is_upper else 97))

        return HordeResult(bytes(result))

    def encrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=True)

    def decrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=False)
