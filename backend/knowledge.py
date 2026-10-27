"""Load 4 Unified Canonical Master CSVs from data/csv/ and join by scientific name."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "csv"
KNOW = ROOT / "knowledge"


@lru_cache(maxsize=1)
def _tables():
    """Load the 4 canonical master CSV tables + neural label mapping."""
    tables = {
        "medicinal": CSV_DIR / "medicinal.csv",
        "fertiliser": CSV_DIR / "fertiliser.csv",
        "chemicaltaxonomy": CSV_DIR / "chemicaltaxonomy.csv",
        "disease": CSV_DIR / "disease.csv",
        "label_mapping": CSV_DIR / "label_mapping.csv",
        "curated": KNOW / "medicinal_plants_global_curated.csv",
        "hybridization": KNOW / "chemotaxonomy_hybridization.csv",
    }
    out = {}
    for key, path in tables.items():
        if path.exists():
            out[key] = pd.read_csv(path)
        else:
            out[key] = pd.DataFrame()
    return out


def row_for(table: str, scientific_name: str) -> dict:
    """Retrieve row for a scientific name from one of the canonical CSVs."""
    df = _tables().get(table)
    if df is None or df.empty:
        return {}
    name_col = "scientific_name" if "scientific_name" in df.columns else ("Scientificname" if "Scientificname" in df.columns else None)
    if not name_col:
        return {}

    target = str(scientific_name).strip().lower()
    hit = df[df[name_col].astype(str).str.strip().str.lower() == target]
    if hit.empty:
        # Fallback to genus-level or substring search
        genus = target.split()[0] if target else ""
        hit = df[df[name_col].astype(str).str.lower().str.contains(genus, case=False, na=False)]
    if hit.empty:
        return {}
    return hit.iloc[0].fillna("").to_dict()


def curated_row_for(scientific_name: str) -> dict:
    """Retrieve canonical medicinal profile for a species."""
    res = row_for("curated", scientific_name)
    if res:
        return res
    return row_for("medicinal", scientific_name)


def hybridization_for(scientific_name: str) -> list[dict]:
    """Retrieve hybridization pairs from knowledge/chemotaxonomy_hybridization.csv."""
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
    """Compile a complete multi-catalog agronomy, botanical, phytochemical, and disease bundle."""
    med = row_for("medicinal", scientific_name)
    fert = row_for("fertiliser", scientific_name)
    chem = row_for("chemicaltaxonomy", scientific_name)
    dis = row_for("disease", scientific_name)

    soil_block = {}
    if med or fert:
        ph_val = str(med.get("edaphic_soil_ph", fert.get("soil_ph_optimal", "6.0 - 7.5")))
        ph_parts = ph_val.split("-") if "-" in ph_val else [ph_val, ph_val]
        temp_val = str(med.get("temperature_optimum_c", "15 - 30 °C")).replace("°C", "").strip()
        temp_parts = temp_val.split("-") if "-" in temp_val else [temp_val, temp_val]
        npk = str(fert.get("npk_ratio_kg_ha", "60:40:40")).split(":")
        soil_block = {
            "pH_min": ph_parts[0].strip(),
            "pH_max": ph_parts[-1].strip(),
            "Texture": med.get("soil_texture", fert.get("soil_texture_drainage", "Well-drained loam")),
            "Temp_C_min": temp_parts[0].strip(),
            "Temp_C_max": temp_parts[-1].strip(),
            "N_level": npk[0] if len(npk) > 0 else "60",
            "P_level": npk[1] if len(npk) > 1 else "40",
            "K_level": npk[2] if len(npk) > 2 else "40",
            "Irrigation": fert.get("irrigation_strategy", "Regular moisture, avoid waterlogging"),
            "Altitude_note": f"Optimal: {med.get('optimal_altitude_min_m', 0)}–{med.get('optimal_altitude_max_m', 2500)} m. Rainfall: {med.get('annual_rainfall_mm', '800-1500 mm')}",
        }

    cultivation_block = {}
    if med or fert:
        cultivation_block = {
            "MonthsToFirstHarvest": "6–12",
            "Propagation": f"Harvest Season: {med.get('harvesting_season', 'Autumn')}",
            "PlantingSeason": med.get("harvesting_season", "Spring/Autumn"),
            "YieldNote": fert.get("expected_yield_per_hectare", "1.5–3.5 t/ha dry herb"),
            "Pros": f"Difficulty: {fert.get('cultivation_difficulty', 'Moderate')}. Yield: {fert.get('expected_yield_per_hectare', '1.5–3.5 t/ha')}",
            "WildCollectionWarning": med.get("toxicological_notes", "Harvest with standard protective protocols."),
        }

    fertilizer_block = {}
    if fert:
        fertilizer_block = {
            "BasalFYM_tha": fert.get("basal_fym_compost_tha", "10.0"),
            "NPK_strategy": f"NPK: {fert.get('npk_ratio_kg_ha', '60:40:40')} kg/ha. Schedule: {fert.get('application_schedule', 'Basal at prep, splits top-dressed')}",
            "Avoid": fert.get("agronomic_avoid_contraindications", "Avoid waterlogging and unbuffered acid soils."),
            "Micronotes": f"Biofertilizers: {fert.get('organic_biofertilizers', 'Azotobacter, PSB')}. Micronutrients: {fert.get('micronutrient_requirements', 'Zinc, Boron')}",
        }

    disease_block = {}
    if dis:
        disease_block = {
            "CommonRisks": dis.get("primary_diseases", "Damping off, foliar leaf spots"),
            "Prevention": dis.get("prevention_cultural_control", "Crop rotation, well-aerated spacing"),
            "OrganicControl": dis.get("biological_organic_ipm", "Trichoderma viride, Neem formulation"),
            "Evidence": f"Pesticide Warning: {dis.get('chemical_control_warning', 'Zero synthetic organophosphates')}. Resistance: {dis.get('disease_resistance_rating', 'Moderate')}",
        }

    return {
        "medicinal": med,
        "fertiliser": fert,
        "chemicaltaxonomy": chem,
        "disease": dis,
        "curated": curated_row_for(scientific_name),
        "soil": soil_block,
        "cultivation": cultivation_block,
        "fertilizer": fertilizer_block,
        "disease_card": disease_block,
        "hybridization": hybridization_for(scientific_name),
    }


def plant_index(limit: int = 400) -> list[dict]:
    """Return unified list of all species with standardized keys for table rendering."""
    df = _tables().get("medicinal")
    if df is None or df.empty:
        return []

    cols = ["scientific_name", "common_name", "family", "iucn_conservation_status", "endemic_to_kashmir_himalayas", "species_id"]
    available_cols = [c for c in cols if c in df.columns]
    records = df[available_cols].head(limit).fillna("").to_dict(orient="records")

    normalized = []
    for r in records:
        normalized.append({
            "Scientificname": r.get("scientific_name", ""),
            "Biologicalname": r.get("common_name", ""),
            "Family": r.get("family", ""),
            "ToxicityLevel": r.get("iucn_conservation_status", "Least Concern"),
            "is_kashmir": r.get("endemic_to_kashmir_himalayas") == "Yes",
            "species_id": r.get("species_id", ""),
            "SourceCatalog": "POWO 2024 / ICMR / AYUSH Master Catalog (216 Taxa)",
        })
    return normalized
