import asyncio
import os
from playwright.async_api import async_playwright

async def record():
    rec_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(rec_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=rec_dir,
            record_video_size={"width": 1400, "height": 900}
        )
        page = await context.new_page()
        await page.goto("http://localhost:8081")
        await page.wait_for_timeout(2000)
        
        # Click Prompt Chip 1 (CoinGecko Crypto REST API)
        chip1 = page.locator(".chip", has_text="Crypto Prices").first
        await chip1.click()
        await page.wait_for_timeout(3000)
        
        # Click Prompt Chip 2 (Logistics Weather REST API)
        chip2 = page.locator(".chip", has_text="Logistics Weather").first
        await chip2.click()
        await page.wait_for_timeout(3000)
        
        # Click Prompt Chip 5 (MCP Microservice Hub)
        chip5 = page.locator(".chip", has_text="MCP Microservice").first
        await chip5.click()
        await page.wait_for_timeout(3000)
        
        # Click Card Action Button
        card_btn = page.locator(".card-btn.primary", has_text="Refresh Stream").first
        if await card_btn.is_visible():
            await card_btn.click()
            await page.wait_for_timeout(3000)
            
        await context.close()
        await browser.close()
        print("Master recording completed successfully!")

if __name__ == "__main__":
    asyncio.run(record())
