import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from display_window import DisplayWindow
from mqtt_handler import MQTTClient
from chatgpt_handler import generate_response

def run_listener(config):
    # Get personality settings
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

    topic_in = config["topics"]["chat_out"]   # Listener receives from talker here
    topic_out = config["topics"]["chat_in"]   # Listener sends to talker here
    device_id = config.get("device_id", "pi_listener")

    history = []

    def on_message(topic, message):
        nonlocal history
        print(f"[MQTT] Received from talker: {message}")
        window.display_text(message)
        history.append({"role": "user", "content": message})

        # Delay before responding
        time.sleep(5)

        response = generate_chat_response(config, history, personality)
        history.append({"role": "assistant", "content": response})
        window.display_text(response)
        mqtt.publish(topic_out, response)

    mqtt = MQTTClient(device_id, on_message)
    mqtt.connect(config["mqtt"]["broker"], config["mqtt"]["port"])
    mqtt.subscribe(topic_in)

    def idle_mode():
        thoughts = config.get("idle_thoughts", [])
        if not thoughts:
            thoughts = ["Just sitting here...", "Nothing to hear yet...", "Waiting..."]
        window.display_text(f"[Idle] {random.choice(thoughts)}")

    # Periodic idle display
    idle_timer = QTimer()
    idle_timer.timeout.connect(idle_mode)
    idle_timer.start(15000)  # show an idle thought every 15 seconds

    sys.exit(app.exec_())
