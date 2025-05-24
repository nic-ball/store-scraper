import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL and pagination template
BASE_URL = "https://www.musicglue.com/falseheads"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PRODUCTS = []

def scrape_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust these selectors to match the website’s structure
    product_cards = soup.select('.ProductDisdplay-item')

    for card in product_cards:
        title = card.select_one('.ProductName').get_text(strip=True)
        price = card.select_one('.BundlePrice-discounted-price').get_text(strip=True)    
    
        link = card.select_one('a')['href']

        PRODUCTS.append({
            'Title': title,
            'Price': price,
            'Link': link if link.startswith("http") else f"https://musicglue.com{link}"
        })

def get_all_pages():
    page = 1
    while True:
        print(f"Scraping page {page}...")
        url = f"{BASE_URL}?page={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        if not soup.select('.ProductBundle'):
            print("No more products found.")
            break

        scrape_page(url)
        page += 1
        time.sleep(1)  # Be kind to the server

# Run the scraper
get_all_pages()

# Save to CSV
df = pd.DataFrame(PRODUCTS)
df.to_csv("products.csv", index=False)
print("Scraping complete. Data saved to products.csv")
