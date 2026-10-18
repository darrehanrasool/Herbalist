"""Unit tests for hardware detection and memory monitoring."""
import unittest
from src.herbalist.hardware import detect_hardware, get_optimal_device, get_memory_stats, calculate_optimal_batch_size


class TestHardware(unittest.TestCase):

    def test_detect_hardware(self):
        hw = detect_hardware()
        self.assertIn(hw.os_name, ["Darwin", "Linux", "Windows"])
        self.assertGreater(hw.cpu_count_logical, 0)
        self.assertGreater(hw.ram_total_gb, 0.0)

    def test_get_optimal_device(self):
        device = get_optimal_device()
        self.assertIn(device, ["mps", "cuda", "cpu"])

    def test_memory_stats(self):
        stats = get_memory_stats()
        self.assertIn("system_ram_total_gb", stats)
        self.assertIn("system_ram_avail_gb", stats)
        self.assertIn("is_low_memory", stats)

    def test_batch_size_limits(self):
        bs = calculate_optimal_batch_size((180, 180), preferred_batch=32)
        self.assertIn(bs, [1, 4, 8, 16, 32])


if __name__ == "__main__":
    unittest.main()
