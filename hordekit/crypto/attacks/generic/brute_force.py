import math
from collections.abc import Callable
from typing import Any

from hordekit.core.base import BaseCipher
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


def _default_scorer(data: bytes) -> float:
    text = data.decode("utf-8", errors="ignore").lower()
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return float("-inf")
    return sum(math.log(_EN_FREQ.get(c, 1e-10)) for c in letters)


def brute_force(
    cipher_cls: type[BaseCipher],
    ciphertext: bytes,
    scorer: Callable[[bytes], float] | None = None,
) -> HordeResult:
    score_fn = scorer if scorer is not None else _default_scorer
    keys = cipher_cls.possible_keys()

    candidates: list[dict[str, Any]] = []
    for key in keys:
        instance = cipher_cls(**key)
        result = instance.decrypt(ciphertext)
        score = score_fn(result.as_bytes())
        candidates.append({"key": key, "result": result, "score": score})

    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[0]["result"]

    return HordeResult(best.as_bytes(), metadata={"candidates": candidates})
