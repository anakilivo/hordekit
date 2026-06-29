import math

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
    return [[cof[j][i] for j in range(n)] for i in range(n)]


def _inverse_mod26(matrix: list[list[int]]) -> list[list[int]]:
    det = _det(matrix) % 26
    try:
        det_inv = pow(det, -1, 26)
    except ValueError as exc:
        g = math.gcd(det, 26)
        raise ValueError(
            f"Plaintext matrix not invertible mod 26: det ≡ {det} (mod 26), gcd = {g}. "
            "Choose different plaintext blocks."
        ) from exc
    adj = _adjugate(matrix)
    n = len(matrix)
    return [[(det_inv * adj[i][j]) % 26 for j in range(n)] for i in range(n)]


def _matmul_mod26(A: list[list[int]], B: list[list[int]], n: int) -> list[list[int]]:
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % 26 for j in range(n)] for i in range(n)]


def hill_known_plaintext(
    plaintext: bytes,
    ciphertext: bytes,
    n: int,
) -> HordeResult:
    """Recover a Hill cipher key matrix from n² known plaintext/ciphertext letter pairs.

    Solves K = C × P⁻¹ (mod 26), where P and C are n×n matrices whose columns
    are successive n-letter plaintext and ciphertext blocks respectively.

    Args:
        plaintext:  Known plaintext — at least n² alphabetic characters.
        ciphertext: Corresponding ciphertext — at least n² alphabetic characters.
        n:          Matrix dimension (2 for 2×2, 3 for 3×3, etc.).

    Returns:
        HordeResult whose bytes are the flattened key matrix (row-major, values 0–25).
        metadata["key_matrix"] is the recovered n×n list-of-lists.
        metadata["n"] is the matrix dimension.

    Raises:
        ValueError: If fewer than n² letters are provided, or the plaintext matrix
                    is not invertible mod 26.
    """
    if n < 2:
        raise ValueError(f"Matrix dimension must be at least 2, got {n}")

    def _letters(data: bytes) -> list[int]:
        return [b - 65 if 65 <= b <= 90 else b - 97 for b in data if 65 <= b <= 90 or 97 <= b <= 122]

    plain_vals = _letters(plaintext)
    cipher_vals = _letters(ciphertext)

    needed = n * n
    if len(plain_vals) < needed:
        raise ValueError(f"Need ≥ {needed} plaintext letters for {n}×{n} Hill, got {len(plain_vals)}")
    if len(cipher_vals) < needed:
        raise ValueError(f"Need ≥ {needed} ciphertext letters for {n}×{n} Hill, got {len(cipher_vals)}")

    plain_vals = plain_vals[:needed]
    cipher_vals = cipher_vals[:needed]

    # Build n×n matrices whose columns are successive n-letter blocks.
    # P[i][j] = j-th block's i-th letter  (column j = block j)
    P = [[plain_vals[j * n + i] for j in range(n)] for i in range(n)]
    C = [[cipher_vals[j * n + i] for j in range(n)] for i in range(n)]

    # K = C × P⁻¹ (mod 26)
    P_inv = _inverse_mod26(P)
    K = _matmul_mod26(C, P_inv, n)

    return HordeResult(
        bytes(val for row in K for val in row),
        metadata={"key_matrix": K, "n": n},
    )
