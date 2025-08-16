import asyncio
from urllib.parse import parse_qs
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
#ABRI O NAVEGADOR
#payloads é uma lista de batch (dicionários).
#batch é um dicionário com valores codificados que representam veículos/produtos.
async def capturar_payload(url: str):
    """
    Abre a página com Playwright, intercepta a request POST para Google Analytics
    contendo os dados de veículos e retorna uma lista de dicionários com os payloads brutos.
    Faz fallback para 'load' caso 'networkidle' estoure timeout.

    :param payload: URL guardada em variável de ambiente.
    :type payload: str
    :return: Lista de dicionários com os dados capturados.
    :rtype: List[dict]
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            )
        )
        page = await context.new_page()

        payloads = []

        def handle_request(request):
            #Pega a URL da requisição
            url_req = request.url
            #A condição verifica se a string "analytics.google.com/g/collect" está presente na URL da requisição e se o método HTTP é "POST".
            #Ou seja, a parte analytics.google.com/g/collect faz parte da URL requisitada
            #é o endpoint do Google Analytics para coleta de dados.
            if "analytics.google.com/g/collect" in url_req and request.method == "POST":
                #captura os dados enviados no corpo da requisição POST
                post_data = request.post_data
                #ndicam parâmetros de produtos ou itens
                if post_data and ("pr1=" in post_data or "pr2=" in post_data):
                    #converter a string post_data em um dicionário,
                    # onde cada chave é um parâmetro e o valor é uma lista de valores daquele parâmetro.
                    params = parse_qs(post_data)
                    #cria um novo dicionário pr_items contendo apenas os parâmetros que começam com "pr",
                    # pegando só o primeiro valor da lista (índice [0]).
                    pr_items = {k: v[0] for k, v in params.items() if k.startswith("pr")}
                    #dicionário pr_items não estiver vazio, adiciona ele na lista global payloads
                    if pr_items:
                        payloads.append(pr_items)
        #o código registra essa função handle_request como callback para o evento "request" da página,
        # toda vez que a página fizer uma requisição,
        # essa função é chamada para analisar e eventualmente capturar os dados relevantes.
        page.on("request", handle_request)

        try:
            print(f"[INFO] Tentando acessar (networkidle): {url}")
            await page.goto(url, wait_until="networkidle", timeout=80000)
        except PlaywrightTimeoutError:
            print("[AVISO] Timeout com 'networkidle'. Tentando com 'load'...")
            try:
                await page.goto(url, wait_until="load", timeout=70000)
            except PlaywrightTimeoutError:
                print(f"[ERRO] Falha ao carregar página: {url}")
                await browser.close()
                return payloads


        await asyncio.sleep(30)

        await browser.close()
        return payloads

        """
        Esse código monitora as requisições POST feitas para o endpoint de coleta do Google Analytics
        na página carregada e extrai os parâmetros que representam produtos (prefixados por "pr"), armazenando esses dados numa lista.
        
        """