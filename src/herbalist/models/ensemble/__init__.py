"""Ensemble architectures combining vision, tabular, and sensor classifiers."""
from .voting_ensemble import get_voting_ensemble, SoftVotingEnsemble

__all__ = ["get_voting_ensemble", "SoftVotingEnsemble"]
