"""
Download research datasets into data/raw/kaggle/<slug>/.

Kaggle: put credentials in ~/.kaggle/kaggle.json (or KAGGLE_USERNAME + KAGGLE_KEY).
Without Kaggle, this still pulls the VNPlant-200 community listing + small GitHub chemistry repo.
"""
from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlretrieve, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw" / "kaggle"
LOG = ROOT / "research" / "datasets" / "download_log.txt"

# Only SMALL tables by default. The Indian medicinal leaves dump is ~9GB — do not
# auto-download it. Fetch it yourself into data/raw/kaggle/indian-medicinal-leaves-dataset
# when you have disk: kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset
KAGGLE_SETS = [
    "atharvaingle/crop-recommendation-dataset",
]


def log(msg: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(msg + "\n")
    print(msg)


def download(url: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "HerbalistAI/1.0"})
    with urlopen(req, timeout=60) as r, open(path, "wb") as out:
        out.write(r.read())
    log(f"OK {url} -> {path} ({path.stat().st_size} bytes)")


def try_kaggle():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "kaggle"])
    except subprocess.CalledProcessError:
        log("pip kaggle failed")
        return
    for slug in KAGGLE_SETS:
        owner, name = slug.split("/")
        out = DEST / name
        out.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable, "-m", "kaggle", "datasets", "download",
            "-d", slug, "-p", str(out), "--unzip",
        ]
        try:
            subprocess.check_call(cmd)
            log(f"KAGGLE OK {slug}")
        except subprocess.CalledProcessError as e:
            log(f"KAGGLE SKIP {slug} ({e})")


def github_small_files():
    # VNPlant-200 README mirror
    download(
        "https://raw.githubusercontent.com/kencoca/VietNam-Medicinal-Plant/master/README.md",
        DEST / "vnplant-200" / "README.md",
    )
    (DEST / "vnplant-200" / "SOURCE.txt").write_text(
        "Original paper: VNPlant-200\n"
        "GitHub listing: https://github.com/kencoca/VietNam-Medicinal-Plant\n"
        "Google Drive images (from that README): "
        "https://drive.google.com/drive/folders/1DaoCCGhx1SYDYSFgYbbMr7RJ0Y9Ht5GL\n"
        "Place unzipped class folders in data/splits/train and data/splits/validation\n"
    )
    # Crop recommendation CSV is small and useful for soil-NPK UI prototypes
    # (Kaggle clone often mirrored; try official kaggle first)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    github_small_files()
    try_kaggle()
    log("Done. See research/DATASETS.md")


if __name__ == "__main__":
    main()
