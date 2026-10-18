"""Decision threshold tuning for high-stakes botanical and toxicity predictions."""
from __future__ import annotations

from typing import Tuple
import numpy as np
from sklearn.metrics import precision_recall_curve, f1_score


def optimize_classification_threshold(
    y_true_binary: np.ndarray,
    y_pred_proba_pos: np.ndarray
) -> Tuple[float, float]:
    """Find the optimal probability threshold that maximizes F1 score for critical binary alerts."""
    precisions, recalls, thresholds = precision_recall_curve(y_true_binary, y_pred_proba_pos)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
    best_idx = np.argmax(f1_scores)

    best_threshold = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5
    best_f1 = float(f1_scores[best_idx])

    return round(best_threshold, 4), round(best_f1, 4)
