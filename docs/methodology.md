# Methodology · Herbalist AI

## 1. Deep Learning Vision Architecture

### 1.1 Depthwise Separable Convolutions (Xception Backbone)
Standard convolutions perform spatial filtering and channel cross-correlation simultaneously at computational cost $\mathcal{O}(D_K \cdot D_K \cdot M \cdot N \cdot D_F \cdot D_F)$.

In Xception (*Extreme Inception*), this process is decoupled into:
1. **Depthwise Convolution**: Applies a single spatial convolutional filter per input channel:
   $$\text{Computational Cost} = D_K \cdot D_K \cdot M \cdot D_F \cdot D_F$$
2. **Pointwise Convolution**: Applies $1 \times 1$ convolutions to linearly project channels into a new feature space:
   $$\text{Computational Cost} = M \cdot N \cdot D_F \cdot D_F$$

This yields an empirical reduction in floating-point operations (FLOPs) of approximately:
$$\frac{D_K \cdot D_K \cdot M + M \cdot N}{D_K \cdot D_K \cdot M \cdot N} = \frac{1}{N} + \frac{1}{D_K^2} \approx \frac{1}{9}$$
allowing deep representational learning without memory exhaustion on mobile or edge agricultural devices.

```mermaid
flowchart LR
    A[RGB Image 180x180x3] --> B[Entry Flow: 36 Conv Layers]
    B --> C[Middle Flow: Residual Blocks x8]
    C --> D[Exit Flow: Depthwise Separable Convs]
    D --> E[Global Average Pooling 2048-D]
    E --> F[Dense Layer 200 Neurons]
    F --> G[Softmax Probabilities]
```

### 1.2 Transfer Learning & Feature Vectorization
The convolutional backbone is initialized with pretrained ImageNet weights $\mathbf{W}_{\text{ImageNet}}$.
During baseline training, $\mathbf{W}_{\text{ImageNet}}$ remains frozen ($\nabla_{\mathbf{W}} \mathcal{L} = 0$), acting as a fixed high-dimensional visual feature extractor.

The output spatial activation map $\mathbf{A} \in \mathbb{R}^{H \times W \times C}$ (where $H=6, W=6, C=2048$) is collapsed via **Global Average Pooling (GAP)**:
$$z_c = \frac{1}{H \cdot W} \sum_{i=1}^H \sum_{j=1}^W A_{i, j, c}, \quad \forall c \in \{1, \dots, 2048\}$$
eliminating millions of dense parameters and mitigating overfitting.

### 1.3 Loss Function & Optimization
The classification head outputs unnormalized logits $\mathbf{z} \in \mathbb{R}^{200}$. Softmax normalization produces predicted probabilities:
$$p_k = \frac{\exp(z_k)}{\sum_{j=1}^{200} \exp(z_j)}$$

Optimization minimizes Categorical Cross-Entropy with optional label smoothing $\epsilon = 0.1$:
$$\mathcal{L}_{\text{CE}}(\mathbf{y}, \mathbf{p}) = -\sum_{k=1}^{200} y_k \log(p_k)$$

Gradient updates are computed via the **Adam** adaptive moment estimation optimizer:
$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

---

## 2. Agronomic Soil Gap Analysis Methodology

When real-time sensor readings $\mathbf{s} = \{ \text{pH}, \text{N}, \text{P}, \text{K}, \text{Moisture}, \text{Temp} \}$ are submitted, the system queries the species agronomic envelope $[\mathbf{l}_{\min}, \mathbf{l}_{\max}]$ from `knowledge/soil_requirements.csv`.

For each parameter $i$, the discrepancy $\Delta_i$ is evaluated:
$$\Delta_i = \begin{cases}
s_i - l_{\min, i} & \text{if } s_i < l_{\min, i} \quad (\text{Deficiency}) \\
s_i - l_{\max, i} & \text{if } s_i > l_{\max, i} \quad (\text{Toxicity / Excess}) \\
0 & \text{if } l_{\min, i} \leq s_i \leq l_{\max, i} \quad (\text{Optimal})
\end{cases}$$

Soil health status is flagged as:
- **Optimal (green)**: Within safe physiological growth envelope.
- **Deficient (yellow)**: Sub-optimal yield / chlorosis risk; prompts organic fertilizer advisory.
- **Critical (red)**: Severe stress or toxic salt accumulation.
