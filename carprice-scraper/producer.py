import json
import os
import pika
import logging
from dotenv import load_dotenv
load_dotenv()

#level=logging.WARNING
#level=logging.DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def publicar_dados_producer(dados_carro:dict):
    """
    Publica dados no RabbitMQ via exchange e fila configuradas.

    Esta função recebe uma lista de dicionários contendo dados dos carros,
    conecta-se ao RabbitMQ usando as variáveis de ambiente para host, usuário e senha,
    declara a exchange e a fila, faz o binding, e publica a mensagem em formato JSON.

    Args:
        dados_carro (List[Dict]): Lista de dicionários com os dados dos carros a serem enviados.

    Raises:
        pika.exceptions.AMQPConnectionError: Caso a conexão com o RabbitMQ falhe.

    Mini tutorial de como conectar e publicar no RabbitMq!
    Primeiro crie um arquivo .py e dentro uma função que recebe como argumento dados do tipo dict.
    Essa será a função para publicar os dados no PRODUCER do RabbitMQ.

    .. code-block:: python

        def publicar_dados_producer(argumento:dict):


    Primeiro passando o parametro e credencial do RabbitMQ, crie um arquivo .env na raiz do projeto
    onde serão armazenadas as suas informações pessoais.

    exemplo:
    Crie um arquivo .env e adicione esse script


    .. code-block:: python

        RABBITMQ_HOST=rabbitmq
        RABBITMQ_USER=user
        RABBITMQ_PASS=password
        RABBITMQ_QUEUE=nome_da_queue


    Criando uma conexão entre seu código Python e o servidor RabbitMQ

    import 'os' para usar os.getenv, assim terá acesso aos dados do seu .env

    .. code-block:: python

        connection_parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=5672,
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER'),
            password=os.getenv('RABBITMQ_PASS')
        ))



    Abre uma conexão TCP síncrona (bloqueante) entre seu programa Python e o servidor RabbitMQ, usando os parâmetros de conexão (host, porta, usuário, senha)
    definidos em connection_parameters.

    .. code-block:: python

        connection = pika.BlockingConnection(connection_parameters)


    canal é uma via de comunicação leve para enviar e receber mensagens. Você pode ter vários canais na mesma conexão, e o RabbitMQ recomenda usar canais para operações

    .. code-block:: python

        channel = connection.channel()



    cria uma fila no RabbitMQ com o nome especificado no arquivo .env

    -> RABBITMQ_QUEUE=nome_da_queue

    queue=queue_name - > atribui o nome a fila que será declarada!

    durable=True -> caso o servidor reinicialize a fila ainda existirá!

    .. code-block:: python

        queue_name = os.getenv('RABBITMQ_QUEUE')
        channel.queue_declare(queue=queue_name, durable=True)


    Declaração de um EXCHANGE:
    Um exchange é o roteador da mensageria no RabbitMQ.

    Ele é responsável por receber mensagens dos produtores e encaminhá-las para as filas apropriadas,
    com base nas regras definidas pelos bindings.

    .. code-block:: python

        channel.exchange_declare(
        exchange='scraper_exchanger',
        exchange_type='fanout',
        durable=True )




    Um binding é uma ligação entre um exchange e uma fila no RabbitMQ. Ele define a regra ou critério que o exchange usa para encaminhar mensagens para essa fila específica.
    Sem bindings, as mensagens enviadas para um exchange não seriam entregues a nenhuma fila.

    .. code-block:: python

        channel.queue_bind(
        exchange='scraper_exchanger',
        queue='carprice_queue',
        routing_key=queue_name )


    Converte o objeto Python dados_carro (dicionário) em uma string JSON, json.dumps() significa "dump string", transforma o dado em uma representação textual JSON.
    RabbitMQ trabalha com mensagens em formato texto ou bytes.

    .. code-block:: python

          mensagem = json.dumps(dados_carro)

    O producer é o responsável por enviar mensagens para o sistema de mensageria RabbitMQ.
    Envia a mensagem para a fila. -> queue='carprice_queue'

    .. code-block:: python

        channel.basic_publish(
        exchange='scraper_exchanger',
        routing_key=queue_name,
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2
        )

    Poucas mensagens → abre e fecha rápido.

    Muitas mensagens → abre e mantém aberta.

    .. code-block:: python

        connection.close()


    Conexão curta → você cria e fecha a conexão dentro da função que publica.

    Cada vez que chama a função, abre/fecha a conexão.

    .. code-block:: python

        def publicar_dados_producer(dados_carro):
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key='fila', body='msg')
        connection.close()


    Conexão longa → você cria a conexão uma vez fora da função e só fecha no final.

    A conexão fica aberta enquanto o programa roda.

    .. code-block:: python

        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        def publicar_dados_producer(dados_carro):
        channel.basic_publish(exchange='', routing_key='fila', body='msg')

        #Loop enviando mensagens...
        for carro in carros:
            publicar_dados_producer(carro)

        connection.close()

    Para o CarPrice-project que pode capturar vários carros por vez, o ideal é abrir a conexão antes de começar a publicar e fechá-la só no final.

    Para o projeto seria uma conexão longa,

    pois se abrir e fechar a conexão para cada carro (Conexão curta)

    .Vai ter mais latência por mensagem

    .Pode sobrecarregar o RabbitMQ com muitas conexões curtas

    .Pode dar erros de “connection reset” se for muito rápido

    """
    connection_parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=os.getenv('RABBITMQ_PORT'),
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER'),
            password=os.getenv('RABBITMQ_PASS')
        )
    )


    connection = pika.BlockingConnection(connection_parameters)

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


    logging.info(f"Mensagem enviada com sucesso")


    connection.close()
