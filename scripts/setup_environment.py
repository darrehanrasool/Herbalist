"""Environment setup and dependency check script."""
from __future__ import annotations

import sys
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("KERAS_HOME", str(ROOT / ".keras"))
os.makedirs(os.environ["KERAS_HOME"], exist_ok=True)


def check_python_version():
    major, minor = sys.version_info[:2]
    print(f"Checking Python version: {major}.{minor} ...", end=" ")
    if (major, minor) < (3, 9):
        print("❌ FAILED. Python 3.9+ required.")
        return False
    print("✅ OK")
    return True


def check_dependencies():
    required_packages = [
        "tensorflow",
        "numpy",
        "pandas",
        "PIL",
        "sklearn",
        "flask",
        "yaml",
        "matplotlib",
    ]
    print("\nChecking core packages:")
    all_ok = True
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} (missing)")
            all_ok = False
    return all_ok


def setup_directories():
    print("\nVerifying directory layout:")
    dirs = [
        ROOT / ".keras",
        ROOT / "checkpoints" / "best",
        ROOT / "checkpoints" / "latest",
        ROOT / "data" / "raw" / "clinical",
        ROOT / "data" / "raw" / "imaging",
        ROOT / "data" / "processed",
        ROOT / "data" / "splits" / "train",
        ROOT / "data" / "splits" / "validation",
        ROOT / "data" / "splits" / "test",
        ROOT / "logs" / "application",
        ROOT / "logs" / "training",
        ROOT / "logs" / "hardware",
        ROOT / "outputs" / "predictions",
        ROOT / "outputs" / "trained_models",
        ROOT / "visualizations" / "training" / "summaries",
        ROOT / "visualizations" / "data_exploration",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  📁 {d.relative_to(ROOT)}")


def main():
    print("=" * 60)
    print("HERBALIST AI - ENVIRONMENT SETUP")
    print("=" * 60)
    v_ok = check_python_version()
    setup_directories()

    # Pre-configure KERAS_HOME before importing tensorflow
    os.environ["KERAS_HOME"] = str(ROOT / ".keras")
    print(f"\n✅ KERAS_HOME configured to: {ROOT / '.keras'}")

    d_ok = check_dependencies()

    if v_ok and d_ok:
        print("\n🎉 Environment is fully configured and ready for research!")
    else:
        print("\n⚠️ Environment setup completed with warnings. Run: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
