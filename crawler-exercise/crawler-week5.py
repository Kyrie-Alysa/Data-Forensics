import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time


# Instantiate the UserAgent class
ua = UserAgent()

http_proxy = "socks5h://localhost:9050"
proxy = {"http": http_proxy, "https": http_proxy}


def crawl(url):
    # Random user agent generation
    header = {
        'User-Agent': ua.random,
        'Cookie': "dcap=vQJNVasv/s/44FVnL1BxrCVNozla7n24GcxMMj3BUs2BLJPgmzzKtdkBhdGus1Fc6dOJRWl4cf00zG7BaThSRw6o6ck81nh2Fgi/ufyAs0L0Q3Vlm0ignNJZdpJYdE5z/gWJGLiAxyIfu9iCgl3H58GYh0WWpApADedH/nFxpkOb7d0tzTT1lA=="
    }

    response = requests.get(url, headers=header, proxies=proxy)
    # response = requests.get(url, headers=header)
    return response

def save(filename, html_content):
    with open(filename, 'w') as hiddenwiki_file:
        hiddenwiki_file.write(html_content)

def load(path):
    content = ""

    with open(path, 'r') as file:
        content = file.read()

    return content

if __name__ == '__main__':
    # url = "http://wiki47qqn6tey4id7xeqb6l7uj6jueacxlqtk3adshox3zdohvo35vad.onion/"
    # response = crawl(url)
    # print(response.text)
    #
    # hiddenwiki_filename = "hiddenwiki.html"
    # save(hiddenwiki_filename, response.text)

    hiddenwiki_filename = "hiddenwiki.html"
    html_content = load(hiddenwiki_filename)

    bs4 = BeautifulSoup(html_content, 'html.parser')
    links = bs4.find_all("a", {"class": "site-url"})

    queue = []
    for link in links:
        queue.append(link['href'])

    i = 1

    for link in queue:
        # Wait 1 second
        time.sleep(1)

        # Execute the request
        response = crawl(link)

        page_filename = str(i) + ".html"
        i = i + 1
        # Save the html page
        save(page_filename, response.text)

        print("Page " + page_filename + " saved.")
        if i == 10:
            break


