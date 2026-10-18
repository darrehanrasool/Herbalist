"""Script to partition datasets into train, validation, and test splits."""
from __future__ import annotations

import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from src.herbalist.data.data_splitting import create_stratified_splits


def split_tabular_data():
    master_path = ROOT / "knowledge" / "plants_master.csv"
    if not master_path.exists():
        print("Warning: plants_master.csv not found")
        return

    df = pd.read_csv(master_path)
    if "ToxicityLevel" not in df.columns:
        return

    train_df, val_df, test_df = create_stratified_splits(
        df, target_column="ToxicityLevel", train_ratio=0.70, val_ratio=0.15, test_ratio=0.15
    )

    splits_dir = ROOT / "data" / "splits"
    train_df.to_csv(splits_dir / "train" / "plants_tabular_train.csv", index=False)
    val_df.to_csv(splits_dir / "validation" / "plants_tabular_val.csv", index=False)
    test_df.to_csv(splits_dir / "test" / "plants_tabular_test.csv", index=False)

    print(f"✅ Tabular splits created: {len(train_df)} train, {len(val_df)} val, {len(test_df)} test")


def split_image_directories():
    raw_images = ROOT / "data" / "raw" / "imaging"
    splits_dir = ROOT / "data" / "splits"

    for s in ("train", "validation", "test"):
        (splits_dir / s).mkdir(parents=True, exist_ok=True)

    print("✅ Verified split directories in data/splits/")


if __name__ == "__main__":
    split_tabular_data()
    split_image_directories()
