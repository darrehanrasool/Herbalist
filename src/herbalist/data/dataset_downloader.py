"""Downloader utility for external datasets and mirrors."""
from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen
from typing import Optional


def download_file(url: str, destination: Path, timeout: int = 60) -> bool:
    """Download a file via HTTP/HTTPS with proper User-Agent headers."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = Request(url, headers={"User-Agent": "HerbalistAI-Research/2.0"})
        with urlopen(req, timeout=timeout) as response, open(destination, "wb") as out_file:
            out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def extract_zip(archive_path: Path, extract_to: Path) -> bool:
    """Unzip an archive safely."""
    if not archive_path.exists():
        return False
    extract_to.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")
        return False


def download_from_kaggle(dataset_slug: str, target_dir: Path) -> bool:
    """Download a dataset via Kaggle CLI if credentials are present."""
    target_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "kaggle", "datasets", "download",
        "-d", dataset_slug, "-p", str(target_dir), "--unzip"
    ]
    try:
        subprocess.check_call(cmd)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Kaggle download skipped or failed for {dataset_slug}: {e}")
        return False
