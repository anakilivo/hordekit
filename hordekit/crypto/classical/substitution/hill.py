import math

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


def _det(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = 0
    for col in range(n):
        sub = [[matrix[r][c] for c in range(n) if c != col] for r in range(1, n)]
        total += ((-1) ** col) * matrix[0][col] * _det(sub)
    return total


def _submatrix(matrix: list[list[int]], skip_row: int, skip_col: int) -> list[list[int]]:
    n = len(matrix)
    return [[matrix[r][c] for c in range(n) if c != skip_col] for r in range(n) if r != skip_row]


def _adjugate(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    cof = [[((-1) ** (i + j)) * _det(_submatrix(matrix, i, j)) for j in range(n)] for i in range(n)]
    return [[cof[j][i] for j in range(n)] for i in range(n)]  # transpose


def _inverse_mod26(matrix: list[list[int]]) -> list[list[int]]:
    det = _det(matrix) % 26
    try:
        det_inv = pow(det, -1, 26)
    except ValueError as exc:
        g = math.gcd(det, 26)
        raise ValueError(f"Key matrix not invertible mod 26: det ≡ {det} (mod 26), gcd = {g}") from exc
    adj = _adjugate(matrix)
    n = len(matrix)
    return [[(det_inv * adj[i][j]) % 26 for j in range(n)] for i in range(n)]


def _matmul_mod26(A: list[list[int]], B: list[list[int]], n: int) -> list[list[int]]:
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % 26 for j in range(n)] for i in range(n)]


class Hill(BaseCipher):
    """Hill polygraphic substitution cipher using matrix multiplication mod 26."""

    def __init__(self, key: list[list[int]]) -> None:
        if not key or not key[0]:
            raise ValueError("Key matrix must be non-empty")
        n = len(key)
        if any(len(row) != n for row in key):
            raise ValueError("Key must be a square matrix")
        if any(not (0 <= v <= 25) for row in key for v in row):
            raise ValueError("Key matrix entries must be integers in [0, 25]")
        self._n = n
        self._key = [row[:] for row in key]
        self._key_inv = _inverse_mod26(key)

    def _transform_block(self, vals: list[int], key: list[list[int]]) -> list[int]:
        n = self._n
        return [sum(key[i][j] * vals[j] for j in range(n)) % 26 for i in range(n)]

    def _process(self, data: bytes, encrypt: bool) -> HordeResult:
        key = self._key if encrypt else self._key_inv
        result: list[int] = []
        pending: list[tuple[int, bool]] = []

        for b in data:
            if 65 <= b <= 90:
                pending.append((b - 65, True))
            elif 97 <= b <= 122:
                pending.append((b - 97, False))
            else:
                result.append(b)
                continue

            if len(pending) == self._n:
                vals = [v for v, _ in pending]
                cases = [u for _, u in pending]
                for tv, isu in zip(self._transform_block(vals, key), cases, strict=True):
                    result.append(tv + (65 if isu else 97))
                pending.clear()

        if pending:
            last_upper = pending[-1][1]
            while len(pending) < self._n:
                pending.append((23, last_upper))  # pad with X
            vals = [v for v, _ in pending]
            cases = [u for _, u in pending]
            for tv, isu in zip(self._transform_block(vals, key), cases, strict=True):
                result.append(tv + (65 if isu else 97))

        return HordeResult(bytes(result))

    def encrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=True)

    def decrypt(self, data: bytes) -> HordeResult:
        return self._process(data, encrypt=False)
