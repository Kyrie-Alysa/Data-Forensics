import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

# Config
BASE_URL = "https://boards.4chan.org"
BOARD = "pol"
CATALOG_DIR = "4chan/html"
THREAD_DIR = "4chan/threads_html"
os.makedirs(THREAD_DIR, exist_ok=True)

# Extract thread URLs from catalog page
def extract_threads_from_catalog(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.select("a[href^='/pol/thread/']"):
        href = a['href']
        thread_id = href.split('/')[-1]
        full_url = urljoin(BASE_URL, href)
        links.add((thread_id, full_url))
    return list(links)

# Download thread HTML using Playwright
def download_thread_page(thread_id, url, save_path, delay=5):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        try:
            print(f"[→] Downloading thread {thread_id} from {url}")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(delay * 1000)
            content = page.content()
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[✓] Saved thread {thread_id}")
        except Exception as e:
            print(f"[!] Failed to download {thread_id}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    for file in os.listdir(CATALOG_DIR):
        if not file.endswith(".html"):
            continue

        catalog_path = os.path.join(CATALOG_DIR, file)
        with open(catalog_path, 'r', encoding='utf-8') as f:
            html = f.read()

        threads = extract_threads_from_catalog(html)

        for thread_id, url in threads:
            save_path = os.path.join(THREAD_DIR, f"thread_{thread_id}.html")
            if os.path.exists(save_path):
                print(f"[✓] Already exists: thread {thread_id}")
                continue
            download_thread_page(thread_id, url, save_path)
            time.sleep(2)  # polite delay

        print(f"[✓] Finished downloading threads from {file}")
