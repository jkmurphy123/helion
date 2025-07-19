import sys
import argparse

from config_loader import load_config
from talker import run_talker
from listener import run_listener
from logger import setup_logger

logger = setup_logger(name="main", log_file="logs/main.log")

def main():
    config_path = "device_config.yaml"
    config = load_config(config_path)
    role = config.get("role", "talker").lower()
    
    if role == "talker":
        logger.info("[Main] Starting in TALKER mode")
        run_talker(config)
    elif role == "listener":
        logger.info("[Main] Starting in LISTENER mode")
        run_listener(config)
    else:
        logger.error(f"[Main] Invalid or missing role in config: '{role}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
