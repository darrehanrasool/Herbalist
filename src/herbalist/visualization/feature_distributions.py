"""Feature distribution and agronomic range histogram plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, List
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_feature_distributions(
    df: pd.DataFrame,
    feature_cols: List[str],
    output_path: Optional[Path] = None
) -> Path:
    """Plot distribution histograms for continuous numerical agronomic features."""
    cols_to_plot = [c for c in feature_cols if c in df.columns]
    if not cols_to_plot:
        cols_to_plot = df.select_dtypes(include=["float64", "int64"]).columns[:6].tolist()

    n = len(cols_to_plot)
    if n == 0:
        return Path("no_features.png")

    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, col in zip(axes, cols_to_plot):
        data = df[col].dropna()
        ax.hist(data, bins=20, color="#1fb890", edgecolor="#101826", alpha=0.8)
        ax.set_title(col)
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("feature_distributions.png")
