# Troubleshooting Guide · Herbalist AI

### 1. Uploaded Image Not Displaying in UI
- **Cause**: In early iterations, `UPLOAD_FOLDER` was set to a relative path (`'static/uploads'`), causing uploads to be saved in the parent directory while Flask was serving static files from `api/static/`.
- **Resolution**: Configured `app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')`. Both `report.html` and `results.html` query `{{ url_for('static', filename=result.image_path) }}` which matches `/static/uploads/<filename>`.

---

### 2. `PermissionError: [Errno 1] Operation not permitted: '/Users/.../.keras/keras.json'`
- **Cause**: On sandboxed or restricted systems, TensorFlow/Keras attempts to read/write its global configuration file at `~/.keras/keras.json`.
- **Resolution**: Set the environment variable `KERAS_HOME` inside the workspace:
  ```python
  import os
  ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  os.environ.setdefault('KERAS_HOME', os.path.join(ROOT, '.keras'))
  os.makedirs(os.environ['KERAS_HOME'], exist_ok=True)
  ```
  This is now handled automatically at the very top of `api/app.py` and `src/herbalist/__init__.py`.

---

### 3. Apple Silicon Metal (MPS) Out-of-Memory
- **Symptom**: Process killed with exit code 137 or high resident memory warnings during training.
- **Resolution**:
  1. Reduce batch size:
     ```python
     python scripts/train_all.py --batch_size 16
     ```
  2. Set `hardware: allow_mps: false` in `configs/hardware.yaml` to fall back to CPU if memory is constrained.

---

### 4. `plant.h5` Model Weight Not Found
- **Symptom**: `ModelNotLoadedError` or demo mode activated.
- **Resolution**:
  The system automatically searches:
  - `checkpoints/best/plant.h5`
  - `models/deep_learning/plant.h5`
  - `api/plant.h5`
  - `./plant.h5`
  If not found locally, `load_ml_model()` automatically streams the release binary from GitHub releases.
