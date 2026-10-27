# Working Model (Model 1): Vision Dataset Partitions (200 Taxa)

This directory stores the official dataset partitions corresponding to the active 200-class medicinal plant model (`models/working_model/plant.h5`).

### 📁 Directory Partitions
- `train/`: 3,746 leaf/plant images across 200 medicinal species
- `val/`: 704 validation images across 200 medicinal species
- `test/`: 972 test images across 200 medicinal species

### 🗺️ Output Label Mapping
Each subfolder name corresponds directly to `class_folder_name` in `data/csv/label_mapping.csv`, which maps model prediction indices `0..199` to `data/csv/medicinal.csv`, `data/csv/fertiliser.csv`, `data/csv/chemicaltaxonomy.csv`, and `data/csv/disease.csv`.
