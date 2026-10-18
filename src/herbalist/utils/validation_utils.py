"""Validation helpers for user inputs and file paths."""
from __future__ import annotations

from pathlib import Path
from typing import Union, List


def check_file_exists(file_path: Union[str, Path]) -> bool:
    """Return True if path exists and is a file."""
    p = Path(file_path)
    return p.exists() and p.is_file()


def check_allowed_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file suffix against whitelist."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in [e.lower().lstrip(".") for e in allowed_extensions]
