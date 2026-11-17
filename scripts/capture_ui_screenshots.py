#!/usr/bin/env python3
"""
Herbalist AI - Automated UI Screenshot Generation Script
Captures high-resolution, publication-grade Retina screenshots of the live platform UI
and output diagnostics using headless Google Chrome.
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets" / "screenshots"
DOCS_ASSETS_DIR = ROOT / "docs" / "assets" / "screenshots"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 5001
BASE_URL = f"http://127.0.0.1:{PORT}"

def ensure_dirs():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def start_server():
    print(f"[*] Starting Herbalist AI server on {BASE_URL}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    python_bin = str(ROOT / ".venv" / "bin" / "python")
    if not os.path.exists(python_bin):
        python_bin = sys.executable

    server_proc = subprocess.Popen(
        [python_bin, str(ROOT / "api" / "app.py")],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Wait for server to become responsive
    max_wait = 30
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            r = requests.get(f"{BASE_URL}/", timeout=1)
            if r.status_code == 200:
                print(f"[+] Server online in {time.time() - start_time:.1f}s")
                return server_proc
        except Exception:
            pass
        time.sleep(0.5)

    print("[-] Server failed to respond within timeout.")
    server_proc.kill()
    sys.exit(1)

def capture_screenshot(url, filename, window_size="1440,1100", scale=2):
    out_path = ASSETS_DIR / filename
    docs_path = DOCS_ASSETS_DIR / filename
    print(f"[*] Capturing screenshot for {url} -> {filename}...")

    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={window_size}",
        f"--force-device-scale-factor={scale}",
        "--hide-scrollbars",
        "--virtual-time-budget=3000",
        f"--screenshot={str(out_path)}",
        url,
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out_path.exists():
        import shutil
        shutil.copyfile(out_path, docs_path)
        print(f"[+] Successfully captured: {out_path} ({out_path.stat().st_size // 1024} KB)")
    else:
        print(f"[-] Failed to capture {filename}: {res.stderr.decode('utf-8')[:300]}")

def main():
    if not os.path.exists(CHROME_BIN):
        print(f"[-] Google Chrome binary not found at {CHROME_BIN}")
        sys.exit(1)

    ensure_dirs()
    proc = start_server()

    try:
        # 1. UI Output Report (Botanical Diagnostic Dossier)
        capture_screenshot(
            f"{BASE_URL}/report",
            "01_botanical_diagnostic_report_output.png",
            window_size="1440,1200",
            scale=2,
        )

        # 2. Main Workspace Dashboard
        capture_screenshot(
            f"{BASE_URL}/",
            "02_workspace_telemetry_dashboard.png",
            window_size="1440,1150",
            scale=2,
        )

        # 3. Specimen Ingestion Studio
        capture_screenshot(
            f"{BASE_URL}/upload",
            "03_specimen_ingestion_studio.png",
            window_size="1440,950",
            scale=2,
        )

        # 4. Terminal Research Lab Console
        capture_screenshot(
            f"{BASE_URL}/research-lab",
            "04_terminal_research_console.png",
            window_size="1440,1050",
            scale=2,
        )

        print("\n[+] All UI screenshots captured successfully!")
    finally:
        print("[*] Stopping server process...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("[+] Server stopped.")

if __name__ == "__main__":
    main()
