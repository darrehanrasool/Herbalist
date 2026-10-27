#!/usr/bin/env python3
"""Organize datasets into Working Model and Kashmir Future Model folders.

Structure created:
data/
├── working_model/
│   ├── train/ (200 classes)
│   ├── val/   (200 classes)
│   └── test/  (200 classes)
└── kashmir/
    ├── train/ (Kashmir taxa)
    ├── val/   (Kashmir taxa)
    ├── test/  (Kashmir taxa)
    └── README.md
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
WM_DATA = DATA_DIR / "working_model"
KASHMIR_DATA = DATA_DIR / "kashmir"
PROCESSED = DATA_DIR / "processed"
RAW_KASHMIR = DATA_DIR / "raw" / "kashmir"

# 1. Setup data/working_model
WM_DATA.mkdir(parents=True, exist_ok=True)
for split in ("train", "val", "test"):
    src_split = PROCESSED / split
    dst_split = WM_DATA / split
    dst_split.mkdir(parents=True, exist_ok=True)
    if src_split.exists():
        for class_dir in src_split.iterdir():
            if class_dir.is_dir() and not class_dir.name.startswith("."):
                target_cls = dst_split / class_dir.name
                target_cls.mkdir(parents=True, exist_ok=True)
                for img in class_dir.iterdir():
                    if img.is_file() and img.suffix.lower() in (".jpg", ".jpeg", ".png"):
                        dst_img = target_cls / img.name
                        if not dst_img.exists():
                            try:
                                os.link(str(img), str(dst_img))
                            except Exception:
                                shutil.copyfile(str(img), str(dst_img))

print(f"✅ data/working_model ready with train, val, and test splits.")

# 2. Setup data/kashmir
KASHMIR_DATA.mkdir(parents=True, exist_ok=True)
for split in ("train", "val", "test"):
    (KASHMIR_DATA / split).mkdir(parents=True, exist_ok=True)

# Copy initial samples for Aconitum and Gentiana into data/kashmir/train and test
for sp in ("Aconitum_heterophyllum", "Gentiana_kurroo"):
    sp_src = RAW_KASHMIR / sp
    if sp_src.exists():
        for i, img in enumerate(sp_src.glob("*.jpg")):
            split_target = "train" if i == 0 else "test"
            dst_cls = KASHMIR_DATA / split_target / sp
            dst_cls.mkdir(parents=True, exist_ok=True)
            dst_img = dst_cls / img.name
            if not dst_img.exists():
                try:
                    os.link(str(img), str(dst_img))
                except Exception:
                    shutil.copyfile(str(img), str(dst_img))

with open(KASHMIR_DATA / "README.md", "w", encoding="utf-8") as f:
    f.write("""# Kashmir Endemic Medicinal Flora Dataset (Future Work)

This directory is dedicated exclusively to the upcoming high-altitude Kashmir medicinal flora dataset.

### Folder Structure:
- `train/<species_name>/*.jpg` — Training photos collected across Kashmir alpine zones.
- `val/<species_name>/*.jpg` — Validation photos for hyperparameter tuning.
- `test/<species_name>/*.jpg` — Independent holdout test set for generalization evaluation.

### Planned Kashmir Taxa (16 Species):
1. *Crocus sativus* (Kashmir Saffron / Kong)
2. *Aconitum heterophyllum* (Atis / Patrees)
3. *Gentiana kurroo* (Nilkanth / Gulu)
4. *Picrorhiza kurroa* (Kutki / Kour)
5. *Saussurea costus* (Kuth)
6. *Podophyllum hexandrum* (Bankakri)
7. *Fritillaria roylei* (Kakoli / Sheethkhar)
8. *Rheum emodi* (Pambchalan)
9. *Taxus wallichiana* (Himalayan Yew / Posthal)
10. *Artemisia absinthium* (Tethwan)
11. *Berberis lycium* (Kawdakh)
12. *Colchicum luteum* (Virkum)
13. *Datura stramonium* (Dhatur)
14. *Hyoscyamus niger* (Bazarbhang)
15. *Jurinea dolomiaea* (Dhoop)
16. *Valeriana jatamansi* (Mushkbala)

### Training Workflow:
Once images are organized in `train/` and `val/`, execute:
```bash
python scripts/train_kashmir_model.py
```
This automatically compiles the Kashmir model and saves weights to `models/kashmir/kashmir_plant.h5`.
""")

print(f"✅ data/kashmir ready with train, val, and test partitions.")
