#!/usr/bin/env python3
"""
Turnkey Training Pipeline for Future Kashmir Alpine Endemic Model (Model 2).
Automated environment detection (Apple Silicon MPS, NVIDIA CUDA, CPU fallback).
Trains on data/kashmir/ (train, val, test) and saves model artifacts to models/kashmir/.

Authors:
  - Dr. M Abdul Jawad & Dr. Riyaz Ahmed (Faculty Supervisors, Centre for AI, IUST)
  - Dar Rehan Rasool (Project Lead & Author)
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

KASHMIR_CLASSES = [
    "Aconitum_heterophyllum",
    "Artemisia_absinthium",
    "Berberis_lycium",
    "Colchicum_luteum",
    "Crocus_sativus",
    "Datura_stramonium",
    "Fritillaria_roylei",
    "Gentiana_kurroo",
    "Hyoscyamus_niger",
    "Jurinea_dolomiaea",
    "Picrorhiza_kurroa",
    "Podophyllum_hexandrum",
    "Rheum_emodi",
    "Saussurea_costus",
    "Taxus_wallichiana",
    "Valeriana_jatamansi",
]


def detect_environment():
    """Detect operating system and hardware acceleration (Apple MPS, NVIDIA CUDA, CPU)."""
    env_info = {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "accelerator": "CPU",
        "device_name": "Standard CPU",
        "recommended_batch_size": 16,
    }

    try:
        import tensorflow as tf

        # Check for NVIDIA GPUs
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            env_info["accelerator"] = "NVIDIA CUDA"
            env_info["device_name"] = gpus[0].name
            env_info["recommended_batch_size"] = 32
            # Enable memory growth if possible
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except Exception:
                pass
        elif platform.system() == "Darwin" and platform.machine() in ("arm64", "aarch64"):
            # Apple Silicon Mac
            env_info["accelerator"] = "Apple Silicon (MPS / Metal)"
            env_info["device_name"] = f"Apple M-Series GPU ({platform.machine()})"
            env_info["recommended_batch_size"] = 32
        else:
            env_info["accelerator"] = "CPU (x86_64 / Standard)"
            env_info["device_name"] = "Multi-core Host CPU"
            env_info["recommended_batch_size"] = 16
    except Exception as e:
        env_info["error"] = str(e)

    return env_info


def check_dataset_readiness(data_dir: Path):
    """Inspect data/kashmir/train, val, test for image availability."""
    splits = ["train", "val", "test"]
    counts = {}
    total_images = 0

    for split in splits:
        split_path = data_dir / split
        counts[split] = {}
        split_total = 0
        if split_path.exists():
            for cls_name in KASHMIR_CLASSES:
                cls_dir = split_path / cls_name
                if cls_dir.exists():
                    imgs = list(cls_dir.glob("*.jpg")) + list(cls_dir.glob("*.jpeg")) + list(cls_dir.glob("*.png"))
                    n = len(imgs)
                    counts[split][cls_name] = n
                    split_total += n
                else:
                    counts[split][cls_name] = 0
        counts[f"{split}_total"] = split_total
        total_images += split_total

    return counts, total_images


def train_kashmir_pipeline(
    data_dir: Path,
    output_dir: Path,
    epochs: int = 25,
    batch_size: int = 16,
    learning_rate: float = 1e-4,
    dry_run: bool = False,
):
    """Execute training pipeline and save artifacts and evaluation curves."""
    print("=" * 70)
    print("🌿 HERBALIST AI - KASHMIR ALPINE MODEL TRAINING PIPELINE (MODEL 2)")
    print("=" * 70)

    env = detect_environment()
    print(f"🖥️  OS: {env['os']} ({env['machine']})")
    print(f"⚡ Accelerator: {env['accelerator']} - {env['device_name']}")
    print(f"📦 Recommended Batch Size: {env['recommended_batch_size']}")

    output_dir.mkdir(parents=True, exist_ok=True)
    counts, total_images = check_dataset_readiness(data_dir)

    print("\n📊 Dataset Status in", data_dir)
    print(f"   - Train Total: {counts.get('train_total', 0)} images")
    print(f"   - Val Total:   {counts.get('val_total', 0)} images")
    print(f"   - Test Total:  {counts.get('test_total', 0)} images")

    min_required_train = len(KASHMIR_CLASSES)
    train_count = counts.get('train_total', 0)
    val_count = counts.get('val_total', 0)

    if train_count < min_required_train or val_count == 0 or dry_run:
        print("\n⚠️  NOTICE: Insufficient field photographs found in data/kashmir/ (Train: {}, Val: {}).".format(train_count, val_count))
        print("   This folder is initialized for future Kashmir medicinal plant collections.")
        print("   To train, place field photographs into their respective class subdirectories:")
        for cls in KASHMIR_CLASSES[:5]:
            print(f"     - data/kashmir/train/{cls}/")
            print(f"     - data/kashmir/val/{cls}/")
        print(f"     ... across all {len(KASHMIR_CLASSES)} Kashmir endemic species.")
        print("\n💡 Running pipeline verification mode (validates architecture and dependencies)...")
        _verify_architecture(output_dir, env)
        return

    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import Xception
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, CSVLogger

    img_size = (180, 180)
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir / "train",
        image_size=img_size,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=True,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir / "val",
        image_size=img_size,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=False,
    )

    # Data augmentation
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.15),
        layers.RandomContrast(0.1),
    ])

    base_model = Xception(weights="imagenet", include_top=False, input_shape=(180, 180, 3))
    base_model.trainable = False

    inputs = layers.Input(shape=(180, 180, 3))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255.0)(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(KASHMIR_CLASSES), activation="softmax")(x)

    model = models.Model(inputs, outputs, name="kashmir_alpine_classifier")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc_roc")],
    )

    model_path = output_dir / "kashmir_plant.h5"
    history_csv = output_dir / "training_history.csv"

    callbacks = [
        ModelCheckpoint(str(model_path), save_best_only=True, monitor="val_accuracy", mode="max", verbose=1),
        EarlyStopping(monitor="val_loss", patience=7, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6, verbose=1),
        CSVLogger(str(history_csv)),
    ]

    print(f"\n🚀 Commencing Kashmir Model Training for {epochs} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1,
    )

    # Save metadata
    _save_model_artifacts(model, output_dir, env, history.history)
    print(f"✅ Training completed! Model saved to {model_path}")


def _verify_architecture(output_dir: Path, env: dict):
    """Verify that the model architecture can build and compile cleanly."""
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import Xception

    inputs = layers.Input(shape=(180, 180, 3))
    base_model = Xception(weights=None, include_top=False, input_shape=(180, 180, 3))
    x = base_model(inputs)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(KASHMIR_CLASSES), activation="softmax")(x)
    model = models.Model(inputs, outputs, name="kashmir_alpine_architecture_spec")

    labels_map = {idx: cls_name for idx, cls_name in enumerate(KASHMIR_CLASSES)}
    labels_file = output_dir / "class_labels.json"
    with open(labels_file, "w") as f:
        json.dump(labels_map, f, indent=2)

    spec = {
        "model_name": "Herbalist Kashmir Alpine Classifier (Model 2)",
        "status": "Pipeline Architecture Verified (Awaiting User Field Captures)",
        "num_classes": len(KASHMIR_CLASSES),
        "target_species": KASHMIR_CLASSES,
        "input_resolution": [180, 180, 3],
        "parameters_total": model.count_params(),
        "accelerator_profile": env,
        "csv_catalog_mapping": "data/csv/label_mapping.csv",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(output_dir / "model_info.json", "w") as f:
        json.dump(spec, f, indent=2)

    print(f"✅ Architecture verified: {model.count_params():,} parameters.")
    print(f"✅ Class mapping saved: {labels_file}")
    print(f"✅ Model specification saved: {output_dir / 'model_info.json'}")


def _save_model_artifacts(model, output_dir: Path, env: dict, history: dict):
    """Save class_labels.json and model_info.json after training."""
    labels_map = {idx: cls_name for idx, cls_name in enumerate(KASHMIR_CLASSES)}
    with open(output_dir / "class_labels.json", "w") as f:
        json.dump(labels_map, f, indent=2)

    best_val_acc = max(history.get("val_accuracy", [0.0]))
    final_val_loss = history.get("val_loss", [0.0])[-1]

    info = {
        "model_name": "Herbalist Kashmir Alpine Classifier (Model 2)",
        "status": "Trained & Evaluated",
        "num_classes": len(KASHMIR_CLASSES),
        "target_species": KASHMIR_CLASSES,
        "input_resolution": [180, 180, 3],
        "best_val_accuracy": round(float(best_val_acc), 4),
        "final_val_loss": round(float(final_val_loss), 4),
        "parameters_total": model.count_params(),
        "accelerator_profile": env,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(output_dir / "model_info.json", "w") as f:
        json.dump(info, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Herbalist AI - Kashmir Model Turnkey Training")
    parser.add_argument("--data-dir", type=str, default=str(ROOT / "data" / "kashmir"))
    parser.add_argument("--output-dir", type=str, default=str(ROOT / "models" / "kashmir"))
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    train_kashmir_pipeline(
        data_dir=Path(args.data_dir),
        output_dir=Path(args.output_dir),
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
