import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, client_id, broker, port, topic_in, topic_out, on_message_callback):
        self.client = mqtt.Client(client_id)
        self.broker = broker
        self.port = port
        self.topic_in = topic_in
        self.topic_out = topic_out
        self.on_message_callback = on_message_callback

        self.client.on_connect = self.on_connect
        self.client.on_message = self.handle_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Connected to {self.broker}:{self.port} with result code {rc}")
        client.subscribe(self.topic_in)

    def handle_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        print(f"[MQTT] Received: {message}")
        self.on_message_callback(message)

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, message):
        print(f"[MQTT] Sending: {message}")
        self.client.publish(self.topic_out, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
