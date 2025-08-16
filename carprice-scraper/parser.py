from urllib.parse import unquote_plus

def parse_pr_item(pr_str):
    """
    campos prefixados.
    Retorna um dicionário com as informações extraídas.

    separa os campos pelo delimitador '~'

    Exemplo:

    .. code-block:: python

        parts = pr_str.split("~")
        data = {}


    Para cada prefixo esperado, extrai o valor após os 2 primeiros caracteres.
    Quebra essa string em partes e transforma em um dicionário com campos identificados por prefixos (id, nm, af, pr)

    .. code-block:: python

        for part in parts:
            if part.startswith("id"):
                data["id"] = part[2:]
            elif part.startswith("nm"):
                data["nome"] = part[2:]
            elif part.startswith("af"):
    """
    # separa os campos pelo delimitador '~'
    parts = pr_str.split("~")
    data = {}
    for part in parts:
        # Para cada prefixo esperado, extrai o valor após os 2 primeiros caracteres
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
            # tenta converter preço para float, se falhar deixa None
            try:
                data["preco"] = float(part[2:])
            except:
                data["preco"] = None
        elif part.startswith("qt"):
            # tenta converter quantidade para int, se falhar deixa None
            try:
                data["quantidade"] = int(part[2:])
            except:
                data["quantidade"] = None
    return data

#payloads é uma lista de batch (dicionários).
#batch é um dicionário com valores codificados que representam veículos/produtos.
#parse_batch(batch) recebe esse dicionário e retorna uma lista de dicionários limpos, cada um representando um carro
def parse_batch(batch):
    """
    Recebe um dicionário `batch` onde os valores são strings URL-encoded.
    Decodifica cada valor, interpreta com `parse_pr_item` e retorna uma lista de dicionários.
    uma lista de dicionários com os parâmetros brutos dos produtos capturados das requisições POST.

    .. code-block:: python

        parsed_items = []
        for val in batch.values():

    decodifica URL (ex: %20 → espaço)
    "id123~nmFiat%20Uno~afMovida~pr100.50~qt2"


    .. code-block:: python

            decoded = unquote_plus(val)
            parsed_items.append(parse_pr_item(decoded))
        return parsed_items

    Exemplo:

    .. code-block:: python

        batch = {
            "pr1": "id123~nmFiat%20Uno~afMovida~pr100.50~qt2",
            "pr2": "id124~nmFord%20Ka~afLocaliza~pr200.00~qt1"
        }

        result = parse_batch(batch)
        print(result)

    Resultado:

    .. code-block:: python

        [
            {'id': '123', 'nome': 'Fiat Uno', 'afiliado': 'Movida', 'preco': 100.5, 'quantidade': 2},
            {'id': '124', 'nome': 'Ford Ka', 'afiliado': 'Localiza', 'preco': 200.0, 'quantidade': 1}
        ]
    """

    parsed_items = []
    for val in batch.values():
        # decodifica URL (ex: %20 → espaço)
        decoded = unquote_plus(val)
        parsed_items.append(parse_pr_item(decoded))
        #lista de dicionários limpos
    return parsed_items

#prefixos (id, nm, af, pr, qt etc) são comuns em parâmetros compactados para reduzir tamanho,
#especialmente em analytics, tracking, ou APIs que enviam dados codificados.
#interpretando e mapeando esses prefixos para nomes mais amigáveis no seu código (ex: "nm" vira "nome").