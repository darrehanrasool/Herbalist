"""Dataclass and parser for literature publications."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List


@dataclass
class PaperMetadata:
    paper_id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    doi: Optional[str]
    taxa_focus: str
    dataset_name: str
    reported_accuracy: float
    reported_top5_accuracy: Optional[float]
    model_architecture: str
    input_resolution: str
    key_findings: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
