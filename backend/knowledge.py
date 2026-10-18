"""Load knowledge CSVs and join by scientific name."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
KNOW = ROOT / "knowledge"


@lru_cache(maxsize=1)
def _tables():
    files = {
        "master": "plants_master.csv",
        "soil": "soil_requirements.csv",
        "cultivation": "cultivation.csv",
        "fertilizer": "fertilizer_guide.csv",
        "disease": "disease_ipm.csv",
        "chemistry": "chemistry_literature.csv",
    }
    out = {}
    for key, name in files.items():
        path = KNOW / name
        out[key] = pd.read_csv(path) if path.exists() else pd.DataFrame()
    return out


def row_for(table: str, scientific_name: str) -> dict:
    df = _tables().get(table)
    if df is None or df.empty or "Scientificname" not in df.columns:
        return {}
    hit = df[df["Scientificname"].astype(str) == str(scientific_name)]
    if hit.empty:
        return {}
    return hit.iloc[0].fillna("").to_dict()


def agronomy_bundle(scientific_name: str) -> dict:
    return {
        "soil": row_for("soil", scientific_name),
        "cultivation": row_for("cultivation", scientific_name),
        "fertilizer": row_for("fertilizer", scientific_name),
        "disease": row_for("disease", scientific_name),
        "chemistry": row_for("chemistry", scientific_name),
    }


def plant_index(limit: int = 400) -> list[dict]:
    df = _tables()["master"]
    if df.empty:
        return []
    cols = [c for c in ["Scientificname", "Biologicalname", "Family", "ToxicityLevel", "SourceCatalog"] if c in df.columns]
    return df[cols].head(limit).fillna("").to_dict(orient="records")
