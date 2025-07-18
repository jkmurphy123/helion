import sys
import time
from PyQt5.QtWidgets import QApplication
from display_window import ConversationWindow
from chatgpt_handler import generate_response
from mqtt_handler import MQTTClient
from conversation_memory import ConversationMemory

def run_listener(config):
    device_id = config["device_id"]
    personality = config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]

    memory = ConversationMemory()
    app = QApplication(sys.argv)
    window = ConversationWindow()
    conversation_lines = []

    def update_display(new_line):
        conversation_lines.append(new_line)
        if len(conversation_lines) > 50:
            conversation_lines.pop(0)
        window.update_text("\n".join(conversation_lines))

    def on_prompt(message):
        update_display(f"[Talker] {message}")
        memory.add_user_message(message)

        time.sleep(5)

        response = generate_response(
            system_prompt=f"You are a {personality}. Respond in character and stay on topic.",
            user_input=message,
            history=memory.get(),
            model=model,
            api_key=api_key
        )

        update_display(f"[Listener] {response}")
        memory.add_assistant_message(response)
        mqtt.publish(response)

    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],
        topic_out=config["topics"]["chat_out"],
        on_message_callback=on_prompt
    )
    mqtt.connect()

    update_display(f"[{device_id}] Waiting in idle mode...")

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        mqtt.disconnect()
        update_display("[System] Listener stopped.")
        sys.exit()

if __name__ == "__main__":
    from config_loader import load_config
    run_listener(load_config())