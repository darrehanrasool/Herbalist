"""Stratified K-Fold Cross-Validation runner."""
from __future__ import annotations

from typing import Dict, Any, List
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score


def run_kfold_cv(
    estimator_factory,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    seed: int = 42
) -> Dict[str, Any]:
    """Execute stratified k-fold cross validation and aggregate mean/std metrics."""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    fold_accuracies: List[float] = []
    fold_f1s: List[float] = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        clf = estimator_factory()
        clf.fit(X[train_idx], y[train_idx])
        y_val_pred = clf.predict(X[val_idx])

        fold_accuracies.append(float(accuracy_score(y[val_idx], y_val_pred)))
        fold_f1s.append(float(f1_score(y[val_idx], y_val_pred, average="weighted", zero_division=0)))

    return {
        "n_splits": n_splits,
        "mean_accuracy": round(float(np.mean(fold_accuracies)), 4),
        "std_accuracy": round(float(np.std(fold_accuracies)), 4),
        "mean_f1": round(float(np.mean(fold_f1s)), 4),
        "std_f1": round(float(np.std(fold_f1s)), 4),
        "fold_accuracies": [round(x, 4) for x in fold_accuracies],
    }
