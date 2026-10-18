"""Progress tracking utility for multi-stage ML pipelines."""
from __future__ import annotations

import time
from typing import Optional


class ProgressTracker:
    """Prints elapsed time and step completion status."""

    def __init__(self, task_name: str, total_steps: Optional[int] = None):
        self.task_name = task_name
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()

    def step(self, info: str = "") -> None:
        self.current_step += 1
        elapsed = time.time() - self.start_time
        if self.total_steps:
            pct = (self.current_step / self.total_steps) * 100
            print(f"[{self.task_name}] Step {self.current_step}/{self.total_steps} ({pct:.1f}%) - {info} [{elapsed:.1f}s elapsed]")
        else:
            print(f"[{self.task_name}] Step {self.current_step} - {info} [{elapsed:.1f}s elapsed]")

    def finish(self, message: str = "Completed successfully") -> None:
        total_time = time.time() - self.start_time
        print(f"✅ [{self.task_name}] {message} in {total_time:.2f}s")
