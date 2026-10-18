"""
Herbalist AI - Enterprise Command-Line Interface and Pipeline Runner.
"""
from __future__ import annotations

import argparse
import sys
import json
from pathlib import Path

from .core.constants import ROOT_DIR, PLANT_CLASSES
from .hardware.hardware_detector import detect_hardware
from .data.dataset_manifest import load_manifest, verify_manifest_checksums
from .data.preprocessing import load_and_preprocess_image
from .models.deep_learning.training_utils import load_trained_vision_model
import numpy as np


def cmd_hardware(args):
    """Inspect and display system hardware report."""
    hw = detect_hardware()
    print("\n" + "=" * 55)
    print("HERBALIST AI - HARDWARE DIAGNOSTICS")
    print("=" * 55)
    print(f"OS Platform:          {hw.os_name} ({hw.machine_arch})")
    print(f"CPU Cores:            {hw.cpu_count_physical} physical / {hw.cpu_count_logical} logical")
    print(f"RAM Available:        {hw.ram_available_gb} GB / {hw.ram_total_gb} GB total")
    print(f"Disk Free:            {hw.disk_free_gb} GB / {hw.disk_total_gb} GB total")
    print(f"GPU Hardware:         {hw.gpu_type.upper()} ({', '.join(hw.gpu_devices) or 'None'})")
    print("=" * 55 + "\n")


def cmd_verify_data(args):
    """Verify integrity and presence of datasets."""
    print("🔍 Verifying dataset manifests and checksums...")
    results = verify_manifest_checksums()
    for ds_id, exists in results.items():
        status = "✅ Found" if exists else "❌ Missing"
        print(f"  {status:<12} {ds_id}")


def cmd_predict(args):
    """Perform species inference on a leaf image."""
    img_path = Path(args.image)
    if not img_path.exists():
        print(f"❌ Error: Image file not found: {img_path}")
        sys.exit(1)

    print(f"📷 Preprocessing image: {img_path}")
    arr = load_and_preprocess_image(img_path, target_size=(180, 180))

    print("🧠 Loading vision neural network...")
    model = load_trained_vision_model()
    if model is None:
        print("❌ Error: Trained model plant.h5 not found in repository.")
        sys.exit(1)

    preds = model.predict(arr, verbose=0)
    top_idx = int(np.argmax(preds))
    confidence = float(np.max(preds) * 100)
    species_name = PLANT_CLASSES.get(top_idx, "Unknown Taxon")

    print("\n" + "=" * 55)
    print("HERBALIST AI - INFERENCE REPORT")
    print("=" * 55)
    print(f"Predicted Species:    {species_name}")
    print(f"Top-1 Confidence:     {confidence:.2f}%")
    print(f"Class Index:          {top_idx}")
    print("=" * 55 + "\n")


def cmd_serve(args):
    """Launch Flask web platform."""
    from api.app import app
    print("🌱 Launching Herbalist AI Platform...")
    app.run(host=args.host, port=args.port, debug=args.debug)


def main():
    parser = argparse.ArgumentParser(
        prog="herbalist",
        description="Herbalist AI - Enterprise Computational Botany and Pharmacognosy Framework."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # hardware
    subparsers.add_parser("hardware", help="Display hardware and memory diagnostics")

    # verify-data
    subparsers.add_parser("verify-data", help="Verify presence and checksums of datasets")

    # predict
    predict_parser = subparsers.add_parser("predict", help="Predict medicinal species from image")
    predict_parser.add_argument("image", type=str, help="Path to leaf image file")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Launch interactive web platform")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Binding host")
    serve_parser.add_argument("--port", type=int, default=5001, help="Binding port")
    serve_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.command == "hardware":
        cmd_hardware(args)
    elif args.command == "verify-data":
        cmd_verify_data(args)
    elif args.command == "predict":
        cmd_predict(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
