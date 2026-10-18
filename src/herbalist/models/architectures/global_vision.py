"""
Global Vision Classifier (Model A: Baseline 200 Species).
Decoupled Xception architecture with Global Average Pooling and Softmax classification.
"""
from __future__ import annotations

import os
from typing import Optional, Tuple
import numpy as np

os.environ.setdefault("KERAS_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".keras"))
import tensorflow as tf
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential, load_model


class GlobalVisionClassifier:
    """
    200-class Botanical Classifier using Xception backbone.
    Matches the historical B.Tech Capstone architecture (21,271,280 parameters).
    """

    def __init__(
        self,
        num_classes: int = 200,
        input_shape: Tuple[int, int, int] = (180, 180, 3),
        weights_path: Optional[str] = None,
        dropout_rate: float = 0.0,
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

    def build(self) -> tf.keras.Model:
        """Construct model with frozen backbone (offline safe)."""
        try:
            base_model = Xception(
                weights="imagenet",
                include_top=False,
                input_shape=self.input_shape,
            )
        except Exception:
            base_model = Xception(
                weights=None,
                include_top=False,
                input_shape=self.input_shape,
            )
        base_model.trainable = False

        layers = [base_model, GlobalAveragePooling2D()]
        if self.dropout_rate > 0.0:
            layers.append(Dropout(self.dropout_rate))
        layers.append(Dense(self.num_classes, activation="softmax", name="global_species_probs"))

        self.model = Sequential(layers, name="GlobalVision_Xception200")
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        return self.model

    def load(self, weights_path: str) -> None:
        """Load pretrained model weights."""
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weight file not found: {weights_path}")
        self.model = load_model(weights_path, compile=False)
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        self.weights_path = weights_path

    def extract_features(self, image_batch: np.ndarray) -> np.ndarray:
        """Extract 2048-dimensional visual feature vectors prior to classification."""
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        feature_extractor = tf.keras.Model(
            inputs=self.model.inputs,
            outputs=self.model.layers[-2].output if isinstance(self.model.layers[-2], GlobalAveragePooling2D) else self.model.layers[-3].output,
        )
        return feature_extractor.predict(image_batch, verbose=0)

    def predict_proba(self, image_batch: np.ndarray) -> np.ndarray:
        """Return softmax probability distribution over 200 species."""
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        return self.model.predict(image_batch, verbose=0)
