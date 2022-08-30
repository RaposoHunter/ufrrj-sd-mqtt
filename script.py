from queue import Queue
from threading import Thread

import bme280
import publisher
import queue_broker

# Criar Thread para Sensor - FEITO
# Criar Thread para leitura de erros - FEITO
# Criar Thread para envio de erros - FEITO
# OPCIONAL - Criar Thread para envio dos dados

# readings_queue = Queue(maxsize=10)
errors_queue = Queue(maxsize=10)
publisher_queue = Queue(maxsize=10) # maxsize <= 0 === Infinite

def main():
    sensor_thread = Thread(target=bme280.main, args=[errors_queue])
    sensor_thread.start()

    queue_broker_thread = Thread(target=queue_broker.run, args=[errors_queue, publisher_queue])
    queue_broker_thread.start()

    publisher_thread = Thread(target=publisher.run, args=[publisher_queue])
    publisher_thread.start()

if __name__=="__main__":
   main()