# Installation & Environment Setup Guide · Herbalist AI

## Prerequisites
- **Operating System**: macOS (Apple Silicon M1/M2/M3/M4 or Intel), Linux (Ubuntu 20.04+), or Windows 10/11 with WSL2.
- **Python**: Version 3.9, 3.10, or 3.11.
- **Disk Space**: At least 5 GB for checkpoints, code, and processed catalogs (~15 GB if downloading raw image datasets).
- **RAM**: Minimum 8 GB recommended (16 GB for training new CNN backbones).

---

## 1. Quick Start Installation

```bash
# Clone the repository
git clone https://github.com/darrehanrasool/Herbalist.git
cd Herbalist

# Create and activate a Python 3.11 virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install core production dependencies
pip install -r requirements.txt

# Install development & testing dependencies
pip install -r requirements-dev.txt

# Run automated environment setup & verification
python scripts/setup_environment.py
python scripts/verify_hardware.py
```

---

## 2. Hardware Acceleration Setup

### Apple Silicon (macOS)
TensorFlow and PyTorch use Apple Metal Performance Shaders (MPS):
```bash
pip install tensorflow-macos
```
Verify hardware detection:
```bash
python -m src.herbalist.main hardware
```

### NVIDIA CUDA (Linux / Windows WSL2)
For NVIDIA GPUs, install matching CUDA Toolkit (e.g. CUDA 11.8 or 12.x) and cuDNN. TensorFlow will automatically detect physical GPUs when configured.

---

## 3. Running Pre-Flight Verifications & Tests

To execute the unit and integration test suites:
```bash
# Run unit and integration tests
python -m unittest discover -s tests -p "test_*.py"

# Or using pytest if installed
pytest
```

---

## 4. Launching the Interactive Web Platform

```bash
# Start Flask web server on port 5001
python -m src.herbalist.main serve --port 5001

# Open in browser:
# http://localhost:5001
```
