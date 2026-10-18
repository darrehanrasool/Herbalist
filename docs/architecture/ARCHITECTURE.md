# Herbalist AI — architecture

The live identification service is still the BTech Flask app (`api/app.py`, port **5001**). New modules attach to it. They do not replace the `.h5` model until you retrain.

## Runtime (what stays up)

```Browser →  Flask (api/app.py)
              ├─ POST /analyze          existing Xception + CSV
              ├─ POST /api/predict      existing JSON API
              ├─ /lab /sensors /agronomy /research /login   new UI
              ├─ POST /api/sensors/ingest
              └─ knowledge/*.csv        agronomy join after ID
```

Run (unchanged):

```bash
cd api
python app.py
# http://localhost:5001
```

## Layers

1. **Perception** — photo → species (current: Xception 200-way). Future: EfficientNet / disease head.
2. **Knowledge** — scientific name → chemistry literature, soil bands, fertilizer, IPM, cultivation.
3. **Sensing** — pH, N, P, K, moisture, temperature, EC (manual form or JSON ingest). Hardware can POST later.
4. **Decision** — gap vs target bands (rules). Not a claim of HPLC yield.
5. **Lab UI** — graphs, catalogs, research dataset links.

## Data layout

| Path                                   | Purpose                          |
| -------------------------------------- | -------------------------------- |
| `data/raw/catalog/`                    | Copies of BTech CSVs             |
| `data/raw/kaggle/<dataset_id>/`        | One folder per Kaggle download   |
| `data/processed/`                      | Cleaned tables / resized indexes |
| `data/splits/{train,test,validation}/` | Image folders for new training   |
| `knowledge/`                           | Join tables for the web report   |
| `research/`                            | Links, paper notes, dataset log  |
| `training/`                            | Train-from-scratch code          |
| `artifacts/graphs/`                    | 20 lab figures                   |
| `auth/`                                | Demo scientist login             |
| `sensors/`                             | Protocol + simulator             |

## Training (new, does not run unless you start it)

`training/src/train.py` supports Xception, EfficientNetV2B0, ResNet50, MobileNetV3, VGG16. Logs go to `training/experiments/experiment_log.csv`. Graphs refresh via `training/scripts/generate_lab_graphs.py`.
