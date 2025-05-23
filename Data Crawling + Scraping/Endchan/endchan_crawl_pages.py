# Wat gekke stappen als de packages of path niet werkt:
# Deactivate .venv in de terminal met 'deactivate'
# Activate forensics venv met command: source forensics/bin/activate
# Navigeer naar crawler-exercise met command: cd forensics/crawler-exercise
# Run main.py met command: python main.py

# Deze code is een voorbeeld van een simpele crawler die een website bezoekt en de html opslaat in een bestand.

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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

if __name__ == '__main__':

    for i in range (1, 15):
        if i == 1:
            url = 'http://enxx3byspwsdo446jujc52ucy2pf5urdbhqw3kbsfhlfjwmbpj5smdad.onion/pol/index.html'
        else:
            url = f'http://enxx3byspwsdo446jujc52ucy2pf5urdbhqw3kbsfhlfjwmbpj5smdad.onion/pol/{i}.html'

        content = crawl_page(url)
        html_content = content.text

        html_path = f'endchan V2/html/page_{i}.html'

        # Save html page
        with open(html_path, 'w') as file:
            file.write(html_content)