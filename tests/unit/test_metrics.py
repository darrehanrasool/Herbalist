"""Unit tests for evaluation metrics computation."""
import unittest
import numpy as np
from src.herbalist.evaluation.metrics import compute_classification_metrics
from src.herbalist.validation.calibration import calculate_expected_calibration_error


class TestMetrics(unittest.TestCase):

    def test_compute_metrics_perfect_predictions(self):
        y_true = np.array([0, 1, 2, 3, 4])
        # Perfect one-hot probabilities
        y_pred_proba = np.eye(5)

        metrics = compute_classification_metrics(y_true, y_pred_proba, top_k=3)
        self.assertEqual(metrics["top1_accuracy"], 1.0)
        self.assertEqual(metrics["top3_accuracy"], 1.0)
        self.assertEqual(metrics["macro_f1"], 1.0)
        self.assertEqual(metrics["cohens_kappa"], 1.0)

    def test_compute_metrics_imperfect_predictions(self):
        y_true = np.array([0, 1, 2, 0])
        y_pred_proba = np.array([
            [0.8, 0.1, 0.1],
            [0.2, 0.7, 0.1],
            [0.3, 0.4, 0.3],  # Incorrect: predicts 1 instead of 2
            [0.9, 0.05, 0.05],
        ])
        metrics = compute_classification_metrics(y_true, y_pred_proba, top_k=2)
        self.assertEqual(metrics["top1_accuracy"], 0.75)
        self.assertTrue(metrics["top2_accuracy"] >= 0.75)

    def test_ece_calculation(self):
        y_true = np.array([0, 1, 0, 1])
        y_pred_proba = np.array([
            [0.9, 0.1],
            [0.2, 0.8],
            [0.85, 0.15],
            [0.1, 0.9],
        ])
        ece = calculate_expected_calibration_error(y_true, y_pred_proba, n_bins=5)
        self.assertTrue(0.0 <= ece <= 1.0)


if __name__ == "__main__":
    unittest.main()
