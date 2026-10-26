#!/usr/bin/env python3
"""
train_model.py
---------------
CLI tool for training deep neural architectures on Apple Silicon MPS / NVIDIA CUDA GPUs.

Usage:
  python scripts/train_model.py --arch xception --epochs 10 --batch-size 32
  python scripts/train_model.py --arch mobilenet --epochs 15
  python scripts/train_model.py --arch himalayan_cnn --device auto
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.herbalist.training.gpu_trainer import GPUTrainingEngine

def main():
    parser = argparse.ArgumentParser(description="Herbalist AI GPU Deep Learning Trainer")
    parser.add_argument("--arch", type=str, default="xception", choices=["xception", "mobilenet", "himalayan_cnn"], help="Deep vision backbone architecture")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs (default: 10)")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size (default: 32)")
    parser.add_argument("--lr", type=float, default=1e-4, help="Initial learning rate (default: 1e-4)")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "gpu", "cuda", "mps", "cpu"], help="Hardware acceleration device")

    args = parser.parse_args()

    engine = GPUTrainingEngine(
        architecture=args.arch,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        device=args.device,
    )

    engine.train_mock_session(epochs=args.epochs)

if __name__ == "__main__":
    main()
