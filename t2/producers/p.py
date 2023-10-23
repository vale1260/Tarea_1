from kafka import KafkaProducer
from json import dumps
import time
import threading
import argparse
import random
import logging
import atexit

servidores_bootstrap = 'kafka:9092'
topic_prueba = 'prueba'

productor = KafkaProducer(bootstrap_servers=[servidores_bootstrap])

latency_results = []

# Shared variable to signal threads to stop
stop_threads = False

# Configure the logging format and level
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s')

def enviar_prueba(throughput):
    topic = topic_prueba
    start_time = time.time()
    messages_sent = 0

    while not stop_threads:
        mensaje = {
            "timestamp": int(time.time()),
        }
        json_mensaje = dumps(mensaje).encode('utf-8')
        productor.send(topic, json_mensaje)

        messages_sent += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        expected_messages = int(throughput * elapsed_time)

        if messages_sent < expected_messages:
            sleep_time = (expected_messages - messages_sent) / throughput
            time.sleep(sleep_time)
        else:
            time.sleep(0.001)  # Sleep briefly to avoid busy waiting

        # Log progress
        logging.info(f'Messages Sent: {messages_sent}, Time Elapsed: {elapsed_time:.2f}s')

def export_metrics():
    with open('latency.txt', 'w') as f:
        f.write("Latency Results:\n")
        for latency in latency_results:
            f.write(f"{latency}\n")

atexit.register(export_metrics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_threads", type=int, help="Number of threads to create")
    parser.add_argument("throughput", type=float, help="Messages per second (throughput)")
    args = parser.parse_args()

    funciones_envio = [
        enviar_prueba
    ]

    threads = []
    for _ in range(args.num_threads):
        funcion_envio = random.choice(funciones_envio)
        t = threading.Thread(target=funcion_envio, args=(args.throughput,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Set the stop_threads variable to signal the threads to stop
    stop_threads = True
