# Wat gekke stappen als de packages of path niet werkt:
# Deactivate .venv in de terminal met 'deactivate'
# Activate forensics venv met command: source forensics/bin/activate
# Navigeer naar crawler-exercise met command: cd forensics/crawler-exercise
# Run main.py met command: python main.py

# Deze code is een scraper die gedownloade pages al kan scrapen.
# De scraper is nog niet in staat om zelf pages te downloaden (dit zou je dan moeten combineren met een crawler)

from bs4 import BeautifulSoup

def scrape_products(content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Insert the tag you want to scrape (so a rule).
    # If you just use find_all() you get everything.

    # Poging 1: find all h4 tags
    # products = soup.find_all("h4") 

    # Poging 2: class product-thumb transition
    products = soup.find_all("div", {'class': 'row'})[1].find_all("div", {"class": "product-layout col-lg-3 col-md-3 col-sm-6 col-xs-12"}) 


    # Example: find div at 3rd position
    # soup.find_all('div')[2].find()
    # Or find all in a div
    # soup.find('div')[2].find_all()

    # To find tags -> right-click element and inspect

    return products

if __name__ == '__main__':

    html_path = 'crawler-exercise/cocorico_home_page.html'

    # Save html page
    with open(html_path, 'r') as html_file:
        html_content = html_file.read()

    # Scrape the content
    products = scrape_products(html_content)
    for product in products:
        print(product.text)
        print()

    