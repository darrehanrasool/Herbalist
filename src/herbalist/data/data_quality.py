"""Data quality assessment, completeness metrics, and imbalance reporting."""
from __future__ import annotations

from typing import Dict, Any
import pandas as pd


def compute_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze DataFrame completeness, schema integrity, and distribution statistics."""
    total_rows = len(df)
    if total_rows == 0:
        return {"total_rows": 0, "status": "empty"}

    missing_counts = df.isnull().sum().to_dict()
    missing_pct = {k: round((v / total_rows) * 100, 2) for k, v in missing_counts.items()}
    completeness = round((1 - (df.isnull().sum().sum() / (total_rows * len(df.columns)))) * 100, 2)

    unique_counts = df.nunique().to_dict()

    return {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "overall_completeness_pct": completeness,
        "missing_counts": missing_counts,
        "missing_percentages": missing_pct,
        "unique_counts": unique_counts,
    }
