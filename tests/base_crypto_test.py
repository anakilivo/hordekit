"""
Base test class for cryptographic algorithms.

Provides common test methods and utilities for testing:
- Basic encryption/decryption
- Parameter validation
- Attack methods
- Input/output formats
- Error handling
"""

import sys

import pytest
from faker import Faker
from pathlib import Path
from typing import Any, Dict, List, Type

from hordekit.crypto.utils import CryptoAlgorithm

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class BaseCryptoTest:
    """
    Base test class for cryptographic algorithms.

    Provides common test methods and utilities for testing:
    - Basic encryption/decryption
    - Parameter validation
    - Attack methods
    - Input/output formats
    - Error handling
    """

    # Override these in subclasses
    algorithm_class: Type[CryptoAlgorithm] = None
    valid_parameters: Dict[str, Any] = {}
    invalid_parameters: List[Dict[str, Any]] = []

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Skip setup if this is the base class (algorithm_class is None)
        if self.algorithm_class is None:
            pytest.skip("Base class - no algorithm_class defined")

        # Create instance with valid parameters
        self.algorithm = self.algorithm_class(**self.valid_parameters)

    def test_basic_encryption_decryption(self):
        """Test basic encryption and decryption functionality."""
        fake = Faker()

        # Test with random strings
        for _ in range(5):  # Test 5 random strings
            random_message = fake.text(max_nb_chars=50).strip()
            if random_message:  # Skip empty strings
                encrypted = self.algorithm.encode(random_message)
                decrypted = self.algorithm.decode(encrypted)
                assert random_message == decrypted

    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test valid parameters
        try:
            instance = self.algorithm_class(**self.valid_parameters)
            assert isinstance(instance, self.algorithm_class)
        except Exception as e:
            pytest.fail(f"Valid parameters should not raise exception: {e}")

        # Test invalid parameters
        for invalid_params in self.invalid_parameters:
            with pytest.raises(ValueError):
                self.algorithm_class(**invalid_params)

    def test_unknown_attack_method(self):
        """Test error handling for unknown attack methods."""
        with pytest.raises(ValueError):
            self.algorithm.attack("unknown_method", ciphertext="test")

    def test_missing_attack_parameters(self):
        """Test error handling for missing attack parameters."""
        # Get first available attack method
        methods = self.algorithm_class.SUPPORTED_ATTACK_METHODS
        if methods:
            first_method = methods[0]
            with pytest.raises(ValueError):
                self.algorithm.attack(first_method)

    def test_bytes_input(self):
        """Test encryption with bytes input."""
        fake = Faker()

        # Test with random strings
        for _ in range(3):  # Test 3 random strings
            random_message = fake.text(max_nb_chars=30).strip()
            if random_message:  # Skip empty strings
                message_bytes = random_message.encode("utf-8")
                encrypted = self.algorithm.encode(message_bytes)
                decrypted = self.algorithm.decode(encrypted)
                assert message_bytes == decrypted

    def test_empty_string(self):
        """Test encryption of empty string."""
        encrypted = self.algorithm.encode("")
        decrypted = self.algorithm.decode(encrypted)
        assert "" == decrypted

    def test_key_generation(self):
        """Test key generation functionality."""
        generated = self.algorithm_class.generate_key()
        assert isinstance(generated, self.algorithm_class)

    def test_algorithm_initialization(self):
        """Test that algorithm can be initialized with valid parameters."""
        instance = self.algorithm_class(**self.valid_parameters)
        assert isinstance(instance, self.algorithm_class)
        assert isinstance(instance, CryptoAlgorithm)

    def test_attack_methods_availability(self):
        """Test that all listed attack methods are available."""
        methods = self.algorithm_class.SUPPORTED_ATTACK_METHODS
        for method in methods:
            assert hasattr(self.algorithm_class, f"_attack_{method.value}"), f"Attack method {method.value} not found"

    def test_algorithm_inheritance(self):
        """Test that algorithm properly inherits from CryptoAlgorithm."""
        assert issubclass(self.algorithm_class, CryptoAlgorithm)

    def test_abstract_methods_implementation(self):
        """Test that all abstract methods are implemented."""
        required_methods = [
            "_validate_parameters",
            "_setup_algorithm",
            "_encode_raw",
            "_decode_raw",
            "generate_key",
        ]

        for method_name in required_methods:
            assert hasattr(self.algorithm_class, method_name), f"Required method {method_name} not implemented"

    def test_algorithm_consistency(self):
        """Test that algorithm produces consistent results."""
        fake = Faker()

        # Test with random message
        random_message = fake.text(max_nb_chars=40).strip()
        if random_message:
            results_random = []
            for _ in range(3):
                encrypted = self.algorithm.encode(random_message)
                results_random.append(encrypted)

            # For deterministic algorithms, results should be the same
            if hasattr(self, "test_deterministic") and self.test_deterministic:
                assert (
                    len(set(results_random)) == 1
                ), "Deterministic algorithm should produce same results for random input"

    def test_error_messages(self):
        """Test that error messages are informative."""
        # Test invalid parameters
        for invalid_params in self.invalid_parameters:
            try:
                self.algorithm_class(**invalid_params)
                pytest.fail("Should have raised ValueError")
            except ValueError as e:
                assert isinstance(str(e), str)
                assert len(str(e)) > 0

    def test_algorithm_properties(self):
        """Test that algorithm has expected properties."""
        # Test that algorithm can be instantiated
        assert self.algorithm is not None

        # Test that algorithm can encode/decode
        test_message = "test"
        encrypted = self.algorithm.encode(test_message)
        assert encrypted is not None

        decrypted = self.algorithm.decode(encrypted)
        assert test_message == decrypted
