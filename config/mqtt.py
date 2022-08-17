from pickle import TRUE
from re import M
import time
import os
import json
from paho.mqtt import client as mqtt

def connect_mqtt(client_id, username="", password="", broker="localhost", port=1883, transport='tcp'):
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_subscribe(client, userdata, mid, granted_qos, properties=None):
        print(f'Subscribed: {str(mid)} {str(granted_qos)}')

    def on_message(client, userdata, message):
        print(f'Received message: `{str(message.payload)}`')

    # Set Connecting Client ID
    client = mqtt.Client(client_id, userdata=None, protocol=mqtt.MQTTv5)
    client.username_pw_set(username, password)
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    if(transport == 'websockets'):
        client.ws_set_options('/mqtt', {
            "port": 9001
        })

    client.connect(broker, port)
    
    return client

def publish(topic, client, qos=1):
     msg_count = 0

     while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg, qos)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            details = {
                "result": result[0],
                "message": msg.split(':')[1], 
            }

            print(f"Failed to send message to topic {topic}")
            os.system(f'echo {json.dumps(details)} >> ./logs/mqtt.log')
        msg_count += 1

def subscribe(topic, client, qos=1):
    result = client.subscribe(topic, qos)

    status = result[0]
    if status == 0:
        print(f"Client subscribed to topic `{topic}`")

        while True:
            pass
    else:
        print(f"Failed to subscribe to topic `{topic}`")
