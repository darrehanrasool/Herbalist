# Working Model (Model 1): 200-Taxa Botanical Neural Vision Engine

This directory stores the verified, active deep learning model for 200 medicinal plant species.

### 🔬 Model Specifications
- **Model File**: `plant.h5` (84.5 MB)
- **Architecture**: Deep Convolutional Vision Network (Xception Backbone with Global Average Pooling)
- **Input Dimension**: $180 \times 180 \times 3$ (Normalized RGB)
- **Total Parameters**: 20,894,264 parameters
- **Output Classes**: 200 validated global and Indian medicinal plant taxa
- **Validation Accuracy**: 96.79%
- **Validation Loss**: 0.1241
- **Top-1 Empirical Test Accuracy**: 88.0% on verified sample test images

### 📁 Associated Data Partitions
The training, validation, and testing partitions corresponding to this exact model are located in:
- `data/working_model/train/` (3,746 images across 200 classes)
- `data/working_model/val/` (704 images across 200 classes)
- `data/working_model/test/` (972 images across 200 classes)

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
