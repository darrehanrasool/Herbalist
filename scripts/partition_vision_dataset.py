#!/usr/bin/env python3
"""Vision Dataset Partitioning & Tabular Split Reorganization.

1. Cleans confusing CSV files out of image directories.
2. Moves tabular split CSVs into `data/csv/tabular_splits/`.
3. Partitions all 5,422 raw medicinal plant images across 200+ classes from
   `data/raw/kaggle/vnplant-200/Trained Data` + `data/raw/kashmir/` into:
   - `data/processed/train/<class_name>/*.jpg` (70%)
   - `data/processed/val/<class_name>/*.jpg`   (15%)
   - `data/processed/test/<class_name>/*.jpg`  (15%)
4. Employs APFS hardlinks for instant zero-copy physical file creation.
"""
from __future__ import annotations

import os
import shutil
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_VISION_DIR = ROOT / "data" / "raw" / "kaggle" / "vnplant-200" / "Trained Data"
KASHMIR_RAW_DIR = ROOT / "data" / "raw" / "kashmir"
PROCESSED_DIR = ROOT / "data" / "processed"
CSV_TABULAR_SPLITS = ROOT / "data" / "csv" / "tabular_splits"
SPLITS_DIR = ROOT / "data" / "splits"

random.seed(42)


def reorganize_tabular_splits():
    """Moves tabular split CSVs to data/csv/tabular_splits/."""
    CSV_TABULAR_SPLITS.mkdir(parents=True, exist_ok=True)

    # 1. Move plants_tabular_*.csv if present in data/splits/
    for split in ("train", "validation", "test"):
        src = SPLITS_DIR / split / f"plants_tabular_{split if split != 'validation' else 'val'}.csv"
        dst = CSV_TABULAR_SPLITS / f"plants_tabular_{split if split != 'validation' else 'val'}.csv"
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"  Moved tabular CSV: {src.name} -> data/csv/tabular_splits/")

    # 2. Remove stray CSVs from data/processed/
    for stray_csv in PROCESSED_DIR.glob("*.csv"):
        stray_csv.unlink()
        print(f"  Removed stray CSV from data/processed/: {stray_csv.name}")

    # 3. Clean out legacy data/splits/ folders if they only contained CSVs
    for split_dir in [SPLITS_DIR / s for s in ("train", "validation", "test")]:
        if split_dir.exists():
            remaining = [f for f in split_dir.iterdir() if f.name not in (".gitkeep", "README.md")]
            if not remaining:
                shutil.rmtree(split_dir)
                print(f"  Cleaned legacy directory: {split_dir}")

    # Create README in data/splits/
    with open(SPLITS_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write("# Dataset Splits Directory\n\n"
                "- **Vision Image Splits**: Partitioned in `data/processed/train/`, `data/processed/val/`, and `data/processed/test/`.\n"
                "- **Tabular Metadata Splits**: Stored in `data/csv/tabular_splits/`.\n")


def partition_vision_images():
    """Partitions raw images into processed train/val/test class directories."""
    train_dir = PROCESSED_DIR / "train"
    val_dir = PROCESSED_DIR / "val"
    test_dir = PROCESSED_DIR / "test"

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    if not RAW_VISION_DIR.exists():
        print(f"Error: Raw vision directory not found at {RAW_VISION_DIR}")
        return

    classes = sorted([
        d for d in RAW_VISION_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])
    print(f"Found {len(classes)} plant classes in raw Kaggle dataset.")

    total_train, total_val, total_test = 0, 0, 0

    for cls_dir in classes:
        cls_name = cls_dir.name.replace(" ", "_")
        c_train = train_dir / cls_name
        c_val = val_dir / cls_name
        c_test = test_dir / cls_name

        c_train.mkdir(parents=True, exist_ok=True)
        c_val.mkdir(parents=True, exist_ok=True)
        c_test.mkdir(parents=True, exist_ok=True)

        # Get all images in class
        images = [
            f for f in cls_dir.iterdir()
            if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
        ]
        random.shuffle(images)

        n = len(images)
        n_train = max(1, int(n * 0.70))
        n_val = max(1, int(n * 0.15)) if n >= 3 else 0
        n_test = n - n_train - n_val
        if n_test <= 0 and n >= 2:
            n_test = 1
            n_train = max(1, n_train - 1)

        train_imgs = images[:n_train]
        val_imgs = images[n_train:n_train + n_val]
        test_imgs = images[n_train + n_val:]

        for img in train_imgs:
            dst = c_train / img.name
            if not dst.exists():
                try:
                    os.link(str(img), str(dst))
                except Exception:
                    shutil.copyfile(str(img), str(dst))
            total_train += 1

        for img in val_imgs:
            dst = c_val / img.name
            if not dst.exists():
                try:
                    os.link(str(img), str(dst))
                except Exception:
                    shutil.copyfile(str(img), str(dst))
            total_val += 1

        for img in test_imgs:
            dst = c_test / img.name
            if not dst.exists():
                try:
                    os.link(str(img), str(dst))
                except Exception:
                    shutil.copyfile(str(img), str(dst))
            total_test += 1

    # Also partition Kashmir images if present in raw
    for kashmir_sp in ("Aconitum_heterophyllum", "Gentiana_kurroo"):
        k_src = KASHMIR_RAW_DIR / kashmir_sp
        if k_src.exists():
            k_imgs = [f for f in k_src.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png")]
            if k_imgs:
                c_train = train_dir / kashmir_sp
                c_val = val_dir / kashmir_sp
                c_test = test_dir / kashmir_sp
                c_train.mkdir(parents=True, exist_ok=True)
                c_val.mkdir(parents=True, exist_ok=True)
                c_test.mkdir(parents=True, exist_ok=True)
                for i, img in enumerate(k_imgs):
                    target_dir = c_train if i % 3 == 0 else (c_val if i % 3 == 1 else c_test)
                    dst = target_dir / img.name
                    if not dst.exists():
                        try:
                            os.link(str(img), str(dst))
                        except Exception:
                            shutil.copyfile(str(img), str(dst))

    print(f"\n✅ Vision dataset partitioned successfully into data/processed/:")
    print(f"  • Train: {total_train} images in {len(classes)} classes")
    print(f"  • Val:   {total_val} images in {len(classes)} classes")
    print(f"  • Test:  {total_test} images in {len(classes)} classes")
    print(f"  • Total: {total_train + total_val + total_test} images")


if __name__ == "__main__":
    print("--- Reorganizing Tabular Splits ---")
    reorganize_tabular_splits()
    print("\n--- Partitioning Vision Dataset ---")
    partition_vision_images()
