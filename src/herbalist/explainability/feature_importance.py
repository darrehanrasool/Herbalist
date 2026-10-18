"""Permutation feature importance and Gini importance calculator."""
from __future__ import annotations

from typing import Dict, List, Any
import numpy as np
from sklearn.inspection import permutation_importance


def calculate_permutation_importance(
    model: Any,
    X_val: np.ndarray,
    y_val: np.ndarray,
    feature_names: List[str],
    n_repeats: int = 10,
    seed: int = 42
) -> Dict[str, float]:
    """Calculate normalized permutation feature importance scores."""
    result = permutation_importance(
        model, X_val, y_val, n_repeats=n_repeats, random_state=seed, n_jobs=-1
    )
    importances = result.importances_mean
    # Normalize to sum = 1.0
    total = np.sum(np.maximum(0, importances)) + 1e-10
    normalized = np.maximum(0, importances) / total

    return {
        name: round(float(score), 4)
        for name, score in sorted(zip(feature_names, normalized), key=lambda x: x[1], reverse=True)
    }
