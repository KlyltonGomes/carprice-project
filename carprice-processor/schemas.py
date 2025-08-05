from pydantic import BaseModel

class CarItem(BaseModel):
    id:str
    nome:str
    afiliado:str
    lp:str
    locadora:str
    categoria:str
    subcategoria:str
    pais:str
    tipo:str
    mercado:str
    local_id:int
    local_name:str
    preco:float
    quantidade:int