"""Reproducibility utilities for deterministic experiments across ML backends."""
import os
import random
import numpy as np


def seed_everything(seed: int = 42) -> None:
    """Set random seed across all libraries to enforce strict reproducibility."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    # Optional TensorFlow seed
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
        os.environ["TF_DETERMINISTIC_OPS"] = "1"
    except ImportError:
        pass

    # Optional PyTorch seed
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass
