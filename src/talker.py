import sys
import random
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from display_window import DisplayWindow
from mqtt_handler import MQTTClient
from chatgpt_handler import generate_response

def run_talker(config):
    # Get selected personality info
    personality_data = config["selected_personality"]
    personality = personality_data["personality"]
    image_file = personality_data["image_file_name"]
    dialog_x = personality_data["dialog_x"]
    dialog_y = personality_data["dialog_y"]
    dialog_width = personality_data["dialog_width"]
    dialog_height = personality_data["dialog_height"]

    # Setup GUI
    app = QApplication(sys.argv)
    window = DisplayWindow(
        image_path=image_file,
        dialog_x=dialog_x,
        dialog_y=dialog_y,
        dialog_width=dialog_width,
        dialog_height=dialog_height
    )
    window.showFullScreen()

    # Setup conversation parameters
    start_delay = config.get("conversation_start_delay", 10)
    prompt_starters = config["topics"]["prompt_starters"]
    conversation_turns = config.get("conversation_turns", 6)
    topic_out = config["topics"]["chat_out"]
    topic_in = config["topics"]["chat_in"]
    device_id = config.get("device_id", "pi_talker")

    # Setup history
    history = []

    # Setup MQTT
    def on_message(topic, message):
        nonlocal history
        print(f"[MQTT] Received from listener: {message}")
        window.display_text(message)
        history.append({"role": "user", "content": message})

        if len(history) < 2 * conversation_turns:
            time.sleep(5)
            response = generate_chat_response(config, history, personality)
            history.append({"role": "assistant", "content": response})
            window.display_text(response)
            mqtt.publish(topic_out, response)
        else:
            print("[Talker] Ending conversation, returning to idle.")
            idle_mode()

    mqtt = MQTTClient(device_id, on_message)
    mqtt.connect(config["mqtt"]["broker"], config["mqtt"]["port"])
    mqtt.subscribe(topic_in)

    def start_conversation():
        nonlocal history
        window.display_text("Starting conversation...")
        prompt = random.choice(prompt_starters)
        window.display_text(prompt)
        history = [{"role": "user", "content": prompt}]
        mqtt.publish(topic_out, prompt)

    def idle_mode():
        thoughts = config.get("idle_thoughts", [])
        if not thoughts:
            thoughts = ["Did I leave the stove on?", "I wonder what clouds taste like...", "Why is bacon so delicious?"]
        thought = random.choice(thoughts)
        window.display_text(thought)

    # Initial idle mode
    idle_mode()

    # Delay then start conversation
    QTimer.singleShot(start_delay * 1000, start_conversation)

    sys.exit(app.exec_())
