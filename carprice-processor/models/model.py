from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Carro(Base):
    __tablename__ = "carros"
    id = Column(String, primary_key=True)
    veiculo = Column(String)
    afiliado = Column(String)
    lp = Column(Integer)
    locadora = Column(String)
    categoria = Column(String)
    subcategoria = Column(String)
    pais = Column(String)
    tipo = Column(String)
    mercado = Column(String)
    local_id = Column(Integer)
    local_nome = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    data_coleta = Column(DateTime, default=datetime.utcnow)
