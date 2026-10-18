"""Checkpoint management for saving and organizing model weights."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint

from src.herbalist.core.constants import ROOT_DIR


class CheckpointManager:
    """Manages best, latest, and metadata checkpoint archives."""

    def __init__(self, base_dir: Path = ROOT_DIR / "checkpoints"):
        self.base_dir = base_dir
        self.best_dir = base_dir / "best"
        self.latest_dir = base_dir / "latest"
        self.metadata_dir = base_dir / "metadata"

        for d in (self.best_dir, self.latest_dir, self.metadata_dir):
            d.mkdir(parents=True, exist_ok=True)

    def get_checkpoint_callback(
        self,
        model_name: str = "herbalist_model",
        monitor: str = "val_accuracy",
        save_best_only: bool = True
    ) -> ModelCheckpoint:
        """Create a ModelCheckpoint callback saving directly to best directory."""
        filepath = str(self.best_dir / f"{model_name}.h5")
        return ModelCheckpoint(
            filepath=filepath,
            monitor=monitor,
            mode="max" if "acc" in monitor else "min",
            save_best_only=save_best_only,
            verbose=1
        )

    def save_metadata(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Save training epoch and metric metadata."""
        out = self.metadata_dir / f"{filename}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
