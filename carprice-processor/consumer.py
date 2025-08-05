import json
import os
import time
import pika
from schemas import CarItem
from db import SessionLocal
from models import Car
from sqlalchemy.exc import IntegrityError

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "carprice_queue")


def process_message(ch, method, properties, body):
    session = SessionLocal()
    try:
        data = json.loads(body)
        car = CarItem(**data)
        db_car = Car(
            id=car.id,
            nome=car.nome,
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
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    # Espera o RabbitMQ ficar pronto
    for attempt in range(10):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
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
