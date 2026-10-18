"""Learning rate schedulers and callbacks."""
from __future__ import annotations
import tensorflow as tf
from tensorflow.keras.callbacks import ReduceLROnPlateau, LearningRateScheduler


def get_lr_scheduler(
    scheduler_name: str = "ReduceLROnPlateau",
    monitor: str = "val_loss",
    factor: float = 0.5,
    patience: int = 3,
    min_lr: float = 1e-6
) -> tf.keras.callbacks.Callback:
    """Build dynamic learning rate reduction callback."""
    if scheduler_name.lower() == "reducelronplateau":
        return ReduceLROnPlateau(
            monitor=monitor,
            factor=factor,
            patience=patience,
            min_lr=min_lr,
            verbose=1
        )
    elif scheduler_name.lower() == "exponential":
        def exp_decay(epoch, lr):
            return lr * 0.95
        return LearningRateScheduler(exp_decay, verbose=0)
    else:
        return ReduceLROnPlateau(monitor=monitor, factor=factor, patience=patience, min_lr=min_lr)
