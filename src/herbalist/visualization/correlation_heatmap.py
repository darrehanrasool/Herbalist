"""Correlation heatmap for continuous agronomic and chemical features."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_correlation_heatmap(
    df: pd.DataFrame,
    output_path: Optional[Path] = None
) -> Path:
    """Plot Pearson correlation matrix for numerical features."""
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty or len(num_df.columns) < 2:
        return Path("no_correlation.png")

    corr = num_df.corr().values
    cols = num_df.columns

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax)

    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(cols, fontsize=9)
    ax.set_title("Agronomic & Chemical Feature Correlation")

    # Annotate values
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", color="black" if abs(corr[i, j]) < 0.6 else "white", fontsize=8)

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("correlation_heatmap.png")
