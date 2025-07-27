import json
# import logging
import requests
import urllib.parse
from lxml  import html
from scraper.models import Product
from scraper.exceptions import ProductNotFound
from scraper.scrapers.base_scraper import Scraper
# logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)


class ScrapIlandino(Scraper):
    FORM_XPATH = '//form[contains(@class, "variations_form")]'
    PRICE_XPATH = "//div[contains(@class, 'product')]/div[1]/div[2]/div/div/div[2]/div/p[1]/span/bdi/text()"
    DESCRIPTION_XPATHS = '//div[contains(@class, "summary")]//p[1]/text()'

    
    def extract_color_price(self, form_nodes):
        form_data = []
        for form in form_nodes:
            variations = form.get('data-product_variations')
            if variations:
                variations_data = json.loads(variations)
                form_data.append(variations_data)
        color_price_pairs = {}
        for variations in form_data:
            for variation in variations:
                color = urllib.parse.unquote(variation['attributes']['attribute_pa_color'])
                price = variation['display_price']
                color_price_pairs[color] = price
        return color_price_pairs


    def scrap(self, product=None):

        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://ilandino.com/',
                    'Connection': 'keep-alive'
                }
        
        url_list = []
        results = []
        if product is not None:
            try:
                product = Product.objects.get(product_name=product)
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
                
                price_nodes = tree.xpath(self.PRICE_XPATH)
                price = int(price_nodes[0].strip().replace('$', '').replace(',', '')) if price_nodes else None

                form_nodes = tree.xpath(self.FORM_XPATH)
                color_price_data = self.extract_color_price(form_nodes)

                description = ''
                description_nodes = tree.xpath(self.DESCRIPTION_XPATHS)
                description = ' '.join(text.strip() for text in description_nodes if text.strip())
                
                try:
                    product = Product.objects.get(url=url)
                    product_name_for_save = product.product_name
                except Product.DoesNotExist:
                    results.append(f"Skipped {url}: No product record found")
                    continue
                
                # Save the scraped data in database
                try:
                    message = Product.save_product_data(
                        product_name=product_name_for_save,
                        color_price_data=color_price_data,
                        description=description,
                        price=price,
                    )
                    results.append(message)
                except ProductNotFound as e:
                    results.append(f"Failed {product_name_for_save}: {e.message} (Code: {e.code})")
        
            except requests.RequestException as e:
                results.append(f"Failed {url}: Network error - {e}")
            except Exception as e:
                results.append(f"Failed {url}: Unexpected error - {e}")
        
        return results if results else ["No URLs processed"]




















