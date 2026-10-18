"""Centralized logging configuration."""
from __future__ import annotations

import logging
from pathlib import Path
from ..core.constants import ROOT_DIR


def setup_logging(
    name: str = "herbalist",
    log_category: str = "application",
    level: int = logging.INFO
) -> logging.Logger:
    """Configure a structured file and stream logger."""
    log_dir = ROOT_DIR / "logs" / log_category
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{name}.log"

    logger = logging.getLogger(f"{name}_{log_category}")
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # File handler
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Stream handler
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger
