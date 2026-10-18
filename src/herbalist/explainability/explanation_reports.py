"""Automated generation of explainability reports."""
from __future__ import annotations

from typing import Dict, Any, List


def generate_explanation_report(
    predicted_species: str,
    confidence: float,
    feature_attributions: Dict[str, float],
    clinical_notes: str = ""
) -> Dict[str, Any]:
    """Generate a structured interpretability report for clinician/botanist review."""
    top_drivers = list(feature_attributions.items())[:3]
    top_driver_str = ", ".join(f"{k} ({v*100:.1f}%)" for k, v in top_drivers)

    summary = (
        f"Prediction '{predicted_species}' achieved {confidence:.1f}% confidence. "
        f"Primary influential factors: {top_driver_str}. {clinical_notes}"
    )

    return {
        "species": predicted_species,
        "confidence": confidence,
        "feature_attributions": feature_attributions,
        "top_drivers": top_drivers,
        "human_readable_summary": summary,
    }
