# Wat gekke stappen als de packages of path niet werkt:
# Deactivate .venv in de terminal met 'deactivate'
# Activate forensics venv met command: source forensics/bin/activate
# Navigeer naar crawler-exercise met command: cd forensics/crawler-exercise
# Run main.py met command: python main.py

# Deze code is een scraper die gedownloade pages al kan scrapen.
# De scraper is nog niet in staat om zelf pages te downloaden (dit zou je dan moeten combineren met een crawler)

from bs4 import BeautifulSoup
import pandas as pd

def scrape_products(content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Insert the tag you want to scrape (so a rule).
    # If you just use find_all() you get everything.

    main_div = soup.find("div", {'id': 'main'})

    # Split the text in lines
    lines = main_div.decode_contents().split('<br>')
        
    return lines

if __name__ == '__main__':

    html_path = 'test-crawl/rent_a_hacker.html'

    # Save html page
    with open(html_path, 'r') as html_file:
        html_content = html_file.read()

    # Scrape the content
    content = scrape_products(html_content)
    
    # We want a list of all the lines that we can convert into a dataframe
    lines = []

    # Clean and print each line
    for line in content:
        clean = BeautifulSoup(line, 'html.parser').text
        lines.append(clean)
        print(clean)
        print()

# Lines is now a list with 1 element of text separated by newlines, 
# so we need to split the lines using '\n'
lines = lines[0].split('\n')

# Remove empty lines, so the empty strings
cleaned_lines = [line for line in lines if line.strip()]

# Print the cleaned lines
print(cleaned_lines) 

# Create Dataframe with one column
df = pd.DataFrame(cleaned_lines, columns=['Text'])

print(df)

# Save the dataframe to a csv file
df.to_csv('test-crawl/rent_a_hacker.csv', index=False)


    