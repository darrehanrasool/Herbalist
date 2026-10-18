"""Integration tests for model factory, training loop, and evaluation."""
import unittest
import numpy as np

from src.herbalist.models.model_factory import create_model
from src.herbalist.models.deep_learning import load_trained_vision_model
from src.herbalist.evaluation import compute_classification_metrics
from src.herbalist.data.preprocessing import load_and_preprocess_image
from src.herbalist.core.constants import ROOT_DIR


class TestTrainingPipelineIntegration(unittest.TestCase):

    def test_classical_model_fit_and_eval(self):
        rf = create_model("random_forest", n_estimators=10)
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 3, size=50)

        rf.fit(X, y)
        probs = rf.predict_proba(X)
        self.assertEqual(probs.shape, (50, 3))

        metrics = compute_classification_metrics(y, probs, top_k=2)
        self.assertGreater(metrics["top1_accuracy"], 0.0)

    def test_vision_model_predict_on_fixture(self):
        fixture_path = ROOT_DIR / "tests" / "fixtures" / "sample_leaf_34.jpg"
        if not fixture_path.exists():
            self.skipTest("Sample image fixture not found")

        model = load_trained_vision_model()
        if model is None:
            self.skipTest("Trained model plant.h5 not found")

        arr = load_and_preprocess_image(fixture_path, target_size=(180, 180))
        preds = model.predict(arr, verbose=0)

        self.assertEqual(preds.shape, (1, 200))
        top_idx = int(np.argmax(preds))
        self.assertGreaterEqual(top_idx, 0)
        self.assertLess(top_idx, 200)


if __name__ == "__main__":
    unittest.main()
