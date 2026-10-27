"""Feature engineering for botanical catalogs, phytochemicals, and soil chemistry."""
from __future__ import annotations

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def encode_botanical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract genus, family encoding, and toxicity ordinals from botanical catalog."""
    df_out = df.copy()
    col_name = None
    for candidate in ["scientific_name", "Scientificname"]:
        if candidate in df_out.columns:
            col_name = candidate
            break
    if col_name:
        df_out["Genus"] = df_out[col_name].apply(lambda x: str(x).split()[0] if str(x) else "Unknown")

    tox_col = None
    for candidate in ["ToxicityLevel", "toxicological_notes", "iucn_conservation_status"]:
        if candidate in df_out.columns:
            tox_col = candidate
            break
    if tox_col:
        toxicity_map = {"None": 0, "Low": 1, "Moderate": 2, "High": 3, "Extreme": 4}
        df_out["Toxicity_Ordinal"] = df_out[tox_col].map(toxicity_map).fillna(1).astype(int)

    return df_out


def compute_soil_ratios(reading: Dict[str, float]) -> Dict[str, float]:
    """Calculate key agronomic nutrient ratios and pH divergence."""
    n = reading.get("N", 0.0)
    p = reading.get("P", 0.0)
    k = reading.get("K", 0.0)
    ph = reading.get("pH", 7.0)

    return {
        "np_ratio": round(n / (p + 1e-5), 2),
        "nk_ratio": round(n / (k + 1e-5), 2),
        "pk_ratio": round(p / (k + 1e-5), 2),
        "ph_divergence": round(abs(ph - 7.0), 2),
        "npk_sum": round(n + p + k, 2),
    }
