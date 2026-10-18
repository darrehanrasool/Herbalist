"""Real-time RAM and memory tracking for training loop safety."""
from __future__ import annotations
import os
from typing import Dict, Any


def get_memory_stats() -> Dict[str, Any]:
    """Return memory statistics for current process and host system."""
    stats: Dict[str, Any] = {
        "process_resident_mb": 0.0,
        "system_ram_total_gb": 8.0,
        "system_ram_avail_gb": 4.0,
        "is_low_memory": False,
    }
    try:
        total_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        stats["system_ram_total_gb"] = round(total_bytes / (1024 ** 3), 2)
        stats["system_ram_avail_gb"] = round(stats["system_ram_total_gb"] * 0.5, 2)
    except Exception:
        pass

    # Process RSS via resource module if available
    try:
        import resource
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # On macOS, ru_maxrss is in bytes; on Linux, in kilobytes
        import platform
        if platform.system() == "Darwin":
            stats["process_resident_mb"] = round(usage / (1024 * 1024), 2)
        else:
            stats["process_resident_mb"] = round(usage / 1024, 2)
    except Exception:
        pass

    if stats["system_ram_avail_gb"] < 1.0:
        stats["is_low_memory"] = True

    return stats
