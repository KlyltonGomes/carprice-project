import json
import os
import pika
from pika import connection


def publicar_dados_producer(dados_carro:dir):
    connection_parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=5672,
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER'),
            password=os.getenv('RABBITMQ_PASS')
        )
    )

    connection = pika.BlockingConnection(connection_parameters)
    #pika.ConnectionParameters(host="localhost", port=5672)

    channel = connection.channel()

    queue_name = os.getenv('RABBITMQ_QUEUE')

    channel.queue_declare(queue=queue_name, durable=True)

    # EXCHANGER
    channel.exchange_declare(
        exchange='scraper_exchanger',
        exchange_type='fanout',
        durable=True
    )
    # BINDING
    channel.queue_bind(
        exchange='scraper_exchanger',
        queue='carprice_queue',
        routing_key=queue_name
    )
    #transforma dir vindo do scraper em bite
    mensagem = json.dumps(dados_carro)

    # PRODUCER
    channel.basic_publish(
        exchange='scraper_exchanger',
        routing_key=queue_name,
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2
        )

    )

    print("Mensagem enviada com sucesso")

    connection.close()
