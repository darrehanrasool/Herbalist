"""
Agronomic Tabular MLP (Model C: Soil Sensors, Elevation & Microclimate).
Maps physicochemical soil sensor readings and altitude to species habitat suitability and bioactive compound potential.
"""
from __future__ import annotations

import os
from typing import List, Optional, Tuple
import numpy as np

os.environ.setdefault("KERAS_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".keras"))
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.models import Sequential, load_model


class AgronomyTabularMLP:
    """
    Multilayer Perceptron mapping 7 Agronomic & Microclimatic features:
    [pH, N, P, K, moisture_pct, temp_c, elevation_masl]
    to species habitat suitability distribution or bioactive yield index.
    """

    FEATURE_NAMES = [
        "soil_ph",
        "nitrogen_mg_kg",
        "phosphorus_mg_kg",
        "potassium_mg_kg",
        "moisture_pct",
        "temperature_c",
        "elevation_masl",
    ]

    def __init__(
        self,
        input_dim: int = 7,
        output_dim: int = 200,
        hidden_units: Tuple[int, ...] = (128, 64, 32),
        dropout_rate: float = 0.2,
        weights_path: Optional[str] = None,
    ) -> None:
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_units = hidden_units
        self.dropout_rate = dropout_rate
        self.weights_path = weights_path
        self.model: Optional[tf.keras.Model] = None

        if weights_path and os.path.exists(weights_path):
            self.load(weights_path)
        else:
            self.build()

    def build(self) -> tf.keras.Model:
        layers = [Input(shape=(self.input_dim,))]
        for i, units in enumerate(self.hidden_units):
            layers.append(Dense(units, activation="relu", name=f"agronomy_dense_{i+1}"))
            layers.append(BatchNormalization())
            if self.dropout_rate > 0.0:
                layers.append(Dropout(self.dropout_rate))

        layers.append(Dense(self.output_dim, activation="softmax", name="agronomic_compatibility_probs"))
        self.model = Sequential(layers, name="Agronomy_SoilSuitabilityMLP")

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        return self.model

    def load(self, weights_path: str) -> None:
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weight file not found: {weights_path}")
        self.model = load_model(weights_path, compile=False)
        self.weights_path = weights_path

    def predict_suitability(self, sensor_features: np.ndarray) -> np.ndarray:
        """Evaluate agronomic compatibility for a given soil reading."""
        if self.model is None:
            raise RuntimeError("Model is not initialized.")
        return self.model.predict(sensor_features, verbose=0)
