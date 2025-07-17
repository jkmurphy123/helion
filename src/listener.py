import time
import random
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient

def run_listener(config):
    device_id = config["device_id"]
    personality = config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]

    idle_thoughts = generate_idle_thoughts(personality, config["idle_thought_count"], api_key, model)

    def on_message(message):
        print(f"[{device_id}] Received: {message}")
        time.sleep(5)

        response = generate_response(
            f"You are a {personality}. Respond to the message appropriately.",
            message,
            history=None,
            model=model,
            api_key=api_key
        )
        #print(f"[{device_id}] Responding with: {response}")
        mqtt.publish(response)

    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],
        topic_out=config["topics"]["chat_out"],
        on_message_callback=on_message
    )
    mqtt.connect()

    print(f"[{device_id}] Waiting in idle mode...")

    try:
        while True:
            thought = random.choice(idle_thoughts)
            #print(f"[{device_id} thinks] {thought}")
            time.sleep(random.randint(*config["idle_interval_range"]))
    except KeyboardInterrupt:
        mqtt.disconnect()
        print("\n[System] Listener stopped.")
