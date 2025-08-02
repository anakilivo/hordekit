"""
Abstract base class for cryptographic algorithms.
"""

import io
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Optional, Tuple

from .attack_methods import AttackMethod


class CryptoAlgorithm(ABC):
    # supported attack methods
    SUPPORTED_ATTACK_METHODS: List[AttackMethod] = []

    def __init__(self, **kwargs: Any) -> None:
        """Initialize algorithm with given parameters"""
        self._validate_parameters(**kwargs)
        self._setup_algorithm(**kwargs)

    @abstractmethod
    def _validate_parameters(self, **kwargs: Any) -> None:
        """Validate algorithm parameters, raise exception if invalid"""

    @abstractmethod
    def _setup_algorithm(self, **kwargs: Any) -> None:
        """Configure algorithm with validated parameters"""

    def encode(self, input_data: Any, **kwargs: Any) -> Any:
        """Encrypt/encode input data with automatic format detection"""
        data, data_type = self._parse_input(input_data)
        processed = self._encode_raw(data, **kwargs)
        return self._format_output(processed, data_type, **kwargs)

    def decode(self, input_data: Any, **kwargs: Any) -> Any:
        """Decrypt/decode input data with automatic format detection"""
        data, data_type = self._parse_input(input_data)
        processed = self._decode_raw(data, **kwargs)
        return self._format_output(processed, data_type, **kwargs)

    @abstractmethod
    def _encode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Low-level encryption implementation (to be implemented by subclasses)"""

    @abstractmethod
    def _decode_raw(self, data: bytes, **kwargs: Any) -> bytes:
        """Low-level decryption implementation (to be implemented by subclasses)"""

    def _parse_input(self, input_data: Any) -> Tuple[bytes, str]:
        """
        Detect input data format and convert to bytes.
        Supported formats:
        - bytes, bytearray
        - str (utf-8, base64, hex)
        - files (paths, file-like objects)
        - JSON (dict, list)
        Returns tuple of (data_bytes, data_type)
        """
        if isinstance(input_data, (bytes, bytearray)):
            return bytes(input_data), "bytes"

        elif isinstance(input_data, str):
            try:
                return input_data.encode("utf-8"), "string"
            except UnicodeEncodeError:
                raise ValueError("String encoding failed. Use explicit format prefix like " "base64: or hex:")

        elif isinstance(input_data, (io.IOBase, io.BufferedIOBase)):
            return input_data.read(), "file-like"

        elif isinstance(input_data, Path):
            with input_data.open("rb") as f:
                return f.read(), "path"

        elif isinstance(input_data, (dict, list)):
            return json.dumps(input_data).encode("utf-8"), "json"

        else:
            raise ValueError(f"Unsupported input type: {type(input_data)}. " "Supported: bytes, str, file, dict, list")

    def _format_output(self, data: bytes, data_type: str, **kwargs: Any) -> Any:
        """
        Convert output bytes back to original format.
        Supports explicit format specification via output_format parameter.
        """
        # Automatic conversion based on input type
        if data_type == "bytes":
            return data
        elif data_type == "string":
            return data.decode("utf-8")
        elif data_type in ("file", "path"):
            output_path = kwargs.get("output_path", "output.bin")
            Path(output_path).write_bytes(data)
            return output_path
        elif data_type == "file-like":
            output = kwargs.get("output_file")
            if not output:
                raise ValueError("output_file required for file-like output")
            output.write(data)
            return True
        elif data_type == "json":
            return json.loads(data.decode("utf-8"))
        else:
            return data

    @classmethod
    @abstractmethod
    def generate_key(cls, key_size: Optional[int] = None, **kwargs: Any) -> Any:
        """Generate cryptographic key for the algorithm"""

    @classmethod
    def attack(cls, attack_method: AttackMethod, **kwargs: Any) -> Optional[Any]:
        """Execute specified attack method on the algorithm"""
        if attack_method not in cls.SUPPORTED_ATTACK_METHODS:
            raise ValueError(
                f"Unknown attack method: {attack_method}. Available: {[m.value for m in cls.SUPPORTED_ATTACK_METHODS]}"
            )

        method = getattr(cls, f"_attack_{attack_method.value}", None)
        if not method:
            raise NotImplementedError(f"Attack method '{attack_method.value}' not implemented")

        return method(**kwargs)
