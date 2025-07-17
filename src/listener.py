import time
import random
from chatgpt_handler import generate_idle_thoughts

def run_listener(config):
    print(f"[{config['device_id']}] Running in TALKER mode with personality: {config['personality']}")
    
    # Load idle thoughts
    thoughts = generate_idle_thoughts(
        personality=config["personality"],
        count=config["idle_thought_count"],
        api_key=config["openai"]["api_key"],
        model=config["openai"]["model"]
    )

    print("\nEntering idle mode. Press Ctrl+C to stop.\n")
    try:
        while True:
            thought = random.choice(thoughts)
            print(f"[{config['device_id']} thinks] {thought}")

            min_delay, max_delay = config.get("idle_interval_range", [15, 45])
            delay = random.randint(min_delay, max_delay)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[System] Idle mode stopped.")
