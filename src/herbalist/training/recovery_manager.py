"""Training recovery manager for resuming interrupted training jobs."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple
import tensorflow as tf
from tensorflow.keras.models import load_model

from src.herbalist.core.constants import ROOT_DIR


class RecoveryManager:
    """Detects and loads the latest saved checkpoint to resume training."""

    def __init__(self, checkpoints_dir: Path = ROOT_DIR / "checkpoints"):
        self.checkpoints_dir = checkpoints_dir
        self.best_dir = checkpoints_dir / "best"
        self.latest_dir = checkpoints_dir / "latest"

    def find_latest_checkpoint(self, check_fallback: bool = True) -> Optional[Path]:
        """Search checkpoints directories for the newest .h5 or .keras model file."""
        candidates = list(self.best_dir.glob("*.h5")) + list(self.latest_dir.glob("*.h5"))
        if not candidates and check_fallback:
            # Check models/deep_learning
            dl_dir = ROOT_DIR / "models" / "deep_learning"
            if dl_dir.exists():
                candidates = list(dl_dir.glob("*.h5"))
        if not candidates:
            return None
        # Sort by modification time descending
        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return candidates[0]

    def resume_model(self) -> Tuple[Optional[tf.keras.Model], Optional[Path]]:
        """Load latest checkpoint if present."""
        latest = self.find_latest_checkpoint()
        if not latest or not latest.exists():
            return None, None
        try:
            from tensorflow.keras.metrics import AUC
            model = load_model(str(latest), custom_objects={"auc_roc": AUC, "AUC": AUC})
            return model, latest
        except Exception as e:
            print(f"Error resuming from {latest}: {e}")
            return None, None
