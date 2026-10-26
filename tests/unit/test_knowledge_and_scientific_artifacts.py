"""Unit tests for curated medicinal catalog, chemotaxonomy hybridization, and publication artifacts."""
import unittest
from pathlib import Path
import pandas as pd

from src.herbalist.core.constants import ROOT_DIR
from backend.knowledge import agronomy_bundle, curated_row_for, hybridization_for


class TestKnowledgeAndScientificArtifacts(unittest.TestCase):

    def test_curated_global_catalog_attributes(self):
        curated_path = ROOT_DIR / "knowledge" / "medicinal_plants_global_curated.csv"
        self.assertTrue(curated_path.exists(), f"Missing {curated_path}")

        df = pd.read_csv(curated_path)
        self.assertEqual(len(df), 215, "Curated catalog must contain 215 species")
        self.assertEqual(len(df.columns), 22, "Curated catalog must contain exactly 22 standardized attributes")

        expected_columns = [
            "scientific_name", "common_name", "family", "local_names_kashmir_india",
            "primary_bioactives", "chemical_classes", "therapeutic_indications",
            "part_used", "edaphic_soil_ph", "optimal_altitude_min_m",
            "optimal_altitude_max_m", "soil_texture", "moisture_requirement",
            "rainfall_annual_mm", "temperature_optimum_c", "iucn_conservation_status",
            "endemic_to_kashmir_himalayas", "pharmacopeial_standard",
            "ayurvedic_unani_siddha_usage", "toxicological_notes_contraindications",
            "harvesting_season", "reference_citations"
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Missing required attribute: {col}")

    def test_chemotaxonomy_hybridization_integrity(self):
        hyb_path = ROOT_DIR / "knowledge" / "chemotaxonomy_hybridization.csv"
        self.assertTrue(hyb_path.exists(), f"Missing {hyb_path}")

        df = pd.read_csv(hyb_path)
        self.assertGreaterEqual(len(df), 12, "Must contain at least 12 hybridization pairs")

        # Verify key scientific columns
        for col in ["hybrid_id", "genus_group", "parent_species_1", "parent_species_2",
                    "chromosome_parent_1_2n", "chromosome_parent_2_2n", "genetic_distance_index",
                    "hybridization_feasibility", "hypothetical_bioactive_synergy", "breeding_pros",
                    "breeding_cons_risks", "scientific_literature_reference"]:
            self.assertIn(col, df.columns, f"Missing hybridization column: {col}")

        # Check no blank literature citations
        for ref in df["scientific_literature_reference"]:
            self.assertTrue(bool(ref and str(ref).strip()), "Literature reference cannot be empty")

    def test_backend_knowledge_bundle_resolution(self):
        bundle = agronomy_bundle("Gentiana kurroo")
        self.assertTrue(bool(bundle.get("curated")), "Gentiana kurroo must resolve in curated catalog")
        self.assertGreaterEqual(len(bundle.get("hybridization", [])), 1, "Gentiana kurroo must have hybridization records")

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

        required_csvs = [
            "medicinal_plants_master.csv",
            "kashmir_medicinal_plants.csv",
            "chemotaxonomy_hybridization.csv",
            "soil_pedological_requirements.csv",
            "agronomic_cultivation_protocols.csv",
            "nutrient_fertilizer_guidelines.csv",
            "phytopathology_disease_ipm.csv",
            "biochemical_literature.csv",
            "dataset_image_sample_counts.csv",
        ]
        for name in required_csvs:
            csv_path = csv_dir / name
            self.assertTrue(csv_path.exists(), f"Missing canonical CSV: {name}")
            df = pd.read_csv(csv_path)
            self.assertGreater(len(df), 0, f"Canonical CSV {name} cannot be empty")

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
