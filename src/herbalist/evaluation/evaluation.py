"""Master evaluation pipeline runner."""
from __future__ import annotations

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from .metrics import compute_classification_metrics
from .statistical_analysis import bootstrap_confidence_interval


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    metadata_df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """Execute complete evaluation suite including metrics, confidence intervals, and summary."""
    metrics = compute_classification_metrics(y_true, y_pred_proba)
    y_pred = np.argmax(y_pred_proba, axis=-1)

    mean_acc, lower_ci, upper_ci = bootstrap_confidence_interval(y_true, y_pred)
    metrics["accuracy_95_ci"] = [lower_ci, upper_ci]

    return {
        "summary": metrics,
        "sample_count": len(y_true),
        "num_classes": y_pred_proba.shape[-1],
    }
