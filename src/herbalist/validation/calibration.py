"""Probability calibration and Expected Calibration Error (ECE) calculations."""
from __future__ import annotations

import numpy as np


class TemperatureScaling:
    """Scales logits by a learned or fixed temperature parameter T > 0."""

    def __init__(self, temperature: float = 1.0):
        self.temperature = max(1e-4, temperature)

    def calibrate(self, logits: np.ndarray) -> np.ndarray:
        """Apply temperature scaling to raw logits before softmax."""
        scaled_logits = logits / self.temperature
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def calculate_expected_calibration_error(
    y_true: np.ndarray,
    y_pred_proba: np.ndarray,
    n_bins: int = 10
) -> float:
    """Calculate the Expected Calibration Error (ECE) across confidence bins."""
    confidences = np.max(y_pred_proba, axis=-1)
    predictions = np.argmax(y_pred_proba, axis=-1)
    accuracies = predictions == y_true

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        bin_lower, bin_upper = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return round(float(ece), 4)
