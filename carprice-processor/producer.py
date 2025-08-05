import os
import pika

connection_parameters = pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    port=5672,
    credentials=pika.PlainCredentials(
        username=os.getenv('RABBITMQ_USER'),
        password=os.getenv('RABBITMQ_PASS')
    )
)
#abrir conexao
connection = pika.BlockingConnection(connection_parameters)

#abrir canal e conectar o rabbit e declarar o nome da fila
channel = connection.channel()
channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))