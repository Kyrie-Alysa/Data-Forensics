# Wat gekke stappen als de packages of path niet werkt:
# Deactivate .venv in de terminal met 'deactivate'
# Activate forensics venv met command: source forensics/bin/activate
# Navigeer naar crawler-exercise met command: cd forensics/crawler-exercise
# Run main.py met command: python main.py

# Deze code is een voorbeeld van een simpele crawler die een website bezoekt en de html opslaat in een bestand.

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
from urllib.parse import urljoin

# Socks connection 
http_proxy = "socks5h://localhost:9050"
proxy = {"http": http_proxy, "https": http_proxy}

# Instantiate the UserAgent class
ua = UserAgent()

# Cookie -> go to the website, login, get the cookie
# For extra anonimity, use fake-useragent and rotate them
# Random user agent generation
header = {
    'User-Agent': ua.random,
    'Cookie': 'captchaid=67dd71e3be1c1d595e4be985ftqitl7wyqso1q0dyjkng+ldcqmu24vutl+i946cm/cjokx0hhmcj9f3m1jpvfduktp2lbjmrm3qkvkrrjcuuq=='
}

def crawl_page(url):
    # Send request
    response = requests.get(url, proxies=proxy)

    # Get the content and return the content
    return response

def extract_thread_links(index_html, base_url):
    soup = BeautifulSoup(index_html, 'html.parser')
    thread_links = []
    for a in soup.select('a.linkReply'):
        href = a.get('href')
        if href and '/res/' in href:
            full_url = urljoin(base_url, href)
            thread_id = href.split('/')[-1].split('.')[0]
            thread_links.append((thread_id, full_url))
            
    return thread_links

if __name__ == '__main__':

    BASE_URL = 'http://enxx3byspwsdo446jujc52ucy2pf5urdbhqw3kbsfhlfjwmbpj5smdad.onion'
    thread_dir = 'endchan V2/threads_html'
    os.makedirs(thread_dir, exist_ok=True)

    for i in range(1, 15):
        html_path = f'endchan V2/html/page_{i}.html'
        if not os.path.exists(html_path):
            print(f"[!] Skipping missing file: {html_path}")
            continue

        with open(html_path, 'r', encoding='utf-8') as f:
            index_html = f.read()

        thread_links = extract_thread_links(index_html, BASE_URL)

        for thread_id, thread_url in thread_links:
            save_path = f"{thread_dir}/thread_{thread_id}.html"
            if os.path.exists(save_path):
                print(f"[✓] Already downloaded: {thread_id}")
                continue

            try:
                print(f"[→] Downloading thread {thread_id}")
                response = requests.get(thread_url, headers=header, proxies=proxy, timeout=20)
                if response.status_code == 200:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"[✓] Saved thread {thread_id}")
                else:
                    print(f"[✗] Failed to fetch {thread_id}, status code {response.status_code}")
            except Exception as e:
                print(f"[!] Error fetching {thread_url}: {e}")

        print(f"Page {i} done")
        print()


        
