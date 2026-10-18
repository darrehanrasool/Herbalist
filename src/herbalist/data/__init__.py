"""Data ingestion, validation, preprocessing, feature engineering, and splitting."""
from .dataset_registry import DatasetRegistry, get_dataset_info
from .dataset_manifest import load_manifest, verify_manifest_checksums
from .data_validator import validate_image, validate_dataframe
from .preprocessing import preprocess_image, load_and_preprocess_image
from .feature_engineering import encode_botanical_features, compute_soil_ratios
from .missing_values import impute_soil_readings
from .data_quality import compute_data_quality_report
from .deduplication import find_duplicate_images
from .data_splitting import create_stratified_splits

__all__ = [
    "DatasetRegistry",
    "get_dataset_info",
    "load_manifest",
    "verify_manifest_checksums",
    "validate_image",
    "validate_dataframe",
    "preprocess_image",
    "load_and_preprocess_image",
    "encode_botanical_features",
    "compute_soil_ratios",
    "impute_soil_readings",
    "compute_data_quality_report",
    "find_duplicate_images",
    "create_stratified_splits",
]
