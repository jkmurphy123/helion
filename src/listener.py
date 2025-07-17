import time
import random
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient

def run_listener(config):
    device_id = config["device_id"]
    personality = config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]

    idle_thoughts = generate_idle_thoughts(
        personality,
        config["idle_thought_count"],
        api_key,
        model
    )

    history = []  # 💡 Must be declared here for use in nonlocal below

    def on_message(message):
        nonlocal history

        try:
            print(f"[{device_id}] Received: {message}")
            time.sleep(5)

            # Update history with received message
            history.append({"role": "user", "content": message})

            response = generate_response(
                system_prompt=f"You are a {personality}. Respond to the message appropriately.",
                user_input=message,
                history=history,
                model=model,
                api_key=api_key
            )

            history.append({"role": "assistant", "content": response})
            print(f"[{device_id}] Responding with: {response}")
            mqtt.publish(response)

            # Optionally limit history length
            if len(history) > 10:
                history = history[-10:]

        except Exception as e:
            print(f"[{device_id} ERROR] Exception in on_message: {e}")

    # Create MQTT client and connect
    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],       # e.g., "chat/send"
        topic_out=config["topics"]["chat_out"],     # e.g., "chat/receive"
        on_message_callback=on_message
    )
    mqtt.connect()

    print(f"[{device_id}] Waiting in idle mode...")

    try:
        while True:
            thought = random.choice(idle_thoughts)
            print(f"[{device_id} thinks] {thought}")
            time.sleep(random.randint(*config["idle_interval_range"]))
    except KeyboardInterrupt:
        mqtt.disconnect()
        print("\n[System] Listener stopped.")
