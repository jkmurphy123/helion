import time
import random
from chatgpt_handler import generate_idle_thoughts, generate_response
from mqtt_handler import MQTTClient
from conversation_memory import ConversationMemory

def run_talker(config):
    device_id = config["device_id"]
    personality = config["personality"]
    model = config["openai"]["model"]
    api_key = config["openai"]["api_key"]
    delay_to_start = config.get("conversation_start_delay", 10)
    idle_thoughts = generate_idle_thoughts(personality, config["idle_thought_count"], api_key, model)

    memory = ConversationMemory(max_length=10)
    conversation_active = False
    waiting_for_reply = False
    last_prompt_time = None
    max_turns = 0
    conversation_turns = 0
    start_time = time.time()

    def on_reply(message_from_listener):
        nonlocal conversation_active, waiting_for_reply, last_prompt_time, conversation_turns

        #print(f"[{device_id}] Received reply: {message_from_listener}")
        waiting_for_reply = False
        memory.add_assistant_message(message_from_listener)  # ← This is listener's line

        time.sleep(5)

        if conversation_turns >= max_turns:
            print(f"[{device_id}] That was a nice chat. I'm going idle now.")
            conversation_active = False
            return

        response = generate_response(
            system_prompt=f"You are a {personality}. Continue the conversation naturally.",
            user_input=message_from_listener,
            history=memory.get(),
            model=model,
            api_key=api_key
        )

        print(f"[{device_id}] Responding with: {response}")
        memory.add_user_message(response)  # ← This is talker’s next prompt
        mqtt.publish(response)
        conversation_turns += 1

    def print_conversation_history(history):
        print("\n--- Conversation History ---")
        for i, msg in enumerate(history):
            role = msg["role"]
            content = msg["content"]
            print(f"{i+1}. [{role.upper()}]: {content}")
        print("--- End of History ---\n")

    mqtt = MQTTClient(
        client_id=device_id,
        broker=config["mqtt"]["broker"],
        port=config["mqtt"]["port"],
        topic_in=config["topics"]["chat_in"],     # should be "chat/receive"
        topic_out=config["topics"]["chat_out"],   # should be "chat/send"
        on_message_callback=on_reply
    )
    mqtt.connect()

    print(f"[{device_id}] Starting idle mode...")

    try:
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
                memory = ConversationMemory(max_length=10)
                memory.add_user_message(topic_prompt)
                mqtt.publish(topic_prompt)
                conversation_active = True
                waiting_for_reply = True
                last_prompt_time = current_time
                conversation_turns = 1
                max_turns = random.randint(4, 10)
            elif conversation_active and waiting_for_reply and (current_time - last_prompt_time > 60):
                print(f"[{device_id}] No response. Going back to idle.")
                conversation_active = False
                waiting_for_reply = False
                start_time = time.time()
            else:
                thought = random.choice(idle_thoughts)
                #print(f"[{device_id} thinks] {thought}")
                time.sleep(random.randint(*config["idle_interval_range"]))
    except KeyboardInterrupt:
        mqtt.disconnect()
        print("\n[System] Talker stopped.")
