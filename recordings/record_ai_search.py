import asyncio
import os
from playwright.async_api import async_playwright

async def record():
    rec_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(rec_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=rec_dir,
            record_video_size={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        await page.goto("http://localhost:8081")
        await page.wait_for_timeout(2000)
        
        # Click Prompt 1 Chip
        chip1 = page.locator(".chip", has_text="ORD-98214")
        await chip1.click()
        await page.wait_for_timeout(3000)
        
        # Click Prompt 4 Chip
        chip4 = page.locator(".chip", has_text="Resolve SKU-4091")
        await chip4.click()
        await page.wait_for_timeout(4000)
        
        await context.close()
        await browser.close()
        print("Recording completed successfully!")

if __name__ == "__main__":
    asyncio.run(record())
