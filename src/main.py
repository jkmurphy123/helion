import sys
import yaml
from talker import run_talker
from listener import run_listener

def load_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config_path = "device_config.yaml"
    config = load_config(config_path)
    mode = config.get("role", "talker")

    if mode == "talker":
        run_talker(config)
    else:
        run_listener(config)

if __name__ == "__main__":
    main()
