from collections.abc import Callable
from typing import Any

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult
from hordekit.crypto.attacks.scoring import quadgram_score


def brute_force(
    cipher_cls: type[BaseCipher],
    ciphertext: bytes,
    scorer: Callable[[bytes], float] | None = None,
) -> HordeResult:
    score_fn = scorer if scorer is not None else quadgram_score
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
