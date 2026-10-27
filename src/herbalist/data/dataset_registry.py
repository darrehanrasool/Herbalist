"""Registry of all local and external research datasets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
from ..core.constants import ROOT_DIR


@dataclass
class DatasetEntry:
    id: str
    name: str
    modality: str  # "tabular", "vision", "multimodal"
    region: str    # "kashmir", "india", "global", "vietnam"
    path: str
    num_classes: Optional[int]
    status: str    # "available", "downloadable", "external_api"
    description: str
    citation: Optional[str] = None


class DatasetRegistry:
    """Central catalog and lookup table for all datasets."""

    def __init__(self):
        self._registry: Dict[str, DatasetEntry] = {}
        self._populate_defaults()

    def _populate_defaults(self):
        self.register(DatasetEntry(
            id="medicinal",
            name="Master Medicinal Flora & Ethnopharmacology Catalog",
            modality="tabular",
            region="global_and_kashmir",
            path="data/csv/medicinal.csv",
            num_classes=216,
            status="available",
            description="Reference catalog of 216 medicinal species with active compounds, uses, and conservation status.",
            citation="POWO 2024 / ICMR / Rasool et al., 2025"
        ))
        self.register(DatasetEntry(
            id="fertiliser",
            name="Precision Agronomy & Nutrient Guidelines Catalog",
            modality="tabular",
            region="global_and_kashmir",
            path="data/csv/fertiliser.csv",
            num_classes=216,
            status="available",
            description="Precision agronomy catalog with NPK ratios, basal FYM, and application schedules."
        ))
        self.register(DatasetEntry(
            id="chemicaltaxonomy",
            name="Chemotaxonomy & Cytogenetic Breeding Catalog",
            modality="tabular",
            region="global_and_kashmir",
            path="data/csv/chemicaltaxonomy.csv",
            num_classes=216,
            status="available",
            description="Phytochemical classes, 2n karyotypes, and hybridization breeding objectives."
        ))
        self.register(DatasetEntry(
            id="disease",
            name="Phytopathology & Integrated Pest Management Catalog",
            modality="tabular",
            region="global_and_kashmir",
            path="data/csv/disease.csv",
            num_classes=216,
            status="available",
            description="Crop protection, foliar diagnostic symptoms, and biological organic IPM controls."
        ))
        self.register(DatasetEntry(
            id="label_mapping",
            name="Neural Vision Output to Catalog Mapping",
            modality="tabular",
            region="global_and_kashmir",
            path="data/csv/label_mapping.csv",
            num_classes=216,
            status="available",
            description="One-to-one neural index mapping connecting output logits to canonical catalogs."
        ))
        self.register(DatasetEntry(
            id="vnplant_images",
            name="VNPlant-200 Image Repository",
            modality="vision",
            region="global",
            path="data/raw/kaggle/vnplant-200",
            num_classes=200,
            status="downloadable",
            description="17,973 foliar RGB photos (12,000 train / 5,973 test) across 200 medicinal species.",
            citation="https://github.com/kencoca/VietNam-Medicinal-Plant"
        ))
        self.register(DatasetEntry(
            id="indian_medicinal_leaves",
            name="Indian Medicinal Leaves (Kaggle)",
            modality="vision",
            region="india",
            path="data/raw/kaggle/indian-medicinal-leaves-dataset",
            num_classes=80,
            status="downloadable",
            description="80 common Indian medicinal leaf taxa (~9GB) for subcontinent model transfer.",
            citation="Kaggle: aryashah2k/indian-medicinal-leaves-dataset"
        ))

    def register(self, entry: DatasetEntry) -> None:
        self._registry[entry.id] = entry

    def get(self, dataset_id: str) -> Optional[DatasetEntry]:
        return self._registry.get(dataset_id)

    def list_all(self) -> List[DatasetEntry]:
        return list(self._registry.values())

    def filter_by_region(self, region: str) -> List[DatasetEntry]:
        return [e for e in self._registry.values() if e.region.lower() == region.lower()]

    def filter_by_modality(self, modality: str) -> List[DatasetEntry]:
        return [e for e in self._registry.values() if e.modality.lower() == modality.lower()]


_GLOBAL_REGISTRY = DatasetRegistry()


def get_dataset_info(dataset_id: str) -> Optional[DatasetEntry]:
    return _GLOBAL_REGISTRY.get(dataset_id)
