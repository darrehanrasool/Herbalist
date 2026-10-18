"""Model benchmarking and comparison leaderboard generator."""
from __future__ import annotations

from typing import Dict, Any, List
import pandas as pd


def compare_models(model_results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """Generate a clean sorted comparison leaderboard DataFrame."""
    records = []
    for model_name, metrics in model_results.items():
        row = {"model_name": model_name, **metrics}
        records.append(row)

    df = pd.DataFrame(records)
    if "top1_accuracy" in df.columns:
        df = df.sort_values(by="top1_accuracy", ascending=False)
    elif "accuracy" in df.columns:
        df = df.sort_values(by="accuracy", ascending=False)
    return df.reset_index(drop=True)
