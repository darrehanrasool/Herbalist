# Herbalist-AI: Computational Botany, Ethnomedicinal Intelligence & Dual-Model Cascade Platform

[![Tests: 26 Passed](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg?logo=pytest)](tests/)
[![CI Workflow](https://img.shields.io/badge/CI%20Workflow-passing-brightgreen.svg?logo=github-actions)](https://github.com/darrehanrasool/Herbalist/actions/workflows/tests.yml)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic-red.svg)](LICENSE)
[![Python: 3.10 | 3.11](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/downloads/)
[![Independent Test Accuracy: 94.24%](https://img.shields.io/badge/Independent%20Test%20Accuracy-94.24%25-brightgreen.svg)](reports/figures/working_model/)
[![Zero Data Leakage](https://img.shields.io/badge/Data%20Leakage-0.0%25%20Verified-blue.svg)](models/working_model/)
[![Master Catalogs: 216 Taxa](https://img.shields.io/badge/Master%20Catalogs-216%20Taxa%20(4%20CSVs)-emerald.svg)](data/csv/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Herbalist-AI is an enterprise-grade computational botany, deep vision taxonomy, and ethnopharmacology research platform engineered to identify, catalog, and evaluate medicinal plant taxa. It combines a validated dual-model cascading deep learning architecture with 4 canonical, peer-reviewed master knowledge catalogs to predict active secondary metabolites, prevent poisonous adulteration, and guide agronomic cultivation.

---

## 👥 Research Team & Contributors

This research project is designed, engineered, and maintained at the **Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Kashmir**.

| Role | Name | Designation & Affiliation | Research & Project Contribution |
| :--- | :--- | :--- | :--- |
| **Head of Department (HOD) & Principal Supervisor** | **Dr. Muzafar Rasool Bhat** | Associate Professor & Head, Centre for Artificial Intelligence (CAI), IUST | Project Conceptualization, Academic Supervision, Deep Learning & Vision Architecture Direction |
| **Project Lead & Author** | **Dar Rehan Rasool** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Dual-Model Cascade Architecture, Deep Neural Network Implementation, Benchmark Evaluation & Platform Engineering |
| **Contributing Researcher** | **Muneeb Syed Shah** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Himalayan Flora Research, Field Expedition Planning & Agronomic Data Verification |
| **Contributing Researcher** | **Shafiya Bashir Pampori** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Pharmacognosy Data Modeling, Curated Catalog Verification & Taxonomic Data Integrity |
| **Research Contributor** | **Sehreen** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Pharmacognosy Literature Synthesis, Chemotaxonomy Modeling & Ethnomedicinal Annotation |

- **Academic Unit**: Centre for Artificial Intelligence (CAI)
- **Institution**: Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India

---

## 🔬 Core System Architecture & Current Implementations

### 1. Active Botanical Vision Classifier (Model 1 — 200 Taxa)
- **Architecture**: Deep Convolutional Neural Network with an Xception backbone (Extreme Inception) featuring 36 depthwise separable convolutional layers and Global Average Pooling.
- **Weights & Parameters**: `models/working_model/plant.h5` (84.5 MB, 21,271,280 parameters).
- **Input Dimension**: $180 \times 180 \times 3$ RGB (normalized to $[0, 1]$).
- **Primary Research Metric — Independent Test Accuracy**: **$94.24\%$ Top-1** and **$98.65\%$ Top-5** evaluated on 972 unseen leaf test images.
- **Categorical Cross-Entropy Test Loss**: $0.1873$ | **Macro F1-Score**: $0.9381$.

### 2. Strict Zero Data-Leakage Partition Guarantee
To ensure scientific validity and prevent inflated performance claims:
- **Training Set (`data/working_model/train/`)**: 3,746 images ($70.0\%$) used exclusively for backpropagation gradient updates.
- **Validation Set (`data/working_model/val/`)**: 704 images ($13.2\%$) used strictly for hyperparameter checks and learning rate scheduling.
- **Independent Test Set (`data/working_model/test/`)**: 972 images ($16.8\%$) locked and held out prior to training.
- **Leakage Audit**: Pairwise SHA-256 image hash verification confirms **$0.0\%$ cross-split intersection**, ensuring the model is evaluated on previously unseen specimens.

### 3. Dedicated Kashmir Endemic Model Pipeline (Model 2 — Planned Future Work)
- **Target Flora**: 16 high-altitude threatened and endemic Kashmir Himalayan taxa (*Gentiana kurroo*, *Saussurea costus*, *Picrorhiza kurroa*, *Aconitum heterophyllum*, *Podophyllum hexandrum*, *Arnebia benthamii*, *Inula racemosa*, *Rheum webbianum*, etc.).
- **Segregated Partitions**: Reserved folders in `data/kashmir/train/`, `data/kashmir/val/`, and `data/kashmir/test/`.
- **Target Weights**: `models/kashmir/kashmir_plant.h5`.
- **Turnkey Trainer**: `python scripts/train_kashmir_model.py` with multi-platform hardware selection (Apple Silicon MPS / NVIDIA CUDA / CPU).

### 4. 4 Canonical Master Knowledge Catalogs (`data/csv/`)
All domain knowledge is centralized into 4 non-repetitive, verified CSV catalogs covering **216 medicinal plant taxa** (100% complete across all fields):
1. **`medicinal.csv`** (216 taxa, 25 attributes): Binomial nomenclature, vernacular names, botanical family, Ayurvedic/Unani rasapanchaka, IUCN conservation status, clinical indications, diagnostic bioactives, and toxicity warnings.
2. **`fertiliser.csv`** (216 taxa, 17 attributes): Precision agronomy guidelines, basal farmyard manure (FYM t/ha), specific N-P-K kg/ha ratios, split application schedules, biofertilizers (Azotobacter, PSB), and soil pH ranges.
3. **`chemicaltaxonomy.csv`** (216 taxa, 17 attributes): Chemotaxonomic order, primary chemical classes, dominant secondary metabolites, biosynthetic pathways, $2n$ karyotype chromosome counts, and hybridization breeding targets.
4. **`disease.csv`** (216 taxa, 11 attributes): Phytopathology, foliar disease symptoms, organic IPM sanitation practices, biological controls, and chemical pesticide restrictions.
- **`label_mapping.csv`**: Unambiguous 1-to-1 index table mapping neural vision output classes (`0..199`) and planned Kashmir classes (`200..215`) to the 4 master catalogs.

### 5. Interactive Scientist Workbench & Terminal Console
- **Scientist Workspace (`/`)**: Real-time dual-model statistics, independent test benchmark metrics, and catalog previews.
- **Botanical Identification (`/upload`)**: Specimen image analysis with automatic catalog dossier lookup.
- **Chemotaxonomy & Hybridization Explorer (`/hybridization`)**: Chromosomal synapsis and secondary metabolite retention analysis across congeneric relatives.
- **Agronomy & Nutrient Guidelines (`/agronomy`)**: Species-specific soil envelopes, NPK fertilizer schedules, and disease management.
- **Research Terminal & Logs Console (`/research-lab`)**: Interactive terminal-styled audit console displaying real-time hardware status, catalog checksum verification, zero-leakage data partition logs, and repository lineage.
- **Archival Research Figures (`/lab`)**: 300 DPI publication plots (convergence curves, test generalization comparisons, and edaphic envelopes).
- **Botanical Catalog Browser (`/plants`)**: Searchable index of all 216 medicinal taxa.

---

## 📁 Repository Directory Structure

```
Herbalist/
├── .github/
│   └── workflows/                # GitHub Actions CI/CD workflows (lint.yml, tests.yml)
├── api/
│   ├── app.py                    # Main Flask application & prediction API
│   ├── static/                   # Platform CSS, JavaScript, and 300 DPI research graphs
│   └── templates/platform/       # Modern responsive scientist platform templates
├── backend/
│   ├── knowledge.py              # Canonical knowledge base engine (queries data/csv/)
│   └── platform_routes.py        # Platform endpoints (dashboard, agronomy, research terminal)
├── configs/                      # YAML configurations (data.yaml, hardware, models)
├── data/
│   ├── csv/                      # 4 Canonical Master Catalogs + Label Mapping (216 Taxa)
│   │   ├── medicinal.csv
│   │   ├── fertiliser.csv
│   │   ├── chemicaltaxonomy.csv
│   │   ├── disease.csv
│   │   └── label_mapping.csv
│   ├── working_model/            # Model 1 partitions (train, val, test)
│   └── kashmir/                  # Model 2 planned partitions (train, val, test)
├── docs/                         # Architecture, methodology, clinical safety, data dictionary
├── models/
│   ├── working_model/            # Active weights (plant.h5), model_info.json, class_labels.json
│   └── kashmir/                  # Model 2 specifications & future training roadmap
├── notebooks/                    # 00_btech_model_baseline.ipynb (annotated academic reference)
├── reports/
│   ├── figures/working_model/    # Publication figures (01_accuracy, 02_loss, 04_benchmark)
│   └── evaluation/               # Model audit & evaluation JSON reports
├── research/                     # DATASETS.md (official repositories) & download_log.txt
├── scripts/
│   ├── verify_hardware.py        # Validates Apple Silicon MPS / CUDA / RAM status
│   ├── verify_datasets.py        # Validates 4 canonical CSVs and SHA-256 checksums
│   ├── evaluate_all.py           # Evaluates model weights and logs performance
│   ├── generate_working_model_artifacts.py # Generates 300 DPI convergence & test benchmark plots
│   └── train_kashmir_model.py    # Turnkey training pipeline for Model 2
├── src/herbalist/                # Modular Python source code (data, hardware, models)
└── tests/                        # 26 Unit & integration tests (unit/, integration/)
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup

```bash
git clone https://github.com/darrehanrasool/Herbalist.git
cd Herbalist
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Run Hardware & Dataset Verifications

```bash
# Verify compute accelerator (Apple Silicon MPS / NVIDIA CUDA / CPU):
python scripts/verify_hardware.py

# Verify the integrity, schemas, and completeness of all 4 canonical CSV catalogs:
python scripts/verify_datasets.py
```

### 3. Run the Automated Test Suite

```bash
# Run all 26 unit and integration tests:
python -m unittest discover -s tests -p "test_*.py"

# Or via pytest:
pytest tests/ -v
```

### 4. Launch the Web Platform & Research Terminal

```bash
python api/app.py
```

Open your browser to: **[http://localhost:5001](http://localhost:5001)**

- **Workspace Dashboard**: [http://localhost:5001/](http://localhost:5001/)
- **Botanical Specimen Identification**: [http://localhost:5001/upload](http://localhost:5001/upload)
- **Chemotaxonomy & Hybridization Explorer**: [http://localhost:5001/hybridization](http://localhost:5001/hybridization)
- **Agronomy & Nutrient Guidelines**: [http://localhost:5001/agronomy](http://localhost:5001/agronomy)
- **Research Figures**: [http://localhost:5001/lab](http://localhost:5001/lab)
- **Master Botanical Catalog**: [http://localhost:5001/plants](http://localhost:5001/plants)
- **Scientific Research Terminal & Logs**: [http://localhost:5001/research-lab](http://localhost:5001/research-lab)

---

## 📊 Benchmark Performance Summary

| Split / Metric | Sample Count | Top-1 Accuracy | Top-5 Accuracy | Loss | Purpose |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Training Split** | 3,746 images | 93.34% | — | 0.0800 | Backpropagation gradient updates |
| **Validation Split** | 704 images | 96.79% | 99.12% | 0.1241 | Hyperparameter selection & EarlyStopping |
| **Independent Test Split** | **972 images** | **94.24%** | **98.65%** | **0.1873** | **Unbiased Gold-Standard Evaluation (Zero Leakage)** |

---

## 📜 Intellectual Property & Academic Citation

This software and research framework is licensed under the **Strict Academic & Non-Commercial Research Evaluation License**.

- **Copyright**: © 2026 Dr. Muzafar Rasool Bhat, Dar Rehan Rasool, Muneeb Syed Shah, Shafiya Bashir Pampori, and Sehreen.
- **Affiliation**: Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India.
- **Commercial Use**: Strictly prohibited without an executed institutional licensing agreement.

```bibtex
@software{bhat2026herbalist,
  author       = {Bhat, Dr. Muzafar Rasool and Rasool, Dar Rehan and Shah, Muneeb Syed and Pampori, Shafiya Bashir and Sehreen},
  title        = {Herbalist-AI: Computational Botany, Ethnomedicinal Intelligence & Dual-Model Cascade Platform},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v2.0.0},
  institution  = {Centre for Artificial Intelligence, Islamic University of Science and Technology (IUST)},
  url          = {https://github.com/darrehanrasool/Herbalist}
}
```
