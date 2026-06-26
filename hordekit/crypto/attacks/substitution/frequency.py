from hordekit.core.result import HordeResult

_EN_FREQ: dict[str, float] = {
    "e": 0.1202,
    "t": 0.0910,
    "a": 0.0812,
    "o": 0.0768,
    "i": 0.0731,
    "n": 0.0695,
    "s": 0.0628,
    "r": 0.0602,
    "h": 0.0592,
    "d": 0.0432,
    "l": 0.0398,
    "u": 0.0288,
    "c": 0.0271,
    "m": 0.0261,
    "f": 0.0230,
    "y": 0.0211,
    "w": 0.0209,
    "g": 0.0203,
    "p": 0.0182,
    "b": 0.0149,
    "v": 0.0111,
    "k": 0.0069,
    "x": 0.0017,
    "q": 0.0011,
    "j": 0.0010,
    "z": 0.0007,
}


def _letter_frequencies(text: str) -> dict[str, float]:
    letters = [c for c in text.lower() if c.isalpha()]
    total = len(letters)
    if total == 0:
        return {}
    counts: dict[str, int] = {}
    for c in letters:
        counts[c] = counts.get(c, 0) + 1
    return {c: count / total for c, count in counts.items()}


def _rank_by_frequency(text: str) -> list[str]:
    freq = _letter_frequencies(text)
    return [c for c, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)]


def frequency_analysis(ciphertext: bytes) -> HordeResult:
    text = ciphertext.decode("utf-8", errors="ignore")
    cipher_ranked = _rank_by_frequency(text)
    en_ranked = list(_EN_FREQ.keys())

    mapping: dict[str, str] = {}
    for i, cipher_char in enumerate(cipher_ranked):
        if i < len(en_ranked):
            mapping[cipher_char] = en_ranked[i]

    translation: dict[int, int] = {}
    for cipher_char, plain_char in mapping.items():
        translation[ord(cipher_char)] = ord(plain_char)
        translation[ord(cipher_char.upper())] = ord(plain_char.upper())

    decrypted = bytes(translation.get(b, b) for b in ciphertext)

    candidates: list[tuple[str, str]] = [(k, v) for k, v in sorted(mapping.items())]

    return HordeResult(decrypted, metadata={"mapping": mapping, "candidates": candidates})
