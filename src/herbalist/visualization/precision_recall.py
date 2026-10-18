"""Precision-Recall curve plotting for imbalanced botanical classes."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score


def plot_precision_recall_curve(
    y_true_binary: np.ndarray,
    y_pred_proba_pos: np.ndarray,
    class_label: str = "Endangered Taxa",
    output_path: Optional[Path] = None
) -> Path:
    """Plot Precision-Recall curve with average precision."""
    precision, recall, _ = precision_recall_curve(y_true_binary, y_pred_proba_pos)
    ap = average_precision_score(y_true_binary, y_pred_proba_pos)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(recall, precision, color="#4cc3ff", lw=2, label=f"PR curve (AP = {ap:.3f})")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(f"Precision-Recall Curve - {class_label}")
    ax.legend(loc="lower left")
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("precision_recall.png")
