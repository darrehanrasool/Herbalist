"""Training loss and accuracy convergence curves."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_training_curves(
    history: Dict[str, List[float]],
    output_path: Optional[Path] = None,
    title_suffix: str = "Xception Baseline"
) -> Path:
    """Plot training and validation accuracy/loss across epochs."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    epochs = range(1, len(history.get("accuracy", history.get("acc", []))) + 1)

    # Accuracy subplot
    train_acc = history.get("accuracy", history.get("acc", []))
    val_acc = history.get("val_accuracy", history.get("val_acc", []))
    if train_acc:
        ax1.plot(epochs, train_acc, "o-", label="Training Accuracy", color="#1fb890")
    if val_acc:
        ax1.plot(epochs, val_acc, "s--", label="Validation Accuracy", color="#4cc3ff")
    ax1.set_title(f"Accuracy vs Epochs ({title_suffix})")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.set_ylim([0.0, 1.05])
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # Loss subplot
    train_loss = history.get("loss", [])
    val_loss = history.get("val_loss", [])
    if train_loss:
        ax2.plot(epochs, train_loss, "o-", label="Training Loss", color="#ff6b6b")
    if val_loss:
        ax2.plot(epochs, val_loss, "s--", label="Validation Loss", color="#f5c15c")
    ax2.set_title(f"Loss vs Epochs ({title_suffix})")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Categorical Crossentropy")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path or Path("training_curves.png")
