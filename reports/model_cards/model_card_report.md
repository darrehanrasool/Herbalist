# Formal Model Card Summary Report

- **Model Name**: Herbalist-AI-Xception-v1.0
- **Task**: 200-class fine-grained medicinal flora classification.
- **Backbone**: Frozen ImageNet Xception CNN.
- **Top-1 Accuracy**: 96.79% (Validation).
- **Top-5 Accuracy**: 99.12% (Validation).
- **Inference Latency**: ~32 ms (Apple Silicon M-series via MPS).
- **Storage Size**: 88,635,144 bytes (`plant.h5`).
- **Input Preprocessing**: Bilinear resize to $180 \times 180 \times 3$, rescaled by $1/255.0$.
- **Downstream Joining**: Scientific binomial joins against `data/processed/medicinal.csv` for ethnopharmacological profile.
