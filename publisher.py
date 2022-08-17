import os
import random
from dotenv import load_dotenv

import config.mqtt as mqtt

load_dotenv()

broker = os.getenv('MQTT_HOSTNAME')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')
client_id = f'{os.getenv("APP_NAME")}-pub'

def run():
    client = mqtt.connect_mqtt(client_id, username, password, broker, port)
    client.loop_start()
    mqtt.publish(topic, client, 1)

if __name__ == '__main__':
    run()