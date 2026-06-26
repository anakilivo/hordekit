from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hordekit.legacy.ngram_score import BigramScore, MonogramScore, QuadgramScore, TrigramScore

_mono: MonogramScore | None = None
_bi: BigramScore | None = None
_tri: TrigramScore | None = None
_quad: QuadgramScore | None = None


def _get_mono() -> MonogramScore:
    global _mono
    if _mono is None:
        from hordekit.legacy.ngram_score import MonogramScore

        _mono = MonogramScore()
    return _mono


def _get_bi() -> BigramScore:
    global _bi
    if _bi is None:
        from hordekit.legacy.ngram_score import BigramScore

        _bi = BigramScore()
    return _bi


def _get_tri() -> TrigramScore:
    global _tri
    if _tri is None:
        from hordekit.legacy.ngram_score import TrigramScore

        _tri = TrigramScore()
    return _tri


def _get_quad() -> QuadgramScore:
    global _quad
    if _quad is None:
        from hordekit.legacy.ngram_score import QuadgramScore

        _quad = QuadgramScore()
    return _quad


def monogram_score(data: bytes) -> float:
    return _get_mono().score(data.decode("utf-8", errors="ignore"))


def bigram_score(data: bytes) -> float:
    return _get_bi().score(data.decode("utf-8", errors="ignore"))


def trigram_score(data: bytes) -> float:
    return _get_tri().score(data.decode("utf-8", errors="ignore"))


def quadgram_score(data: bytes) -> float:
    return _get_quad().score(data.decode("utf-8", errors="ignore"))
