import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from logger import setup_logger

logger = setup_logger(name="mqtt_handler", log_file="logs/mqtt_handler.log")

class MQTTClient:
    def __init__(self, client_id, broker, port, topic_in, topic_out, on_message_callback):
        self.client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)

        self.broker = broker
        self.port = port
        self.topic_in = topic_in
        self.topic_out = topic_out
        self.on_message_callback = on_message_callback

        self.client.on_connect = self.on_connect
        self.client.on_message = self.handle_message

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"[MQTT] Connected with result code {rc}")
        logger.info(f"[MQTT] Subscribing to topic: {self.topic_in}")
        client.subscribe(self.topic_in)

    def handle_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        logger.info(f"[MQTT] Received: {message}")
        self.on_message_callback(message)

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, message):
        logger.info(f"[MQTT] Sending: {message}")
        self.client.publish(self.topic_out, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
