"""Model comparison grouped bar chart plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_model_comparison(
    comparison_df: pd.DataFrame,
    output_path: Optional[Path] = None
) -> Path:
    """Plot benchmark metrics across candidate models in a grouped bar chart."""
    if comparison_df.empty or "model_name" not in comparison_df.columns:
        return Path("no_comparison.png")

    models = comparison_df["model_name"].tolist()
    metrics_to_plot = [c for c in ["top1_accuracy", "accuracy", "macro_f1", "top5_accuracy"] if c in comparison_df.columns]

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#1fb890", "#4cc3ff", "#f5c15c"]

    for i, metric in enumerate(metrics_to_plot[:3]):
        vals = comparison_df[metric].tolist()
        ax.bar(x + (i - 1) * width, vals, width, label=metric.replace("_", " ").title(), color=colors[i % len(colors)])

    ax.set_ylabel("Score (0.0 - 1.0)")
    ax.set_title("Architecture Benchmark Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=20, ha="right")
    ax.set_ylim([0.0, 1.1])
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("model_comparison.png")
