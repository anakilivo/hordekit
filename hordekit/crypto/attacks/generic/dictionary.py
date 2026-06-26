from collections.abc import Callable
from typing import Any

from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult
from hordekit.crypto.attacks.scoring import quadgram_score


def dictionary_attack(
    cipher_cls: type[BaseCipher],
    ciphertext: bytes,
    wordlist: list[dict[str, Any]],
    scorer: Callable[[bytes], float] | None = None,
) -> HordeResult:
    """Try each entry in wordlist as cipher kwargs and return the best-scoring decryption.

    Args:
        cipher_cls: Cipher class to instantiate for each key.
        ciphertext: Bytes to decrypt.
        wordlist: List of kwarg dicts, e.g. [{"key": b"lemon"}, {"key": b"apple"}].
        scorer: Scoring function bytes -> float (higher = more likely English).
                Defaults to quadgram scoring.

    Example::

        from hordekit.crypto.attacks.generic import dictionary_attack
        from hordekit.crypto.classical.substitution import Vigenere

        keys = [{"key": b"lemon"}, {"key": b"apple"}, {"key": b"secret"}]
        result = dictionary_attack(Vigenere, ciphertext, keys)
        print(result.as_str())
        print(result.metadata["candidates"][0]["key"])
    """
    score_fn = scorer if scorer is not None else quadgram_score

    candidates: list[dict[str, Any]] = []
    for key_kwargs in wordlist:
        try:
            instance = cipher_cls(**key_kwargs)
            result = instance.decrypt(ciphertext)
            score = score_fn(result.as_bytes())
            candidates.append({"key": key_kwargs, "result": result, "score": score})
        except Exception:  # noqa: BLE001
            continue

    if not candidates:
        raise ValueError("No valid candidates found — wordlist may be empty or all keys invalid")

    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[0]["result"]

    return HordeResult(best.as_bytes(), metadata={"candidates": candidates})
