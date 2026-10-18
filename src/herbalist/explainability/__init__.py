"""Model interpretability, permutation importance, Grad-CAM, and SHAP placeholders."""
from .feature_importance import calculate_permutation_importance
from .shap_analysis import compute_tabular_shap_summary
from .explanation_reports import generate_explanation_report

__all__ = [
    "calculate_permutation_importance",
    "compute_tabular_shap_summary",
    "generate_explanation_report",
]
