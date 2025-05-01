import configparser
from pathlib import Path


def load_config():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent.parent / "config.ini")
    return config
