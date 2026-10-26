"""Load unified canonical CSVs from data/csv/ and join by scientific name."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "csv"
KNOW = ROOT / "knowledge"


@lru_cache(maxsize=1)
def _tables():
    mapping = {
        "master": (CSV_DIR / "medicinal_plants_master.csv", KNOW / "plants_master.csv"),
        "curated": (CSV_DIR / "medicinal_plants_master.csv", KNOW / "medicinal_plants_global_curated.csv"),
        "soil": (CSV_DIR / "soil_pedological_requirements.csv", KNOW / "soil_requirements.csv"),
        "cultivation": (CSV_DIR / "agronomic_cultivation_protocols.csv", KNOW / "cultivation.csv"),
        "fertilizer": (CSV_DIR / "nutrient_fertilizer_guidelines.csv", KNOW / "fertilizer_guide.csv"),
        "disease": (CSV_DIR / "phytopathology_disease_ipm.csv", KNOW / "disease_ipm.csv"),
        "chemistry": (CSV_DIR / "biochemical_literature.csv", KNOW / "chemistry_literature.csv"),
        "hybridization": (CSV_DIR / "chemotaxonomy_hybridization.csv", KNOW / "chemotaxonomy_hybridization.csv"),
        "kashmir": (CSV_DIR / "kashmir_medicinal_plants.csv", ROOT / "data" / "processed" / "kashmir_medicinal.csv"),
        "counts": (CSV_DIR / "dataset_image_sample_counts.csv", ROOT / "data" / "manifests" / "imagesamplecount.csv"),
    }
    out = {}
    for key, (primary, fallback) in mapping.items():
        if primary.exists():
            out[key] = pd.read_csv(primary)
        elif fallback.exists():
            out[key] = pd.read_csv(fallback)
        else:
            out[key] = pd.DataFrame()
    return out


def row_for(table: str, scientific_name: str) -> dict:
    df = _tables().get(table)
    if df is None or df.empty:
        return {}
    name_col = "Scientificname" if "Scientificname" in df.columns else ("scientific_name" if "scientific_name" in df.columns else None)
    if not name_col:
        return {}
    hit = df[df[name_col].astype(str).str.lower() == str(scientific_name).strip().lower()]
    if hit.empty:
        genus = str(scientific_name).split()[0] if str(scientific_name) else ""
        hit = df[df[name_col].astype(str).str.contains(genus, case=False, na=False)]
    if hit.empty:
        return {}
    return hit.iloc[0].fillna("").to_dict()


def curated_row_for(scientific_name: str) -> dict:
    df = _tables().get("curated")
    if df is None or df.empty:
        return {}
    name_col = "scientific_name" if "scientific_name" in df.columns else ("Scientificname" if "Scientificname" in df.columns else None)
    if not name_col:
        return {}
    hit = df[df[name_col].astype(str).str.lower() == str(scientific_name).strip().lower()]
    if hit.empty:
        genus = str(scientific_name).split()[0] if str(scientific_name) else ""
        hit = df[df[name_col].astype(str).str.contains(genus, case=False, na=False)]
    if hit.empty:
        return {}
    return hit.iloc[0].fillna("").to_dict()


def hybridization_for(scientific_name: str) -> list[dict]:
    df = _tables().get("hybridization")
    if df is None or df.empty:
        return []
    s = str(scientific_name).strip().lower()
    genus = s.split()[0] if s else ""
    hits = df[
        (df["parent_species_1"].astype(str).str.lower().str.contains(s)) |
        (df["parent_species_2"].astype(str).str.lower().str.contains(s)) |
        (df["genus_group"].astype(str).str.lower() == genus.lower())
    ]
    if hits.empty:
        return []
    return hits.fillna("").to_dict(orient="records")


def agronomy_bundle(scientific_name: str) -> dict:
    return {
        "soil": row_for("soil", scientific_name),
        "cultivation": row_for("cultivation", scientific_name),
        "fertilizer": row_for("fertilizer", scientific_name),
        "disease": row_for("disease", scientific_name),
        "chemistry": row_for("chemistry", scientific_name),
        "curated": curated_row_for(scientific_name),
        "hybridization": hybridization_for(scientific_name),
    }


def plant_index(limit: int = 400) -> list[dict]:
    df = _tables().get("master")
    if df is None or df.empty:
        return []
    cols = [c for c in ["Scientificname", "scientific_name", "Biologicalname", "common_name", "Family", "family", "ToxicityLevel", "iucn_conservation_status", "SourceCatalog"] if c in df.columns]
    records = df[cols].head(limit).fillna("").to_dict(orient="records")
    normalized = []
    for r in records:
        normalized.append({
            "Scientificname": r.get("Scientificname") or r.get("scientific_name", ""),
            "Biologicalname": r.get("Biologicalname") or r.get("common_name", ""),
            "Family": r.get("Family") or r.get("family", ""),
            "ToxicityLevel": r.get("ToxicityLevel") or r.get("iucn_conservation_status", "Low"),
            "SourceCatalog": r.get("SourceCatalog", "POWO / ICMR / AYUSH Master")
        })
    return normalized
