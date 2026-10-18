"""Vision CNN backbones and transfer learning model utilities."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple, Optional
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import AUC

from src.herbalist.core.constants import ROOT_DIR, DEFAULT_IMAGE_SIZE


def build_vision_backbone(
    architecture: str = "Xception",
    input_shape: Tuple[int, int, int] = (180, 180, 3),
    num_classes: int = 200,
    freeze_backbone: bool = True,
    dropout_rate: float = 0.2
) -> models.Model:
    """Build a transfer learning classifier on top of a standard vision backbone."""
    if architecture.lower() == "xception":
        from tensorflow.keras.applications import Xception
        base = Xception(weights="imagenet", include_top=False, input_shape=input_shape)
    elif architecture.lower() == "mobilenetv3":
        from tensorflow.keras.applications import MobileNetV3Large
        base = MobileNetV3Large(weights="imagenet", include_top=False, input_shape=input_shape)
    elif architecture.lower() == "efficientnetb0":
        from tensorflow.keras.applications import EfficientNetB0
        base = EfficientNetB0(weights="imagenet", include_top=False, input_shape=input_shape)
    elif architecture.lower() == "resnet50v2":
        from tensorflow.keras.applications import ResNet50V2
        base = ResNet50V2(weights="imagenet", include_top=False, input_shape=input_shape)
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")

    base.trainable = not freeze_backbone

    inputs = layers.Input(shape=input_shape, name="image_input")
    x = base(inputs, training=not freeze_backbone)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    if dropout_rate > 0.0:
        x = layers.Dropout(dropout_rate, name="dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="species_softmax")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name=f"Herbalist_{architecture}")
    return model


def load_trained_vision_model(model_path: Optional[str] = None) -> Optional[models.Model]:
    """Load a pretrained Keras model (.h5) with custom objects."""
    candidates = [
        model_path,
        str(ROOT_DIR / "checkpoints" / "best" / "plant.h5"),
        str(ROOT_DIR / "models" / "deep_learning" / "plant.h5"),
        str(ROOT_DIR / "api" / "plant.h5"),
        str(ROOT_DIR / "plant.h5"),
    ]
    target_path = next((c for c in candidates if c and os.path.exists(c)), None)
    if not target_path:
        return None

    try:
        custom_objects = {"auc_roc": AUC, "AUC": AUC}
        model = load_model(target_path, custom_objects=custom_objects)
        return model
    except Exception as e:
        print(f"Warning: Could not load model from {target_path}: {e}")
        return None
