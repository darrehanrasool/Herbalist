# System Architecture · Herbalist AI

## 1. High-Level Architectural Overview

Herbalist AI is designed as a modular, enterprise-grade research framework that bridges **computer vision for botanical taxa classification**, **pharmacognosy/phytochemical knowledge synthesis**, and **precision agronomic soil monitoring**.

```mermaid
flowchart TD
    subgraph Data Sources
        A1[Foliar / Floral RGB Images] --> B1[Vision Pipeline]
        A2[Soil Probes: NPK, pH, EC, Temp] --> B2[Agronomy Ingestion]
        A3[Kashmir & Global Catalogs] --> B3[Master Knowledge Graph]
    end

    subgraph Deep Learning Engine
        B1 --> C1[Image Normalization 180x180]
        C1 --> C2[Xception / EfficientNet Backbone]
        C2 --> C3[Global Avg Pooling + Softmax]
        C3 --> C4[200-Taxa Probabilities]
    end

    subgraph Decision & Agronomy Engine
        C4 --> D1[Species Resolution Engine]
        B3 --> D1
        B2 --> D2[Soil Gap & Threshold Analysis]
        D1 --> D3[Comprehensive Field Report]
        D2 --> D3
    end

    subgraph Presentation & APIs
        D3 --> E1[Interactive Web Platform / UI]
        D3 --> E2[REST API Endpoints: /api/predict]
        D3 --> E3[Sensor Ingestion API: /api/sensors/ingest]
    end
```

---

## 2. Component Subsystems

### 2.1 Core Computational Framework (`src/herbalist/core/`)
- **`config.py`**: Central YAML loading with environment variable overrides.
- **`constants.py`**: Botanical taxonomy dictionaries (200 VNPlant classes, 15 Kashmir high-altitude taxa).
- **`exceptions.py`**: Custom domain exceptions for corrupt images, hardware errors, and schema mismatches.
- **`reproducibility.py`**: Deterministic seeding across Python, NumPy, TensorFlow, and PyTorch.

### 2.2 Hardware & Accelerator Subsystem (`src/herbalist/hardware/`)
- Detects host capabilities: Apple Silicon Metal (MPS), NVIDIA CUDA, multi-core CPU.
- Dynamically throttles batch sizes based on RAM availability to prevent out-of-memory (OOM) failures.

### 2.3 Data Engineering Subsystem (`src/herbalist/data/`)
- **Manifest Verification**: Cryptographic SHA-256 verification of datasets.
- **Image Preprocessing**: Aspect-ratio preserving resizing, standard ImageNet normalization.
- **Feature Engineering**: Genus extraction, toxicity ordinals, soil NPK balance ratios.
- **Deduplication**: Perceptual difference hashing (`dHash`) and MD5 deduplication.

### 2.4 Model Subsystem (`src/herbalist/models/`)
- **Classical Models**: Random Forest, Gradient Boosting, SVM, Logistic Regression.
- **Deep Neural Networks**: Transfer learning backbones (Xception, MobileNetV3, EfficientNetB0) and Tabular MLPs.
- **Ensembles**: Weighted soft-voting ensembles combining visual and agronomic predictions.

### 2.5 Monitoring & Telemetry Subsystem (`src/herbalist/monitoring/`)
- Application, training, hardware, and error logs stored under `logs/`.
- Experiment runs recorded to `experiments/experiment_registry.csv`.
