import json
import os
from pathlib import Path
import sys

from utils.config_reader import load_config


def load_registry() -> list:
    conf = load_config()
    REGISTRY_FILE = Path(conf["Paths"]["REGISTRY_FILE"])
    if not os.path.exists(REGISTRY_FILE):
        return []  # Return empty list if file doesn't exist
    with open(REGISTRY_FILE) as f:
        data = json.load(f)
        return [] if data == {} else data  # Convert empty dict to empty list


def save_registry(reg: list[dict]):
    """Persist registry back to disk."""
    conf = load_config()
    REGISTRY_FILE = Path(conf["Paths"]["REGISTRY_FILE"])
    CONFIG_ROOT = Path(conf["Paths"]["CONFIG_ROOT"])
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2))
