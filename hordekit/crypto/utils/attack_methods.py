"""
Attack method enums for cryptographic algorithms.
"""

from enum import Enum


class AttackMethod(Enum):
    """Available attack methods."""

    BRUTE_FORCE = "brute_force"
    FREQUENCY_ANALYSIS = "frequency_analysis"
    KNOWN_PLAINTEXT = "known_plaintext"
