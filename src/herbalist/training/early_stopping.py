"""Early stopping callback wrapper."""
from __future__ import annotations
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping


def get_early_stopping(
    monitor: str = "val_loss",
    patience: int = 6,
    min_delta: float = 0.001,
    restore_best_weights: bool = True
) -> EarlyStopping:
    """Build early stopping callback to prevent overfitting."""
    return EarlyStopping(
        monitor=monitor,
        patience=patience,
        min_delta=min_delta,
        restore_best_weights=restore_best_weights,
        verbose=1
    )
