# Model Card · Herbalist AI Vision Classifier

## 1. Model Details
- **Developer**: Darrehan Rasool (Islamic University of Science & Technology, Kashmir).
- **Model Release Date**: June 2025 (Initial BTech release v1.0.0); October 2026 (Enterprise v2.0.0).
- **Model Type**: Deep Convolutional Neural Network (Transfer Learning).
- **Backbone Architecture**: Xception (36 convolutional stages, depthwise separable convolutions, Global Average Pooling).
- **Weight Archive**: `models/deep_learning/plant.h5` (~88 MB, 20.8 million parameters).
- **Input Dimensions**: $180 \times 180 \times 3$ RGB (Normalized $[0, 1]$).
- **Output Layer**: 200-dimensional categorical softmax.
- **License**: MIT.

---

## 2. Intended Use
### In-Scope Uses:
- Botanical species classification of fresh, well-lit medicinal plant leaves and flowers.
- Educational reference for botany and pharmacognosy students.
- Agronomic decision support linking identified taxa to optimal NPK soil envelopes.

### Out-of-Scope & Prohibited Uses:
- **Emergency medical triage or poison ingestion diagnosis.**
- Autonomous ingestion of wild-collected plants without chemical verification.
- Identification from dry, ground, or processed herbal powders where morphological leaf features are absent.

---

## 3. Factors & Quantitative Metrics

| Evaluation Split | Top-1 Accuracy | Top-5 Accuracy | Macro F1-Score | Loss (Cross-Entropy) |
|---|---|---|---|---|
| **Training (12,000 images)** | 93.34% | 98.70% | 0.9280 | 0.2240 |
| **Validation / Test (5,973 images)** | **96.79%** | **99.12%** | **0.9540** | **0.1824** |

---

## 4. Ethical Considerations & Safety
- **High Toxicity Warnings**: Species containing deadly alkaloids (e.g. *Abrus precatorius* [abrin], *Datura stramonium* [atropine, scopolamine], *Aconitum* spp.) trigger prominent red alerts in the user interface.
- **Endangered Species Protection**: Critically Endangered Himalayan taxa (e.g. *Saussurea costus*, *Gentiana kurroo*) display conservation flags prohibiting destructive harvesting.
