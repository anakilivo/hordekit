from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Porta(BaseCipher):
    """Della Porta polyalphabetic substitution cipher (1563).

    The cipher is *reciprocal* — encryption and decryption are the same
    operation. Each key letter selects one of 13 reciprocal alphabets; key
    letters are paired, so A and B share a row, C and D share a row, and so on
    (row index = key_letter // 2). Letters in the first half of the alphabet
    (A–M) always map to the second half (N–Z) and vice versa, which is what
    makes every row an involution.
    """

    def __init__(self, key: bytes) -> None:
        rows: list[int] = []
        for b in key:
            if 65 <= b <= 90:
                rows.append((b - 65) // 2)
            elif 97 <= b <= 122:
                rows.append((b - 97) // 2)
            else:
                raise ValueError(f"Key must contain only ASCII letters, got byte {b!r}")
        if not rows:
            raise ValueError("Key must not be empty")
        self._rows = rows

    def _transform(self, data: bytes) -> HordeResult:
        result: list[int] = []
        key_idx = 0
        for b in data:
            if 65 <= b <= 90:
                base = 65
            elif 97 <= b <= 122:
                base = 97
            else:
                result.append(b)
                continue
            p = b - base
            n = self._rows[key_idx % len(self._rows)]
            if p < 13:  # first half A–M -> second half N–Z
                c = (p + n) % 13 + 13
            else:  # second half N–Z -> first half A–M (inverse of above)
                c = (p - 13 - n) % 13
            result.append(c + base)
            key_idx += 1
        return HordeResult(bytes(result))

    def encrypt(self, data: bytes) -> HordeResult:
        return self._transform(data)

    def decrypt(self, data: bytes) -> HordeResult:
        # Porta is reciprocal: decryption is identical to encryption.
        return self._transform(data)
