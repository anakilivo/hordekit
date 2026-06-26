from functools import reduce
from math import gcd

from hordekit.core.result import HordeResult


def _gcd_list(numbers: list[int]) -> int:
    return reduce(gcd, numbers)


def kasiski(ciphertext: bytes, ngram_size: int = 3, max_key_length: int = 20) -> HordeResult:
    """Kasiski test: find repeated n-grams to estimate Vigenère key length.

    Repeated substrings in a Vigenère ciphertext tend to appear at distances
    that are multiples of the key length. This test collects those distances,
    factors them, and ranks the most frequent factors as likely key lengths.

    Args:
        ciphertext: Bytes to analyse (only letter bytes are considered).
        ngram_size: Minimum repeated substring length to search for (default 3).
        max_key_length: Maximum factor to consider as a key length (default 20).

    Returns:
        HordeResult wrapping the original ciphertext with metadata:
            - ``likely_key_lengths``: list of up to 5 candidate lengths, best first.
            - ``factor_counts``: dict mapping each factor to how many spacings it divides.
            - ``spacings``: raw list of distances between repeated n-grams.

    Example::

        from hordekit.crypto.attacks.vigenere import kasiski

        result = kasiski(ciphertext)
        print(result.metadata["likely_key_lengths"])  # e.g. [6, 3, 12, ...]
    """
    text = ciphertext.decode("utf-8", errors="ignore").upper()
    letters = "".join(c for c in text if c.isalpha())

    if len(letters) < ngram_size * 3:
        return HordeResult(
            ciphertext,
            metadata={
                "likely_key_lengths": [],
                "factor_counts": {},
                "spacings": [],
                "error": "Insufficient ciphertext length for Kasiski test",
            },
        )

    seen: dict[str, int] = {}
    spacings: list[int] = []

    for i in range(len(letters) - ngram_size + 1):
        ngram = letters[i : i + ngram_size]
        if ngram in seen:
            spacings.append(i - seen[ngram])
        seen[ngram] = i

    if not spacings:
        return HordeResult(
            ciphertext,
            metadata={
                "likely_key_lengths": [],
                "factor_counts": {},
                "spacings": [],
                "error": "No repeated trigrams found — ciphertext may be too short",
            },
        )

    factor_counts: dict[int, int] = {}
    for spacing in spacings:
        for f in range(2, min(spacing + 1, max_key_length + 1)):
            if spacing % f == 0:
                factor_counts[f] = factor_counts.get(f, 0) + 1

    sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
    likely_key_lengths = [k for k, _ in sorted_factors[:5]]

    return HordeResult(
        ciphertext,
        metadata={
            "likely_key_lengths": likely_key_lengths,
            "factor_counts": factor_counts,
            "spacings": spacings,
        },
    )
