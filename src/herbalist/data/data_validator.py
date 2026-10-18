"""Data validation routines for image files and tabular catalogs."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple, List, Optional
import pandas as pd
from PIL import Image

from ..core.exceptions import CorruptImageError, DataValidationError


def validate_image(image_path: Path) -> Tuple[bool, Optional[str]]:
    """Check if an image exists, can be opened, and has valid non-zero dimensions."""
    if not image_path.exists():
        return False, f"File does not exist: {image_path}"
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify integrity without decoding fully
        # Re-open to check mode & size since verify() closes/invalidates the handle
        with Image.open(image_path) as img:
            width, height = img.size
            if width <= 0 or height <= 0:
                return False, f"Invalid image dimensions: {width}x{height}"
            if img.mode not in ("RGB", "RGBA", "L"):
                return False, f"Unsupported color mode: {img.mode}"
        return True, None
    except Exception as e:
        return False, f"Corrupted or invalid image: {e}"


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """Verify that a DataFrame contains all mandatory schema columns."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return False, missing
    return True, []
