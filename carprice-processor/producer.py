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

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

queue_name = os.getenv('RABBITMQ_QUEUE')

channel.queue_declare(queue=queue_name, durable=True)


channel.exchange_declare(
    exchange='scraper_exchanger',
    exchange_type='direct',
    durable=True
)

channel.queue_bind(
    exchange='scraper_exchanger',
    queue='carprice_queue',
    routing_key=queue_name
)

channel.basic_publish(
    exchange='scraper_exchanger',
    routing_key=queue_name,
    body='Hello world!',
    properties=pika.BasicProperties(
        delivery_mode=2
    )

)

print("Mensagem enviada com sucesso")

connection.close()
