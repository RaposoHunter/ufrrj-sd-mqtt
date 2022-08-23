from queue import Queue
import time
import os
import json
from paho.mqtt import client as mqtt

def connect_mqtt(client_id, username="", password="", broker="localhost", port=1883, transport='tcp'):
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            # TODO: Notificar de outra maneira ao usuário
            print(f'Failed to connect to MQTT Broker. Return code {rc}')

    def on_subscribe(client, userdata, mid, granted_qos, properties=None):
        print(f'Subscribed: {str(mid)} {str(granted_qos)}')

    def on_message(client, userdata, message):
        print(f'Received message: `{str(message.payload)}`')

    # Set Connecting Client ID
    client = mqtt.Client(client_id, clean_session=False, userdata=None, protocol=mqtt.MQTTv31)
    client.username_pw_set(username, password)
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    client.connect(broker, port)
    
    return client

def publish(topic, message, client: mqtt.Client, qos=1):
    result = client.publish(topic, message, qos)

    status = result[0]
    if status == 0:
        print(f"Sent `{message}` to topic `{topic}`")
    else:
        details = {
            "status": status,
            "message": message
        }

        print(f"Failed to send message to topic {topic}")
        os.system(f'echo {json.dumps(details)} >> ./logs/mqtt.log')

def subscribe(topic, client, qos=1):
    result = client.subscribe(topic, qos)

    status = result[0]
    if status == 0:
        print(f"Client subscribed to topic `{topic}`")

        while True:
            pass
    else:
        print(f"Failed to subscribe to topic `{topic}`")
