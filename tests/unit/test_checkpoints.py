"""Unit tests for checkpoint manager and recovery routines."""
import unittest
import tempfile
import json
from pathlib import Path

from src.herbalist.training.checkpoint_manager import CheckpointManager
from src.herbalist.training.recovery_manager import RecoveryManager


class TestCheckpoints(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.ckpt_mgr = CheckpointManager(base_dir=self.temp_dir)

    def test_checkpoint_directories_created(self):
        self.assertTrue((self.temp_dir / "best").exists())
        self.assertTrue((self.temp_dir / "latest").exists())
        self.assertTrue((self.temp_dir / "metadata").exists())

    def test_save_metadata(self):
        metadata = {"epoch": 5, "val_accuracy": 0.9679}
        self.ckpt_mgr.save_metadata("test_meta", metadata)

        out_file = self.temp_dir / "metadata" / "test_meta.json"
        self.assertTrue(out_file.exists())
        with open(out_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["val_accuracy"], 0.9679)

    def test_recovery_manager_empty(self):
        rec_mgr = RecoveryManager(checkpoints_dir=self.temp_dir)
        latest = rec_mgr.find_latest_checkpoint(check_fallback=False)
        self.assertIsNone(latest)


if __name__ == "__main__":
    unittest.main()
