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
    modality: str  # "tabular", "vision", "multimodal", "sensor"
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
            id="kashmir_endemics",
            name="Kashmir High-Altitude Endemic Medicinal Flora",
            modality="tabular",
            region="kashmir",
            path="data/processed/kashmir_medicinal.csv",
            num_classes=15,
            status="available",
            description="15 Critically endangered & endangered high-altitude medicinal herbs endemic to Kashmir Himalaya.",
            citation="Herbalist AI Ethnobotany Catalog (Rasool et al., 2025)"
        ))
        self.register(DatasetEntry(
            id="medicinal_200",
            name="VNPlant-200 Medicinal Flora Benchmark Catalog",
            modality="tabular",
            region="global",
            path="data/processed/medicinal.csv",
            num_classes=200,
            status="available",
            description="Reference catalog of 200 medicinal species with active compounds, uses, and toxicity levels.",
            citation="Nguyen Quoc & Truong Hoang, 2020"
        ))
        self.register(DatasetEntry(
            id="plants_master",
            name="Integrated Master Medicinal & Agronomy Catalog",
            modality="tabular",
            region="global",
            path="knowledge/plants_master.csv",
            num_classes=215,
            status="available",
            description="Unified catalog merging Kashmir endemic taxa with global 200 species and agronomic parameters."
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
        self.register(DatasetEntry(
            id="soil_sensors",
            name="Agronomic Soil NPK and pH Sensor Stream",
            modality="sensor",
            region="kashmir",
            path="artifacts/metrics/sensor_latest.json",
            num_classes=None,
            status="available",
            description="Real-time and simulated soil NPK, pH, moisture, and temperature readings for precision agronomy."
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
