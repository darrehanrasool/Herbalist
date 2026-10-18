"""Script to verify hardware, GPU acceleration, and system memory limits."""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.herbalist.hardware import detect_hardware, get_optimal_device, get_memory_stats


def main():
    print("=" * 60)
    print("🌿 HERBALIST AI - HARDWARE VERIFICATION")
    print("=" * 60)
    hw = detect_hardware()
    print(f"OS:                 {hw.os_name} {hw.os_release} ({hw.machine_arch})")
    print(f"Physical CPU Cores: {hw.cpu_count_physical}")
    print(f"Logical CPU Cores:  {hw.cpu_count_logical}")
    print(f"System RAM:         {hw.ram_available_gb:.1f} GB avail / {hw.ram_total_gb:.1f} GB total")
    print(f"Disk Space:         {hw.disk_free_gb:.1f} GB free / {hw.disk_total_gb:.1f} GB total")
    print(f"Optimal Backend:    {get_optimal_device().upper()}")
    print(f"GPU Available:      {hw.gpu_available} ({hw.gpu_type})")
    if hw.gpu_devices:
        print(f"GPU Devices:        {', '.join(hw.gpu_devices)}")

    mem = get_memory_stats()
    print(f"Process Resident:   {mem.get('process_resident_mb', 0.0):.1f} MB")
    print(f"Memory Status:      {'⚠️ LOW MEMORY WARNING' if mem.get('is_low_memory') else '✅ Healthy'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
