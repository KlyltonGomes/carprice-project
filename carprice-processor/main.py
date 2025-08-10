from bd.db import engine
from models import Base
from rabbitmq.consumer import start_consumer

if __name__ == "__main__":
    try:
        print("Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas.")
    except Exception as e:
        print(f"Erro criado tabelas: {e}")

    start_consumer()
