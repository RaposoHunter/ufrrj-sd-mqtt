from queue import Empty, Full, Queue

def run(entry_queue: Queue, publisher_queue: Queue):
    while True:
        try:
            message = entry_queue.get(timeout=5)
            
            publisher_queue.put(message)
        except Empty:
            # Nenhum erro na fila...
            print('Fila vazia - queue_broker')
            # TODO: Ler arquivo de erros não adicionados na fila e enviar novamente
            pass
        except Full:
            print('Fila cheia - queue_broker')
            # TODO: Guardar a mensagem em um arquivo a ser lido futuramente
            pass
