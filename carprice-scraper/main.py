import asyncio
import yaml
from parser import parse_batch
from pathlib import Path
from playwright_handler import capturar_payload

# Caminho do arquivo YAML
CONFIG_PATH = Path(__file__).parent / "carprice-scraper.yaml"
config = yaml.safe_load(CONFIG_PATH.read_text())

rentcars_url = config["rentcars"]["url"]
browser_type = config["rentcars"]["browser"]

print(f"Scraping URL: {rentcars_url} usando {browser_type}")

async def scraper():
    # Chama a função que usa Playwright para capturar os dados
    print("Scraper ativado! Loading...")
    payloads = await capturar_payload(rentcars_url)

    # Aqui você pode enviar para o RabbitMQ ou salvar em arquivo
    print(f"Total payloads capturados: {len(payloads)}")
    carros = []
    for batch in payloads:
        carros.extend(parse_batch(batch))

    print(f"Carros processados: {len(carros)}")
    for carro in carros:
        print(carro)

    #return payloads

if __name__ == "__main__":
    asyncio.run(scraper())
