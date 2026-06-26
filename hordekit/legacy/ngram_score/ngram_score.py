from math import log10

import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.resolve()


class _NScoring:
    _ngrams: dict[str, float]
    _filename: str = ""
    _N: int = 0
    _floor: float = 0.01

    def __init__(self) -> None:
        ngrams = str(ROOT_DIR.joinpath(self._filename).resolve())
        self._ngrams = {}
        for line in open(ngrams, "r"):
            key, count = line.split(" ")
            self._ngrams[key] = int(count)

        summary = sum(self._ngrams.values())
        # calculate log probabilities
        for key in self._ngrams.keys():
            self._ngrams[key] = log10(self._ngrams[key] / summary)

        self._floor = log10(0.01 / summary)

    def score(self, text: str) -> float:
        score = 0.0
        ngrams = self._ngrams.__getitem__
        for i in range(len(text) - self._N + 1):
            ngram = text[i : i + self._N].upper()
            if ngram in self._ngrams:
                score += ngrams(ngram)
            else:
                score += self._floor
        return score


class MonogramScore(_NScoring):
    _N = 1
    _filename = "monograms.txt"


class BigramScore(_NScoring):
    _N = 2
    _filename = "bigrams.txt"


class TrigramScore(_NScoring):
    _N = 3
    _filename = "trigrams.txt"


class QuadgramScore(_NScoring):
    _N = 4
    _filename = "quadgrams.txt"
