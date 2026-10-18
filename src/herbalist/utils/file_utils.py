"""Safe file input/output utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union
import pandas as pd


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists and return Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_read_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """Safely load CSV returning empty DataFrame if missing."""
    p = Path(file_path)
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p, **kwargs)
    except Exception as e:
        print(f"Error reading CSV at {p}: {e}")
        return pd.DataFrame()


def safe_write_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> bool:
    """Write dictionary or serializable object to JSON file."""
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        print(f"Error writing JSON to {p}: {e}")
        return False
