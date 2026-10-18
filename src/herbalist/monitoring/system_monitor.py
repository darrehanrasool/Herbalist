"""System hardware and resource utilization monitor."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
from ..core.constants import ROOT_DIR
from ..hardware.memory_monitor import get_memory_stats
from ..hardware.hardware_detector import detect_hardware


class SystemMonitor:
    """Logs system health, memory headroom, and CPU usage."""

    def __init__(self, log_dir: Path = ROOT_DIR / "logs" / "hardware"):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "system_telemetry.jsonl"

    def record_snapshot(self, stage: str = "general") -> Dict[str, Any]:
        """Record current memory and device telemetry snapshot."""
        mem = get_memory_stats()
        hw = detect_hardware()

        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stage": stage,
            "process_resident_mb": mem.get("process_resident_mb", 0.0),
            "system_ram_avail_gb": mem.get("system_ram_avail_gb", 0.0),
            "is_low_memory": mem.get("is_low_memory", False),
            "gpu_type": hw.gpu_type,
            "disk_free_gb": hw.disk_free_gb,
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot) + "\n")

        return snapshot
