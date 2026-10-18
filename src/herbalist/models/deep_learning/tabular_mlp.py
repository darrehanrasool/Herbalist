"""Multi-Layer Perceptron (MLP) for tabular and sensor data classification."""
from __future__ import annotations

from typing import List
import tensorflow as tf
from tensorflow.keras import layers, models


def build_tabular_mlp(
    input_dim: int = 7,
    hidden_dims: List[int] = [128, 64, 32],
    num_classes: int = 200,
    dropout_rate: float = 0.2,
    activation: str = "relu"
) -> models.Model:
    """Construct a feed-forward MLP with batch normalization and dropout."""
    inputs = layers.Input(shape=(input_dim,), name="tabular_input")
    x = inputs

    for idx, dim in enumerate(hidden_dims):
        x = layers.Dense(dim, activation=activation, name=f"dense_{idx + 1}")(x)
        x = layers.BatchNormalization(name=f"bn_{idx + 1}")(x)
        x = layers.Dropout(dropout_rate, name=f"dropout_{idx + 1}")(x)

    outputs = layers.Dense(num_classes, activation="softmax", name="classification_head")(x)
    model = models.Model(inputs=inputs, outputs=outputs, name="TabularMLP")
    return model
