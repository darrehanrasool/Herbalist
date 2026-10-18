"""Receiver Operating Characteristic (ROC) curve plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def plot_roc_curve(
    y_true_binary: np.ndarray,
    y_pred_proba_pos: np.ndarray,
    class_label: str = "Target Taxa",
    output_path: Optional[Path] = None
) -> Path:
    """Plot ROC curve and calculate area under the curve."""
    fpr, tpr, _ = roc_curve(y_true_binary, y_pred_proba_pos)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color="#1fb890", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], color="#8aa0b8", lw=1.5, linestyle="--")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve - {class_label}")
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("roc_curve.png")
