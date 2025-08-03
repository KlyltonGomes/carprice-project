import asyncio
from playwright.async_api import async_playwright

URL = "https://m.rentcars.com/pt-br/reserva/listar/9-1754226000-9-1754312400-0-0-0-0-0-0-0-0"

async def run():
    print("Iniciando scraping...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headful
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()

        await page.goto(URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(10000)  # espera manual

        html = await page.content()
        print("Tamanho da página:", len(html))

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
