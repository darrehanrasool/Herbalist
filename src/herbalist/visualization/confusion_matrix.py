"""Confusion matrix heatmap visualization."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: Optional[List[str]] = None,
    output_path: Optional[Path] = None,
    max_classes: int = 25
) -> Path:
    """Generate normalized confusion matrix heatmap for top classes."""
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape[0] > max_classes:
        cm = cm[:max_classes, :max_classes]
        if class_names:
            class_names = class_names[:max_classes]

    # Normalize by row sums
    cm_norm = cm.astype("float") / (cm.sum(axis=1)[:, np.newaxis] + 1e-10)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm_norm, interpolation="nearest", cmap="viridis")
    fig.colorbar(im, ax=ax)

    if class_names:
        ax.set_xticks(range(len(class_names)))
        ax.set_yticks(range(len(class_names)))
        ax.set_xticklabels(class_names, rotation=45, ha="right", fontsize=8)
        ax.set_yticklabels(class_names, fontsize=8)

    ax.set_title(f"Normalized Confusion Matrix (Top {min(len(cm), max_classes)} Taxa)")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Botanical Label")

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("confusion_matrix.png")
