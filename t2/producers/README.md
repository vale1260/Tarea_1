```sh

docker compose -f docker-compose-brokers.yml up --build

python3 cdb.py

python3 pdb.py 1 formulario

kafka-topics.sh --alter --bootstrap-server kafka:9092 --partitions 2 --topic formulario

python3 pdb.py 1 inventario

python3 pdb.py 1 venta

docker compose -f docker-compose-brokers.yml down -v

```