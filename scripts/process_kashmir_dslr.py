#!/usr/bin/env python3
"""
process_kashmir_dslr.py
------------------------
CLI operational script to trigger automated quality auditing, EXIF altitude extraction,
and stratified train/validation/test splitting for Kashmir DSLR botanical captures.

Usage:
  python scripts/process_kashmir_dslr.py
  python scripts/process_kashmir_dslr.py --source /path/to/dslr_card/ --size 224
  python scripts/process_kashmir_dslr.py --dry-run
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.herbalist.data.kashmir_dslr_pipeline import KashmirDSLRDatasetPipeline

def main():
    parser = argparse.ArgumentParser(description="Kashmir DSLR Botanical Dataset Processing Pipeline")
    parser.add_argument("--source", type=str, default=None, help="Custom source folder of raw DSLR captures")
    parser.add_argument("--size", type=int, default=180, help="Target square resolution (default: 180)")
    parser.add_argument("--blur-thresh", type=float, default=80.0, help="Laplacian variance threshold for blur detection (default: 80.0)")
    parser.add_argument("--dry-run", action="store_true", help="Perform discovery and quality audit without saving images")

    args = parser.parse_args()

    source_path = Path(args.source) if args.source else None
    pipeline = KashmirDSLRDatasetPipeline(
        target_size=(args.size, args.size),
        blur_threshold=args.blur_thresh
    )

    pipeline.run_pipeline(source_dir=source_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
