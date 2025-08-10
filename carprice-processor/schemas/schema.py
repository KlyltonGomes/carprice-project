from dataclasses import dataclass

#Pydantic
@dataclass
class CarroItem:
    id: str
    nome: str
    afiliado: str
    lp: str
    locadora: str
    categoria: str
    subcategoria: str
    pais: str
    tipo: str
    mercado: str
    local_id: str
    local_nome: str
    preco: float
    quantidade: int