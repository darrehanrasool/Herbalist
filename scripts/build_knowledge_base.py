#!/usr/bin/env python3
"""Build agronomy knowledge CSVs from the BTech medicinal catalog + Kashmir list.

Ranges are literature-typical defaults by growth habit / family, not HPLC lab
measurements. Every row is tagged so scientists can replace values later.
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "catalog"
OUT = ROOT / "knowledge"

HABIT_SOIL = {
    "Succulent": dict(ph_min=6.0, ph_max=7.5, n="Low", p="Medium", k="Medium", moisture="Low-Medium", temp_min=18, temp_max=35, texture="Sandy loam", irrigation="Sparse, well-drained"),
    "Herb": dict(ph_min=5.8, ph_max=7.2, n="Medium", p="Medium", k="Medium", moisture="Medium", temp_min=15, temp_max=32, texture="Loam", irrigation="Regular, not waterlogged"),
    "Shrub": dict(ph_min=5.5, ph_max=7.0, n="Medium", p="Medium", k="Medium", moisture="Medium", temp_min=12, temp_max=32, texture="Loam", irrigation="Moderate"),
    "Tree": dict(ph_min=5.5, ph_max=7.5, n="Medium", p="Low-Medium", k="Medium", moisture="Medium", temp_min=10, temp_max=38, texture="Deep loam", irrigation="Deep, infrequent"),
    "Vine": dict(ph_min=5.8, ph_max=7.0, n="Medium", p="Medium", k="High", moisture="Medium-High", temp_min=16, temp_max=34, texture="Rich loam", irrigation="Consistent moisture"),
}

HABIT_GROW = {
    "Succulent": dict(months_to_harvest=8, propagation="Offsets / leaf cuttings", season="Year-round warm", yield_note="Leaf gel after 8–12 months"),
    "Herb": dict(months_to_harvest=4, propagation="Seed / cuttings", season="Kharif or rabi by species", yield_note="Leaf harvest in 3–6 months"),
    "Shrub": dict(months_to_harvest=12, propagation="Cuttings / seed", season="Spring planting", yield_note="First economic harvest year 1–2"),
    "Tree": dict(months_to_harvest=36, propagation="Seed / grafting", season="Monsoon / spring", yield_note="Woody parts after 3+ years"),
    "Vine": dict(months_to_harvest=8, propagation="Cuttings", season="Warm moist", yield_note="Leaves from month 4–8"),
}

FAMILY_DISEASE = {
    "Solanaceae": "Early blight, leaf spot, fruit rot; avoid water on foliage.",
    "Zingiberaceae": "Rhizome rot, bacterial wilt; raised beds and drainage.",
    "Fabaceae": "Root rot, aphids, powdery mildew; do not over-irrigate.",
    "Lamiaceae": "Rust, wilt, leaf miner; air flow and morning irrigation.",
    "Asteraceae": "Powdery mildew, aphids; sulfur-safe sprays if needed.",
    "Asphodelaceae": "Soft rot, scale insects; keep crown dry.",
    "Malvaceae": "Leaf curl, whitefly; neem and yellow traps.",
    "Moraceae": "Anthracnose, fruit fly; sanitation and pruning.",
    "Araceae": "Corm rot, spider mites; shade and drainage.",
    "Acanthaceae": "Damping-off in nursery; sterile media.",
}

FAMILY_FERT = {
    "Zingiberaceae": "Split N, extra K at rhizome swell; FYM 15–20 t/ha.",
    "Asphodelaceae": "Low N; excess nitrogen reduces gel quality. Compost + K.",
    "Lamiaceae": "Light N after each harvest cut; avoid heavy urea.",
    "Solanaceae": "Balanced NPK 10-10-10; Ca to prevent blossom-end issues.",
    "Fabaceae": "Low N (fixes nitrogen); P and K emphasis, rhizobium if seed.",
}


def soil_row(habit: str, is_himalayan: bool) -> dict:
    base = dict(HABIT_SOIL.get(habit, HABIT_SOIL["Herb"]))
    if is_himalayan:
        base["ph_min"] = min(base["ph_min"], 5.2)
        base["temp_min"] = min(base["temp_min"], 5)
        base["temp_max"] = min(base["temp_max"], 26)
        base["texture"] = "Acidic mountain loam / well-drained slope"
        base["moisture"] = "Medium; snowmelt + monsoon, avoid waterlogging"
    return base


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    vn = pd.read_csv(RAW / "medicinal.csv")
    vn["SourceCatalog"] = "VNPlant-200 / BTech medicinal.csv"
    vn["RegionFocus"] = vn["GeographicalDistribution"]
    ka = pd.read_csv(RAW / "kashmir_medicinal.csv")
    ka["SourceCatalog"] = "Kashmir Himalayan list"
    ka["RegionFocus"] = "Kashmir / Himalaya"

    master = pd.concat([vn, ka], ignore_index=True)
    master["Scientificname"] = master["Scientificname"].astype(str).str.strip()
    master = master.drop_duplicates(subset=["Scientificname"], keep="first")
    master.to_csv(OUT / "plants_master.csv", index=False)

    soil_rows, cult_rows, fert_rows, dis_rows, chem_rows = [], [], [], [], []
    for _, r in master.iterrows():
        name = r["Scientificname"]
        habit = str(r.get("GrowthHabit", "Herb"))
        family = str(r.get("Family", ""))
        him = "Kashmir" in str(r.get("SourceCatalog", "")) or "Himalay" in str(r.get("GeographicalDistribution", ""))
        s = soil_row(habit, him)
        g = HABIT_GROW.get(habit, HABIT_GROW["Herb"])
        soil_rows.append({
            "Scientificname": name,
            "Family": family,
            "GrowthHabit": habit,
            "pH_min": s["ph_min"],
            "pH_max": s["ph_max"],
            "Texture": s["texture"],
            "N_level": s["n"],
            "P_level": s["p"],
            "K_level": s["k"],
            "Moisture": s["moisture"],
            "Temp_C_min": s["temp_min"],
            "Temp_C_max": s["temp_max"],
            "Irrigation": s["irrigation"],
            "Altitude_note": "Temperate Himalayan band preferred" if him else "Follow native range",
            "Evidence": "Heuristic by habit/region — replace with ICAR/NMPB/plot data",
        })
        cult_rows.append({
            "Scientificname": name,
            "MonthsToFirstHarvest": g["months_to_harvest"] + (6 if him and habit == "Herb" else 0),
            "Propagation": g["propagation"],
            "PlantingSeason": "Spring after frost" if him else g["season"],
            "Spacing": "30–45 cm herbs; 1–3 m shrubs/trees",
            "Shade": "Partial for forest species; full sun for Aloe/Ocimum types",
            "YieldNote": g["yield_note"],
            "Pros": "Medicinal cash crop; biodiversity; AYUSH demand",
            "Cons": "Misidentification risk; toxicity; conservation law if wild-collected",
            "WildCollectionWarning": "Prefer cultivated material. CITES/state rules may apply.",
            "Evidence": "Generic cultivation template — specialist crop guides needed per species",
        })
        fert_rows.append({
            "Scientificname": name,
            "BasalFYM_tha": 10 if habit != "Succulent" else 5,
            "NPK_strategy": FAMILY_FERT.get(family, "Balanced NPK; organic first; tissue test before high urea"),
            "Avoid": "Excess N on succulents and essential-oil herbs (dilutes actives)",
            "Micronotes": "Correct pH first; Fe/Zn if chlorosis on high-pH soils",
            "Evidence": "Family-level agronomy heuristic",
        })
        dis_rows.append({
            "Scientificname": name,
            "CommonRisks": FAMILY_DISEASE.get(family, "Damping-off, leaf spot, root rot, sap-sucking insects"),
            "Prevention": "Clean seed, drainage, crop rotation, avoid overhead night irrigation",
            "OrganicControl": "Neem, Trichoderma in nursery, sticky traps, remove infected leaves",
            "Evidence": "Family-level IPM heuristic — not a diagnosis model yet",
        })
        chem_rows.append({
            "Scientificname": name,
            "Biologicalname": r.get("Biologicalname", ""),
            "ActiveCompounds": r.get("ActiveCompounds", ""),
            "Medicinalvalue": r.get("Medicinalvalue", ""),
            "ToxicityLevel": r.get("ToxicityLevel", ""),
            "PartsUsed": r.get("PartsUsed", ""),
            "PreparationMethods": r.get("PreparationMethods", ""),
            "LabStatus": "Literature text from BTech CSV — not quantified HPLC",
        })

    pd.DataFrame(soil_rows).to_csv(OUT / "soil_requirements.csv", index=False)
    pd.DataFrame(cult_rows).to_csv(OUT / "cultivation.csv", index=False)
    pd.DataFrame(fert_rows).to_csv(OUT / "fertilizer_guide.csv", index=False)
    pd.DataFrame(dis_rows).to_csv(OUT / "disease_ipm.csv", index=False)
    pd.DataFrame(chem_rows).to_csv(OUT / "chemistry_literature.csv", index=False)
    print(f"Wrote knowledge tables for {len(master)} taxa -> {OUT}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
