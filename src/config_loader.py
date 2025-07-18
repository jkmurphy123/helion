import yaml
import random
import os

def load_config(filename="device_config.yaml"):
    # Resolve path relative to this file
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)

    with open(full_path, "r") as file:
        config = yaml.safe_load(file)

    # Select a random personality
    if "personalities" in config:
        selected = random.choice(config["personalities"])
        config["selected_personality"] = selected
    else:
        raise ValueError("No personalities defined in config")

    return config
