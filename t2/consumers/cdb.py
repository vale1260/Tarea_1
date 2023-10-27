from kafka import KafkaConsumer
import json  # Agrega la importación de json para deserializar los mensajes
import sqlite3
con = sqlite3.connect("/usr/src/app/db/maestros2.db", check_same_thread=False)
cur = con.cursor()

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
        cur.execute("""
            INSERT INTO masters (id, nombre, inventario, ventas)
            VALUES (?, ?, ?, ?)
            """, (id_m, nombre, 0, 0))
        con.commit()

    elif msg.topic == 'inventario':
        id_m = msg.value.get('id')
        cur.execute("""
            UPDATE masters
            SET inventario = 10
            WHERE id = ?
            """, (id_m,))
        con.commit()        
        print("Resupliendo inventario")

    elif msg.topic == 'venta':
        id_m = msg.value.get('id')
        total = msg.value.get('total')
        cur.execute("""
            UPDATE masters
            SET ventas = ?
            WHERE id = ?
            """, (total, id_m))
        con.commit()        
        print(f"Numero de ventas: {total}")