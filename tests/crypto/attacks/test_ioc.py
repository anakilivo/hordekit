from hordekit.crypto.attacks.substitution import index_of_coincidence
from hordekit.crypto.classical.substitution import Caesar, Vigenere

# Natural English text with realistic letter frequency distribution (not a pangram)
_EN_TEXT = (
    b"when in the course of human events it becomes necessary for one people to dissolve "
    b"the political bands which have connected them with another and to assume among the "
    b"powers of the earth the separate and equal station to which the laws of nature and "
    b"of natures god entitle them a decent respect to the opinions of mankind requires "
    b"that they should declare the causes which impel them to the separation we hold "
    b"these truths to be self evident that all men are created equal "
)


def test_monoalphabetic_classified_correctly() -> None:
    ct = Caesar(shift=13).encrypt(_EN_TEXT * 2).as_bytes()
    result = index_of_coincidence(ct)
    assert result.metadata["interpretation"] == "monoalphabetic"


def test_polyalphabetic_classified_correctly() -> None:
    ct = Vigenere(key=b"crypto").encrypt(_EN_TEXT * 2).as_bytes()
    result = index_of_coincidence(ct)
    assert result.metadata["interpretation"] == "polyalphabetic"


def test_overall_ioc_range() -> None:
    ct = Caesar(shift=5).encrypt(_EN_TEXT).as_bytes()
    result = index_of_coincidence(ct)
    ioc = result.metadata["overall_ioc"]
    assert 0.03 < ioc < 0.08


def test_likely_key_length_vigenere() -> None:
    key = b"lemon"
    ct = Vigenere(key=key).encrypt(_EN_TEXT * 4).as_bytes()
    result = index_of_coincidence(ct)
    assert result.metadata["likely_key_length"] == len(key)


def test_metadata_keys_present() -> None:
    ct = Caesar(shift=1).encrypt(b"hello world " * 10).as_bytes()
    result = index_of_coincidence(ct)
    assert "overall_ioc" in result.metadata
    assert "ioc_by_key_length" in result.metadata
    assert "likely_key_length" in result.metadata
    assert "interpretation" in result.metadata


def test_returns_original_ciphertext() -> None:
    ct = b"KHOOR ZRUOG" * 5
    result = index_of_coincidence(ct)
    assert result.as_bytes() == ct
