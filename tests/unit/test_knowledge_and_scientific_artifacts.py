"""Unit tests for curated medicinal catalog, chemotaxonomy hybridization, and publication artifacts."""
import unittest
from pathlib import Path
import pandas as pd

from src.herbalist.core.constants import ROOT_DIR
from backend.knowledge import agronomy_bundle, curated_row_for, hybridization_for


class TestKnowledgeAndScientificArtifacts(unittest.TestCase):

    def test_curated_global_catalog_attributes(self):
        med_path = ROOT_DIR / "data" / "csv" / "medicinal.csv"
        self.assertTrue(med_path.exists(), f"Missing {med_path}")

        df = pd.read_csv(med_path)
        self.assertEqual(len(df), 216, "Master catalog must contain 216 species")
        self.assertEqual(len(df.columns), 25, "Master catalog must contain exactly 25 standardized attributes")

        expected_columns = [
            "species_id", "scientific_name", "common_name", "family", "genus",
            "local_names", "origin_geography", "plant_type_habit", "part_used",
            "primary_bioactives", "chemical_classes", "therapeutic_indications",
            "ayurvedic_unani_siddha_usage", "iucn_conservation_status",
            "endemic_to_kashmir_himalayas", "optimal_altitude_min_m",
            "optimal_altitude_max_m", "edaphic_soil_ph", "soil_texture",
            "temperature_optimum_c", "annual_rainfall_mm", "toxicological_notes",
            "harvesting_season", "pharmacopeial_standard", "reference_citations"
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Missing required attribute: {col}")

    def test_chemotaxonomy_hybridization_integrity(self):
        chem_path = ROOT_DIR / "data" / "csv" / "chemicaltaxonomy.csv"
        self.assertTrue(chem_path.exists(), f"Missing {chem_path}")

        df = pd.read_csv(chem_path)
        self.assertEqual(len(df), 216, "Must contain 216 taxa chemotaxonomy records")

        # Verify key scientific columns
        for col in [
            "species_id", "scientific_name", "common_name", "family", "order",
            "primary_chemical_class", "secondary_chemical_class",
            "dominant_secondary_metabolites", "biosynthetic_pathway",
            "diagnostic_chemomarker", "diploid_chromosome_number_2n",
            "congeneric_relatives", "hybridization_compatibility",
            "hybridization_breeding_objective", "chemodiversity_altitude_effect",
            "analytical_quantification_method", "pharmacopeial_literature_doi"
        ]:
            self.assertIn(col, df.columns, f"Missing column: {col}")

    def test_backend_knowledge_bundle_resolution(self):
        bundle = agronomy_bundle("Gentiana kurroo")
        self.assertTrue(bool(bundle.get("medicinal")), "Gentiana kurroo must resolve in medicinal catalog")
        self.assertTrue(bool(bundle.get("fertiliser")), "Gentiana kurroo must resolve in fertiliser catalog")
        self.assertTrue(bool(bundle.get("chemicaltaxonomy")), "Gentiana kurroo must resolve in chemicaltaxonomy")
        self.assertTrue(bool(bundle.get("disease")), "Gentiana kurroo must resolve in disease catalog")

        # Check curated row content
        curated = curated_row_for("Aconitum heterophyllum")
        self.assertEqual(curated.get("scientific_name"), "Aconitum heterophyllum")
        self.assertEqual(curated.get("endemic_to_kashmir_himalayas"), "Yes")

    def test_publication_figures_existence(self):
        reports_dir = ROOT_DIR / "reports" / "figures"
        static_dir = ROOT_DIR / "api" / "static" / "graphs"

        expected_figs = [
            "01_chemotaxonomy_distribution.png",
            "02_kashmir_alpine_elevation_gradient.png",
            "03_edaphic_suitability_envelopes.png",
            "04_model_architecture_benchmark.png",
            "05_training_convergence_dynamics.png",
            "06_kashmir_endemics_confusion_matrix.png",
            "07_multiclass_roc_auc_envelopes.png",
            "08_hybridization_bioactive_synergy_matrix.png",
            "09_iucn_conservation_vulnerability.png",
            "10_npk_macronutrient_moisture_profiles.png"
        ]

        for fig_name in expected_figs:
            self.assertTrue((reports_dir / fig_name).exists(), f"Missing figure in reports: {fig_name}")
            self.assertTrue((static_dir / fig_name).exists(), f"Missing figure in static graphs: {fig_name}")

    def test_unified_csv_directory_integrity(self):
        csv_dir = ROOT_DIR / "data" / "csv"
        self.assertTrue(csv_dir.exists(), "data/csv/ directory must exist")

        useful_csvs = {
            "medicinal.csv",
            "fertiliser.csv",
            "chemicaltaxonomy.csv",
            "disease.csv",
            "label_mapping.csv",
        }

        # Check that all useful CSVs exist and have data
        for name in useful_csvs:
            csv_path = csv_dir / name
            self.assertTrue(csv_path.exists(), f"Missing canonical CSV: {name}")
            df = pd.read_csv(csv_path)
            self.assertGreater(len(df), 0, f"Canonical CSV {name} cannot be empty")

        # Check that no non-useful/redundant CSVs remain in data/csv/
        actual_csvs = {p.name for p in csv_dir.glob("*.csv")}
        self.assertEqual(actual_csvs, useful_csvs, f"data/csv/ contains unexpected CSVs: {actual_csvs - useful_csvs}")

    def test_non_repetitive_scientific_data_and_image_splits(self):
        csv_dir = ROOT_DIR / "data" / "csv"
        fert_df = pd.read_csv(csv_dir / "fertiliser.csv")
        self.assertEqual(len(fert_df), 216, "fertiliser.csv must have 216 rows")
        self.assertGreater(fert_df["agronomic_avoid_contraindications"].nunique(), 15, "Avoid must have distinct values")

        chem_df = pd.read_csv(csv_dir / "chemicaltaxonomy.csv")
        self.assertEqual(len(chem_df), 216, "chemicaltaxonomy.csv must have 216 rows")
        self.assertGreater(chem_df["primary_chemical_class"].nunique(), 5)

        med_df = pd.read_csv(csv_dir / "medicinal.csv")
        self.assertEqual(len(med_df), 216, "medicinal.csv must have 216 rows")

        # Verify no stray CSVs in data/processed/ or data/splits/
        processed_dir = ROOT_DIR / "data" / "processed"
        splits_dir = ROOT_DIR / "data" / "splits"
        self.assertEqual(len(list(processed_dir.glob("*.csv"))), 0, "No CSV files allowed in data/processed/")
        self.assertEqual(len(list(splits_dir.rglob("*.csv"))), 0, "No CSV files allowed in data/splits/")

        # Verify processed/train contains image folders
        train_dir = processed_dir / "train"
        self.assertTrue(train_dir.exists())
        self.assertGreater(len(list(train_dir.iterdir())), 50, "processed/train must contain class image folders")

    def test_kashmir_dslr_pipeline_components(self):
        from src.herbalist.data.kashmir_dslr_pipeline import KashmirDSLRDatasetPipeline
        from PIL import Image

        pipeline = KashmirDSLRDatasetPipeline()
        hw = pipeline.detect_hardware_accelerator()
        self.assertIn("device", hw)

        # Test quality audit on synthetic image
        test_img = Image.new("RGB", (200, 200), color=(120, 180, 100))
        audit = pipeline.audit_quality(test_img)
        self.assertTrue(audit.is_valid)
        self.assertGreaterEqual(audit.blur_score, 0.0)

    def test_gpu_trainer_device_resolution(self):
        from src.herbalist.training.gpu_trainer import GPUTrainingEngine
        engine = GPUTrainingEngine(architecture="xception", device="auto")
        self.assertIn(engine.resolved_device, ["GPU", "CPU"])
        self.assertIn("type", engine.device_details)


if __name__ == "__main__":
    unittest.main()
