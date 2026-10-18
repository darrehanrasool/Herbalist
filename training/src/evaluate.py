#!/usr/bin/env python3
"""Evaluate a saved .h5 on data/splits/test (or validation)."""
from __future__ import annotations

import argparse
from pathlib import Path

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--data-dir", required=True)
    p.add_argument("--img-size", type=int, default=180)
    p.add_argument("--batch-size", type=int, default=16)
    args = p.parse_args()

    gen = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        args.data_dir,
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=False,
    )
    model = load_model(args.model)
    loss, acc = model.evaluate(gen)
    Path("artifacts/metrics").mkdir(parents=True, exist_ok=True)
    Path("artifacts/metrics/last_eval.txt").write_text(f"loss={loss}\naccuracy={acc}\n")
    print(f"loss={loss:.4f} accuracy={acc:.4f}")


if __name__ == "__main__":
    main()
