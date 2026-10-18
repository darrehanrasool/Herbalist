"""Literature comparison table generator."""
from __future__ import annotations

import pandas as pd
from .paper_registry import get_paper_registry


def get_literature_comparison() -> pd.DataFrame:
    """Return DataFrame comparing published studies against Herbalist AI."""
    reg = get_paper_registry()
    records = []
    for p in reg.list_all():
        records.append({
            "paper_id": p.paper_id,
            "title": p.title,
            "architecture": p.model_architecture,
            "dataset": p.dataset_name,
            "reported_accuracy": p.reported_accuracy,
            "resolution": p.input_resolution,
            "year": p.year,
        })
    return pd.DataFrame(records)
