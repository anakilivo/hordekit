from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Baconian(BaseCipher):
    """Baconian (Bacon's) cipher — a 5-bit binary encoding of the alphabet.

    Each letter is replaced by a group of five symbols drawn from two distinct
    characters (``A`` and ``B`` by default). This implementation uses the modern
    unambiguous 26-letter mapping, where the code is simply the letter's index
    in MSB-first binary: A = ``AAAAA`` (00000), B = ``AAAAB`` (00001), … Z =
    ``BBAAB`` (11001). Case is not preserved (the output is a binary code), and
    non-letter bytes pass through unchanged. The two code symbols are
    configurable so the cipher can be layered into a steganographic carrier.
    """

    def __init__(self, zero: bytes = b"A", one: bytes = b"B") -> None:
        if len(zero) != 1 or len(one) != 1:
            raise ValueError("zero and one must each be exactly one byte")
        if zero == one:
            raise ValueError("zero and one must be different bytes")
        self._zero = zero[0]
        self._one = one[0]

    def encrypt(self, data: bytes) -> HordeResult:
        result: list[int] = []
        for b in data:
            if 65 <= b <= 90:
                v = b - 65
            elif 97 <= b <= 122:
                v = b - 97
            else:
                result.append(b)
                continue
            for i in range(5):  # MSB first
                result.append(self._one if (v >> (4 - i)) & 1 else self._zero)
        return HordeResult(bytes(result))

    def decrypt(self, data: bytes) -> HordeResult:
        result: list[int] = []
        bits: list[int] = []
        for b in data:
            if b == self._zero:
                bits.append(0)
            elif b == self._one:
                bits.append(1)
            else:
                # Non-code byte: flush any partial group as raw symbols, then
                # pass the byte through unchanged.
                for bit in bits:
                    result.append(self._one if bit else self._zero)
                bits = []
                result.append(b)
                continue
            if len(bits) == 5:
                v = 0
                for bit in bits:
                    v = (v << 1) | bit
                result.append(65 + v)  # uppercase letter
                bits = []
        # Dangling incomplete group — emit its raw symbols unchanged
        for bit in bits:
            result.append(self._one if bit else self._zero)
        return HordeResult(bytes(result))
