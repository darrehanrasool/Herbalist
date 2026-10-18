"""Context manager for accurate runtime profiling."""
from __future__ import annotations

import time
from typing import Optional


class Timer:
    """Context manager measuring execution time."""

    def __init__(self, description: Optional[str] = None):
        self.description = description
        self.elapsed: float = 0.0
        self.start_time: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        if self.description:
            print(f"⏱️ [{self.description}] elapsed: {self.elapsed:.4f}s")
