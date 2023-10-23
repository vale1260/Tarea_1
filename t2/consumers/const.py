from kafka import KafkaConsumer
import json  # Agrega la importación de json para deserializar los mensajes

servidores_bootstrap = 'kafka:9092'
topics = ['formulario', 'inventario', 'venta']

grupo_consumidores = 'grupo_consumidores'

# Configurar el consumidor con el group_id y añadir deserializador de json
consumer = KafkaConsumer(
    *topics,
    group_id=grupo_consumidores,
    bootstrap_servers=[servidores_bootstrap],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
)
ventas=0
# Consumir mensajes de los topics elegidos
for msg in consumer:
    print(f"Recibido de tópico {msg.topic}: {msg.value}")


    if msg.topic == 'formulario':
        nombre = msg.value.get('nombre')
        id_m = msg.value.get('id')
        estado = msg.value.get('estado')
        print(f"nombre: {nombre}")
        print(f"id: {id_m}")
        print(f"estado: {estado}")

    elif msg.topic == 'inventario':
        print("Resupliendo inventario")

    elif msg.topic == 'venta':
        ventas += 1
        print(f"Numero de ventas: {ventas}")
