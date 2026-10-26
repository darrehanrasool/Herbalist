"""Script to partition datasets into train, validation, and test splits.

- Vision Image Datasets: Partitioned into class folders in `data/processed/train/`, `val/`, `test/`.
- Tabular Metadata Splits: Stored cleanly in `data/csv/tabular_splits/`.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from src.herbalist.data.data_splitting import create_stratified_splits


def split_tabular_data():
    master_path = ROOT / "data" / "csv" / "medicinal.csv"
    if not master_path.exists():
        master_path = ROOT / "knowledge" / "plants_master.csv"
    if not master_path.exists():
        print("Warning: medicinal.csv / plants_master.csv not found")
        return

    df = pd.read_csv(master_path)
    target_col = "iucn_conservation_status" if "iucn_conservation_status" in df.columns else (
        "ToxicityLevel" if "ToxicityLevel" in df.columns else None
    )
    if not target_col:
        return

    train_df, val_df, test_df = create_stratified_splits(
        df, target_column=target_col, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15
    )

    splits_dir = ROOT / "data" / "csv" / "tabular_splits"
    splits_dir.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(splits_dir / "plants_tabular_train.csv", index=False)
    val_df.to_csv(splits_dir / "plants_tabular_val.csv", index=False)
    test_df.to_csv(splits_dir / "plants_tabular_test.csv", index=False)

    print(f"✅ Tabular splits created in data/csv/tabular_splits/: {len(train_df)} train, {len(val_df)} val, {len(test_df)} test")


def partition_vision_data():
    from scripts.partition_vision_dataset import partition_vision_images
    partition_vision_images()


if __name__ == "__main__":
    split_tabular_data()
    partition_vision_data()
