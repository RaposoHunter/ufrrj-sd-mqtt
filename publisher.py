import os
import config.mqtt as mqtt
from queue import Empty, Queue
from dotenv import load_dotenv

load_dotenv()

broker = os.getenv('MQTT_HOSTNAME')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')
client_id = f'{os.getenv("APP_NAME")}-pub'

def run(queue: Queue):
    client = mqtt.connect_mqtt(client_id, username, password, broker, port)
    client.loop_start()

    while True:
        try:
            error = queue.get(timeout=5)

            mqtt.publish(topic, error, client)
        except Empty:
            # Nenhum erro na fila...
            pass
        except:
            print('Algo deu errado ao ler a fila de erros. Tente novamente mais tarde!')
