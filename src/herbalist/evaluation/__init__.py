"""Evaluation metrics, subgroup disparity analysis, and statistical significance testing."""
from .evaluation import evaluate_predictions
from .metrics import compute_classification_metrics
from .statistical_analysis import bootstrap_confidence_interval, mcnemar_test
from .subgroup_analysis import analyze_subgroups
from .model_comparison import compare_models

__all__ = [
    "evaluate_predictions",
    "compute_classification_metrics",
    "bootstrap_confidence_interval",
    "mcnemar_test",
    "analyze_subgroups",
    "compare_models",
]
