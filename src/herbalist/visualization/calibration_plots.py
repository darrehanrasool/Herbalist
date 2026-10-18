"""Calibration curve and reliability diagram plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve


def plot_calibration_curve(
    y_true_binary: np.ndarray,
    y_pred_proba_pos: np.ndarray,
    n_bins: int = 10,
    output_path: Optional[Path] = None
) -> Path:
    """Plot reliability diagram comparing confidence against empirical accuracy."""
    prob_true, prob_pred = calibration_curve(y_true_binary, y_pred_proba_pos, n_bins=n_bins)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(prob_pred, prob_true, "s-", color="#1fb890", label="Model Calibration")
    ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    ax.set_xlabel("Mean Predicted Probability")
    ax.set_ylabel("Fraction of Positives")
    ax.set_title("Probability Calibration (Reliability Diagram)")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("calibration_plot.png")
