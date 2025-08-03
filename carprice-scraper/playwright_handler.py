import asyncio
from urllib.parse import parse_qs, unquote_plus
from playwright.async_api import async_playwright

async def capturar_payload(url: str):
    """
    Abre a página com Playwright, intercepta a request POST para Google Analytics
    contendo os dados de veículos e retorna uma lista de dicionários com os payloads brutos.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                       "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()

        payloads = []

        def handle_request(request):
            url_req = request.url
            if "analytics.google.com/g/collect" in url_req and request.method == "POST":
                post_data = request.post_data
                if post_data and ("pr1=" in post_data or "pr2=" in post_data):
                    # Extrai todos os prX do corpo
                    params = parse_qs(post_data)
                    pr_items = {k: v[0] for k, v in params.items() if k.startswith("pr")}
                    if pr_items:
                        payloads.append(pr_items)

        page.on("request", handle_request)

        await page.goto(url, wait_until="networkidle")

        await asyncio.sleep(15)  # Espera requisições adicionais

        await browser.close()

        return payloads
