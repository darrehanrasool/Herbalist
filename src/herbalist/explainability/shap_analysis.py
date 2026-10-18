"""SHAP (Shapley Additive exPlanations) analysis routines."""
from __future__ import annotations

from typing import Dict, List, Any
import numpy as np


def compute_tabular_shap_summary(
    model: Any,
    X_sample: np.ndarray,
    feature_names: List[str]
) -> Dict[str, float]:
    """Compute surrogate Shapley attribution values across features."""
    # Marginal perturbation baseline attribution
    base_preds = model.predict_proba(X_sample) if hasattr(model, "predict_proba") else model.predict(X_sample)
    attributions = {}

    for i, name in enumerate(feature_names):
        X_perturbed = X_sample.copy()
        np.random.shuffle(X_perturbed[:, i])
        perturbed_preds = model.predict_proba(X_perturbed) if hasattr(model, "predict_proba") else model.predict(X_perturbed)
        diff = np.mean(np.abs(base_preds - perturbed_preds))
        attributions[name] = float(diff)

    total = sum(attributions.values()) + 1e-10
    return {k: round(v / total, 4) for k, v in sorted(attributions.items(), key=lambda x: x[1], reverse=True)}
