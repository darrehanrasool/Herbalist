# Data Architecture & Repository Guide · Herbalist AI

This repository hosts multi-modal datasets spanning **computer vision (foliar and floral photography)**, **ethnopharmacology / phytochemistry catalogs**, and **agronomic soil sensor readings**, with special emphasis on the **Kashmir Himalaya** and global benchmark floras.

---

## Directory Organization

```
data/
├── manifests/
│   ├── dataset_manifest.json       # Master machine-readable manifest with SHA-256 hashes
│   └── imagesamplecount.csv        # Class-by-class training image distribution
├── raw/
│   ├── clinical/                   # Pharmacological, toxicity & phytochemical tables
│   │   ├── Kashmere.csv            # 15 High-altitude endemic Himalayan taxa
│   │   └── medicinal.csv           # 200 species benchmark reference catalog
│   ├── imaging/                    # Unprocessed field captures & external raw imagery
│   └── kaggle/                     # Cached downloads from Kaggle / mirrors
├── interim/                        # Cleaned, standardized, or intermediate transformed data
├── processed/                      # Canonical validated feature tables & normalized datasets
│   ├── kashmir_medicinal.csv
│   └── medicinal.csv
├── splits/
│   ├── train/                      # Categorical image class directories for training
│   ├── validation/                 # Validation set for hyperparameter tuning & early stopping
│   └── test/                       # Holdout test set for unbiased final benchmark
└── external/                       # Third-party taxonomic lookups (POWO, GBIF, KNApSAcK)
```

---

## Datasets Overview

### 1. Kashmir High-Altitude Endemic Medicinal Flora (`data/raw/clinical/Kashmere.csv`)
Focuses on endangered, vulnerable, and pharmacologically critical taxa native to the Kashmir Valley and greater Himalayan ranges:
- **Gentiana kurroo** (*Indian Gentian*) – Critically Endangered. Potent bitter glycosides (*gentiopicrin*).
- **Saussurea costus** (*Kuth*) – Critically Endangered. CITES Appendix I. Anti-inflammatory sesquiterpenes.
- **Aconitum heterophyllum** (*Atees*) – Endangered. Non-toxic diterpene alkaloids (*atisine*).
- **Picrorhiza kurroa** (*Kutki*) – Endangered. Hepatoprotective iridoid glycosides (*kutkin, picroside*).
- **Podophyllum hexandrum** (*Mayapple*) – Endangered. Lignan antineoplastic precursor (*podophyllotoxin*).
- **Taxus wallichiana** (*Himalayan Yew*) – Endangered. Diterpenoid precursor for Paclitaxel (*Taxol*).
- **Fritillaria roylei** (*Patees*) – Endangered. Traditional respiratory remedy.
- **Colchicum luteum**, **Rheum emodi**, **Berberis lycium**, **Valeriana jatamansi**, and others.

### 2. VNPlant-200 Global Benchmark (`data/raw/clinical/medicinal.csv`)
- **200 medicinal species** spanning 17,973 labeled foliar images.
- Serves as the pretraining and benchmark backbone for the vision neural network (`plant.h5`).
- Class mapping: indices 0–199 map directly to botanical binomials.

### 3. Integrated Knowledge Base (`knowledge/*.csv`)
Contains cross-referenced agronomy tables for:
- `plants_master.csv` (215 integrated species with family, biological name, conservation status)
- `soil_requirements.csv` (Optimal pH ranges, N-P-K bands, moisture & temperature tolerances)
- `fertilizer_guide.csv` (Organic vs inorganic amendments, seasonal fertilization schedules)
- `disease_ipm.csv` (Integrated Pest Management, common foliar blights, biological controls)
- `cultivation.csv` (Harvest cycles, propagation methods, wild-collection warnings)
- `chemistry_literature.csv` (Active compounds, pharmacological mechanism references)

---

## Data Ingestion & Splitting

To download or unpack images:
```bash
python scripts/download_datasets.py
python scripts/verify_datasets.py
python scripts/create_splits.py
```
Split parameters:
- **70% Training**
- **15% Validation**
- **15% Holdout Testing**
Stratified by species label to prevent imbalance artifacts.
