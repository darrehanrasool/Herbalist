# Contributing to Herbalist AI

We welcome contributions from researchers, botanists, computational biologists, and software engineers.

---

## 1. Development Workflow

1. **Fork & Branch**: Create a feature branch off `main` (`git checkout -b feature/himalayan-attention`).
2. **Environment**: Activate your Python virtual environment and install dev dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
3. **Coding Standards**:
   - Adhere to PEP 8.
   - Use explicit type annotations and docstrings.
   - Place all models in `src/herbalist/models/`, data loaders in `src/herbalist/data/`.
4. **Testing**: Ensure all 18+ tests pass:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```
5. **Pull Requests**: Submit PR with clear motivation, methodology references, and benchmark results.

---

## 2. Adding New Taxa or Datasets

- Update `data/manifests/dataset_manifest.json` with cryptographic SHA-256 hashes.
- Register new species in `src/herbalist/core/constants.py` and `data/processed/`.
- Ensure IUCN Red List status and toxicity levels are properly annotated.
