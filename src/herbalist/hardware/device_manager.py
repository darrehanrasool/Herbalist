"""Device manager for hardware acceleration."""
from __future__ import annotations
from typing import Literal
from .hardware_detector import detect_hardware


def get_optimal_device() -> Literal["mps", "cuda", "cpu"]:
    """Select the best available compute backend."""
    hw = detect_hardware()
    if hw.gpu_type == "cuda":
        return "cuda"
    elif hw.gpu_type == "mps":
        return "mps"
    return "cpu"


def configure_tf_runtime() -> str:
    """Configure TensorFlow GPU memory growth and device placement."""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            for gpu in gpus:
                try:
                    tf.config.experimental.set_memory_growth(gpu, True)
                except Exception:
                    pass
            return f"configured_{len(gpus)}_gpus"
        return "tf_cpu_default"
    except Exception as e:
        return f"tf_unconfigured: {e}"
