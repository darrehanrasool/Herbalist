"""Image preprocessing pipeline for deep learning inference and training."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple, Union
import numpy as np
from PIL import Image

from ..core.constants import DEFAULT_IMAGE_SIZE


def preprocess_image(
    image: Image.Image,
    target_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE,
    rescale: bool = True
) -> np.ndarray:
    """Resize, convert to RGB, and scale image to float32 [0, 1]."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    if image.size != target_size:
        image = image.resize(target_size, Image.Resampling.BILINEAR)

    arr = np.array(image, dtype=np.float32)
    if rescale:
        arr /= 255.0
    return arr


def load_and_preprocess_image(
    image_path: Union[str, Path],
    target_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE
) -> np.ndarray:
    """Load an image file from disk and format it for neural network input."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found at {path}")
    with Image.open(path) as img:
        arr = preprocess_image(img, target_size=target_size, rescale=True)
    # Add batch dimension: (1, H, W, C)
    return np.expand_dims(arr, axis=0)
