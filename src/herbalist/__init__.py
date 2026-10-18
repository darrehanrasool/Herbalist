"""
Herbalist AI - Enterprise Computational Botany and Pharmacognosy Framework.
"""

__version__ = "2.0.0"
__author__ = "Darrehan Rasool"

import os
import sys
from pathlib import Path

# Automatically ensure local KERAS_HOME to prevent sandbox/permission issues
_ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("KERAS_HOME", str(_ROOT / ".keras"))
os.makedirs(os.environ["KERAS_HOME"], exist_ok=True)
