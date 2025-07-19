import sys
import os
import time
import random
from PyQt5.QtWidgets import QApplication
from display_window import ConversationWindow
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient
from conversation_memory import ConversationMemory
from logger import setup_logger

logger = setup_logger(name="talker", log_file="logs/talker.log")
logger.info("Talker starting up")

def run_talker(config):
    device_id = config["device_id"]
    personality_config = config["selected_personality"]
    personality = personality_config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]
    max_turns = config["conversation_turns"]
    start_delay = config.get("conversation_start_delay", 30)

    memory = ConversationMemory()
    app = QApplication(sys.argv)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "images", personality_config["image_file_name"])
    logger.info(f"Load image from {image_path}")

    window = ConversationWindow(
        background_image=image_path,
        dialog_x=personality_config.get("dialog_x", 50),
        dialog_y=personality_config.get("dialog_y", 50),
        dialog_width=personality_config.get("dialog_width", 800),
        dialog_height=personality_config.get("dialog_height", 600),
    )
    window.show()

    conversation_lines = []

    def update_display(new_line):
        conversation_lines.append(new_line)
        if len(conversation_lines) > 50:
            conversation_lines.pop(0)
        window.update_text("\n".join(conversation_lines))

    idle_thoughts = generate_idle_thoughts(
        personality,
        config["idle_thought_count"],
        api_key,
        model
    )

    conversation_active = False
    waiting_for_reply = False
    last_prompt_time = time.time()
    conversation_turns = 0

    def on_reply(message):
        nonlocal conversation_active, waiting_for_reply, last_prompt_time, conversation_turns
        #update_display(f"[Listener] {message}")
        logger.debug(f"[Listener] {message}")
        memory.add_assistant_message(message)
        waiting_for_reply = False
        time.sleep(5)

        if conversation_turns >= max_turns:
            update_display("That was a nice chat. I'm going idle now.")
            conversation_active = False
            return

        response = generate_response(
            system_prompt=f"You are a {personality}. Continue the conversation naturally.",
            user_input=message,
            history=memory.get(),
            model=model,
            api_key=api_key
        )

        logger.debug(f"{response}")
        update_display(f"{response}")
        memory.add_user_message(response)
        mqtt.publish(response)
        conversation_turns += 1
        waiting_for_reply = True
        last_prompt_time = time.time()

    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],
        topic_out=config["topics"]["chat_out"],
        on_message_callback=on_reply
    )
    mqtt.connect()

    update_display(f"[{device_id}] Entering idle mode...")

    try:
        while True:
            if not conversation_active:
                if time.time() - last_prompt_time > start_delay:
                    topic_prompt = random.choice(config["topics"]["prompt_starters"])
                    memory.clear()
                    memory.add_user_message(topic_prompt)
                    mqtt.publish(topic_prompt)
                    update_display(f"[Talker] {topic_prompt}")
                    conversation_active = True
                    waiting_for_reply = True
                    conversation_turns = 1
                    last_prompt_time = time.time()
                else:
                    thought = random.choice(idle_thoughts)
                    update_display(f"[{device_id} thinks] {thought}")
            else:
                if waiting_for_reply and (time.time() - last_prompt_time > 60):
                    update_display("[Talker] I guess nobody wants to talk. Going idle.")
                    conversation_active = False
                    memory.clear()
                    last_prompt_time = time.time()

            time.sleep(random.randint(*config["idle_interval_range"]))
    except KeyboardInterrupt:
        mqtt.disconnect()
        update_display("[System] Talker stopped.")
        sys.exit()

if __name__ == "__main__":
    from config_loader import load_config
    run_talker(load_config())
