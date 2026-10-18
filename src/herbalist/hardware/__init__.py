"""Hardware detection, memory monitoring, and device management."""
from .hardware_detector import detect_hardware, HardwareReport
from .device_manager import get_optimal_device
from .memory_monitor import get_memory_stats
from .resource_limits import calculate_optimal_batch_size

__all__ = [
    "detect_hardware",
    "HardwareReport",
    "get_optimal_device",
    "get_memory_stats",
    "calculate_optimal_batch_size",
]
