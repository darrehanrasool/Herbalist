"""Script to resume training from the latest checkpoint."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.herbalist.training.recovery_manager import RecoveryManager
from src.herbalist.training.trainer import Trainer


def resume_training(epochs: int = 5):
    print("🔄 Checking for existing checkpoints to resume training...")
    recovery_mgr = RecoveryManager()
    model, checkpoint_path = recovery_mgr.resume_model()

    if model is None:
        print("❌ No existing checkpoint found to resume from.")
        return

    print(f"✅ Loaded checkpoint from: {checkpoint_path.relative_to(ROOT)}")
    trainer = Trainer(
        model=model,
        model_name="herbalist_resumed",
        learning_rate=0.0001
    )
    print(f"🚀 Ready to resume training for {epochs} additional epochs.")
    return trainer


if __name__ == "__main__":
    resume_training()
