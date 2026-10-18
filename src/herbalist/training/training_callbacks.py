"""Standard training callbacks bundle for Keras models."""
from __future__ import annotations

from pathlib import Path
from typing import List
import tensorflow as tf
from tensorflow.keras.callbacks import CSVLogger, Callback

from .early_stopping import get_early_stopping
from .scheduler import get_lr_scheduler
from .checkpoint_manager import CheckpointManager
from src.herbalist.core.constants import ROOT_DIR


def get_training_callbacks(
    model_name: str = "herbalist_model",
    patience_early_stopping: int = 6,
    patience_lr: int = 3,
    log_dir: Path = ROOT_DIR / "logs" / "training"
) -> List[Callback]:
    """Assemble standard callbacks: Early Stopping, Checkpoint, LR decay, and CSV logging."""
    log_dir.mkdir(parents=True, exist_ok=True)
    csv_log_path = log_dir / f"{model_name}_history.csv"

    ckpt_mgr = CheckpointManager()
    checkpoint_cb = ckpt_mgr.get_checkpoint_callback(model_name=model_name)
    early_stop_cb = get_early_stopping(patience=patience_early_stopping)
    lr_sched_cb = get_lr_scheduler(patience=patience_lr)
    csv_logger = CSVLogger(str(csv_log_path), append=True)

    return [checkpoint_cb, early_stop_cb, lr_sched_cb, csv_logger]
