# Online & Third-Party Datasets · Provenance & Download Guide

This directory houses third-party open-access datasets fetched via automated ingestion scripts or API connectors.

## 1. Directory Structure

```
data/raw/online/
├── README.md               <- This inventory
├── vnplant_200/            <- 200 Species baseline benchmark (17,973 images)
├── indian_medicinal_leaves/<- 80 Common Indian Leaf Taxa
├── crop_health/            <- Agricultural disease datasets (e.g. Rice Leaf Disease)
└── chemodiversity/         <- Global vascular plant metabolite occurrences
```

## 2. Ingestion Commands

To download and extract these datasets automatically, run:
```bash
# Ingest all online datasets specified in configs/data.yaml
python scripts/download_datasets.py

# Verify cryptographic SHA-256 integrity against data/manifests/dataset_manifest.json
python scripts/verify_datasets.py
```

## 3. Whitelist Policy in `.gitignore`
Raw image directories and large compressed archives (`*.zip`, `*.tar.gz`) stored here are excluded from git commits to keep the repository lightweight. Derived tabular manifests, metadata CSVs, and processed splits are tracked.
