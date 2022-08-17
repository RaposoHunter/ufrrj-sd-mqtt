import os
from dotenv import load_dotenv

import config.mqtt as mqtt

load_dotenv()

broker = os.getenv('MQTT_HOSTNAME')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')
client_id = f'{os.getenv("APP_NAME")}-sub0'

def run():
    client = mqtt.connect_mqtt(client_id, username, password, broker, port)
    client.loop_start()
    mqtt.subscribe(topic, client, 1)

if __name__ == '__main__':
    run()