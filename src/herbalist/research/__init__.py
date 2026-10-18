"""Research paper metadata, baseline reproductions, and literature benchmarks."""
from .paper_registry import PaperRegistry, get_paper_registry
from .paper_metadata import PaperMetadata
from .baseline_reproduction import verify_btech_baseline
from .research_comparison import get_literature_comparison

__all__ = [
    "PaperRegistry",
    "get_paper_registry",
    "PaperMetadata",
    "verify_btech_baseline",
    "get_literature_comparison",
]
