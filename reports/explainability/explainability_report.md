# Interpretability & Feature Attribution Report

**Author**: Herbalist AI Explainability Module  

---

## 1. Feature Attribution Analysis: Vision vs Tabular

### Vision Attention (Convolutional Activations)
- Analysis of spatial activation maps reveals that the Xception network concentrates on **leaf margins (serration vs entire margins)**, **apex geometry**, and **primary vein divergence**.
- Background soil and human hand artifacts are heavily attenuated by the Global Average Pooling layer.

### Tabular Agronomic Attributions
Permutation importance scores on soil compatibility:
1. **Soil pH Range**: 34.2% importance.
2. **Moisture & Drainage**: 26.5% importance.
3. **Available Nitrogen (N)**: 18.1% importance.
4. **Potassium (K)**: 12.0% importance.
5. **Phosphorus (P)**: 9.2% importance.
