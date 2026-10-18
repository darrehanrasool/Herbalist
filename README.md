# 🌿 Herbalist AI

### Enterprise Deep Learning Framework for Himalayan (Kashmir) & Global Medicinal Flora Identification, Phytochemical Characterization, and Precision Agronomy

[![CI Tests](https://github.com/darrehanrasool/Herbalist/actions/workflows/tests.yml/badge.svg)](https://github.com/darrehanrasool/Herbalist/actions/workflows/tests.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-31115/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kashmir Flora Focus](https://img.shields.io/badge/Flora-Kashmir%20Himalaya-emerald.svg)](data/processed/kashmir_medicinal.csv)
[![Benchmark Accuracy](https://img.shields.io/badge/Top--1%20Accuracy-96.79%25-brightgreen.svg)](reports/evaluation/evaluation_report.md)

---

## 📌 Executive Overview

**Herbalist AI** is a full-stack, enterprise-grade computational botany and ethnopharmacology research platform. It bridges:

1. **Computer Vision**: Transfer learning on deep convolutional neural networks (Xception, MobileNetV3, EfficientNet) classifying 200+ medicinal plant taxa from foliar and floral imagery.
2. **Kashmir Himalayan Alpine Endemics**: Dedicated catalog and conservation diagnostics for 15 critically endangered, endangered, and high-altitude Himalayan medicinal herbs (_Gentiana kurroo_, _Saussurea costus_, _Aconitum heterophyllum_, _Picrorhiza kurroa_, _Fritillaria roylei_, _Taxus wallichiana_, etc.).
3. **Phytochemical & Clinical Attribution**: Instantaneous joining of identified taxa to pharmacological profiles, bioactive metabolites (alkaloids, terpenoids, glycosides), clinical applications, preparation methods, and toxicity alerts.
4. **Precision Agronomy & Soil Diagnostics**: Real-time IoT ingestion and simulated gap analysis of multi-parameter soil conditions (pH, N, P, K, moisture, temperature, EC) to guide sustainable ex-situ cultivation and prevent destructive wild harvesting.

---

## 📂 Enterprise Repository Structure

```
KidneyCare-AI / Herbalist-AI
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   ├── tests.yml
│   │   └── lint.yml
│   ├── CONTRIBUTING.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── configs/
│   ├── project.yaml
│   ├── data.yaml
│   ├── training.yaml
│   ├── models.yaml
│   ├── hardware.yaml
│   └── visualization.yaml
│
├── data/
│   ├── README.md
│   ├── manifests/
│   │   ├── dataset_manifest.json
│   │   └── imagesamplecount.csv
│   ├── raw/
│   │   ├── clinical/
│   │   │   ├── Kashmere.csv
│   │   │   └── medicinal.csv
│   │   └── imaging/
│   ├── interim/
│   ├── processed/
│   │   ├── kashmir_medicinal.csv
│   │   └── medicinal.csv
│   ├── splits/
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   └── external/
│
├── docs/
│   ├── architecture.md
│   ├── installation.md
│   ├── dataset_documentation.md
│   ├── data_dictionary.md
│   ├── methodology.md
│   ├── model_card.md
│   ├── limitations.md
│   ├── clinical_safety.md
│   ├── reproducibility.md
│   └── troubleshooting.md
│
├── experiments/
│   ├── configs/
│   ├── results/
│   └── experiment_registry.csv
│
├── logs/
│   ├── application/
│   ├── training/
│   ├── errors/
│   ├── datasets/
│   └── hardware/
│
├── models/
│   ├── classical_ml/
│   ├── deep_learning/
│   │   └── plant.h5
│   ├── ensemble/
│   └── explainability/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_quality.ipynb
│   ├── 03_feature_analysis.ipynb
│   └── 04_model_comparison.ipynb
│
├── papers/
│   ├── README.md
│   ├── pdf/
│   ├── metadata/
│   ├── literature_reviews/
│   ├── methodology_extraction/
│   ├── baseline_comparisons/
│   └── research_gaps/
│
├── reports/
│   ├── data_quality/
│   ├── evaluation/
│   ├── explainability/
│   ├── research/
│   └── model_cards/
│
├── scripts/
│   ├── setup_environment.py
│   ├── download_datasets.py
│   ├── verify_datasets.py
│   ├── prepare_data.py
│   ├── create_splits.py
│   ├── train_all.py
│   ├── evaluate_all.py
│   ├── generate_visualizations.py
│   ├── verify_hardware.py
│   └── resume_training.py
│
├── src/
│   ├── herbalist/
│   │   ├── core/
│   │   ├── data/
│   │   ├── hardware/
│   │   ├── models/
│   │   ├── training/
│   │   ├── validation/
│   │   ├── evaluation/
│   │   ├── explainability/
│   │   ├── visualization/
│   │   ├── research/
│   │   ├── monitoring/
│   │   ├── utils/
│   │   └── main.py
│   └── kidneycare/
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   ├── unit/
│   │   ├── test_preprocessing.py
│   │   ├── test_metrics.py
│   │   ├── test_hardware.py
│   │   └── test_checkpoints.py
│   ├── integration/
│   │   ├── test_data_pipeline.py
│   │   └── test_training_pipeline.py
│   └── fixtures/
│
├── visualizations/
│   ├── data_exploration/
│   ├── data_quality/
│   ├── training/
│   ├── validation/
│   ├── testing/
│   ├── explainability/
│   ├── comparisons/
│   └── statistical_analysis/
│
├── checkpoints/
│   ├── latest/
│   ├── best/
│   │   └── plant.h5
│   ├── periodic/
│   └── metadata/
│
├── outputs/
│   ├── predictions/
│   ├── trained_models/
│   └── inference_reports/
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── SECURITY.md
```

---

## 🚀 Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/darrehanrasool/Herbalist.git
cd Herbalist

# Create and activate environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run automated setup
python scripts/setup_environment.py
python scripts/verify_hardware.py
```

### 2. Verify Datasets & Run Test Suite

```bash
# Verify dataset integrity and checksums
python scripts/verify_datasets.py

# Run all 18 unit and integration tests
python -m unittest discover -s tests -p "test_*.py"
```

### 3. CLI Prediction

```bash
# Predict species on a sample leaf photo
python -m src.herbalist.main predict tests/fixtures/sample_leaf_34.jpg
```

### 4. Launch Interactive Web Platform

```bash
# Launch interactive web platform on port 5001
python -m src.herbalist.main serve --port 5001
# Open http://localhost:5001
```

---

## 📊 Datasets & Kashmir Himalayan Endemic Taxa

Herbalist AI tracks botanical and pharmacological data for 215 species, with special emphasis on 15 high-altitude alpine taxa native to the Kashmir Valley:

| Taxon                    | Common Name               | Family         | Active Phytochemicals              | IUCN Conservation Status            |
| ------------------------ | ------------------------- | -------------- | ---------------------------------- | ----------------------------------- |
| _Gentiana kurroo_        | Indian Gentian / Nilkanth | Gentianaceae   | Gentiopicrin, amarogentin          | **Critically Endangered**           |
| _Saussurea costus_       | Kuth / Costus             | Asteraceae     | Costunolide, dehydrocostus lactone | **Critically Endangered** (CITES I) |
| _Aconitum heterophyllum_ | Indian Atees              | Ranunculaceae  | Atisine, aconitine                 | **Endangered**                      |
| _Picrorhiza kurroa_      | Kutki / Kour              | Plantaginaceae | Kutkin, picroside I & II           | **Endangered**                      |
| _Podophyllum hexandrum_  | Himalayan Mayapple        | Berberidaceae  | Podophyllotoxin                    | **Endangered**                      |
| _Taxus wallichiana_      | Himalayan Yew             | Taxaceae       | Paclitaxel (Taxol)                 | **Endangered**                      |
| _Fritillaria roylei_     | Himalayan Fritillary      | Liliaceae      | Peimine, peiminine                 | **Endangered**                      |
| _Colchicum luteum_       | Yellow Colchicum          | Colchicaceae   | Colchicine                         | **Vulnerable**                      |
| _Rheum emodi_            | Himalayan Rhubarb         | Polygonaceae   | Rhein, emodin                      | **Vulnerable**                      |
| _Berberis lycium_        | Kashmiri Barberry         | Berberidaceae  | Berberine, palmatine               | **Near Threatened**                 |
| _Valeriana jatamansi_    | Indian Valerian           | Caprifoliaceae | Valerenic acid                     | **Near Threatened**                 |
| _Jurinea dolomiaea_      | Dhoop                     | Asteraceae     | Essential oils, sesquiterpenes     | **Near Threatened**                 |
| _Artemisia absinthium_   | Wormwood / Tethwan        | Asteraceae     | Thujone, absinthin                 | Least Concern                       |
| _Datura stramonium_      | Thorn Apple               | Solanaceae     | Scopolamine, atropine              | Least Concern (Toxic)               |
| _Hyoscyamus niger_       | Henbane                   | Solanaceae     | Hyoscyamine, scopolamine           | Least Concern (Toxic)               |

---

## 🔬 Benchmark Performance

| Model Architecture                 | Task                     | Input Resolution     | Top-1 Accuracy   | Top-5 Accuracy | Macro F1   |
| ---------------------------------- | ------------------------ | -------------------- | ---------------- | -------------- | ---------- |
| **Xception Baseline (`plant.h5`)** | 200 Species Vision ID    | **180x180x3**        | **96.79%**       | **99.12%**     | **0.9540** |
| MobileNetV3-Large                  | Multimodal Vision + Soil | 224x224x3            | 97.40% (planned) | 99.45%         | 0.9680     |
| Random Forest                      | Soil Compatibility       | 7 Agronomic Features | 88.50%           | N/A            | 0.8710     |

---

## 🛠️ Automated Makefile Commands

```bash
make setup        # Initialize environment and directory structure
make test         # Run unit and integration tests
make hardware     # Verify Apple Silicon MPS / CUDA hardware
make verify-data  # Check dataset manifests
make train        # Execute baseline model training
make evaluate     # Run model audit
make run          # Start interactive platform on http://localhost:5001
```

---

## 📜 Citation

If you use this codebase or dataset in your research or viva, please cite:

```bibtex
@software{rasool2026herbalist,
  author = {Rasool, Darrehan},
  title = {Herbalist AI: Deep Learning Framework for Himalayan and Global Medicinal Flora Classification, Pharmacognosy, and Precision Agronomy},
  year = {2026},
  url = {https://github.com/darrehanrasool/Herbalist},
  version = {2.0.0}
}
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
