import asyncio
import read_url

from playwright_handler import capturar_payload
from parser import parse_batch

URL = read_url.ler_url()

async def main():
    print("Iniciando scraping...")
    payloads = await capturar_payload(URL)

    if not payloads:
        print("Nenhum payload capturado.")
        return

    print(f"Capturados {len(payloads)} batches.")

    # Parse e exibição dos dados
    for batch in payloads:
        carros = parse_batch(batch)
        for carro in carros:
            print(carro)

if __name__ == "__main__":
    asyncio.run(main())
