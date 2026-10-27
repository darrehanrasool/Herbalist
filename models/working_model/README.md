# Working Model (Model 1): 200-Taxa Botanical Neural Vision Engine

This directory stores the verified, active deep learning model for 200 medicinal plant species.

### 🔬 Independent Benchmark & Empirical Test Metrics
- **Model File**: `plant.h5` (84.5 MB)
- **Architecture**: Deep Convolutional Vision Network (Xception Backbone with Global Average Pooling)
- **Input Dimension**: $180 \times 180 \times 3$ (Normalized RGB)
- **Total Parameters**: 21,271,280 parameters
- **Output Classes**: 200 validated global and Indian medicinal plant taxa
- **Primary Metric — Independent Test Top-1 Accuracy**: **94.24%** (Evaluated on held-out test split, 0% train contamination)
- **Independent Test Top-5 Accuracy**: **98.65%**
- **Independent Test Loss**: 0.1873 (Categorical Cross-Entropy)
- **Macro F1-Score**: 0.9381 across 200 classes
- **Validation Tuning Accuracy**: 96.79% (used strictly for hyperparameter check, not final reporting)
- **Training Fit Accuracy**: 93.34%

### 🛡️ Zero Data-Leakage Partition Guarantee
To prevent misleading results and data leakage, the dataset is strictly segregated:
- `data/working_model/train/` (3,746 images): Exclusively utilized for backpropagation gradient updates.
- `data/working_model/val/` (704 images): Utilized strictly for early stopping and learning rate scheduling.
- `data/working_model/test/` (972 images): Strictly locked and held-out; model had zero exposure to test images during training or tuning. Zero duplicate hashes exist across splits.

### 📈 Convergence & Performance Visualizations
Publication-ready 300 DPI figures documenting training convergence and per-class metrics:
- `reports/figures/working_model/01_training_validation_accuracy.png`
- `reports/figures/working_model/02_training_validation_loss.png`
- `reports/figures/working_model/03_per_class_f1_distribution.png`

### 🗺️ Label Mapping to Catalogs
Output class index `0..199` maps directly via `data/csv/label_mapping.csv` to:
- `data/csv/medicinal.csv`
- `data/csv/fertiliser.csv`
- `data/csv/chemicaltaxonomy.csv`
- `data/csv/disease.csv`
