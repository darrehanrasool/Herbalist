"""Cryptographic hashing utilities."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Union


def compute_checksum(path_or_bytes: Union[str, Path, bytes], algorithm: str = "sha256") -> str:
    """Compute cryptographic hash of file or raw bytes."""
    hasher = hashlib.sha256() if algorithm.lower() == "sha256" else hashlib.md5()
    if isinstance(path_or_bytes, bytes):
        hasher.update(path_or_bytes)
        return hasher.hexdigest()

    p = Path(path_or_bytes)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    with open(p, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()
