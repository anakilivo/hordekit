from hordekit.core.result import HordeResult

_EN_IOC = 0.065
_RAND_IOC = 0.038


def _ioc(letters: str) -> float:
    n = len(letters)
    if n < 2:
        return 0.0
    counts: dict[str, int] = {}
    for c in letters:
        counts[c] = counts.get(c, 0) + 1
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def index_of_coincidence(ciphertext: bytes, max_key_length: int = 20) -> HordeResult:
    """Calculate the Index of Coincidence to identify cipher type and likely key length.

    IoC ≈ 0.065 for English plaintext (monoalphabetic cipher or unencrypted).
    IoC ≈ 0.038 for uniform random distribution (polyalphabetic cipher).

    For polyalphabetic ciphers (e.g. Vigenère), splitting ciphertext into columns
    of length equal to the key length produces columns with IoC near 0.065.

    Args:
        ciphertext: Bytes to analyse.
        max_key_length: Maximum key length to test (1 to max_key_length).

    Returns:
        HordeResult wrapping the original ciphertext with metadata:
            - ``overall_ioc``: IoC of the full text.
            - ``ioc_by_key_length``: dict mapping key length -> average column IoC.
            - ``likely_key_length``: key length whose column IoC is closest to English.
            - ``interpretation``: "monoalphabetic" | "polyalphabetic".

    Example::

        from hordekit.crypto.attacks.substitution import index_of_coincidence

        result = index_of_coincidence(ciphertext)
        print(result.metadata["overall_ioc"])
        print(result.metadata["likely_key_length"])
    """
    text = ciphertext.decode("utf-8", errors="ignore").upper()
    letters = "".join(c for c in text if c.isalpha())

    overall = _ioc(letters)

    ioc_by_length: dict[int, float] = {}
    for key_len in range(1, max_key_length + 1):
        columns = [letters[i::key_len] for i in range(key_len)]
        ioc_by_length[key_len] = sum(_ioc(col) for col in columns) / key_len

    # Prefer the *smallest* key length whose average column IoC is above the
    # English threshold (0.060). Multiples of the true key also pass the threshold,
    # but the minimal one is the correct answer.
    _THRESHOLD = 0.060
    above_threshold = {k: v for k, v in ioc_by_length.items() if v >= _THRESHOLD}
    if above_threshold:
        likely_key_length = min(above_threshold)
    else:
        likely_key_length = min(ioc_by_length, key=lambda k: abs(ioc_by_length[k] - _EN_IOC))

    interpretation = "monoalphabetic" if overall > 0.055 else "polyalphabetic"

    return HordeResult(
        ciphertext,
        metadata={
            "overall_ioc": overall,
            "ioc_by_key_length": ioc_by_length,
            "likely_key_length": likely_key_length,
            "interpretation": interpretation,
        },
    )
