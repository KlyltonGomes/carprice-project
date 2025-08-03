import asyncio
from playwright_handler import capturar_payload
from parser import parse_batch

#URL = "https://m.rentcars.com/pt-br/reserva/listar/9-1754226000-9-1754312400-0-0-0-0-0-0-0-0"
URL = "https://www.rentcars.com/pt-br/reserva/listar/54-1754312400-54-1754398800-0-0-0-0-0-0-0-0?"
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
