"""Prepare, clean, and standardize plant catalogs and tabular data."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from src.herbalist.data.missing_values import impute_catalog_missing
from src.herbalist.data.feature_engineering import encode_botanical_features


def prepare_catalogs():
    raw_med = ROOT / "data" / "raw" / "clinical" / "medicinal.csv"
    raw_kashmir = ROOT / "data" / "raw" / "clinical" / "Kashmere.csv"
    out_med = ROOT / "data" / "processed" / "medicinal.csv"
    out_kashmir = ROOT / "data" / "processed" / "kashmir_medicinal.csv"

    print("Cleaning and standardizing catalogs...")
    if raw_med.exists():
        df_med = pd.read_csv(raw_med)
        df_med = impute_catalog_missing(df_med)
        df_med = encode_botanical_features(df_med)
        out_med.parent.mkdir(parents=True, exist_ok=True)
        df_med.to_csv(out_med, index=False)
        print(f"✅ Processed {len(df_med)} records -> {out_med.relative_to(ROOT)}")

    if raw_kashmir.exists():
        df_kash = pd.read_csv(raw_kashmir)
        df_kash = impute_catalog_missing(df_kash)
        df_kash = encode_botanical_features(df_kash)
        out_kashmir.parent.mkdir(parents=True, exist_ok=True)
        df_kash.to_csv(out_kashmir, index=False)
        print(f"✅ Processed {len(df_kash)} records -> {out_kashmir.relative_to(ROOT)}")


if __name__ == "__main__":
    prepare_catalogs()
