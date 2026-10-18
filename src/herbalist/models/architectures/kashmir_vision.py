"""
Kashmir Vision Specialist (Model B: High-Altitude Himalayan Taxa).
Tailored for fine-grained differentiation of endemic and endangered Kashmir medicinal plants.
"""
from __future__ import annotations

import os
from typing import Optional, Tuple
import numpy as np

os.environ["KERAS_HOME"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".keras"))
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential, load_model


class KashmirVisionClassifier:
    """
    Specialized classifier for 15 High-Altitude Kashmir Himalayan Medicinal Taxa.
    Supports mobile edge inference and fine-tuning on field collections.
    """

    KASHMIR_SPECIES = [
        "Aconitum heterophyllum",
        "Gentiana kurroo",
        "Picrorhiza kurroa",
        "Saussurea costus",
        "Podophyllum hexandrum",
        "Arnebia benthamii",
        "Inula racemosa",
        "Rheum webbianum",
        "Atropa belladonna",
        "Hyoscyamus niger",
        "Lavandula angustifolia",
        "Valeriana jatamansi",
        "Jurinea dolomiaea",
        "Berberis lycium",
        "Swertia chirayita",
    ]

    def __init__(
        self,
        num_classes: int = 15,
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        weights_path: Optional[str] = None,
        dropout_rate: float = 0.3,
    ) -> None:
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.weights_path = weights_path
        self.dropout_rate = dropout_rate
        self.model: Optional[tf.keras.Model] = None

        if weights_path and os.path.exists(weights_path):
            self.load(weights_path)
        else:
            self.build()

    def build(self, pretrained: bool = False) -> tf.keras.Model:
        """Construct MobileNetV3Large lightweight backbone with safe offline fallback."""
        try:
            weights_arg = "imagenet" if pretrained else None
            backbone = MobileNetV3Large(
                weights=weights_arg,
                include_top=False,
                input_shape=self.input_shape,
                pooling="avg",
            )
        except Exception:
            # Safe fallback if network is unreachable or offline
            backbone = MobileNetV3Large(
                weights=None,
                include_top=False,
                input_shape=self.input_shape,
                pooling="avg",
            )
        backbone.trainable = False

        self.model = Sequential([
            backbone,
            BatchNormalization(),
            Dropout(self.dropout_rate),
            Dense(128, activation="relu", name="kashmir_embedding"),
            Dropout(self.dropout_rate / 2),
            Dense(self.num_classes, activation="softmax", name="kashmir_species_probs"),
        ], name="KashmirVision_AlpineSpecialist")

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
            loss="categorical_crossentropy",
            metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_accuracy")],
        )
        return self.model

    def unfreeze_top_layers(self, num_blocks: int = 4) -> None:
        """Unfreeze top convolutional blocks for domain adaptation on Kashmir flora."""
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        backbone = self.model.layers[0]
        backbone.trainable = True
        for layer in backbone.layers[:-num_blocks]:
            layer.trainable = False
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

    def load(self, weights_path: str) -> None:
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weight file not found: {weights_path}")
        self.model = load_model(weights_path, compile=False)
        self.weights_path = weights_path

    def predict_proba(self, image_batch: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        return self.model.predict(image_batch, verbose=0)
