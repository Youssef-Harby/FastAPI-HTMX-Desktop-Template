import yaml
from pathlib import Path
import sys


# def get_bundled_path(relative_path):
#     if hasattr(sys, "_MEIPASS"):
#         return Path(sys._MEIPASS) / relative_path
#     else:
#         return Path(relative_path)


# Load the YAML configuration file
def load_config():
    config_path = Path("config.yaml")
    with config_path.open() as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config()
