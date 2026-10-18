"""Central factory for instantiating classical, deep, and ensemble architectures."""
from __future__ import annotations

from typing import Any, Dict
from .classical import (
    get_logistic_regression,
    get_random_forest,
    get_gradient_boosting,
    get_svm,
)
from .deep_learning import (
    build_tabular_mlp,
    build_vision_backbone,
    load_trained_vision_model,
)
from .ensemble import SoftVotingEnsemble


class ModelFactory:
    """Factory creating configured models by identifier."""

    @staticmethod
    def create(model_name: str, **kwargs) -> Any:
        name = model_name.lower()
        if name in ("logistic_regression", "lr"):
            return get_logistic_regression(**kwargs)
        elif name in ("random_forest", "rf"):
            return get_random_forest(**kwargs)
        elif name in ("gradient_boosting", "gbdt"):
            return get_gradient_boosting(**kwargs)
        elif name in ("svm", "svc"):
            return get_svm(**kwargs)
        elif name in ("tabular_mlp", "mlp"):
            return build_tabular_mlp(**kwargs)
        elif name in ("xception", "mobilenetv3", "efficientnetb0", "resnet50v2"):
            return build_vision_backbone(architecture=name, **kwargs)
        elif name == "voting_ensemble":
            return SoftVotingEnsemble(**kwargs)
        elif name in ("global_vision", "global_classifier", "btech_baseline"):
            from .architectures import GlobalVisionClassifier
            return GlobalVisionClassifier(**kwargs)
        elif name in ("kashmir_vision", "kashmir_classifier", "alpine_specialist"):
            from .architectures import KashmirVisionClassifier
            return KashmirVisionClassifier(**kwargs)
        elif name in ("agronomy_tabular", "soil_mlp"):
            from .architectures import AgronomyTabularMLP
            return AgronomyTabularMLP(**kwargs)
        elif name in ("hierarchical_fusion", "combined_ensemble", "multimodal_fusion"):
            from .architectures import HierarchicalFusionEnsemble
            return HierarchicalFusionEnsemble(**kwargs)
        else:
            raise ValueError(f"Unknown model architecture requested: {model_name}")


def create_model(model_name: str, **kwargs) -> Any:
    return ModelFactory.create(model_name, **kwargs)
