#!/usr/bin/env python3
"""Train a Herbalist classifier from data/splits.

Reproduces the BTech setup with:
  python training/src/train.py --arch xception --freeze-backbone --epochs 6

Requires TensorFlow and image folders:
  data/splits/train/<class_name>/*.jpg
  data/splits/validation/<class_name>/*.jpg
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "training" / "src"))

from data import make_generators  # noqa: E402
from models import build_model  # noqa: E402


def log_experiment(row: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if write_header:
            w.writeheader()
        w.writerow(row)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--arch", default="xception")
    p.add_argument("--train-dir", default=str(ROOT / "data/splits/train"))
    p.add_argument("--val-dir", default=str(ROOT / "data/splits/validation"))
    p.add_argument("--img-size", type=int, default=180)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--epochs", type=int, default=6)
    p.add_argument("--lr", type=float, default=0.001)
    p.add_argument("--num-classes", type=int, default=0, help="0 = infer from folders")
    p.add_argument("--freeze-backbone", action="store_true")
    p.add_argument("--augment", action="store_true")
    p.add_argument("--dropout", type=float, default=0.2)
    args = p.parse_args()

    train, val = make_generators(
        args.train_dir, args.val_dir, args.img_size, args.batch_size, args.augment
    )
    n_classes = args.num_classes or train.num_classes
    model = build_model(args.arch, args.img_size, n_classes, args.freeze_backbone, args.dropout)

    from tensorflow.keras.optimizers import Adam

    model.compile(
        optimizer=Adam(learning_rate=args.lr),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    history = model.fit(train, validation_data=val, epochs=args.epochs)

    ckpt = ROOT / "artifacts" / "checkpoints"
    ckpt.mkdir(parents=True, exist_ok=True)
    out_h5 = ckpt / f"{args.arch}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h5"
    model.save(out_h5)

    hist = {k: [float(x) for x in v] for k, v in history.history.items()}
    hist["epochs"] = list(range(1, len(next(iter(hist.values()))) + 1))
    hist["source"] = str(out_h5)
    hist_path = ROOT / "artifacts" / "metrics" / "history.json"
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    hist_path.write_text(json.dumps(hist, indent=2))

    val_acc = hist.get("val_accuracy", [None])[-1]
    log_experiment(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "arch": args.arch,
            "freeze_backbone": args.freeze_backbone,
            "augment": args.augment,
            "epochs": args.epochs,
            "img_size": args.img_size,
            "batch_size": args.batch_size,
            "lr": args.lr,
            "num_classes": n_classes,
            "val_accuracy": val_acc,
            "checkpoint": str(out_h5),
        },
        ROOT / "training" / "experiments" / "experiment_log.csv",
    )
    print(f"Saved {out_h5}")
    print("Refresh UI graphs: python training/scripts/generate_lab_graphs.py")


if __name__ == "__main__":
    main()
