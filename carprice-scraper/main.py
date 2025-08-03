import yaml
from fastapi import FastAPI, HTTPException
from pathlib import Path

from models import CarPrice
from swagger_config import swagger_config
from playwright_handler import capturar_payload
from parser import parse_batch

# Configurações
CONFIG_PATH = Path(__file__).parent.parent / "carprice-scraper.yaml"
config = yaml.safe_load(CONFIG_PATH.read_text())

rentcars_url = config["rentcars"]["url"]
browser_type = config["rentcars"]["browser"]
print(f"Scraping URL: {rentcars_url} usando {browser_type}")

# FastAPI app
app = FastAPI(
    title=swagger_config["title"],
    description=swagger_config["description"],
    version=swagger_config["version"]
)

@app.get(
    "/scraper",
    summary="Dispara o scraper e retorna os dados",
    response_model=list[CarPrice]
)
async def scraper():
    payloads = await capturar_payload(rentcars_url)

    if not payloads:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")

    carros = []
    for batch in payloads:
        carros.extend(parse_batch(batch))

    return carros
