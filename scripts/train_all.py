"""Train all baseline models and log results to experiment registry."""
from __future__ import annotations

import sys
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.herbalist.models.classical import (
    get_random_forest,
    get_gradient_boosting,
    get_logistic_regression,
    get_svm,
)
from src.herbalist.evaluation import compute_classification_metrics
from src.herbalist.monitoring.experiment_logger import ExperimentLogger


def train_classical_baselines():
    print("🌲 Training classical ML baseline models on agronomic/toxicity features...")
    # Generate reproducible synthetic botanical feature matrix for validation
    np.random.seed(42)
    n_samples = 300
    n_features = 7
    n_classes = 4  # Toxicity classes: None, Low, Moderate, High

    X = np.random.randn(n_samples, n_features)
    y = np.random.randint(0, n_classes, size=n_samples)

    split = int(0.8 * n_samples)
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    models = {
        "random_forest": get_random_forest(n_estimators=50),
        "gradient_boosting": get_gradient_boosting(n_estimators=50),
        "logistic_regression": get_logistic_regression(),
        "svm": get_svm(),
    }

    logger = ExperimentLogger()

    for name, clf in models.items():
        clf.fit(X_train, y_train)
        y_val_proba = clf.predict_proba(X_val)
        metrics = compute_classification_metrics(y_val, y_val_proba, top_k=min(3, n_classes))

        print(f"  ✅ {name:<20}: Accuracy = {metrics['top1_accuracy']:.4f}, Macro-F1 = {metrics['macro_f1']:.4f}")

        logger.log_run(
            experiment_id=f"EXP-{name.upper()[:4]}",
            experiment_name=f"{name}_baseline",
            metrics=metrics,
            params={"model_type": "classical", "backbone": name, "dataset": "synthetic_agronomic"}
        )


if __name__ == "__main__":
    train_classical_baselines()
