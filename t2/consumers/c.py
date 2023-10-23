from kafka import KafkaConsumer
from json import loads
import time
import atexit

servidores_bootstrap = 'kafka:9092'
topic_prueba = 'prueba'

consumer = KafkaConsumer(topic_prueba, bootstrap_servers=[servidores_bootstrap], auto_offset_reset='earliest')

latency_results = []
throughput_results = []

def consume_messages():
    for mensaje in consumer:
        message = loads(mensaje.value.decode('utf-8'))
        timestamp = message["timestamp"]
        current_time = time.time()
        latency = current_time - timestamp
        latency_results.append(latency)
        throughput = 1 / latency  # Messages per second
        throughput_results.append(throughput)

        if len(latency_results) % 100 == 0:
            avg_latency = sum(latency_results) / len(latency_results)
            print(f"Number of messages: {len(latency_results)}, Avg Latency: {avg_latency} seconds, Throughput: {throughput} messages per second")

def export_metrics():
    with open('consumer_latency.txt', 'w') as f:
        f.write("Consumer Latency Results:\n")
        for latency in latency_results:
            f.write(f"{latency}\n")

    with open('consumer_throughput.txt', 'w') as f:
        f.write("Consumer Throughput Results:\n")
        for throughput in throughput_results:
            f.write(f"{throughput}\n")

atexit.register(export_metrics)

if __name__ == "__main__":
    consume_messages()
