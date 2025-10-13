import yaml
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# Mapeamento de cidades → IDs da Rentcars
CIDADES_IDS = {
    #"Aphaville_Salvador_BA":"99098"
    #"GRU": "54",    # Guarulhos
     "SSA": "52"  # Salvador
    # CGH": "9"     # Congonhas
}

BR_TZ = ZoneInfo("America/Sao_Paulo")  # Fuso horário de Brasília


def gerar_urls(cidade_retirada: str, cidade_devolucao: str, data_inicio: datetime,
               diarias: int, horas_retirada: list[str], horas_devolucao: list[str]) -> list[dict]:
    """
    Gera URLs válidas para a Rentcars considerando retirada e devolução.
    cidade_devolucao pode ser igual a cidade_retirada (mesmo local).
    """
    urls = []
    agora = datetime.now(BR_TZ)

    cidade_retirada_id = CIDADES_IDS[cidade_retirada]
    cidade_devolucao_id = CIDADES_IDS.get(cidade_devolucao, cidade_retirada_id)  # vazio = mesma cidade

    for hr_pickup in horas_retirada:
        dt_pickup = datetime.combine(data_inicio.date(),
                                     datetime.strptime(hr_pickup, "%H:%M").time()).replace(tzinfo=BR_TZ)

        # Ignora horários passados se a data é hoje
        if dt_pickup <= agora and data_inicio.date() == agora.date():
            print(f"[INFO] Ignorando {cidade_retirada} {hr_pickup}h pois já passou ({agora})")
            continue

        for hr_dropoff in horas_devolucao:
            dt_dropoff = datetime.combine(data_inicio.date() + timedelta(days=diarias),
                                          datetime.strptime(hr_dropoff, "%H:%M").time()).replace(tzinfo=BR_TZ)

            if dt_dropoff <= dt_pickup:
                continue  # evita URL inválida

            # Converter para UTC e gerar timestamps corretos
            pickup_ts = int(dt_pickup.astimezone(ZoneInfo("UTC")).timestamp())
            dropoff_ts = int(dt_dropoff.astimezone(ZoneInfo("UTC")).timestamp())

            # Formato correto da URL Rentcars
            url = f"https://www.rentcars.com/pt-br/reserva/listar/{cidade_retirada_id}-{pickup_ts}-{cidade_devolucao_id}-{dropoff_ts}-0-0-0-0-0-0-0-0"

            urls.append({
                "cidade_retirada": cidade_retirada,
                "cidade_devolucao": cidade_devolucao,
                "dias": diarias,
                "hora_retirada": hr_pickup,
                "hora_devolucao": hr_dropoff,
                "url": url
            })

    return urls


def ler_urls_dinamicas(config_path: str = "config/url_dinamico.yaml") -> list[dict]:
    """
    Lê o arquivo YAML e gera todas as URLs válidas com cidade de retirada,
    cidade de devolução, número de diárias e horários.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    rentcars_cfg = cfg.get("rentcars", {})
    data_inicio = datetime.fromisoformat(rentcars_cfg.get("data_inicio", datetime.now().isoformat()))
    urls = []

    cidades_retirada = rentcars_cfg.get("cidades_retirada", [])
    cidades_devolucao = rentcars_cfg.get("cidades_devolucao", [""])  # vazio = mesma cidade
    faixas_diarias = rentcars_cfg.get("faixas_diarias", [[1, 1]])
    horas_retirada = rentcars_cfg.get("hora_retirada", ["10:00"])
    horas_devolucao = rentcars_cfg.get("hora_devolucao", ["10:00"])

    # Itera sobre todas combinações de retirada → devolução
    for i, cidade_ret in enumerate(cidades_retirada):
        cidade_dev = cidades_devolucao[i] if i < len(cidades_devolucao) else ""  # devolução correspondente ou mesma cidade
        for faixa in faixas_diarias:
            inicio, fim = faixa
            for dias in range(inicio, fim + 1):
                urls += gerar_urls(
                    cidade_retirada=cidade_ret,
                    cidade_devolucao=cidade_dev,
                    data_inicio=data_inicio,
                    diarias=dias,
                    horas_retirada=horas_retirada,
                    horas_devolucao=horas_devolucao
                )

    print(f"[INFO] Total de URLs válidas: {len(urls)}")
    return urls
