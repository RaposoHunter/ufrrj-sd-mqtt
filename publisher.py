import os
from queue import Empty, Queue
from dotenv import load_dotenv

import config.mqtt as mqtt

load_dotenv()

broker = os.getenv('MQTT_HOSTNAME')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')
client_id = f'{os.getenv("APP_NAME")}-pub'

QUEUE=None

def run(queue):
    QUEUE=queue
    
    # TODO: Testar se a fila enviada para o método connect_mqtt() é atualizada no contexto do módulo
    mqtt.connect_mqtt(queue, client_id, username, password, broker, port)
    readSensor()

    # client = mqtt.connect_mqtt(queue, client_id, username, password, broker, port)
    # client.loop_start()
    # mqtt.publish(topic, client, 1)

def readSensor():
    while True:
        try: 
            message = QUEUE.get()
            print(message)
        except Empty:
            print('Fila vazia')
    

if __name__ == '__main__':
    run()