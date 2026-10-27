# Herbalist AI platform routes (imported by api/app.py)
from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import (
    redirect,
    render_template,
    request,
    url_for,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.knowledge import agronomy_bundle, plant_index, _tables  # noqa: E402

GRAPHS = ROOT / "api" / "static" / "graphs"
CSV_DIR = ROOT / "data" / "csv"


def _graphs():
    names = sorted(p.name for p in GRAPHS.glob("*.png")) if GRAPHS.exists() else []
    return names


def register_platform(app):
    app.secret_key = os.environ.get("HERBALIST_SECRET", "herbalist-ai-dev-secret")

    @app.route("/classic")
    def classic_home():
        return redirect(url_for("home"))

    @app.route("/hybridization")
    def hybridization_explorer():
        """Chemotaxonomy & Interspecific Hybridization Explorer."""
        df_chem = _tables().get("chemicaltaxonomy")
        pairs = df_chem.fillna("").to_dict(orient="records") if df_chem is not None and not df_chem.empty else []
        search_query = request.args.get("q", "").strip().lower()
        if search_query:
            pairs = [
                p for p in pairs
                if search_query in str(p.get("scientific_name", "")).lower()
                or search_query in str(p.get("common_name", "")).lower()
                or search_query in str(p.get("congeneric_relatives", "")).lower()
                or search_query in str(p.get("primary_chemical_class", "")).lower()
                or search_query in str(p.get("dominant_secondary_metabolites", "")).lower()
            ]
        return render_template(
            "platform/hybridization.html",
            pairs=pairs,
            query=search_query,
            total_count=len(pairs),
        )

    @app.route("/lab")
    def lab():
        """Research Figures (300 DPI publication visualizations)."""
        graphs = _graphs()
        return render_template(
            "platform/lab.html",
            graphs=graphs,
        )

    @app.route("/agronomy")
    def agronomy():
        """Agronomic cultivation protocols and nutrient guidelines."""
        name = request.args.get("species", "")
        bundle = agronomy_bundle(name) if name else {}
        return render_template(
            "platform/agronomy.html",
            plants=plant_index(),
            species=name,
            bundle=bundle,
        )

    @app.route("/plants")
    def plants_browser():
        """Master Botanical & Pharmacognosy Catalog Browser (216 Taxa)."""
        return render_template(
            "platform/plants.html",
            plants=plant_index(),
        )

    @app.route("/research-lab")
    def research_lab():
        """Lineage, pharmacopeial standards, and verified catalog citations."""
        log_path = ROOT / "research" / "DATASETS.md"
        text = log_path.read_text() if log_path.exists() else "Official Botanical Repositories: POWO 2024, ICMR Standards, NMPB AYUSH."
        dl = ROOT / "research" / "datasets" / "download_log.txt"
        dlog = dl.read_text() if dl.exists() else "Dataset lineage: Working Model (200 Taxa), Kashmir Alpine (16 Taxa), POWO/ICMR 4 Master Catalogs."
        return render_template(
            "platform/research.html",
            catalog=text,
            download_log=dlog,
        )
