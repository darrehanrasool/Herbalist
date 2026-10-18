"""Object-oriented Trainer for neural network training and validation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Optional
import tensorflow as tf
from tensorflow.keras.metrics import AUC, TopKCategoricalAccuracy

from .optimizer import get_optimizer
from .training_callbacks import get_training_callbacks
from ..core.constants import ROOT_DIR


class Trainer:
    """Encapsulates compile, fit, evaluate, and logging steps."""

    def __init__(
        self,
        model: tf.keras.Model,
        model_name: str = "herbalist_model",
        learning_rate: float = 0.0003,
        optimizer_name: str = "AdamW",
        loss: str = "categorical_crossentropy"
    ):
        self.model = model
        self.model_name = model_name
        self.learning_rate = learning_rate
        self.optimizer_name = optimizer_name
        self.loss = loss

        self._compile_model()

    def _compile_model(self):
        opt = get_optimizer(self.optimizer_name, learning_rate=self.learning_rate)
        metrics = [
            "accuracy",
            TopKCategoricalAccuracy(k=5, name="top5_accuracy"),
            AUC(name="auc_roc")
        ]
        self.model.compile(optimizer=opt, loss=self.loss, metrics=metrics)

    def train(
        self,
        train_data: Any,
        val_data: Optional[Any] = None,
        epochs: int = 25,
        callbacks: Optional[list] = None
    ) -> tf.keras.callbacks.History:
        """Run training with callbacks and history logging."""
        if callbacks is None:
            callbacks = get_training_callbacks(model_name=self.model_name)

        history = self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks
        )

        # Save history json
        history_out = ROOT_DIR / "experiments" / "results" / f"{self.model_name}_history.json"
        history_out.parent.mkdir(parents=True, exist_ok=True)
        try:
            cleaned_history = {k: [float(v) for v in vals] for k, vals in history.history.items()}
            with open(history_out, "w", encoding="utf-8") as f:
                json.dump(cleaned_history, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to serialize history: {e}")

        return history
