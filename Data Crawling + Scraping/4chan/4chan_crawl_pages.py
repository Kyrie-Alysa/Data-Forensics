import os
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://boards.4chan.org/pol/"
SAVE_DIR = "4chan/html"
os.makedirs(SAVE_DIR, exist_ok=True)

def download_page(url, save_path, delay=5):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)  
        context = browser.new_context()
        page = context.new_page()
        
        print(f"[→] Visiting {url}")
        page.goto(url, timeout=60000)  # 60 sec timeout
        page.wait_for_timeout(delay * 1000)  # let Cloudflare JS run

        html = page.content()
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[✓] Saved to {save_path}")
        browser.close()

if __name__ == "__main__":

    for i in range(1, 11):
        url = f"{BASE_URL}{i}.html" if i > 1 else BASE_URL
        save_path = os.path.join(SAVE_DIR, f"page_{i}.html")
        download_page(url, save_path)