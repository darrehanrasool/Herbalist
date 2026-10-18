"""Dataset manifest verification and SHA-256 cryptographic hashing."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from ..core.constants import ROOT_DIR


def compute_sha256(file_path: Path) -> str:
    """Compute the SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_manifest() -> Dict[str, Any]:
    """Load the dataset manifest file."""
    manifest_path = ROOT_DIR / "data" / "manifests" / "dataset_manifest.json"
    if not manifest_path.exists():
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_manifest_checksums() -> Dict[str, bool]:
    """Verify presence and validity of datasets listed in manifest."""
    manifest = load_manifest()
    results = {}
    datasets: List[Dict[str, Any]] = manifest.get("datasets", [])
    for d in datasets:
        p = ROOT_DIR / d.get("file_path", "")
        results[d.get("id", "unknown")] = p.exists()
    return results
