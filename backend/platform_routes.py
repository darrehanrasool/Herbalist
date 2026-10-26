# Herbalist AI platform (imported by api/app.py)
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auth.users import verify  # noqa: E402
from backend.knowledge import agronomy_bundle, plant_index, _tables  # noqa: E402
from sensors.protocol import gaps, load_reading, save_reading, simulate  # noqa: E402
from src.herbalist.data.kashmir_dslr_pipeline import KashmirDSLRDatasetPipeline  # noqa: E402

GRAPHS = ROOT / "api" / "static" / "graphs"
MANIFEST = ROOT / "artifacts" / "metrics" / "graphs_manifest.json"
KASHMIR_MANIFEST = ROOT / "data" / "manifests" / "kashmir_dslr_split_manifest.json"
CSV_DIR = ROOT / "data" / "csv"


def _graphs():
    names = sorted(p.name for p in GRAPHS.glob("*.png")) if GRAPHS.exists() else []
    return names


def _require_login():
    if not session.get("user"):
        return redirect(url_for("login", next=request.path))
    return None


def register_platform(app):
    app.secret_key = os.environ.get("HERBALIST_SECRET", "herbalist-ai-dev-secret")

    @app.route("/classic")
    def classic_home():
        return redirect(url_for("home"))

    @app.route("/kashmir-dslr")
    def kashmir_hub():
        manifest_data = {}
        if KASHMIR_MANIFEST.exists():
            try:
                manifest_data = json.loads(KASHMIR_MANIFEST.read_text())
            except Exception:
                pass

        # Load splits CSV if present
        splits_records = []
        splits_csv = CSV_DIR / "kashmir_dslr_splits.csv"
        if splits_csv.exists():
            try:
                import pandas as pd
                df = pd.read_csv(splits_csv)
                splits_records = df.head(30).fillna("").to_dict(orient="records")
            except Exception:
                pass

        hw = KashmirDSLRDatasetPipeline.detect_hardware_accelerator()

        return render_template(
            "platform/kashmir_hub.html",
            manifest=manifest_data,
            splits=splits_records,
            hardware=hw,
            user=session.get("user"),
        )

    @app.route("/api/kashmir/process", methods=["POST"])
    def kashmir_process_api():
        try:
            pipeline = KashmirDSLRDatasetPipeline()
            result = pipeline.run_pipeline()
            return jsonify({"ok": True, "manifest": result})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route("/hybridization")
    def hybridization_explorer():
        df_hyb = _tables().get("hybridization")
        pairs = df_hyb.fillna("").to_dict(orient="records") if df_hyb is not None and not df_hyb.empty else []
        search_query = request.args.get("q", "").strip().lower()
        if search_query:
            pairs = [
                p for p in pairs
                if search_query in str(p.get("parent_species_1", "")).lower()
                or search_query in str(p.get("parent_species_2", "")).lower()
                or search_query in str(p.get("genus_group", "")).lower()
                or search_query in str(p.get("target_secondary_metabolites", "")).lower()
            ]
        return render_template(
            "platform/hybridization.html",
            pairs=pairs,
            query=search_query,
            total_count=len(pairs),
            user=session.get("user"),
        )

    @app.route("/lab")
    def lab():
        graphs = _graphs()
        return render_template(
            "platform/lab.html",
            graphs=graphs,
            user=session.get("user"),
        )

    @app.route("/sensors")
    def sensors_page():
        reading = load_reading() or simulate()
        species = request.args.get("species", "Aloe vera")
        soil = agronomy_bundle(species).get("soil") or {}
        analysis = gaps(reading, soil) if soil else []
        return render_template(
            "platform/sensors.html",
            reading=reading,
            species=species,
            soil=soil,
            analysis=analysis,
            plants=plant_index(),
            user=session.get("user"),
        )

    @app.route("/api/sensors/ingest", methods=["POST"])
    def sensors_ingest():
        payload = request.get_json(silent=True) or request.form.to_dict()
        for key in ("pH", "N", "P", "K", "moisture", "temperature", "ec"):
            if key in payload and payload[key] not in (None, ""):
                try:
                    payload[key] = float(payload[key])
                except (TypeError, ValueError):
                    pass
        saved = save_reading(payload)
        return jsonify({"ok": True, "reading": saved})

    @app.route("/api/sensors/simulate", methods=["POST"])
    def sensors_sim():
        saved = save_reading(simulate())
        return jsonify({"ok": True, "reading": saved})

    @app.route("/agronomy")
    def agronomy():
        name = request.args.get("species", "")
        bundle = agronomy_bundle(name) if name else {}
        return render_template(
            "platform/agronomy.html",
            plants=plant_index(),
            species=name,
            bundle=bundle,
            user=session.get("user"),
        )

    @app.route("/plants")
    def plants_browser():
        return render_template(
            "platform/plants.html",
            plants=plant_index(),
            user=session.get("user"),
        )

    @app.route("/research-lab")
    def research_lab():
        log_path = ROOT / "research" / "DATASETS.md"
        text = log_path.read_text() if log_path.exists() else "Official Botanical Repositories: POWO 2024, ICMR Standards, NMPB AYUSH."
        dl = ROOT / "research" / "datasets" / "download_log.txt"
        dlog = dl.read_text() if dl.exists() else "Dataset lineage: VNPlant-200, Kashmir DSLR In-Situ Captures, GBIF Open Botanical API."
        return render_template(
            "platform/research.html",
            catalog=text,
            download_log=dlog,
            user=session.get("user"),
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            user = verify(request.form.get("username", ""), request.form.get("password", ""))
            if user:
                session["user"] = user
                return redirect(request.args.get("next") or url_for("home"))
            error = "Invalid credentials. Demo: scientist / herbalist"
        return render_template("platform/login.html", error=error)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))
