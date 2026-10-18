"""Dataset splitting routines preserving species balance and preventing leakage."""
from __future__ import annotations

from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd


def create_stratified_splits(
    df: pd.DataFrame,
    target_column: str,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split a DataFrame into train, validation, and test subsets stratified by target."""
    assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5, "Split ratios must sum to 1.0"
    np.random.seed(seed)

    train_indices = []
    val_indices = []
    test_indices = []

    for _, group in df.groupby(target_column):
        indices = group.index.tolist()
        np.random.shuffle(indices)
        n = len(indices)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)

        train_indices.extend(indices[:n_train])
        val_indices.extend(indices[n_train:n_train + n_val])
        test_indices.extend(indices[n_train + n_val:])

    return df.loc[train_indices], df.loc[val_indices], df.loc[test_indices]
