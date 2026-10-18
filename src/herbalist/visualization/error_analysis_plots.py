"""Error breakdown and misclassification distribution plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_error_breakdown(
    error_rates_per_class: Dict[str, float],
    output_path: Optional[Path] = None,
    top_n: int = 15
) -> Path:
    """Plot the taxa suffering the highest classification error rates."""
    sorted_items = sorted(error_rates_per_class.items(), key=lambda x: x[1], reverse=True)[:top_n]
    classes = [k for k, _ in sorted_items][::-1]
    rates = [v for _, v in sorted_items][::-1]

    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.4)))
    ax.barh(classes, rates, color="#ff6b6b", edgecolor="#101826")
    ax.set_xlabel("Error Rate (1 - Accuracy)")
    ax.set_title(f"Top {len(classes)} Challenging Botanical Taxa")
    ax.grid(True, linestyle="--", alpha=0.5, axis="x")

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("error_breakdown.png")
