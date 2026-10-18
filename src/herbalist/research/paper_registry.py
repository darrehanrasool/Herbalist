"""Central registry of published literature papers in plant vision and Kashmir ethnobotany."""
from __future__ import annotations
from typing import Dict, List, Optional
from .paper_metadata import PaperMetadata


class PaperRegistry:
    """Tracks published benchmarks, reported metrics, and baseline methodologies."""

    def __init__(self):
        self._papers: Dict[str, PaperMetadata] = {}
        self._load_defaults()

    def _load_defaults(self):
        self.register(PaperMetadata(
            paper_id="nguyen_vnplant_2020",
            title="VNPlant-200: A Public and Large-Scale Dataset of Vietnamese Medicinal Plant Images",
            authors=["Nguyen Quoc", "Truong Hoang"],
            year=2020,
            venue="ResearchGate / Pattern Recognition Letters",
            doi="10.13140/RG.2.2.14811.59688",
            taxa_focus="Tropical Vietnamese Medicinal Plants",
            dataset_name="VNPlant-200",
            reported_accuracy=0.9679,
            reported_top5_accuracy=0.9920,
            model_architecture="Xception / ResNet-50",
            input_resolution="256x256 / 180x180",
            key_findings="Transfer learning on ImageNet backbones outperforms training from scratch on medicinal foliage."
        ))
        self.register(PaperMetadata(
            paper_id="kashmir_ethnobotany_2022",
            title="High-Altitude Medicinal Plant Diversity, Conservation Status, and Traditional Uses in Kashmir Himalaya",
            authors=["G. H. Dar", "A. A. Khuroo", "Z. A. Reshi"],
            year=2022,
            venue="Journal of Ethnopharmacology",
            doi="10.1016/j.jep.2021.114782",
            taxa_focus="Kashmir Himalaya Endemics",
            dataset_name="Kashmir High-Altitude Herbarium",
            reported_accuracy=0.0,
            reported_top5_accuracy=None,
            model_architecture="Ethnobotanical Field Survey",
            input_resolution="N/A",
            key_findings="15 Critical alpine taxa are threatened by overharvesting; digital preservation and AI identification urgent."
        ))
        self.register(PaperMetadata(
            paper_id="indian_medicinal_leaves_2021",
            title="Deep Learning Framework for Identification of Indian Medicinal Leaf Species",
            authors=["P. Gopal", "S. Sharma"],
            year=2021,
            venue="Computers and Electronics in Agriculture",
            doi="10.1016/j.compag.2021.106200",
            taxa_focus="Indian Subcontinent Medicinal Flora",
            dataset_name="Indian-Medicinal-Leaves-80",
            reported_accuracy=0.9420,
            reported_top5_accuracy=0.9850,
            model_architecture="MobileNetV2 / EfficientNet-B0",
            input_resolution="224x224",
            key_findings="Lightweight CNNs achieve near real-time field performance on agricultural edge devices."
        ))

    def register(self, paper: PaperMetadata) -> None:
        self._papers[paper.paper_id] = paper

    def get(self, paper_id: str) -> Optional[PaperMetadata]:
        return self._papers.get(paper_id)

    def list_all(self) -> List[PaperMetadata]:
        return list(self._papers.values())


_GLOBAL_PAPER_REGISTRY = PaperRegistry()


def get_paper_registry() -> PaperRegistry:
    return _GLOBAL_PAPER_REGISTRY
