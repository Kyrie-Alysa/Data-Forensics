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
}

def crawl_page(url):
    # Send request
    response = requests.get(url, proxies=proxy)

    # Get the content
    # Return the content
    return response

def scrape(response):
    pass

if __name__ == '__main__':
    url = 'http://jn6weomv6klvnwdwcgu55miabpwklsmmyaf5qrkt4miif4shrqmvdhqd.onion/'
    
    # YOUR CODE HERE
    content = crawl_page(url)
    html_content = content.text

    html_path = 'test-crawl/rent_a_hacker.html'

    # Save html page
    with open(html_path, 'w') as file:
        file.write(html_content)