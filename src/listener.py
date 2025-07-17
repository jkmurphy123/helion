import time
import random
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient
from conversation_memory import ConversationMemory

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

    memory = ConversationMemory(max_length=10)

    def on_message(message):
        nonlocal memory

        try:
            print(f"[{device_id}] Received: {message}")
            time.sleep(5)

            # Treat incoming message from talker as user input
            memory.add_user_message(message)

            response = generate_response(
                system_prompt=f"You are a {personality}. Respond to the message appropriately.",
                user_input=message,
                history=memory.get(),
                model=model,
                api_key=api_key
            )

            # Append response to memory
            memory.add_assistant_message(response)

            print(f"[{device_id}] Responding with: {response}")
            mqtt.publish(response)
        except Exception as e:
            print(f"[{device_id} ERROR] Exception in on_message: {e}")

    # Create MQTT client and connect
    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],       # e.g. "chat/send"
        topic_out=config["topics"]["chat_out"],     # e.g. "chat/receive"
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
