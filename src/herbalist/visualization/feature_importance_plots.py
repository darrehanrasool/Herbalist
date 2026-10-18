"""Feature importance bar chart plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_feature_importance(
    importances: Dict[str, float],
    output_path: Optional[Path] = None,
    title: str = "Feature Importance Analysis"
) -> Path:
    """Plot horizontal bar chart ranking feature importance scores."""
    features = list(importances.keys())[::-1]
    scores = list(importances.values())[::-1]

    fig, ax = plt.subplots(figsize=(8, max(4, len(features) * 0.45)))
    ax.barh(features, scores, color="#1fb890", edgecolor="#101826")
    ax.set_xlabel("Normalized Relative Importance")
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.5, axis="x")

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("feature_importance.png")
