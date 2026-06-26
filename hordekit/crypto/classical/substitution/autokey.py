from hordekit.core.base import BaseCipher
from hordekit.core.result import HordeResult


class Autokey(BaseCipher):
    def __init__(self, key: bytes) -> None:
        values: list[int] = []
        for b in key:
            if 65 <= b <= 90:
                values.append(b - 65)
            elif 97 <= b <= 122:
                values.append(b - 97)
            else:
                raise ValueError(f"Key must contain only ASCII letters, got byte {b!r}")
        if not values:
            raise ValueError("Key must not be empty")
        self._key = values

    def encrypt(self, data: bytes) -> HordeResult:
        result = []
        plaintext_letters: list[int] = []
        letter_count = 0
        for b in data:
            if 65 <= b <= 90:
                k = (
                    self._key[letter_count]
                    if letter_count < len(self._key)
                    else plaintext_letters[letter_count - len(self._key)]
                )
                plain_idx = b - 65
                result.append((plain_idx + k) % 26 + 65)
                plaintext_letters.append(plain_idx)
                letter_count += 1
            elif 97 <= b <= 122:
                k = (
                    self._key[letter_count]
                    if letter_count < len(self._key)
                    else plaintext_letters[letter_count - len(self._key)]
                )
                plain_idx = b - 97
                result.append((plain_idx + k) % 26 + 97)
                plaintext_letters.append(plain_idx)
                letter_count += 1
            else:
                result.append(b)
        return HordeResult(bytes(result))

    def decrypt(self, data: bytes) -> HordeResult:
        result = []
        decrypted_letters: list[int] = []
        letter_count = 0
        for b in data:
            if 65 <= b <= 90:
                k = (
                    self._key[letter_count]
                    if letter_count < len(self._key)
                    else decrypted_letters[letter_count - len(self._key)]
                )
                plain_idx = (b - 65 - k) % 26
                result.append(plain_idx + 65)
                decrypted_letters.append(plain_idx)
                letter_count += 1
            elif 97 <= b <= 122:
                k = (
                    self._key[letter_count]
                    if letter_count < len(self._key)
                    else decrypted_letters[letter_count - len(self._key)]
                )
                plain_idx = (b - 97 - k) % 26
                result.append(plain_idx + 97)
                decrypted_letters.append(plain_idx)
                letter_count += 1
            else:
                result.append(b)
        return HordeResult(bytes(result))
