# Methodology Comparison: Xception vs EfficientNet vs MobileNetV3

This analysis provides the technical and mathematical rationale for model selection in Herbalist AI.

---

## 1. Architectural Parameter Trade-Offs

| Architecture | Parameters | Top-1 ImageNet | FLOPs (G) | Input Size | Key Advantage in Herbalist AI |
|---|---|---|---|---|---|
| **Xception** | **22.9 M** | **79.0%** | **8.4** | **180x180** | **Baseline model (`plant.h5`). Robust depthwise separable convs; high accuracy on VNPlant-200.** |
| **MobileNetV3-Large** | 5.4 M | 75.2% | 0.44 | 224x224 | Ideal for lightweight smartphone & edge deployment in rural Kashmir valleys. |
| **EfficientNet-B0** | 5.3 M | 77.1% | 0.39 | 224x224 | Compound scaling; exceptional feature density per parameter. |
| **ResNet-50V2** | 25.6 M | 76.0% | 7.0 | 224x224 | Classical residual connections; stable baseline for fine-tuning. |

---

## 2. Mathematical Comparison: Depthwise Separable vs Inverted Residuals

### Xception Style (Depthwise Separable)
- Performs $3 \times 3$ depthwise spatial convolution across input channels.
- Follows with $1 \times 1$ pointwise convolution to linearly project into higher dimensionality.
- Does not use non-linearities between depthwise and pointwise operations (Chollet, 2017).

### MobileNet / EfficientNet Style (Inverted Residual Block)
- First expands channels via $1 \times 1$ convolution.
- Applies $3 \times 3$ or $5 \times 5$ depthwise convolution with swish/hard-swish activation.
- Projects back to low-dimensional bottleneck via linear $1 \times 1$ convolution (preventing manifold destruction).
- Employs Squeeze-and-Excitation (SE) channel-wise attention.
