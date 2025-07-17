import time
import random
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient

def run_talker(config):
    device_id = config["device_id"]
    personality = config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]

    # Load idle thoughts
    idle_thoughts = generate_idle_thoughts(personality, config["idle_thought_count"], api_key, model)

    # Track conversation state
    conversation_active = False
    history = []

    def on_reply(message):
        nonlocal conversation_active, history, waiting_for_reply
        if not conversation_active:
            return

        print(f"[{device_id}] Received reply: {message}")
        waiting_for_reply = False  # ✅ Mark that we got something
        history.append({"role": "assistant", "content": message})
        time.sleep(5)

        response = generate_response(
            f"You are a {personality}. Continue the conversation.", 
            message, 
            history=history,
            model=model, 
            api_key=api_key
        )
        history.append({"role": "user", "content": response})
        print(f"[{device_id}] Responding with: {response}")
        mqtt.publish(response)

    # Start MQTT
    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],
        topic_out=config["topics"]["chat_out"],
        on_message_callback=on_reply
    )
    mqtt.connect()

    print(f"[{device_id}] Starting in idle mode...")

    try:
        start_time = time.time()
        delay_to_start = config.get("conversation_start_delay", 10)
        reply_timeout = 60  # seconds to wait for response
        waiting_for_reply = False
        last_prompt_time = None

        while True:
            current_time = time.time()

            if not conversation_active and current_time - start_time >= delay_to_start:
                topic_prompt = random.choice([
                    "Let's talk about dreams.",
                    "Do you think AI can fall in love?",
                    "What's your opinion on pineapple pizza?",
                    "How would you explain 'consciousness'?"
                ])
                print(f"[{device_id}] Starting conversation: {topic_prompt}")
                history = [{"role": "user", "content": topic_prompt}]
                print(f"[{device_id}] Publishing to {config['topics']['chat_out']}: {topic_prompt}")
                mqtt.publish(topic_prompt)
                conversation_active = True
                waiting_for_reply = True
                last_prompt_time = current_time

            elif conversation_active and waiting_for_reply:
                if current_time - last_prompt_time > reply_timeout:
                    print(f"[{device_id}] I guess nobody wants to talk right now.")
                    conversation_active = False
                    waiting_for_reply = False
                    start_time = time.time()  # restart idle cycle

            else:
                # Idle behavior
                thought = random.choice(idle_thoughts)
                print(f"[{device_id} thinks] {thought}")
                time.sleep(random.randint(*config["idle_interval_range"]))


    except KeyboardInterrupt:
        mqtt.disconnect()
        print("\n[System] Talker stopped.")
