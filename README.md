# helion
getting 2 raspberry pi's to talk to each other in different personalities

├── config/
│   └── device_config.yaml        # Device-specific settings
├── src/
│   ├── __init__.py
│   ├── main.py                   # Entry point, loads config and starts mode
│   ├── talker.py                 # Talker mode logic (placeholder)
│   ├── listener.py               # Listener mode logic (placeholder)
│   ├── chatgpt_handler.py        # Handles GPT requests, including idle thoughts
│   └── mqtt_handler.py           # MQTT client setup
├── requirements.txt              # Install with pip install -r requirements.txt

