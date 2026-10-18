# Enterprise folder map

```
Herbalist/
├── api/                      # LIVE APP — do not break
│   ├── app.py                # Flask entry (port 5001)
│   ├── plant.h5              # BTech weights
│   ├── medicinal.csv
│   ├── templates/
│   └── static/
├── model/models.ipynb        # Original BTech training notebook
├── plant.h5
├── medicinal.csv / Kashmere.csv / imagesamplecount.csv
├── data/
│   ├── raw/catalog/          # Frozen copies of BTech tables
│   ├── raw/kaggle/<name>/    # One directory per downloaded Kaggle set
│   ├── processed/
│   └── splits/{train,test,validation}/
├── knowledge/                # Join tables for scientists
├── training/                 # Retrain from scratch
├── artifacts/graphs/         # 20 lab figures
├── research/                 # Dataset + paper log
├── auth/                     # Demo login
├── sensors/                  # Ingest protocol + simulator
├── backend/                  # Shared Python services imported by Flask
├── scripts/                  # Knowledge build, downloads
└── docs/                     # Architecture + viva notes
```
