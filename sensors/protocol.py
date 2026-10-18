"""
Herbalist AI sensor contract

Hardware (ESP32 / Arduino / phone) POSTs JSON to the running Flask app:

  POST http://<host>:5001/api/sensors/ingest
  Content-Type: application/json

  {
    "device_id": "plot-aloe-01",
    "pH": 6.4,
    "N": 42,
    "P": 18,
    "K": 28,
    "moisture": 31.5,
    "temperature": 24.2,
    "ec": 1.1,
    "unit_N": "mg/kg",
    "notes": ""
  }

N, P, K are treated as relative kit units unless you calibrate.
The dashboard compares readings to knowledge/soil_requirements.csv for the
identified (or selected) species.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "artifacts" / "metrics" / "sensor_latest.json"


def simulate(device_id: str = "sim-plot-01") -> dict:
    rng = random.Random()
    return {
        "device_id": device_id,
        "pH": round(rng.uniform(5.2, 7.8), 2),
        "N": round(rng.uniform(15, 80), 1),
        "P": round(rng.uniform(8, 40), 1),
        "K": round(rng.uniform(10, 60), 1),
        "moisture": round(rng.uniform(12, 55), 1),
        "temperature": round(rng.uniform(8, 34), 1),
        "ec": round(rng.uniform(0.3, 2.4), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
    }


def save_reading(payload: dict) -> dict:
    payload = dict(payload)
    payload.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(payload, indent=2))
    return payload


def load_reading() -> dict | None:
    if STORE.exists():
        return json.loads(STORE.read_text())
    return None


def gaps(reading: dict, soil_row: dict) -> list[dict]:
    """Rule-based gaps vs knowledge table. Not a yield model."""
    out = []
    try:
        ph = float(reading.get("pH", float("nan")))
        lo, hi = float(soil_row["pH_min"]), float(soil_row["pH_max"])
        if ph < lo:
            out.append({"factor": "pH", "status": "low", "detail": f"{ph} < target {lo}–{hi}. Consider agricultural lime after a lab test."})
        elif ph > hi:
            out.append({"factor": "pH", "status": "high", "detail": f"{ph} > target {lo}–{hi}. Elemental sulfur / acidifying organics — confirm locally."})
        else:
            out.append({"factor": "pH", "status": "ok", "detail": f"{ph} inside {lo}–{hi}."})
    except (TypeError, ValueError, KeyError):
        pass
    try:
        t = float(reading.get("temperature", float("nan")))
        lo, hi = float(soil_row["Temp_C_min"]), float(soil_row["Temp_C_max"])
        if t < lo:
            out.append({"factor": "temperature", "status": "low", "detail": f"{t}°C below {lo}–{hi}°C envelope."})
        elif t > hi:
            out.append({"factor": "temperature", "status": "high", "detail": f"{t}°C above {lo}–{hi}°C envelope."})
        else:
            out.append({"factor": "temperature", "status": "ok", "detail": f"{t}°C inside envelope."})
    except (TypeError, ValueError, KeyError):
        pass
    moist = reading.get("moisture")
    if moist is not None:
        out.append({"factor": "moisture", "status": "info", "detail": f"Probe moisture {moist}%. Catalog target: {soil_row.get('Moisture', 'n/a')}."})
    out.append({"factor": "NPK", "status": "info", "detail": f"Kit N/P/K={reading.get('N')}/{reading.get('P')}/{reading.get('K')}. Catalog bands N={soil_row.get('N_level')} P={soil_row.get('P_level')} K={soil_row.get('K_level')} (relative, calibrate kit)."})
    return out


if __name__ == "__main__":
    save_reading(simulate())
    print(STORE.read_text())
