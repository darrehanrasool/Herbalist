# Contributor Guidelines · Herbalist-AI

Welcome to **Herbalist-AI**! We are glad you are interested in contributing to this enterprise computational botany, deep learning vision, and ethnopharmacology research platform.

This project is developed and maintained at the **Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Kashmir**. We welcome contributions from researchers, graduate students, computer scientists, botanists, agronomists, and software engineers worldwide.

---

## 📋 Table of Contents

1. [Research Principles & Code of Conduct](#1-research-principles--code-of-conduct)
2. [How to Contribute (Fork & Pull Request Workflow)](#2-how-to-contribute-fork--pull-request-workflow)
3. [Local Development Setup](#3-local-development-setup)
4. [Coding Standards & Architectural Guidelines](#4-coding-standards--architectural-guidelines)
5. [Botanical Data & Kashmir Flora Contribution Rules](#5-botanical-data--kashmir-flora-contribution-rules)
6. [Testing & Verification Requirements](#6-testing--verification-requirements)
7. [Submitting a Pull Request](#7-submitting-a-pull-request)
8. [Contributor Recognition](#8-contributor-recognition)

---

## 1. Research Principles & Code of Conduct

All contributors must abide by our [Academic & Research Code of Conduct](../CODE_OF_CONDUCT.md). We demand high academic integrity, respectful and collegial communication, and strict non-destructive conservation ethics regarding endangered Himalayan flora.

---

## 2. How to Contribute (Fork & Pull Request Workflow)

To contribute and be officially recognized as a **GitHub Contributor**, always use the standard Fork and Pull Request model:

### Step 1: Fork the Repository
- Navigate to [https://github.com/darrehanrasool/Herbalist](https://github.com/darrehanrasool/Herbalist).
- Click the **Fork** button (top right) to create a copy under your GitHub profile.

### Step 2: Clone Your Fork Locally
```bash
git clone https://github.com/<YOUR-USERNAME>/Herbalist.git
cd Herbalist
```

### Step 3: Create a Dedicated Feature Branch
*Never commit directly to `main`.* Use clean, descriptive branch names:
```bash
# For new model architectures:
git checkout -b feature/himalayan-attention-module

# For botanical catalog additions:
git checkout -b data/kashmir-subalpine-taxa

# For bug fixes:
git checkout -b fix/image-preprocessing-pipeline

# For documentation improvements:
git checkout -b docs/clarify-gap-derivation
```

---

## 3. Local Development Setup

### Python Environment
Herbalist-AI requires **Python 3.11+**.

```bash
# 1. Create and activate a clean virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Upgrade core tooling
pip install --upgrade pip setuptools wheel

# 3. Install runtime dependencies and development tools
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Verify system accelerators (Apple Silicon MPS / NVIDIA CUDA / CPU)
python -m src.herbalist.main verify-hardware
```

---

## 4. Coding Standards & Architectural Guidelines

### Modular Architecture
Maintain clean separation of concerns within `src/herbalist/`:
- `core/`: Immutable constants, typed exceptions, YAML configuration manager.
- `data/`: Dataset loaders, image augmentation, deduplication, and quality validators.
- `hardware/`: Device detection and bounded memory monitors.
- `models/`: Neural backbones, classical ML models, and multi-modal fusion heads.
- `training/`: Trainers, schedulers, checkpoint handlers, early stopping.
- `evaluation/`: Statistical validation, confusion matrices, ROC/PR curves.
- `visualization/`: High-resolution figures and dashboard plots.

### Code Style Requirements
- **Formatting**: Format all Python code with `black` (`line-length = 100`).
- **Linting**: Ensure code passes `flake8` checks without syntax or formatting errors.
- **Type Annotations**: Provide explicit type hints (`typing.Optional`, `typing.List`, `typing.Dict`, `typing.Tuple`).
- **Docstrings**: Document all public functions, classes, and methods using clear docstrings detailing arguments, returns, and mathematical definitions.
- **Clean Git Commits**: Large binary model weights (`.h5`, `.keras`, `.pt`), virtual environments (`.venv`), and temporary uploads are ignored by `.gitignore`. Never force-commit large binaries.

---

## 5. Botanical Data & Kashmir Flora Contribution Rules

When contributing plant records, clinical literature, or field imagery:

1. **Taxonomic Validity**:
   - Species binomen must follow accepted botanical nomenclature (verified via Kew *Plants of the World Online* or IPNI).
   - Document the Botanical Family, Local/Kashmiri Names, and active therapeutic secondary metabolites.
2. **Conservation & Red List Classification**:
   - Explicitly annotate the IUCN Red List status (e.g. *Critically Endangered (CR)*, *Endangered (EN)*, *Vulnerable (VU)*).
   - If the species is listed under CITES Appendix I/II (such as *Saussurea costus*), ensure strict regulatory adherence.
3. **Data Integrity & Cryptographic Manifest**:
   - Any new tabular dataset or manifest must be hashed and registered in `data/manifests/dataset_manifest.json` with its SHA-256 checksum.
4. **Habitat Protection & OPSEC**:
   - Do **NOT** publish unmasked GPS coordinates of wild, critically endangered alpine habitats. Obfuscate precise micro-locations to prevent illegal commercial bioprospecting.

---

## 6. Testing & Verification Requirements

No Pull Request will be merged without passing automated test verification.

```bash
# 1. Run all unit and integration tests
python -m unittest discover -s tests -p "test_*.py"

# Or via pytest:
pytest tests/ -v --cov=src/herbalist

# 2. Verify dataset manifest checksums
python scripts/verify_datasets.py

# 3. Test multi-modal pipeline execution
python scripts/train_multimodal_fusion.py
```

If you add new functionality, model layers, or data parsers, you are required to include corresponding unit tests under `tests/unit/` or `tests/integration/`.

---

## 7. Submitting a Pull Request

Once your code is ready and tested:

1. **Commit Your Changes with Conventional Commit Messages**:
   ```bash
   git add .
   git commit -m "feat(models): implement attention-gated Kashmir alpine specialist"
   ```
2. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Open a Pull Request**:
   - Navigate to the original repository on GitHub.
   - Click **Compare & pull request**.
   - Fill out the PR template describing the problem solved, methodology, testing steps, and benchmark results.
4. **Code Review**:
   - The maintainers and faculty supervisors at CAI, IUST will review your code.
   - Address any requested changes promptly.

---

## 8. Contributor Recognition

We value our scientific community:
- Once your Pull Request is accepted and merged, GitHub will automatically list your profile in the project's official **Contributors** section.
- High-impact architectural or data contributions may be acknowledged in future peer-reviewed manuscripts and technical reports originating from the Centre of Artificial Intelligence, IUST.
