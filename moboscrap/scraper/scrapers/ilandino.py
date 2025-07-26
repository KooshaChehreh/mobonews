import json
# import logging
import requests
from bs4 import BeautifulSoup
from lxml  import html
# from django.core.management.base import BaseCommand
# from scraper.models import Product

# logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

def scrape_site(phone_model=None):
    # url_list = []
    # if phone_model is not None:
    #     try:
    #         phone_model_url = Product.objects.get(phone_model=phone_model)["path"]
    #     except Product.DoesNotExist:
    #         raise ProductNotFound
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://ilandino.com/',
        'Connection': 'keep-alive'
    }
    response = requests.get("https://ilandino.com/product/samsung-galaxy-s24-fe-256gb-r8/", headers=headers, timeout=10)
    
    tree = html.fromstring(response.content)
    
    form_nodes = tree.xpath('//form[contains(@class, "variations_form")]')
    form_data = []
    for form in form_nodes:
        variations = form.get('data-product_variations')
        if variations:
            variations_data = json.loads(variations)
            form_data.append(variations_data)
    
    description = ''
    # Try primary XPath: product summary or details section
    description_nodes = tree.xpath('//div[contains(@class, "summary")]//p[1]/text()')
    description = ' '.join(text.strip() for text in description_nodes if text.strip())
    
    return {
        'form_data': form_data,
        'description': description
    }

def extract_color_price(data):
    color_price_pairs = {}
    for variations in data:
        for variation in variations:
            color = variation['attributes']['attribute_pa_color']
            price = variation['display_price']
            color_price_pairs[color] = price
    return color_price_pairs

data = scrape_site()
print(extract_color_price(data["form_data"]))
print("desc is", data["description"])















