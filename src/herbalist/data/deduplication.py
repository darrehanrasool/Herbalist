"""Image deduplication via cryptographic and perceptual hashing."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Set
from PIL import Image


def compute_file_md5(path: Path) -> str:
    """Compute MD5 of file content for exact duplicate detection."""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_difference_hash(image_path: Path, hash_size: int = 8) -> str:
    """Compute perceptual difference hash (dHash) for visual duplicate detection."""
    with Image.open(image_path) as img:
        img_gray = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = list(img_gray.getdata())
        diff = []
        for row in range(hash_size):
            for col in range(hash_size):
                idx = row * (hash_size + 1) + col
                diff.append(pixels[idx] > pixels[idx + 1])
        return "".join("1" if b else "0" for b in diff)


def find_duplicate_images(image_dir: Path) -> Dict[str, List[Path]]:
    """Scan directory and group identical files by MD5 checksum."""
    hashes: Dict[str, List[Path]] = {}
    for p in image_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            h = compute_file_md5(p)
            hashes.setdefault(h, []).append(p)
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}
