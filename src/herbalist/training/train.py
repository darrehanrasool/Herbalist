"""Functional training script and pipeline runner."""
from __future__ import annotations

import argparse
from pathlib import Path
from ..core.reproducibility import seed_everything
from ..core.config import get_training_config, get_models_config
from ..models.model_factory import create_model
from ..models.deep_learning import load_trained_vision_model
from .trainer import Trainer


def run_training(
    architecture: str = "Xception",
    epochs: int = 10,
    batch_size: int = 16,
    learning_rate: float = 0.0003,
    model_name: str = "herbalist_custom"
):
    """Orchestrate training of vision backbone."""
    seed_everything(42)
    print(f"🚀 Initializing training pipeline for architecture: {architecture} ({epochs} epochs)...")

    # Instantiate model
    model = create_model(architecture, input_shape=(180, 180, 3), num_classes=200)
    trainer = Trainer(
        model=model,
        model_name=model_name,
        learning_rate=learning_rate
    )
    print(f"✅ Model compiled successfully with AdamW optimizer (lr={learning_rate})")
    return trainer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Herbalist AI models")
    parser.add_argument("--arch", type=str, default="Xception", help="Backbone architecture")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs")
    parser.add_argument("--lr", type=float, default=0.0003, help="Learning rate")
    args = parser.parse_args()
    run_training(architecture=args.arch, epochs=args.epochs, learning_rate=args.lr)
