# Kashmir High-Altitude Medicinal Plant Model (Future Work)

This dedicated directory is reserved for the upcoming Kashmir endemic medicinal flora model.

### Pipeline Architecture:
1. **Target Flora**: 16 High-altitude endemic and threatened Kashmir taxa (*Crocus sativus*, *Gentiana kurroo*, *Picrorhiza kurroa*, *Saussurea costus*, *Aconitum heterophyllum*, *Fritillaria roylei*, etc.).
2. **Dataset Source**: High-resolution field captures collected across Gulmarg, Sonamarg, Pahalgam, and Gurez alpine zones.
3. **Partition Storage**: `data/kashmir/train/`, `data/kashmir/val/`, and `data/kashmir/test/`.
4. **Training Command**: `python scripts/train_kashmir_model.py`
5. **Output Model Weights**: `models/kashmir/kashmir_plant.h5`
6. **Output Graphs**: `reports/figures/kashmir/`

When active, the platform pipeline runs both models in parallel and displays results mapped from `data/csv/`.
