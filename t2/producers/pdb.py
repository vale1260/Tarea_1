from kafka import KafkaProducer
from json import dumps
import time
import threading
import argparse
import random
import string
import atexit
import sqlite3
con = sqlite3.connect("/usr/src/app/db/maestros2.db", check_same_thread=False)
cur = con.cursor()

servidores_bootstrap = 'kafka:9092'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')  # Se agregó un serializador para manejar directamente los diccionarios.
)

total = 0

def generar_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(1, 20)))

# Mapeo de unidades a números de partición
estado_del_pago = {
    'pagado': 0,
    'no_pagado': 1
}

def enviar_formulario():
    topic = 'formulario'  # Updated for consistency
    while True:
        pagar = input("Quiere pagar? (si/no): ").strip().lower()
        id_m = generar_id()
        formulario = input("Como te llamas?")

        if pagar == "si":
            paid = 'pagado'
            print(f"Tu id es: {id_m}")
        elif pagar == "no":
            paid = 'no_pagado'
            time.sleep(5)
            print(f"Tu id es: {id_m}")

        try:
            particion = estado_del_pago[paid]
            mensaje = {
                "id": id_m,
                "nombre": formulario,
                "estado": paid
            }
            productor.send(topic, value=mensaje, partition=particion)
            print(f"Enviando JSON a la partición {particion}: {mensaje}")
        except KeyError:
            print(f"Estado de pago '{paid}' no mapeado a ninguna partición")
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")


def enviar_inventario():
    topic = 'inventario'  # Actualizado para consistencia
    id_m = input("Enter the 'id' value: ")

    while True:
        cur.execute("SELECT inventario FROM masters WHERE id = ?", (id_m,))     
        result = cur.fetchone()
        inventario = result[0]
        if inventario == 0:        
            
            mensaje = {
                "id": id_m,
                "inventario": inventario
            }
            productor.send(topic, mensaje)  # Se envía el diccionario directamente gracias al serializador
            print('Enviando JSON:', mensaje)
            time.sleep(3)

def enviar_venta():
    topic = 'venta'  # Actualizado para consistencia
    id_m = input("Enter the 'id' value: ")
    global total
    total += 1 
    while True:
        cur.execute("UPDATE masters SET inventario = inventario - 1 WHERE id = ?", (id_m,))
        con.commit()        
        venta = 'venta_realizada'              
        mensaje = {
            "id": id_m,
            "venta": venta,
            "total": total
        }
        productor.send(topic, mensaje)  # Se envía el diccionario directamente gracias al serializador

        cur.execute("SELECT inventario FROM masters WHERE id = ?", (id_m,))
        result = cur.fetchone()
        if result is not None:
            new_inventario = result[0]
            print(f"Updated 'inventario' for ID {id_m}: {new_inventario}")      

        print('Enviando JSON:', mensaje)
        sleep_time = random.choice([5, 6, 7])
        time.sleep(sleep_time)
        total += 1
        time.sleep(3)

def print_total_on_exit():
    print(f"Total ventas: {total}")
    print(f"Ganancias: {total * 1000}")

# Register the 'enviar_venta' function to run on script exit
atexit.register(print_total_on_exit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_threads", type=int, help="Número de hilos a crear")
    parser.add_argument("topic", type=str, help="Topic a usar")  # Nuevo argumento para el topic
    args = parser.parse_args()

    topic_to_function = {  # Mapeo de topics a funciones
        'formulario': enviar_formulario,
        'inventario': enviar_inventario,
        'venta': enviar_venta
    }

    funcion_envio = topic_to_function.get(args.topic)  # Obtener la función basada en el topic

    if funcion_envio is not None:  # Verificar si la función existe
        threads = []
        for _ in range(args.num_threads):
            t = threading.Thread(target=funcion_envio)
            t.start()
            threads.append(t)

        # Esperar a que todos los hilos finalicen
        for t in threads:
            t.join()
    else:
        print(f"El topic {args.topic} no es válido.")