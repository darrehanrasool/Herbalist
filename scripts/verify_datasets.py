"""Script to inspect and verify dataset integrity, schemas, and file existence."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from src.herbalist.data import load_manifest, verify_manifest_checksums, compute_data_quality_report


def main():
    print("=" * 65)
    print("🌿 HERBALIST AI - DATASET AUDIT & INTEGRITY VERIFICATION")
    print("=" * 65)

    manifest = load_manifest()
    print(f"Manifest Version: {manifest.get('manifest_version', 'Unknown')}")
    print(f"Generated At:     {manifest.get('generated_at', 'Unknown')}")

    results = verify_manifest_checksums()
    print("\nFile Existence Checks:")
    for ds_id, exists in results.items():
        symbol = "✅" if exists else "❌"
        print(f"  {symbol} [{ds_id}]")

    # Detailed table inspection
    tables = [
        ("data/processed/medicinal.csv", "VNPlant-200 Catalog"),
        ("data/processed/kashmir_medicinal.csv", "Kashmir Endemics Catalog"),
        ("knowledge/plants_master.csv", "Integrated Master Catalog"),
    ]

    print("\nDataset Schema & Quality Reports:")
    for rel_path, label in tables:
        full_path = ROOT / rel_path
        if full_path.exists():
            df = pd.read_csv(full_path)
            report = compute_data_quality_report(df)
            print(f"\n--- {label} ({rel_path}) ---")
            print(f"  Total Records:  {report['total_rows']}")
            print(f"  Total Columns:  {report['total_columns']}")
            print(f"  Completeness:   {report['overall_completeness_pct']}%")
            if "Scientificname" in df.columns:
                print(f"  Distinct Taxa:  {df['Scientificname'].nunique()}")
        else:
            print(f"\n❌ {label} not found at {rel_path}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
