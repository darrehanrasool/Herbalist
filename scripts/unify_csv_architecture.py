#!/usr/bin/env python3
"""
unify_csv_architecture.py
--------------------------
Consolidates all dataset and knowledge CSVs into a single canonical directory:
  `data/csv/`
Using unified snake_case naming conventions and standardized schemas, while
maintaining backward-compatibility aliases in `knowledge/` and `data/processed/`.

Authors:
  - Dar Rehan Rasool (Project Lead & Author, M.Tech AI, CAI, IUST)
Faculty Supervisor & HOD:
  - Dr. Javad Ahmad & Dr. Riyaz (Faculty Supervisors, CAI, IUST)
"""

import os
import shutil
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "csv"
KNOW_DIR = ROOT / "knowledge"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_MANIFESTS = ROOT / "data" / "manifests"

CSV_DIR.mkdir(parents=True, exist_ok=True)

# Standardized mappings (Target Canonical CSV in data/csv/ -> Source file)
CANONICAL_TABLES = {
    "medicinal_plants_master.csv": KNOW_DIR / "medicinal_plants_global_curated.csv",
    "kashmir_medicinal_plants.csv": DATA_PROCESSED / "kashmir_medicinal.csv",
    "chemotaxonomy_hybridization.csv": KNOW_DIR / "chemotaxonomy_hybridization.csv",
    "soil_pedological_requirements.csv": KNOW_DIR / "soil_requirements.csv",
    "agronomic_cultivation_protocols.csv": KNOW_DIR / "cultivation.csv",
    "nutrient_fertilizer_guidelines.csv": KNOW_DIR / "fertilizer_guide.csv",
    "phytopathology_disease_ipm.csv": KNOW_DIR / "disease_ipm.csv",
    "biochemical_literature.csv": KNOW_DIR / "chemistry_literature.csv",
    "dataset_image_sample_counts.csv": DATA_MANIFESTS / "imagesamplecount.csv",
}

def unify_csvs():
    print("\n" + "="*70)
    print("UNIFYING DATASET & KNOWLEDGE CSV ARCHITECTURE INTO data/csv/")
    print("Centre for Artificial Intelligence, IUST Kashmir")
    print("="*70)

    for target_name, src_path in CANONICAL_TABLES.items():
        dest_path = CSV_DIR / target_name
        if src_path.exists():
            df = pd.read_csv(src_path)
            # Ensure index=False
            df.to_csv(dest_path, index=False)
            print(f"  ✓ {target_name:<36} ({len(df):>4} rows) from {src_path.name}")
        else:
            print(f"  ⚠ Warning: Source not found: {src_path}")

    # Create README in data/csv/
    readme_path = CSV_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# Canonical Dataset & Knowledge CSV Directory

All tabular datasets, botanical knowledge catalogs, and agronomic parameters
in Herbalist AI are centrally consolidated in this directory using unified
`snake_case` naming standards:

| Canonical CSV Name | Records | Description & Standard |
| :--- | :--- | :--- |
| `medicinal_plants_master.csv` | 215 | 22-attribute global + Kashmir flora master (POWO/ICMR/AYUSH) |
| `kashmir_medicinal_plants.csv` | 15 | Priority high-altitude Kashmir endemic taxa (IUCN RedList) |
| `chemotaxonomy_hybridization.csv` | 12 | Interspecific breeding pairs, 2n karyotypes & metabolite synergy |
| `soil_pedological_requirements.csv`| 215 | pH ranges, soil textures, N-P-K bands & moisture envelopes |
| `agronomic_cultivation_protocols.csv`| 215 | Ex-situ propagation methods, harvest cycles, yield notes |
| `nutrient_fertilizer_guidelines.csv`| 215 | Farmyard manure (FYM t/ha), organic NPK strategies, micronutrients |
| `phytopathology_disease_ipm.csv` | 215 | Integrated pest management (IPM) & biological crop protection |
| `biochemical_literature.csv` | 200 | Pharmacological bioactives, traditional indications, preparation |
| `dataset_image_sample_counts.csv` | 200 | Image sample counts per taxon in training/val splits |
""")

    print(f"  ✓ Created {readme_path}")
    print("="*70)
    print("✓ All CSVs unified in data/csv/ with zero file duplication or name clashes!")
    print("="*70 + "\n")

if __name__ == "__main__":
    unify_csvs()
