"""
Modular Model Architectures for Herbalist AI.

Includes:
- GlobalVisionClassifier: 200-class Xception baseline for worldwide/Indian taxa.
- KashmirVisionClassifier: Fine-tuned specialist model for Kashmir high-altitude endemics.
- AgronomyTabularMLP: Soil parameters & altitude predictor.
- HierarchicalFusionEnsemble: Combined multi-modal decision network.
"""

from .global_vision import GlobalVisionClassifier
from .kashmir_vision import KashmirVisionClassifier
from .agronomy_tabular import AgronomyTabularMLP
from .hierarchical_fusion import HierarchicalFusionEnsemble

__all__ = [
    "GlobalVisionClassifier",
    "KashmirVisionClassifier",
    "AgronomyTabularMLP",
    "HierarchicalFusionEnsemble",
]
