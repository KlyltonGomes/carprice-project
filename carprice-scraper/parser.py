from urllib.parse import unquote_plus

def parse_pr_item(pr_str):
    parts = pr_str.split("~")
    data = {}
    for part in parts:
        if part.startswith("id"):
            data["id"] = part[2:]
        elif part.startswith("nm"):
            data["nome"] = part[2:]
        elif part.startswith("af"):
            data["afiliado"] = part[2:]
        elif part.startswith("lp"):
            data["lp"] = part[2:]
        elif part.startswith("br"):
            data["locadora"] = part[2:]
        elif part.startswith("ca"):
            data["categoria"] = part[2:]
        elif part.startswith("c2"):
            data["subcategoria"] = part[2:]
        elif part.startswith("c3"):
            data["pais"] = part[2:]
        elif part.startswith("c4"):
            data["tipo"] = part[2:]
        elif part.startswith("c5"):
            data["mercado"] = part[2:]
        elif part.startswith("li"):
            data["local_id"] = part[2:]
        elif part.startswith("ln"):
            data["local_nome"] = part[2:]
        elif part.startswith("pr"):
            try:
                data["preco"] = float(part[2:])
            except:
                data["preco"] = None
        elif part.startswith("qt"):
            try:
                data["quantidade"] = int(part[2:])
            except:
                data["quantidade"] = None
    return data

def parse_batch(batch):
    """
    batch: dict com chave prX e valor string do payload
    Retorna lista de dicts parseados
    """
    parsed_items = []
    for val in batch.values():
        decoded = unquote_plus(val)
        parsed_items.append(parse_pr_item(decoded))
    return parsed_items
