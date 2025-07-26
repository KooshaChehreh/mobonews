import json
# import logging
import requests
from lxml  import html
from scraper.utils import save_product_data
from scraper.models import Product
from scraper.exceptions import ProductNotFound

# logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

FORM_XPATH = '//form[contains(@class, "variations_form")]'
DESCRIPTION_XPATHS = '//div[contains(@class, "summary")]//p[1]/text()'

def extract_color_price(data):
    color_price_pairs = {}
    for variations in data:
        for variation in variations:
            color = variation['attributes']['attribute_pa_color']
            price = variation['display_price']
            color_price_pairs[color] = price
    return color_price_pairs


def scrape_ilandino_site(phone_model=None):

    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://ilandino.com/',
                'Connection': 'keep-alive'
            }
    
    url_list = []
    results = []
    if phone_model is not None:
        try:
            product = Product.objects.get(phone_model=phone_model)
            url_list.append(product.url) 
        except Product.DoesNotExist:
            raise ProductNotFound
    else:
        products = Product.objects.filter(source_site=Product.SITE_ILANDINO).values('url')
        url_list = [product['url'] for product in products]
    
    
    for url in url_list:
        try:
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            tree = html.fromstring(response.content)
            
            form_nodes = tree.xpath(FORM_XPATH)
            form_data = []
            for form in form_nodes:
                variations = form.get('data-product_variations')
                if variations:
                    variations_data = json.loads(variations)
                    form_data.append(variations_data)
            
            description = ''
            description_nodes = tree.xpath(DESCRIPTION_XPATHS)
            description = ' '.join(text.strip() for text in description_nodes if text.strip())
            
            # Extraction of color and price pair
            color_price_data = extract_color_price(form_data)

            if not phone_model:
                try:
                    product = Product.objects.get(url=url)
                    phone_model_for_save = product.phone_model
                except Product.DoesNotExist:
                    results.append(f"Skipped {url}: No product record found")
                    continue
            else:
                phone_model_for_save = phone_model

            # Save the scraped data in database
            try:
                message = save_product_data(
                    phone_model=phone_model_for_save,
                    product_url=url,
                    color_price_data=color_price_data,
                    description=description,
                )
                results.append(message)
            except ProductNotFound as e:
                results.append(f"Failed {phone_model_for_save}: {e.message} (Code: {e.code})")
    
        except requests.RequestException as e:
            results.append(f"Failed {url}: Network error - {e}")
        except Exception as e:
            results.append(f"Failed {url}: Unexpected error - {e}")
    
    return results if results else ["No URLs processed"]




















