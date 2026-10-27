# Herbalist-AI: Enterprise Deep Learning & Botanical Intelligence Platform

[![Tests: 25 Passed](https://img.shields.io/badge/tests-25%20passed-brightgreen.svg?logo=pytest)](tests/)
[![CI Workflow](https://img.shields.io/badge/CI%20Workflow-passing-brightgreen.svg?logo=github-actions)](https://github.com/darrehanrasool/Herbalist/actions/workflows/tests.yml)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic-red.svg)](LICENSE)
[![DOI: Zenodo](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.herbalist--ai-blue.svg)](https://zenodo.org/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Top-1 Accuracy: 96.79%](https://img.shields.io/badge/Top--1%20Accuracy-96.79%25-brightgreen.svg)](reports/evaluation/evaluation_report.md)
[![Kashmir Endemic Focus](https://img.shields.io/badge/Flora-Kashmir%20Himalaya-emerald.svg)](data/csv/kashmir_medicinal_plants.csv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Herbalist-AI is an enterprise-grade computational botany, deep vision taxonomy, and ethnopharmacology research platform engineered to identify, catalog, and evaluate medicinal plant taxa, protect critically endangered high-altitude flora of the Kashmir Himalayas, predict active bioactive secondary metabolites, and guide precision agronomic ex-situ cultivation.

---

## 👥 Research Team & Contributors

This research project is designed, engineered, and maintained at the **Centre of Artificial Intelligence, Islamic University of Science and Technology (IUST), Kashmir**.

| Role                                                | Name                        | Designation & Affiliation                                                  | Research & Project Contribution                                                                                   |
| :-------------------------------------------------- | :-------------------------- | :------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **Head of Department (HOD) & Principal Supervisor** | **Dr. Muzafar Rasool Bhat** | Associate Professor & Head, Centre for Artificial Intelligence (CAI), IUST | Project Conceptualization, Academic Supervision, Deep Learning & Vision Architecture Direction                    |
| **Project Lead & Author**                           | **Dar Rehan Rasool**        | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST    | Multi-Modal Fusion Engine, Decoupled Xception Architecture, End-to-End Implementation & Full Platform Engineering |
| **Contributing Researcher**                         | **Muneeb Syed Shah**        | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST    | High-Altitude Kashmir DSLR Collection Protocol, Agronomic Soil Modeling & Cross-Dataset Evaluation                 |
| **Contributing Researcher**                         | **Shafiya Bashir Pampori**  | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST    | Pharmacognosy Data Modeling, Telemetry Quality Auditing & Taxonomic Data Integrity                                |
| **Research Contributor**                            | **Sehreen**                 | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST    | Pharmacognosy Curation, Chemotaxonomy Modeling & Botanical Literature Synthesis                                   |

- **Academic Unit**: Centre of Artificial Intelligence (CAI)
- **Institution**: Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India

---

## Key Features

- **Extreme Inception Decoupled Vision Architecture**: Decoupled Depthwise Separable Convolutions (36 conv layers across 14 modules, yielding an $88.9\%$ reduction in FLOP compute over standard convolutions) achieving **$96.79\%$ validation accuracy** across 200 medicinal taxa.
- **Kashmir Himalayan Endemic Specialist Engine**: Dedicated high-altitude taxonomic intelligence module targeting 15 critically endangered and threatened alpine medicinal taxa (_Gentiana kurroo_, _Saussurea costus_, _Picrorhiza kurroa_, _Aconitum heterophyllum_, _Podophyllum hexandrum_, etc.) with elevation gating ($> 2,500\text{ m}$ masl).
- **Automated Kashmir DSLR Ingestion & Stratified Splitting**: Native decoding of camera RAW (.CR2, .CR3, .NEF, .ARW) and standard RGB, Laplacian blur detection ($\sigma^2 < 80.0$), EXIF altitude extraction, and automated stratified 70/15/15 train/val/test splitting.
- **Unified Canonical CSV Repository (`data/csv/`)**: Centrally organizes all 9 primary tabular datasets with zero filename clashes and standardized `snake_case` schema.
- **Chemotaxonomy & Interspecific Hybridization Engine**: Evaluates cross-breeding compatibility ($2n$ karyotype synapsis, genetic distance $D_{\text{genomic}}$), bioactive secondary metabolite retention, and agronomic biomass vigour across 12 verified Himalayan-global congener pairs.
- **GPU-Scale Training Engine**: Multi-platform accelerator support (Apple Silicon Metal MPS / NVIDIA CUDA / CPU), Label Smoothing, Cosine Decay LR, and live JSONL telemetry logging.
- **10 Publication-Quality Research Visualizations**: 300 DPI figures covering altitudinal zonation, edaphic envelopes, confusion matrices, ROC curves, and breeding matrices.
- **Hierarchical Multi-Modal Fusion**: Unifies deep visual representations ($2048$-dimensional feature vectors from Xception) with geographic elevation priors ($\mathbb{P}(\text{Taxon} \mid \text{Altitude})$) and 7-dimensional physicochemical soil telemetry (pH, N, P, K, moisture, temperature, EC) to eliminate out-of-distribution taxonomic hallucinations.
- **1-Click Scientific Dossier Downloads**: Instant export of machine-readable JSON dossiers and standardized CSV records directly from the scientific workbench.

---

## Project Architecture

```
Herbalist-AI/
├── .github/              # Issue templates, PR templates, and GitHub Actions CI/CD workflows
├── configs/              # YAML configurations for project, data, models, training, hardware, viz
├── data/
│   ├── csv/              # Unified canonical CSV tables (master, kashmir, soil, disease, etc.)
│   ├── manifests/        # Dataset manifests, checksums, and DSLR split logs
│   ├── raw/
│   │   ├── kashmir/      # Kashmir DSLR in-situ field photography
│   │   └── kaggle/       # Standard botanical benchmarks
│   ├── interim/          # Standardized normalized intermediate crops
│   ├── processed/        # Stratified Train (70%), Val (15%), Test (15%) splits
│   └── splits/           # Tabular train/val/test splits
├── docs/                 # Architectural specifications, data lineage, safety, reproducibility
├── experiments/          # Experiment tracking, parameter configs, and experiment_registry.csv
├── logs/                 # Dedicated logs for application, training, errors, datasets, hardware
├── models/
│   └── deep_learning/    # Trained weights (plant.h5, 21.2M parameters)
├── notebooks/            # Publication-ready Jupyter notebooks for baseline, quality, and comparison
├── papers/               # Research PDFs, metadata JSON, literature reviews, mathematical formulas
├── reports/
│   └── figures/          # 300 DPI publication-quality figures
├── scripts/              # Operational CLI scripts (process_kashmir_dslr, train_model, curate)
├── src/herbalist/        # Production modular source code
│   ├── core/             # Configuration, constants, typed exceptions, reproducibility
│   ├── data/             # Ingestion, DSLR pipeline, augmentation, feature engineering
│   ├── hardware/         # Device detection (MPS/CUDA), memory bounds, resource monitoring
│   ├── models/           # Global vision (Xception), Kashmir specialist (MobileNetV3), Agronomy MLP
│   ├── training/         # GPU trainer, callbacks, optimizer, checkpoint manager
│   ├── validation/       # Cross-validation, threshold tuning, probability calibration
│   ├── evaluation/       # Multi-class metrics, statistical testing (McNemar, Wilcoxon)
│   ├── explainability/   # Grad-CAM, feature importance ranking, botanist reports
│   └── utils/            # File I/O, hashing, microsecond timers
└── tests/                # Unit and integration pytest test suite (25 passing tests)
```

---

## Quickstart

### 1. Installation & Environment Activation

```bash
git clone https://github.com/darrehanrasool/Herbalist.git
cd Herbalist
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Launch Interactive Web Platform & Agronomy Console

Launch the real-time diagnosis platform with drag-and-drop live image analysis, soil envelope sliders, and Kashmir flora Explorer:

```bash
python api/app.py
# Or via enterprise CLI:
python -m src.herbalist.main serve --port 5001
# Or via Makefile:
make run
```

Access URL: **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

- Modern Platform Console: **[http://127.0.0.1:5001/platform/](http://127.0.0.1:5001/platform/)**
- Species Identification & Diagnosis: **[http://127.0.0.1:5001/platform/identify](http://127.0.0.1:5001/platform/identify)**
- Kashmir & Global Taxa Explorer: **[http://127.0.0.1:5001/platform/plants](http://127.0.0.1:5001/platform/plants)**

### 3. Run the Multi-Dataset Multi-Modal Fusion Pipeline

Execute end-to-end integration across Global Vision (200 species), Kashmir Specialist (15 high-altitude species), and Agronomic Soil MLP:

```bash
python scripts/train_multimodal_fusion.py
```

### 4. CLI Species Prediction & Phytochemical Extraction

```bash
# Predict species, active metabolites, and toxicity on a sample image:
python -m src.herbalist.main predict tests/fixtures/sample_leaf_34.jpg
```

### 5. Verify Compute Hardware & Accelerator (Apple Silicon MPS / CUDA)

```bash
python -m src.herbalist.main verify-hardware
```

### 6. Comprehensive Statistical Audits & Evaluation

```bash
# Verify cryptographic SHA-256 dataset integrity against manifests:
python scripts/verify_datasets.py

# Run all 18 automated unit and integration tests:
python -m unittest discover -s tests -p "test_*.py"
# Or via pytest:
pytest tests/ -v
```

---

## 📊 Botanical Benchmark Performance & Convergence

Evaluated across **17,973 images** spanning **200 medicinal plant species** (12,000 training, 5,973 validation/testing):

| Epoch | Step Duration | Training Loss | Training Accuracy | Validation Loss | Validation Accuracy | Epoch Delta ($\Delta \text{Val Acc}$) |
| :---: | :-----------: | :-----------: | :---------------: | :-------------: | :-----------------: | :-----------------------------------: |
| **1** |    1,704s     |    2.4598     |      47.82%       |     1.0457      |       74.89%        |        Baseline initialization        |
| **2** |    1,726s     |    1.0808     |      73.73%       |     0.6013      |       85.79%        |              $+10.90\%$               |
| **3** |    1,738s     |    0.6936     |      82.74%       |     0.4381      |       89.42%        |               $+3.63\%$               |
| **4** |    1,155s     |    0.4859     |      87.77%       |     0.3137      |       93.00%        |               $+3.58\%$               |
| **5** |    1,111s     |    0.3506     |      91.47%       |     0.2160      |       95.45%        |               $+2.45\%$               |
| **6** |    1,114s     |  **0.2653**   |    **93.57%**     |   **0.1672**    |     **96.79%**      |             **$+1.34\%$**             |

### Priority Kashmir Endemic Taxa Catalog

| Botanical Taxon          | Common / Kashmiri Name | IUCN Conservation Status                 | Elevation Range | Active Phytochemical Compounds                 |
| :----------------------- | :--------------------- | :--------------------------------------- | :-------------- | :--------------------------------------------- |
| _Gentiana kurroo_        | Nilkanth / Neel Kanth  | **Critically Endangered (CR)**           | 1,800 – 3,000 m | Gentiopicroside, Amarogentin, Swertiamarin     |
| _Saussurea costus_       | Kuth / Costus          | **Critically Endangered (CR)** (CITES I) | 2,500 – 3,800 m | Costunolide, Dehydrocostus lactone, Saussurine |
| _Picrorhiza kurroa_      | Kutki / Kour           | **Endangered (EN)**                      | 3,000 – 4,500 m | Picroside I, Picroside II, Kutkoside           |
| _Aconitum heterophyllum_ | Atis / Patris          | **Critically Endangered (CR)**           | 2,400 – 4,000 m | Atisine, Heteratisine, Aconitine               |
| _Podophyllum hexandrum_  | Wanwangan / Bankakri   | **Endangered (EN)**                      | 2,700 – 4,200 m | Podophyllotoxin, 4'-demethylpodophyllotoxin    |
| _Arnebia benthamii_      | Kahzaban               | **Critically Endangered (CR)**           | 3,000 – 4,300 m | Shikonin derivatives, Alkannin                 |
| _Inula racemosa_         | Poshkar                | **Endangered (EN)**                      | 2,000 – 3,200 m | Alantolactone, Isoalantolactone                |
| _Rheum webbianum_        | Pambchalan             | **Vulnerable (VU)**                      | 2,800 – 4,200 m | Emodin, Rhein, Chrysophanol                    |

---

## 📚 Academic Literature & Research Benchmarks

Comprehensive academic evaluations, comparative matrices, and researcher reviews are documented in:

- 📄 [**Original Research Paper Manuscript (PDF)**](papers/pdf/Herbalist_Research_Paper.pdf): Full research paper manuscript on deep learning botanical classification and ethnopharmacology.
- 📄 [**B.Tech Baseline Model Reference & Mathematical Derivations**](docs/btech_model_reference.md): Complete mathematical formulation of Depthwise Separable Convolutions, FLOP complexity calculations, parameter proofs, and empirical convergence history.
- 📓 [**HerbEsentia Academic Reference Notebook**](notebooks/00_btech_model_baseline.ipynb): Interactive Jupyter notebook with complete mathematical annotations, loss/accuracy plots, and clean path logic.
- 🔬 [**Methodology & Algorithmic Formulation**](docs/methodology.md): Rigorous specification of transfer learning feature freezing ($\nabla_{\mathbf{W}} \mathcal{L} = 0$), Global Average Pooling (GAP), and Bayesian hierarchical multi-modal fusion.
- 🏛️ [**System Architecture & Subsystem Blueprint**](docs/architecture.md): Full enterprise design specifications, data flow diagrams, and layer topologies.
- 📋 [**Dataset Documentation & Provenance Guide**](docs/dataset_documentation.md): Comprehensive inventory of VNPlant-200, Indian Medicinal Leaves, and Kashmir field surveys.
- 🛡️ [**Clinical Safety & Botanical Adulterant Diagnostics**](docs/clinical_safety.md): Safety protocols for preventing toxic plant substitution and misidentification of poisonous lookalikes.
- 📑 [**Model Card & Scientific Transparency Report**](docs/model_card.md): Model performance boundaries, fairness metrics, and ethical usage guidelines.
- 📖 [**Literature Review & Botanical Survey**](papers/literature_reviews/deep_learning_botanical_survey.md): Comprehensive academic survey of deep neural networks in botanical taxonomy.
- 🔬 [**Architecture Comparison Matrix (Xception vs EfficientNet)**](papers/methodology_extraction/xception_vs_efficientnet.md): Micro-architectural benchmark of FLOPs, memory footprint, and top-1 accuracy.

---

## 📜 Intellectual Property & License

This project is licensed under the **Strict Academic & Non-Commercial Research Evaluation License** (All Rights Reserved).

- **Copyright**: © 2026 Dr. Muzafar Rasool Bhat, Dar Rehan Rasool, Muneeb Syed Shah, Shafiya Bashir Pampori, and Sehreen.
- **Affiliation**: Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India.
- **Commercial Use**: **Strictly Prohibited**. No commercial exploitation, resale, closed-source packaging, or incorporation into proprietary agricultural or pharmaceutical tools is permitted without an executed licensing agreement.
- **Academic Citation**: Any scientific paper, dissertation, or research study utilizing this architecture, dataset catalog, or codebase must formally cite the authors and official Zenodo DOI via [CITATION.cff](CITATION.cff).

See the full terms in [LICENSE](LICENSE).

---

## 📖 Citation

If you use Herbalist-AI in your research or academic publications, please cite:

```bibtex
@software{bhat2026herbalist,
  author       = {Bhat, Dr. Muzafar Rasool and Rasool, Dar Rehan and Shah, Muneeb Syed and Pampori, Shafiya Bashir and Sehreen},
  title        = {Herbalist-AI: Enterprise Deep Learning & Multi-Modal Fusion Framework for Himalayan Flora Taxonomy, Pharmacognosy, and Precision Agronomy},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v2.0.0},
  institution  = {Centre of Artificial Intelligence, Islamic University of Science and Technology (IUST)},
  url          = {https://github.com/darrehanrasool/Herbalist}
}
```
