"""Configuration management using YAML files and environment variable overrides."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict
import yaml

ROOT_DIR = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT_DIR / "configs"


def load_config(config_name: str) -> Dict[str, Any]:
    """Load a YAML config file by name (e.g. 'project.yaml' or 'project')."""
    if not config_name.endswith(".yaml") and not config_name.endswith(".yml"):
        config_name = f"{config_name}.yaml"
    path = CONFIG_DIR / config_name
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def get_project_config() -> Dict[str, Any]:
    """Retrieve master project configuration."""
    return load_config("project.yaml")


def get_data_config() -> Dict[str, Any]:
    """Retrieve data pipeline configuration."""
    return load_config("data.yaml")


def get_training_config() -> Dict[str, Any]:
    """Retrieve training and optimizer configuration."""
    return load_config("training.yaml")


def get_models_config() -> Dict[str, Any]:
    """Retrieve model zoo configuration."""
    return load_config("models.yaml")


def get_hardware_config() -> Dict[str, Any]:
    """Retrieve hardware detection and memory configuration."""
    return load_config("hardware.yaml")


def get_visualization_config() -> Dict[str, Any]:
    """Retrieve plotting and aesthetics configuration."""
    return load_config("visualization.yaml")


class ConfigManager:
    """Convenience class for accessing configuration dictionaries."""
    load = staticmethod(load_config)
    project = staticmethod(get_project_config)
    data = staticmethod(get_data_config)
    training = staticmethod(get_training_config)
    models = staticmethod(get_models_config)
    hardware = staticmethod(get_hardware_config)
    visualization = staticmethod(get_visualization_config)

