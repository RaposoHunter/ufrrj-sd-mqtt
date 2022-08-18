import os
from queue import Empty, Queue
from dotenv import load_dotenv
from threading import Thread

import config.mqtt as mqtt

load_dotenv()

broker = os.getenv('MQTT_HOSTNAME')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')
client_id = f'{os.getenv("APP_NAME")}-sub0'

queue = Queue()

def mqttClient():    
    client = mqtt.connect_mqtt(queue, client_id, username, password, broker, port)
    client.loop_start()
    mqtt.subscribe(topic, client, 1)

def readQueue():
    while(True):
        try:
            message = queue.get(timeout=5)

            print(message)
        except Empty as e:
            # Handle empty queue here
            print('Fila vazia')
        except Exception as e:
            print('Erro na thread de ler fila')

if __name__ == '__main__':
    mqttThread = Thread(target=mqttClient)
    mqttThread.start()

    readThread = Thread(target=readQueue)
    readThread.start()