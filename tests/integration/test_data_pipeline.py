"""Integration tests for dataset manifest, catalog loading, and quality verification."""
import unittest
from pathlib import Path
import pandas as pd

from src.herbalist.core.constants import ROOT_DIR
from src.herbalist.data import load_manifest, verify_manifest_checksums, compute_data_quality_report
from src.herbalist.data.feature_engineering import encode_botanical_features


class TestDataPipelineIntegration(unittest.TestCase):

    def test_dataset_manifest_integrity(self):
        manifest = load_manifest()
        self.assertIn("manifest_version", manifest)
        self.assertIn("datasets", manifest)

        # Check existing datasets
        results = verify_manifest_checksums()
        self.assertTrue(results.get("medicinal_catalog_200", False))
        self.assertTrue(results.get("kashmir_medicinal", False))

    def test_kashmir_catalog_loading_and_features(self):
        kashmir_csv = ROOT_DIR / "data" / "processed" / "kashmir_medicinal.csv"
        self.assertTrue(kashmir_csv.exists())

        df = pd.read_csv(kashmir_csv)
        self.assertEqual(len(df), 15)
        self.assertIn("Scientificname", df.columns)
        self.assertIn("ConservationStatus", df.columns)

        df_feat = encode_botanical_features(df)
        self.assertIn("Genus", df_feat.columns)
        self.assertIn("Toxicity_Ordinal", df_feat.columns)

    def test_data_quality_computation(self):
        csv_path = ROOT_DIR / "data" / "processed" / "medicinal.csv"
        df = pd.read_csv(csv_path)
        report = compute_data_quality_report(df)

        self.assertEqual(report["total_rows"], 200)
        self.assertGreater(report["overall_completeness_pct"], 90.0)


if __name__ == "__main__":
    unittest.main()
