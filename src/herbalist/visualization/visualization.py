"""Master visualization coordinator for automated dashboard and report plotting."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
from .training_curves import plot_training_curves
from .confusion_matrix import plot_confusion_matrix
from .feature_importance_plots import plot_feature_importance
from .correlation_heatmap import plot_correlation_heatmap
from ..core.constants import ROOT_DIR


def generate_all_visualizations(
    output_dir: Path = ROOT_DIR / "visualizations",
    history: Optional[Dict[str, Any]] = None,
    catalog_df: Optional[pd.DataFrame] = None
) -> Dict[str, Path]:
    """Generate and save comprehensive research figures across all modalities."""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = {}

    if history:
        p = plot_training_curves(history, output_path=output_dir / "training" / "summaries" / "loss_acc_curves.png")
        generated["training_curves"] = p

    if catalog_df is not None:
        p_corr = plot_correlation_heatmap(catalog_df, output_path=output_dir / "data_exploration" / "correlation_heatmap.png")
        generated["correlation_heatmap"] = p_corr

    return generated
