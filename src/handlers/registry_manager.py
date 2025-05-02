import json
import os
from pathlib import Path
import sys

from utils.config_reader import load_config


def load_registry():
    conf = load_config()
    REGISTRY_FILE = Path(conf["Paths"]["REGISTRY_FILE"])
    if not os.path.exists(REGISTRY_FILE):
        print(f"Registry file {REGISTRY_FILE} not found.")
        sys.exit(1)
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg: list[dict]):
    """Persist registry back to disk."""
    conf = load_config()
    REGISTRY_FILE = Path(conf["Paths"]["REGISTRY_FILE"])
    CONFIG_ROOT = Path(conf["Paths"]["CONFIG_ROOT"])
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2))
    pass
