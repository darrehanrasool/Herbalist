"""Unit tests for image and tabular preprocessing."""
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

from src.herbalist.data.preprocessing import preprocess_image, load_and_preprocess_image
from src.herbalist.core.constants import ROOT_DIR


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        # Create a synthetic test RGB image in memory
        self.img = Image.new("RGB", (300, 300), color=(100, 150, 200))
        self.fixture_path = ROOT_DIR / "tests" / "fixtures" / "sample_leaf_34.jpg"

    def test_preprocess_image_shape_and_scaling(self):
        arr = preprocess_image(self.img, target_size=(180, 180), rescale=True)
        self.assertEqual(arr.shape, (180, 180, 3))
        self.assertTrue(0.0 <= arr.min() <= arr.max() <= 1.0)
        self.assertEqual(arr.dtype, np.float32)

    def test_preprocess_without_rescaling(self):
        arr = preprocess_image(self.img, target_size=(180, 180), rescale=False)
        self.assertEqual(arr.shape, (180, 180, 3))
        self.assertTrue(arr.max() > 1.0)

    def test_load_and_preprocess_from_disk(self):
        if self.fixture_path.exists():
            batch = load_and_preprocess_image(self.fixture_path, target_size=(180, 180))
            self.assertEqual(batch.shape, (1, 180, 180, 3))
            self.assertEqual(batch.dtype, np.float32)


if __name__ == "__main__":
    unittest.main()
