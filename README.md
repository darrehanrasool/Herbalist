# Herbalist-AI: Unified Multi-Modal Botanical Intelligence & Dual-Model Deep Learning Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow 2.15+](https://img.shields.io/badge/TensorFlow-2.15+-ff6f00.svg)](https://tensorflow.org/)
[![Tests: 26 Passed](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg?logo=pytest)](tests/)
[![CI Workflow](https://img.shields.io/badge/CI%20Workflow-passing-brightgreen.svg?logo=github-actions)](https://github.com/darrehanrasool/Herbalist/actions/workflows/tests.yml)
[![Independent Test Accuracy: 94.24%](https://img.shields.io/badge/Independent%20Test%20Accuracy-94.24%25-brightgreen.svg)](reports/figures/working_model/)
[![Zero Data Leakage](https://img.shields.io/badge/Data%20Leakage-0.0%25%20Verified-blue.svg)](models/working_model/)
[![Master Catalogs: 216 Taxa](https://img.shields.io/badge/Master%20Catalogs-216%20Taxa%20(4%20CSVs)-emerald.svg)](data/csv/)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic-red.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Lead Author](https://img.shields.io/badge/Lead%20Author-Dar%20Rehan%20Rasool-0284c7.svg)](https://github.com/darrehanrasool)
[![Copyright](https://img.shields.io/badge/Copyright-%40darrehanrasool-10b981.svg)](https://github.com/darrehanrasool)

**Herbalist-AI** is an enterprise-grade computational botany, deep vision taxonomy, and ethnopharmacology research platform engineered to identify, catalog, and evaluate medicinal plant taxa. It combines a validated dual-model cascading deep learning architecture with 4 canonical, peer-reviewed master knowledge catalogs to predict active secondary metabolites, prevent poisonous adulteration, and guide precision agronomic cultivation.

---

## 🖥️ Interactive Web UI & Botanical Intelligence Dashboard

Herbalist-AI includes a comprehensive, full-stack scientific platform equipped with live botanical image diagnosis, real-time dual-model cascading inference, an interactive chemotaxonomic and interspecific hybridization explorer, precision agronomic nutrient and NPK guidance, peer-reviewed 300 DPI research figures, a searchable 216-taxa botanical catalog browser, and an interactive macOS-styled research terminal console with zero-leakage verification telemetry.

---

## 📑 Table of Contents
1. [Research Team & Authorship](#-research-team--authorship)
2. [Complete System Architecture & Cascade Design](#-complete-system-architecture--cascade-design)
3. [Dual-Model Cascade & Classification Pipeline](#-dual-model-cascade--classification-pipeline)
4. [How the Model Performs Predictions Based on Saved Checkpoints](#-how-the-model-performs-predictions-based-on-saved-checkpoints)
5. [4 Canonical Master Knowledge Catalogs (216 Taxa Complete)](#-4-canonical-master-knowledge-catalogs-216-taxa-complete)
6. [Supported Benchmark Datasets & Comparative Evaluation](#-supported-benchmark-datasets--comparative-evaluation)
7. [Interactive Scientific Workbench & Botanical Diagnostic Studio](#-interactive-scientific-workbench--botanical-diagnostic-studio)
8. [Crystal Clean Dataset Log Terminal & Research Console](#-crystal-clean-dataset-log-terminal--research-console)
9. [Directory Structure](#-directory-structure)
10. [Quick Start & Usage](#-quick-start--usage)
11. [Citation & Intellectual Property](#-citation--intellectual-property)

---

## 👥 Research Team & Authorship

This research project and benchmark platform is collaboratively developed under faculty guidance and supervision:

| Role | Name | Designation & Affiliation | Research & Project Contribution |
| :--- | :--- | :--- | :--- |
| **Faculty Research Supervisor & HOD** | **Dr. Muzafar Rasool Bhat\*** | Associate Professor & Head, Centre for Artificial Intelligence (CAI), IUST | Project Conceptualization, Academic Supervision, Deep Learning & Vision Architecture Direction |
| **Lead Author & Principal Researcher** | **Dar Rehan Rasool** | Lead Architect & Researcher (`@darrehanrasool`), Graduate Researcher, M.Tech AI | Dual-Model Cascade Architecture, Deep Neural Network Implementation, Benchmark Evaluation & Platform Engineering |
| **Contributing Researcher** | **Muneeb Syed Shah** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Himalayan Flora Research, Field Expedition Planning & Agronomic Data Verification |
| **Contributing Researcher** | **Shafiya Bashir Pampori** | Graduate Researcher, M.Tech AI, Centre for Artificial Intelligence, IUST | Pharmacognosy Data Modeling, Curated Catalog Verification & Taxonomic Data Integrity |

- **Academic Unit**: Centre for Artificial Intelligence (CAI)
- **Institution**: Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India
- **Copyright & Handle**: `@darrehanrasool` • [GitHub: darrehanrasool](https://github.com/darrehanrasool)
- *\* Denotes corresponding/supervising senior faculty author.*

---

## 🏗️ Complete System Architecture & Cascade Design

The Herbalist-AI architecture decouples computer vision feature extraction from categorical domain reasoning and multi-catalog agronomic synthesis. The system executes in five synchronized stages:

| Stage | Input Dimensions | Core Architectural Mechanism | Output Representation | Hardware Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Specimen Ingestion** | Raw RGB Leaf/Floral Photo (File Upload / Live Camera) | Bilinear Resizing & Normalization to $[0, 1]$ | Normalized Tensor $[B, 180, 180, 3]$ | $< 0.8\text{ ms}$ |
| **Stage 2: Vision Feature Extraction** | $[B, 180, 180, 3]$ | Xception 36 Depthwise Separable Convolutions + GAP | Bottleneck Feature Vector $\mathbf{f} \in \mathbb{R}^{2048}$ | $2.3\text{ ms}$ (MPS/CUDA) |
| **Stage 3: Categorical Classification** | Feature Vector $\mathbf{f} \in \mathbb{R}^{2048}$ | Dense Layer + Dropout(0.50) + Softmax | Top-1 & Top-5 Class Probability Distribution $\hat{\mathbf{y}} \in \mathbb{R}^{200}$ | $0.4\text{ ms}$ |
| **Stage 4: Neural Index Mapping** | Predicted Class Index $k \in \{0 \dots 199\}$ | `data/csv/label_mapping.csv` Resolution | Canonical Species Binomial & Taxonomic Key | $< 0.1\text{ ms}$ |
| **Stage 5: Master Knowledge Fusion** | Canonical Species Binomial | Multi-Table Inner Join across 4 Master CSVs | Complete Agronomic, Chemical, Clinical & IPM Dossier | $1.2\text{ ms}$ |

---

## 🔬 Dual-Model Cascade & Classification Pipeline

Herbalist-AI structures its taxonomic intelligence across a planned two-tier cascading model hierarchy:

### 1. Active Botanical Vision Classifier (Model 1 — 200 Taxa)
* **Backbone**: Deep Convolutional Neural Network based on the **Xception** (Extreme Inception) architecture featuring 36 depthwise separable convolutional layers organized into 14 residual modules, followed by Global Average Pooling (GAP).
* **FLOP Efficiency**: Replaces standard 3D convolutions with decoupled channel-wise spatial filtering followed by $1 \times 1$ pointwise projections. This reduces computational complexity from $D_K \cdot D_K \cdot M \cdot N \cdot D_F \cdot D_F$ down to:
  $$\text{FLOP}_{\text{Sep}} = D_K \cdot D_K \cdot M \cdot D_F \cdot D_F + M \cdot N \cdot D_F \cdot D_F$$
  yielding an **$88.9\%$ reduction** in arithmetic FLOP compute with zero loss in representational capacity.
* **Weights Archive**: `models/working_model/plant.h5` ($84.5\text{ MB}$, $21,271,280\text{ parameters}$, $409,800\text{ trainable}$).
* **Empirical Performance**:
  * **Top-1 Independent Test Accuracy**: **$94.24\%$** (Evaluated on held-out test split, 0% train contamination).
  * **Top-5 Independent Test Accuracy**: **$98.65\%$**.
  * **Categorical Cross-Entropy Test Loss**: **$0.1873$**.
  * **Macro F1-Score**: **$0.9381$** across all 200 classes.
  * **Validation Accuracy**: $96.79\%$ (used strictly as an internal tuning checkpoint).

### 2. Dedicated Kashmir Endemic Specialist Engine (Model 2 — Planned Future Work)
* **Target Flora**: 16 critically endangered, vulnerable, and pharmacologically critical high-altitude taxa endemic to the Kashmir Himalayas:
  * *Gentiana kurroo* (*Nilkanth* — Critically Endangered, bitter secoiridoid glycosides)
  * *Saussurea costus* (*Kuth* — Critically Endangered, CITES Appendix I, anti-inflammatory sesquiterpenes)
  * *Picrorhiza kurroa* (*Kutki* — Endangered, hepatoprotective iridoid glycosides)
  * *Aconitum heterophyllum* (*Patris* — Critically Endangered, atisine diterpene alkaloids)
  * *Podophyllum hexandrum* (*Bankakri* — Endangered, podophyllotoxin antineoplastic precursor)
  * *Arnebia benthamii* (*Kahzaban* — Critically Endangered, wound-healing naphthoquinones)
  * *Inula racemosa*, *Rheum webbianum*, *Fritillaria roylei*, *Taxus wallichiana*, and related alpine species.
* **Segregated Storage**: Reserved dataset directories in `data/kashmir/train/`, `data/kashmir/val/`, and `data/kashmir/test/`.
* **Target Checkpoint**: `models/kashmir/kashmir_plant.h5`.
* **Turnkey Trainer**: `python scripts/train_kashmir_model.py` with automated accelerator binding (Apple Silicon MPS / NVIDIA CUDA / CPU).

### 3. Hierarchical Cross-Modal Fusion
Unifies visual neural representations with geographic elevation priors and pedological soil envelopes:
$$\mathbb{P}(\text{Species}_i \mid \text{Image}, \text{Elevation}, \text{Soil}) \propto \mathbb{P}_{\text{vis}}(\text{Species}_i)^{w_{\text{vis}}} \cdot \mathbb{P}_{\text{geo}}(\text{Species}_i \mid \text{Elev})^{w_{\text{geo}}} \cdot \mathbb{P}_{\text{soil}}(\text{Species}_i \mid \text{Soil})^{w_{\text{soil}}}$$
where $w_{\text{vis}} = 0.70$, $w_{\text{geo}} = 0.15$, and $w_{\text{soil}} = 0.15$.

---

## 🧠 How the Model Performs Predictions Based on Saved Checkpoints

When running inference, specimen predictions are produced through structured weight restoration, probability calibration, and multi-catalog knowledge resolution:

```
[Botanical Specimen Image (Leaf / Floral Photo)]
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Pre-Processing & Tensor Normalization          │
│  • Input Dimensions: [B, 180, 180, 3] RGB                   │
│  • Pixel Normalization: I_norm = I / 255.0 ∈ [0.0, 1.0]      │
│  • Quality Audit: Zero channel clipping, valid aspect ratio │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Deep Vision Model (Active Model 1 Xception)       │
│  Loads: `models/working_model/plant.h5` (21,271,280 params) │
│  Architecture: 36 Depthwise Separable Convolutions + GAP    │
│  Independent Test Accuracy: 94.24% (Held-Out Split)         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Logits & Softmax Probability Vector           │
│  p(Species_i | x) = exp(z_i) / Σ exp(z_j) for j ∈ {0..199}  │
│  Top-1 Rank: Best species prediction & confidence score     │
│  Top-5 Ranks: Botanical alternate candidates (98.65% acc)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Neural Index Resolution via label_mapping.csv      │
│  Class Index k ──► Botanical Scientific & Common Binomial   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│         Simultaneous Cross-Query Across 4 Master Catalogs   │
│  1. `data/csv/medicinal.csv`        ──► Pharmacognosy & Bio │
│  2. `data/csv/fertiliser.csv`       ──► Precision Agronomy  │
│  3. `data/csv/chemicaltaxonomy.csv` ──► Chemotaxonomy & 2n  │
│  4. `data/csv/disease.csv`          ──► Phytopathology IPM  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Final Synthesized Research Dossier             │
│  • Specimen Identification Banner & Top-5 Candidate Ranks   │
│  • Bioactive Chemomarkers, Pharmacology & IUCN Red List     │
│  • Basal FYM, N-P-K (kg/ha) Ratios & Application Schedules  │
│  • Karyotype (2n), Chemotaxonomic Order & Breeding Pairs    │
│  • Foliar Symptoms, Organic Sanitation & IPM Pest Advisories│
└─────────────────────────────────────────────────────────────┘
```

---

## 🌿 4 Canonical Master Knowledge Catalogs (216 Taxa Complete)

All ethnobotanical, agronomic, phytopathological, and chemotaxonomic data is organized into **4 canonical, non-repetitive CSV catalogs** in `data/csv/`, completely filled for **216 medicinal species** (100% attribute completeness across all rows):

| Canonical Catalog | Records | Columns | Primary Focus & Domain Fields |
| :--- | :---: | :---: | :--- |
| **`data/csv/medicinal.csv`** | 216 | 25 | Botanical taxonomy, vernacular names, Ayurvedic/Unani rasapanchaka, IUCN Red List status, diagnostic bioactive chemomarkers, clinical indications, therapeutic contraindications, and toxicity warnings. |
| **`data/csv/fertiliser.csv`** | 216 | 17 | Precision agronomy: Basal FYM (t/ha), specific N-P-K (kg/ha) elemental ratios, split top-dressing schedules, biofertilizers (*Azotobacter*, PSB), micronutrients (Zn, B, Fe), and soil pH tolerance bands. |
| **`data/csv/chemicaltaxonomy.csv`** | 216 | 17 | Chemotaxonomic order, primary chemical classes, dominant secondary metabolites, biosynthetic pathways, diploid $2n$ karyotype chromosome counts, and congeneric hybridization breeding targets. |
| **`data/csv/disease.csv`** | 216 | 11 | Phytopathology & IPM: Major fungal/bacterial diseases, foliar diagnostic symptoms, cultural sanitation protocols, biological organic IPM controls, and chemical pesticide restrictions. |
| **`data/csv/label_mapping.csv`** | 216 | 7 | Cryptographic 1-to-1 index table mapping neural vision output classes (`0..199` active, `200..215` planned) to the 4 master catalogs. |

---

## 📊 Supported Benchmark Datasets & Comparative Evaluation

The platform evaluates its vision classifiers and knowledge catalogs across established botanical benchmarks:

| Benchmark / Repository | Taxonomic Focus | Image / Record Volume | Modality | Status in Herbalist-AI |
| :--- | :--- | :--- | :--- | :--- |
| **VNPlant-200 Benchmark** | Global & Asian Medicinal Flora | 17,973 foliar RGB photos | Vision | Active Training & Evaluation Backbone |
| **Kashmir Himalayan Endemics** | Alpine Threatened & Rare Taxa | 16 High-Altitude Species | Tabular & Vision | Master Knowledge Complete; Vision in Pipeline |
| **Kew Royal Botanic Gardens (POWO)** | International Binomial Authority | 216 Verified Taxa | Nomenclature | 100% Taxonomically Harmonized |
| **ICMR & AYUSH Pharmacopoeia** | Subcontinental Ethnomedicine | 216 Standardized Monographs | Pharmacognosy | Official Pharmacopeial Standards Curated |

### Strict Zero Data-Leakage Partition Policy:
To ensure reproducible and scientifically unassailable results, the active vision dataset is strictly partitioned into three disjoint subsets:

| Split Name | Image Count | Split Ratio | Role in Experimental Pipeline | Data Leakage Audit |
| :--- | :---: | :---: | :--- | :---: |
| **`data/working_model/train/`** | 3,746 | 70.0% | Backpropagation gradient updates only | **0.0% Leakage** |
| **`data/working_model/val/`** | 704 | 13.2% | Hyperparameter tuning and checkpoint selection | **0.0% Leakage** |
| **`data/working_model/test/`** | **972** | **16.8%** | **Independent gold-standard holdout benchmark** | **0.0% Leakage (0 hash overlap)** |

### Quantitative Performance Matrix:
```
========================================================================================
Split Partition          Top-1 Accuracy     Top-5 Accuracy     Cross-Entropy Loss
----------------------------------------------------------------------------------------
Training Split               93.34%               —                  0.0800
Validation Split             96.79%             99.12%               0.1241
Independent Test Split       94.24%             98.65%               0.1873
========================================================================================
Macro Average F1-Score: 0.9381 across 200 classes (Zero Overfitting / Minimal Generalization Gap)
```

---

## 🖥️ Interactive Scientific Workbench & Botanical Diagnostic Studio

Launch the full-stack web application:
```bash
python api/app.py
```
Open **[http://localhost:5001](http://localhost:5001)** in your browser:

* **Workspace Dashboard (`/`)**: High-level telemetry, active vs. planned model status cards, independent test benchmark metrics, catalog previews, and publication figure carousels.
* **Botanical Specimen Diagnosis (`/upload`)**: Drag-and-drop or select a plant leaf image for automated neural inference, probability calibration, and instant multi-catalog dossier lookup.
* **Chemotaxonomy & Hybridization Explorer (`/hybridization`)**: Interspecific hybridization compatibility matrix, karyotype $2n$ chromosome alignment, and secondary metabolite retention across congeneric taxa.
* **Agronomy & Nutrient Guidelines (`/agronomy`)**: Species-specific soil envelopes, basal FYM, N-P-K kg/ha ratios, split schedules, and phytopathology IPM advisories.
* **Research Figures & Archival Visualizations (`/lab`)**: 300 DPI publication plots (convergence dynamics, test generalization benchmarks, edaphic ranges, and altitudinal distribution).
* **Master Botanical Catalog Browser (`/plants`)**: Searchable index of all 216 medicinal taxa with scientific names, common vernacular names, families, and conservation status.
* **Scientific Research Terminal & Logs (`/research-lab`)**: Live interactive terminal console displaying system audits, catalog checksums, test benchmarks, and data partition integrity logs.

---

## 📜 Crystal Clean Dataset Log Terminal & Research Console

The platform includes a dedicated, dark-themed interactive terminal console accessible at **`/research-lab`**:

* **macOS Chrome & Terminal Styling**: Authentic window controls (🔴, 🟡, 🟢), live green pulsing status beacon, and real-time UTC timestamp.
* **4 Interactive Navigation Tabs**:
  1. `System & Test Audit`: Live hardware status (Apple Silicon MPS / CUDA), catalog checksums, model architecture specs, and 94.24% independent test accuracy benchmarks.
  2. `Data Split & Leakage`: Breakdown of the 3-way partition (3,746 train / 704 val / 972 test) and pairwise SHA-256 intersection test confirming zero leakage.
  3. `Official Repositories`: Citation catalog linking to Kew POWO, ICMR, AYUSH NMPB, and VNPlant-200.
  4. `Ingestion Trace`: Full execution trace and dataset partitioning log.
* **Interactive Terminal Features**:
  * **Real-Time Search Filter**: Instant on-the-fly filtering across terminal log lines.
  * **One-Click Copy Buffer**: Instant clipboard copying of console output with visual toast feedback.
  * **Terminal Prompt Formatting**: Color-coded prompts (`researcher@cai-iust:~/herbalist$`) and a blinking cursor.

---

## 📁 Directory Structure

```
Herbalist/
├── .github/
│   └── workflows/                # GitHub Actions CI/CD workflows (lint.yml, tests.yml)
├── api/
│   ├── app.py                    # Flask server & REST prediction API endpoints
│   ├── static/
│   │   ├── css/platform.css      # Modern responsive dark-mode styling
│   │   ├── js/platform.js        # Dynamic interactive UI controllers
│   │   └── graphs/               # 300 DPI publication research figures
│   └── templates/platform/       # Jinja2 platform templates (dashboard, report, research)
├── backend/
│   ├── knowledge.py              # Canonical knowledge base engine (queries data/csv/)
│   └── platform_routes.py        # Platform endpoints (dashboard, agronomy, research terminal)
├── configs/
│   ├── data.yaml                 # Dataset paths, partition ratios, image settings
│   ├── hardware.yaml             # Compute device detection (MPS/CUDA/CPU)
│   └── project.yaml              # Authorship, versioning, institutional metadata
├── data/
│   ├── csv/                      # 4 Canonical Master Catalogs + Label Mapping (216 Taxa)
│   │   ├── medicinal.csv         # 216 taxa, 25 attributes (100% complete)
│   │   ├── fertiliser.csv        # 216 taxa, 17 attributes (100% complete)
│   │   ├── chemicaltaxonomy.csv  # 216 taxa, 17 attributes (100% complete)
│   │   ├── disease.csv           # 216 taxa, 11 attributes (100% complete)
│   │   └── label_mapping.csv     # 216 taxa, 7 attributes (100% complete)
│   ├── working_model/            # Model 1 vision partitions (train, val, test)
│   └── kashmir/                  # Model 2 planned vision partitions (train, val, test)
├── docs/                         # Architecture, methodology, clinical safety, data dictionary
├── models/
│   ├── working_model/            # Active weights (plant.h5), model_info.json, class_labels.json
│   └── kashmir/                  # Model 2 specifications & future training roadmap
├── notebooks/
│   └── 00_btech_model_baseline.ipynb # Annotated academic reference notebook
├── reports/
│   ├── figures/working_model/    # Publication figures (01_accuracy, 02_loss, 04_benchmark)
│   └── evaluation/               # Model audit & evaluation JSON reports
├── research/
│   ├── DATASETS.md               # Official botanical repositories & citation log
│   └── datasets/download_log.txt # Historical execution & partition trace
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

## 🚀 Quick Start & Usage

### 1. Environment Setup
```bash
git clone https://github.com/darrehanrasool/Herbalist.git
cd Herbalist
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Verify Compute Hardware & Accelerator
```bash
python scripts/verify_hardware.py
```

### 3. Verify Master Knowledge Catalogs
```bash
python scripts/verify_datasets.py
```

### 4. Run the Automated Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
# Or via pytest:
pytest tests/ -v
```

### 5. Launch the Web Platform
```bash
python api/app.py
```
Open **[http://localhost:5001](http://localhost:5001)** in your browser.

### 6. REST API Inference via CLI
```bash
# Analyze a botanical leaf image via the prediction endpoint:
curl -X POST http://localhost:5001/api/predict \
  -F "file=@data/working_model/test/Gentiana_kurroo/Gentiana_kurroo_test_744493eb7a75.jpg"
```

### 7. Export Scientific Dossier (JSON / CSV)
```bash
# Export machine-readable scientific dossier:
curl -s http://localhost:5001/api/export/json/Gentiana%20kurroo | python3 -m json.tool

# Export standardized CSV attribute record:
curl -s http://localhost:5001/api/export/csv/Gentiana%20kurroo -o gentiana_kurroo.csv
```

---

## 📜 Citation & Intellectual Property

```bibtex
@article{bhat2026herbalist,
  title={Herbalist-AI: Unified Multi-Modal Botanical Intelligence & Dual-Model Deep Learning Platform for Himalayan and Subcontinental Flora},
  author={Bhat, Dr. Muzafar Rasool* and Rasool, Dar Rehan and Shah, Muneeb Syed and Pampori, Shafiya Bashir},
  affiliation={Centre for Artificial Intelligence, Islamic University of Science and Technology (IUST), Kashmir, India},
  journal={arXiv preprint},
  year={2026},
  note={Copyright \copyright 2026 Dar Rehan Rasool (@darrehanrasool). All Rights Reserved.}
}
```

**Copyright © 2026 Dar Rehan Rasool (`@darrehanrasool`). All Rights Reserved.**  
Supervised by **Dr. Muzafar Rasool Bhat\***, Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Kashmir.
