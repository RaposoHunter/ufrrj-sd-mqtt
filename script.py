from queue import Queue
from threading import Thread

import bme280
import publisher

# Criar Thread para Sensor
# Criar Thread para leitura de erros
# Criar Thread para envio de erros
# OPCIONAL - Criar Thread para envio dos dados

readings_queue = Queue(maxsize=10)
errors_queue = Queue(maxsize=10) # maxsize <= 0 === Infinite

def main():
    # sensor_thread = Thread(target=bme280.main, args=[readings_queue, errors_queue])
    # sensor_thread.start()

    publisher_thread = Thread(target=publisher.run, args=[errors_queue])
    publisher_thread.start()

    # errors_thread = Thread(target=None, args=errors_thread)
    # errors_thread.start()


if __name__=="__main__":
   main()