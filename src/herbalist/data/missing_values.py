"""Missing value handling and imputation strategies."""
from __future__ import annotations

from typing import Dict, Any
import pandas as pd


# Default baseline agronomic priors when field sensors fail
AGRONOMIC_DEFAULTS = {
    "pH": 6.5,
    "N": 40.0,
    "P": 20.0,
    "K": 30.0,
    "moisture": 35.0,
    "temperature": 22.0,
    "ec": 1.0,
}


def impute_soil_readings(reading: Dict[str, Any]) -> Dict[str, float]:
    """Impute missing soil readings with agronomic priors."""
    clean_reading = {}
    for param, default_val in AGRONOMIC_DEFAULTS.items():
        val = reading.get(param)
        if val is None or val == "":
            clean_reading[param] = default_val
        else:
            try:
                clean_reading[param] = float(val)
            except (ValueError, TypeError):
                clean_reading[param] = default_val
    return clean_reading


def impute_catalog_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing text and categorical metadata in plant catalogs."""
    df_clean = df.copy()
    defaults = {
        "CommonUses": "Traditional medicinal usage",
        "ActiveCompounds": "Phytochemicals not cataloged",
        "ToxicityLevel": "Low",
        "ConservationStatus": "Not Evaluated",
        "GeographicalDistribution": "Global",
        "GrowthHabit": "Herb",
        "PartsUsed": "Leaves",
        "PreparationMethods": "Decoction",
    }
    for col, val in defaults.items():
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(val)
    return df_clean
