import asyncio
from urllib.parse import parse_qs
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def capturar_payload(url: str):
    """
    Abre a página com Playwright, intercepta a request POST para Google Analytics
    contendo os dados de veículos e retorna uma lista de dicionários com os payloads brutos.
    Faz fallback para 'load' caso 'networkidle' estoure timeout.
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
            url_req = request.url
            if "analytics.google.com/g/collect" in url_req and request.method == "POST":
                post_data = request.post_data
                if post_data and ("pr1=" in post_data or "pr2=" in post_data):
                    params = parse_qs(post_data)
                    pr_items = {k: v[0] for k, v in params.items() if k.startswith("pr")}
                    if pr_items:
                        payloads.append(pr_items)

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
                return payloads  # Retorna o que já tiver capturado (se algo)

        # Aguarda requisições adicionais
        await asyncio.sleep(30)

        await browser.close()
        return payloads
