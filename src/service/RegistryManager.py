import json
import os
import sys

from main import CONFIG_ROOT, REGISTRY_FILE


class RegistryManager:

    @staticmethod
    def load_registry():
        if not os.path.exists(REGISTRY_FILE):
            print(f"Registry file {REGISTRY_FILE} not found.")
            sys.exit(1)
        with open(REGISTRY_FILE) as f:
            return json.load(f)

    @staticmethod
    def save_registry(reg: list[dict]):
        """Persist registry back to disk."""
        CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
        REGISTRY_FILE.write_text(json.dumps(reg, indent=2))
        pass
