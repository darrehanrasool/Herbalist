"""Soft-voting ensemble for probabilistic model aggregation."""
from __future__ import annotations

from typing import List, Optional
import numpy as np
from sklearn.ensemble import VotingClassifier


class SoftVotingEnsemble:
    """Combines predicted probability distributions from multiple model backends."""

    def __init__(self, weights: Optional[List[float]] = None):
        self.weights = weights

    def predict_proba(self, probability_matrices: List[np.ndarray]) -> np.ndarray:
        """Weighted average of predicted probability distributions."""
        num_models = len(probability_matrices)
        if num_models == 0:
            raise ValueError("No probability matrices provided for ensembling.")

        if self.weights is None:
            weights = np.ones(num_models) / num_models
        else:
            weights = np.array(self.weights, dtype=np.float32)
            weights = weights / weights.sum()

        combined = np.zeros_like(probability_matrices[0], dtype=np.float32)
        for w, proba in zip(weights, probability_matrices):
            combined += w * proba
        return combined

    def predict(self, probability_matrices: List[np.ndarray]) -> np.ndarray:
        """Argmax over the ensembled probability distribution."""
        combined = self.predict_proba(probability_matrices)
        return np.argmax(combined, axis=-1)


def get_voting_ensemble(estimators: list, voting: str = "soft") -> VotingClassifier:
    """Scikit-Learn voting classifier wrapper for classical ML models."""
    return VotingClassifier(estimators=estimators, voting=voting, n_jobs=-1)
