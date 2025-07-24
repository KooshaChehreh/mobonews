import json
import logging
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraper.models import Product

logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

SITES = {
    'ilandino': 'https://ilandino.com/{}',
    'dizoland': 'https://dizoland.com/{}',
    'iranpowerology': 'https://iranpowerology.com/{}',
    'greenlionofficial': 'https://greenlionofficial.ir/{}',
}

def scrape_site(site_name, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example parsing (site-specific logic in separate modules)
        name = soup.select_one('.product-title').text.strip()
        price = float(soup.select_one('.price-final').text.replace('$', ''))
        warranty = soup.select_one('.warranty-info').text.strip() if soup.select_one('.warranty-info') else None
        availability = soup.select_one('.stock-status').text.strip() if soup.select_one('.stock-status') else None
        description = soup.select_one('.product-description').text.strip() if soup.select_one('.product-description') else None
        return {'name': name, 'price': price, 'warranty': warranty, 'availability': availability, 'description': description}
    except Exception as e:
        logging.error(f"Error scraping {site_name} at {url}: {str(e)}")
        return None