# Herbalist AI — architecture

The live identification service is still the BTech Flask app (`api/app.py`, port **5001**). New modules attach to it. They do not replace the `.h5` model until you retrain.

## Runtime (what stays up)

```Browser →  Flask (api/app.py)
              ├─ POST /analyze          Active Xception (200 Taxa) + 4 Master Catalogs
              ├─ POST /api/predict      JSON prediction API
              ├─ /lab /agronomy /plants /hybridization /research-lab
              └─ data/csv/*.csv         4 Canonical Master Catalogs
```

Run:

```bash
python api/app.py
# http://localhost:5001
```

## Layers

1. **Perception** — leaf/flower image → species prediction (Active Model 1: Xception 200-way; Planned Model 2: Kashmir Endemics 16-way).
2. **Knowledge Foundation** — scientific name → 4 Canonical Master Catalogs (`medicinal.csv`, `fertiliser.csv`, `chemicaltaxonomy.csv`, `disease.csv`) mapped via `label_mapping.csv`.
3. **Agronomy & Phytopathology** — Soil requirements, NPK basal/top-dress schedules, cultural/organic IPM sanitation protocols.
4. **Research & Terminal Console** — Reproducibility audit, zero-leakage test validation, dataset lineage, and export APIs.

## Data layout

| Path                                   | Purpose                          |
| -------------------------------------- | -------------------------------- |
| `data/csv/`                            | 4 Canonical Master Catalogs (216 Taxa) |
| `data/working_model/`                  | Partitions for Model 1 (train, val, test) |
| `data/kashmir/`                        | Partitions for Model 2 (train, val, test) |
| `models/working_model/`                | Active Model 1 weights & evaluation artifacts |
| `models/kashmir/`                      | Planned Model 2 weights & specs |
| `research/`                            | Links, paper notes, dataset log  |

## Training (new, does not run unless you start it)

`training/src/train.py` supports Xception, EfficientNetV2B0, ResNet50, MobileNetV3, VGG16. Logs go to `training/experiments/experiment_log.csv`. Graphs refresh via `training/scripts/generate_lab_graphs.py`.
