import asyncio
import logging
import pandas as pd
import read_url_dinamico
import os
from datetime import datetime

from playwright_handler import capturar_payload
from parser import parse_batch
# from producer import publicar_dados_producer  # opcional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    print("Iniciando scraping dinâmico...")

    # Lê todas as URLs geradas automaticamente
    urls = read_url_dinamico.ler_urls_dinamicas()
    print(f"[INFO] {len(urls)} URLs geradas para scraping.")

    todos_carros = []

    for i, entrada in enumerate(urls, start=1):
        cidade_retirada = entrada.get("cidade_retirada", "")
        cidade_devolucao = entrada.get("cidade_devolucao", "")
        dias = entrada.get("dias", 1)
        hora_retirada = entrada.get("hora_retirada", "")
        hora_devolucao = entrada.get("hora_devolucao", "")
        url = entrada.get("url", "")

        print(f"\n[{i}/{len(urls)}] Buscando ({cidade_retirada} → {cidade_devolucao}, {dias} diária(s), {hora_retirada}-{hora_devolucao}): {url}")

        payloads = await capturar_payload(url)

        if not payloads:
            print(f"[WARN] Nenhum payload capturado para {url}")
            continue

        for batch in payloads:
            carros = parse_batch(batch)
            for carro in carros:
                # adicionar cidade de retirada/devolução, diárias e horários ao dicionário
                todos_carros.append({
                    **carro,
                    "cidade_retirada": cidade_retirada,
                    "cidade_devolucao": cidade_devolucao,
                    "dias": dias,
                    "hora_retirada": hora_retirada,
                    "hora_devolucao": hora_devolucao
                })

    # Criar pasta de resultados
    base_dir = "resultados"
    os.makedirs(base_dir, exist_ok=True)

    if not todos_carros:
        print("[WARN] Nenhum carro foi extraído para salvar.")
        return

    df = pd.DataFrame(todos_carros)

    agora = datetime.now().strftime("%Y-%m-%d_%Hh")

    # Salvar CSV por cidade de retirada
    for cidade_nome, grupo in df.groupby("cidade_retirada"):
        caminho = os.path.join(base_dir, f"resultados_rentcars_{cidade_nome}_{agora}.csv")
        grupo.to_csv(caminho, index=False, encoding="utf-8-sig")
        print(f"[INFO] Dados salvos em: {caminho}")

if __name__ == "__main__":
    asyncio.run(main())
