from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Car(Base):
    __tablename__ = "carros"

    id = Column(String, primary_key=True)
    nome = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
