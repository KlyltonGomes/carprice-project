import yaml
from pathlib import Path

def ler_url() -> str:
    yaml_path = Path(__file__).parent/"config"/"carprice-scraper.yaml"
    texto_yaml = yaml_path.read_text(encoding="utf-8")

    converte_yaml = yaml.safe_load(texto_yaml)
    rentcars_url = converte_yaml["rentcars"]["url"]

   # print(f"URL Rentcars: {rentcars_url}")
    print(rentcars_url)
    return rentcars_url

#url = ler_url()
