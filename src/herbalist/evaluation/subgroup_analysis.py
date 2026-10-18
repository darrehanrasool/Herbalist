"""Subgroup performance analysis across botanical taxonomy, rarity, and geography."""
from __future__ import annotations

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def analyze_subgroups(
    df_metadata: pd.DataFrame,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    subgroup_column: str
) -> Dict[str, Dict[str, float]]:
    """Calculate accuracy and F1 score per subgroup (e.g. ConservationStatus or ToxicityLevel)."""
    results = {}
    if subgroup_column not in df_metadata.columns:
        return results

    df = df_metadata.copy()
    df["y_true"] = y_true
    df["y_pred"] = y_pred

    for group_name, group_data in df.groupby(subgroup_column):
        if len(group_data) == 0:
            continue
        acc = float(accuracy_score(group_data["y_true"], group_data["y_pred"]))
        f1 = float(f1_score(group_data["y_true"], group_data["y_pred"], average="weighted", zero_division=0))
        results[str(group_name)] = {
            "samples": len(group_data),
            "accuracy": round(acc, 4),
            "weighted_f1": round(f1, 4),
        }

    return results
