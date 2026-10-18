"""Resource constraints and dynamic batch size optimization."""
from __future__ import annotations
from typing import Tuple
from .hardware_detector import detect_hardware


def calculate_optimal_batch_size(
    image_resolution: Tuple[int, int] = (180, 180),
    preferred_batch: int = 32
) -> int:
    """Dynamically determine a safe batch size given hardware and image dimensions."""
    hw = detect_hardware()
    pixels = image_resolution[0] * image_resolution[1]

    # If low memory (e.g. < 4GB RAM) or CPU-only with high resolution, throttle down
    if hw.ram_available_gb < 2.0:
        return min(preferred_batch, 8)
    elif hw.ram_available_gb < 4.0:
        return min(preferred_batch, 16)

    if pixels > (256 * 256):
        return min(preferred_batch, 16)

    return preferred_batch
