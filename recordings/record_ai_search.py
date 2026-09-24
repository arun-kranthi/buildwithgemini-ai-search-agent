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
        
        # Click Sidebar Navigation Item (Supply Chain)
        sc_item = page.locator(".nav-item", has_text="Supply Chain")
        await sc_item.click()
        await page.wait_for_timeout(1500)
        
        # Click Prompt 1 Chip (Order & Shipment)
        chip1 = page.locator(".chip", has_text="ORD-98214")
        await chip1.click()
        await page.wait_for_timeout(3000)
        
        # Click Card Action Button (Track Live Route)
        card_btn = page.locator(".card-btn.primary", has_text="Track Live Route").first
        if await card_btn.is_visible():
            await card_btn.click()
            await page.wait_for_timeout(3000)
        
        # Click Prompt 4 Chip (Supply Chain Shortage Crisis)
        chip4 = page.locator(".chip", has_text="Resolve SKU-4091")
        await chip4.click()
        await page.wait_for_timeout(4000)
        
        await context.close()
        await browser.close()
        print("Recording completed successfully!")

if __name__ == "__main__":
    asyncio.run(record())
