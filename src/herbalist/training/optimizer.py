"""Optimizer construction supporting Adam, AdamW, and SGD."""
from __future__ import annotations
import tensorflow as tf


def get_optimizer(
    optimizer_name: str = "AdamW",
    learning_rate: float = 0.0003,
    weight_decay: float = 0.0001
) -> tf.keras.optimizers.Optimizer:
    """Build a compiled Keras optimizer."""
    name = optimizer_name.lower()
    if name == "adamw":
        try:
            return tf.keras.optimizers.AdamW(learning_rate=learning_rate, weight_decay=weight_decay)
        except AttributeError:
            return tf.keras.optimizers.Adam(learning_rate=learning_rate)
    elif name == "adam":
        return tf.keras.optimizers.Adam(learning_rate=learning_rate)
    elif name == "sgd":
        return tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9, nesterov=True)
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_name}")
