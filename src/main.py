import sys
import argparse

from config_loader import load_config
from talker import run_talker
from listener import run_listener

def main():
    # Allow optional config file override
    parser = argparse.ArgumentParser(description="AI Conversation Agent")
    parser.add_argument("--config", type=str, default="device_config.yaml", help="Path to config file")
    args = parser.parse_args()

    # Load config with selected personality
    config = load_config(args.config)

    role = config.get("role", "").lower()
    if role == "talker":
        print("[Main] Starting in TALKER mode")
        run_talker(config)
    elif role == "listener":
        print("[Main] Starting in LISTENER mode")
        run_listener(config)
    else:
        print(f"[Main] Invalid or missing role in config: '{role}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
