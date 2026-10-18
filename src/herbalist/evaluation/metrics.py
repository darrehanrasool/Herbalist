"""Multi-class evaluation metrics."""
from __future__ import annotations

from typing import Dict, Any
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    top_k_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    cohen_kappa_score,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    top_k: int = 5
) -> Dict[str, float]:
    """Compute standard multi-class botanical classification metrics."""
    y_pred = np.argmax(y_pred_proba, axis=-1)
    acc = float(accuracy_score(y_true, y_pred))

    num_classes = y_pred_proba.shape[-1]
    top_k_acc = acc
    if num_classes >= top_k:
        try:
            top_k_acc = float(top_k_accuracy_score(y_true, y_pred_proba, k=top_k, labels=list(range(num_classes))))
        except Exception:
            pass

    macro_p = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    macro_r = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    kappa = float(cohen_kappa_score(y_true, y_pred))

    return {
        "top1_accuracy": round(acc, 4),
        f"top{top_k}_accuracy": round(top_k_acc, 4),
        "macro_precision": round(macro_p, 4),
        "macro_recall": round(macro_r, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "cohens_kappa": round(kappa, 4),
    }
