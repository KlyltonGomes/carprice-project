import asyncio
import logging
import read_url
import pandas as pd

from playwright_handler import capturar_payload
from parser import parse_batch
from producer import publicar_dados_producer

#level=logging.WARNING
#level=logging.DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lê a URL do arquivo de configuração YAML usando o módulo read_url
URL = read_url.ler_url()

async def main():
    """
    Função principal assíncrona que executa o fluxo de scraping, parsing e publicação dos dados.

    Passos:

        1. Inicia o processo de scraping usando a URL configurada.
        2. Captura os payloads retornados do scraping.
        3. Caso não haja payloads, imprime uma mensagem e encerra.
        4. Para cada batch capturado, faz o parsing para extrair os dados dos carros.
        5. Publica cada dado de carro usando o produtor definido.
        6. Exibe cada carro no console para monitoramento.
    """
    print("Iniciando scraping...")
    #ETAPA 1 DO PROJETO
    payloads = await capturar_payload(URL)

    if not payloads:
        print("Nenhum payload capturado.")
        return

    print(f"Capturados {len(payloads)} batches.")

    todos_carros = []  # Lista para armazenar todos os resultados

    # Parse e exibição dos dados
    for batch in payloads:
        carros = parse_batch(batch)
        for carro in carros:
            #publicar carro no producer RabbitMQ
            #publicar_dados_producer(carro)

            #isolar para visualizar os dados no terminal
            print(carro)

            logging.debug(f"Carros capturados: {carro}")
            todos_carros.append(carro)

    # Salva tudo em um único CSV
    if todos_carros:
        df = pd.DataFrame(todos_carros)
        caminho_arquivo = "resultados_rentcars.csv"
        df.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")
        print(f"[INFO] CSV salvo com sucesso em: {caminho_arquivo}")
    else:
        print("[WARN] Nenhum carro foi extraído para salvar.")



if __name__ == "__main__":
    asyncio.run(main())

#obs: para debbugar, altere  em logging.basicConfig -> INFO para level=logging.DEBUG