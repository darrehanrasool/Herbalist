# Reproducibility Guide · Herbalist AI

## 1. Deterministic Seeding

To ensure bit-for-bit reproducible runs across machines and virtual environments, all random number generators are locked to seed `42` by default:

```python
from src.herbalist.core import seed_everything
seed_everything(seed=42)
```

This enforces:
- `random.seed(42)`
- `numpy.random.seed(42)`
- `os.environ["PYTHONHASHSEED"] = "42"`
- `tensorflow.random.set_seed(42)`
- `os.environ["TF_DETERMINISTIC_OPS"] = "1"`

---

## 2. Re-verifying Baseline Numbers

To replicate the original BTech reported numbers:
```bash
# Run baseline model audit
python scripts/evaluate_all.py
```
Expected output:
- **Architecture**: `Xception` (ImageNet frozen backbone).
- **Training Accuracy**: `93.34%`
- **Validation Accuracy**: `96.79%`
- **Classes**: `200`
- **Input Dimensions**: `[180, 180, 3]`

---

## 3. Dataset Integrity Verification

Before training or fine-tuning, verify dataset checksums:
```bash
python scripts/verify_datasets.py
```
This reads `data/manifests/dataset_manifest.json` and verifies that raw, processed, and manifest files exist with identical cryptographic hashes.
