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
from backend.knowledge import agronomy_bundle, plant_index  # noqa: E402
from sensors.protocol import gaps, load_reading, save_reading, simulate  # noqa: E402

GRAPHS = ROOT / "api" / "static" / "graphs"
MANIFEST = ROOT / "artifacts" / "metrics" / "graphs_manifest.json"


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
        return render_template("index.html")

    @app.route("/lab")
    def lab():
        graphs = _graphs()
        history = {}
        if MANIFEST.exists():
            history = json.loads(MANIFEST.read_text())
        return render_template(
            "platform/lab.html",
            graphs=graphs,
            history=history,
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
        text = log_path.read_text() if log_path.exists() else "Missing research/DATASETS.md"
        dl = ROOT / "research" / "datasets" / "download_log.txt"
        dlog = dl.read_text() if dl.exists() else "No downloads yet. Run: python scripts/download_datasets.py"
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
