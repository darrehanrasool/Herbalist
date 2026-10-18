.PHONY: help setup test lint hardware verify-data train evaluate run clean

PYTHON ?= python3

help:
	@echo "Herbalist AI - Enterprise Command Automation"
	@echo "---------------------------------------------"
	@echo "make setup        - Verify and configure virtual environment & directories"
	@echo "make test         - Run full unit and integration test suites"
	@echo "make lint         - Run syntax and formatting linters"
	@echo "make hardware     - Run hardware and MPS/CUDA acceleration diagnostics"
	@echo "make verify-data  - Check integrity of dataset manifests and catalogs"
	@echo "make train        - Train baseline classical and deep learning models"
	@echo "make evaluate     - Run comprehensive model evaluation and audit"
	@echo "make run          - Launch interactive Flask web platform on port 5001"
	@echo "make clean        - Remove Python bytecode and temporary caches"

setup:
	$(PYTHON) scripts/setup_environment.py

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

lint:
	flake8 src tests scripts --max-line-length=120 --extend-ignore=E203,E402,W503

hardware:
	$(PYTHON) scripts/verify_hardware.py

verify-data:
	$(PYTHON) scripts/verify_datasets.py

train:
	$(PYTHON) scripts/train_all.py

evaluate:
	$(PYTHON) scripts/evaluate_all.py

run:
	$(PYTHON) -m src.herbalist.main serve --port 5001

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
