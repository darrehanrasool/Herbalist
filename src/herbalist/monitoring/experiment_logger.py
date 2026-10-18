"""Experiment logger updating experiment_registry.csv."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
from ..core.constants import ROOT_DIR


class ExperimentLogger:
    """Logs experiment parameters, hyperparameters, and evaluation metrics."""

    def __init__(self, registry_file: Path = ROOT_DIR / "experiments" / "experiment_registry.csv"):
        self.registry_file = registry_file
        self.configs_dir = ROOT_DIR / "experiments" / "configs"
        self.results_dir = ROOT_DIR / "experiments" / "results"

        self.configs_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def log_run(
        self,
        experiment_id: str,
        experiment_name: str,
        metrics: Dict[str, Any],
        params: Dict[str, Any]
    ) -> None:
        """Record experiment run to registry CSV and JSON manifests."""
        # Save JSON config & results
        with open(self.configs_dir / f"{experiment_id}_params.json", "w") as f:
            json.dump(params, f, indent=2)
        with open(self.results_dir / f"{experiment_id}_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        # Append to registry if file exists
        if self.registry_file.exists():
            row = [
                experiment_id,
                experiment_name,
                params.get("model_type", "cnn"),
                params.get("backbone", "Xception"),
                params.get("input_resolution", "180x180x3"),
                params.get("batch_size", 32),
                params.get("learning_rate", 0.0003),
                params.get("epochs", 10),
                metrics.get("train_accuracy", 0.0),
                metrics.get("val_accuracy", metrics.get("accuracy", 0.0)),
                metrics.get("val_loss", 0.0),
                metrics.get("top5_accuracy", 0.0),
                metrics.get("macro_f1", 0.0),
                params.get("hardware", "Apple_MPS"),
                params.get("checkpoint_path", f"checkpoints/best/{experiment_id}.h5"),
                params.get("dataset", "VNPlant-200"),
                datetime.now(timezone.utc).isoformat(),
                "completed",
                params.get("notes", "Auto-logged run"),
            ]
            with open(self.registry_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)
