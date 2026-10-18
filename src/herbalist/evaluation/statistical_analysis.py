"""Statistical significance testing and bootstrap confidence intervals."""
from __future__ import annotations

from typing import Tuple, Dict, Any
import numpy as np
from sklearn.metrics import accuracy_score


def bootstrap_confidence_interval(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42
) -> Tuple[float, float, float]:
    """Compute empirical bootstrap confidence interval for accuracy."""
    rng = np.random.RandomState(seed)
    bootstrapped_scores = []
    n = len(y_true)

    for _ in range(n_bootstraps):
        indices = rng.randint(0, n, n)
        if len(np.unique(y_true[indices])) < 2:
            continue
        score = accuracy_score(y_true[indices], y_pred[indices])
        bootstrapped_scores.append(score)

    alpha = (1.0 - confidence_level) / 2.0
    lower_bound = float(np.percentile(bootstrapped_scores, alpha * 100))
    upper_bound = float(np.percentile(bootstrapped_scores, (1.0 - alpha) * 100))
    mean_score = float(np.mean(bootstrapped_scores))

    return round(mean_score, 4), round(lower_bound, 4), round(upper_bound, 4)


def mcnemar_test(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray
) -> Dict[str, Any]:
    """Perform McNemar contingency test comparing classifier A and B."""
    correct_a = (y_pred_a == y_true)
    correct_b = (y_pred_b == y_true)

    b = np.sum(correct_a & ~correct_b)  # A right, B wrong
    c = np.sum(~correct_a & correct_b)  # A wrong, B right

    # Continuity corrected McNemar chi-square
    statistic = float((abs(b - c) - 1.0) ** 2 / (b + c + 1e-10))
    p_value = float(np.exp(-statistic / 2.0))  # 1-DOF chi2 approx

    return {
        "contingency_table": {"b_only_A": int(b), "c_only_B": int(c)},
        "chi2_statistic": round(statistic, 4),
        "approx_p_value": round(p_value, 5),
        "statistically_significant": p_value < 0.05,
    }
