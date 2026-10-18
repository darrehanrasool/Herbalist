"""Model validation loop and metric extraction."""
from __future__ import annotations

from typing import Dict, Any
import numpy as np
from sklearn.metrics import accuracy_score, top_k_accuracy_score, f1_score


def validate_model(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    top_k: int = 5
) -> Dict[str, float]:
    """Calculate validation metrics given true labels and predicted probabilities."""
    y_pred = np.argmax(y_pred_proba, axis=-1)
    acc = float(accuracy_score(y_true, y_pred))

    num_classes = y_pred_proba.shape[-1]
    top5_acc = acc
    if num_classes >= top_k:
        try:
            top5_acc = float(top_k_accuracy_score(y_true, y_pred_proba, k=top_k, labels=list(range(num_classes))))
        except Exception:
            pass

    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))

    return {
        "accuracy": round(acc, 4),
        "top5_accuracy": round(top5_acc, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
    }
