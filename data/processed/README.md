# Processed Computer Vision Image Directory

This directory contains processed and partitioned image datasets organized into subfolders by botanical taxon:

- `train/<class_name>/*.jpg` — 70% stratified training partition across 200+ medicinal plant species.
- `val/<class_name>/*.jpg` — 15% validation partition used for early stopping and hyperparameter tuning.
- `test/<class_name>/*.jpg` — 15% holdout test partition for final generalization evaluation.

> [!NOTE]
> All tabular knowledge bases and CSV datasets reside in `data/csv/`. No CSV files are stored in this image directory.
