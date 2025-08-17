import json
import os
import time
import pika
from sqlalchemy.exc import IntegrityError
from bd.db import SessionLocal
from models import Carro
from schemas import CarroItem

params = pika.ConnectionParameters(
    host=os.getenv("RABBITMQ_HOST", "localhost"),
    port=int(os.getenv("RABBITMQ_PORT", 5672)),
    credentials=pika.PlainCredentials(
        username=os.getenv("RABBITMQ_USER", "guest"),
        password=os.getenv("RABBITMQ_PASS", "guest")
    )
)
connection = pika.BlockingConnection(params)


#RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "carprice_queue")

def process_message(ch, method, properties, body):
    session = SessionLocal()
    try:
        data = json.loads(body)
        car = CarroItem(**data)
        db_car = Carro(
            id=car.id,
            veiculo=car.nome,
            afiliado=car.afiliado,
            lp=car.lp,
            locadora=car.locadora,
            categoria=car.categoria,
            subcategoria=car.subcategoria,
            pais=car.pais,
            tipo=car.tipo,
            mercado=car.mercado,
            local_id=car.local_id,
            local_nome=car.local_nome,
            preco=car.preco,
            quantidade=car.quantidade,
        )
        session.merge(db_car)
        session.commit()
        print(f"Carro salvo: {car.nome}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (json.JSONDecodeError, IntegrityError) as e:
        session.rollback()
        print(f"Erro ao salvar carro: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    finally:
        session.close()

def start_consumer():
    for attempt in range(10):
        try:
            #params = pika.URLParameters(RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
            break
        except pika.exceptions.AMQPConnectionError:
            print(f"Tentativa {attempt+1}/10: RabbitMQ não disponível, tentando novamente...")
            time.sleep(5)
    else:
        print("Não foi possível conectar ao RabbitMQ")
        return

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)
    print("Esperando mensagens...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
