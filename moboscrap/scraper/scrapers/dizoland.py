import json
import logging
import requests
import urllib.parse
from lxml  import html
from scraper.models import Product
from scraper.exceptions import ProductNotFound
from scraper.scrapers.base_scraper import Scraper


# Log Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ScrapDiznoland(Scraper):
    PRICE_XPATH = "//div[contains(@class, 'product')]/section[2]/div//p[contains(@class, 'price')]/span/bdi/text() | //span[contains(@class, 'woocommerce-Price-amount')]/bdi/text()"
    DESCRIPTION_XPATHS = "//*[@id='tab-description']/p[1]/text()"
    WARRANTY_XPATH = "//form[contains(@class, 'variations_form')]//select[contains(@name, 'guarantee') or contains(@id, 'pa_guarantee')]/option/text()"


    def scrap(self, product=None):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://diznoland.com/',
            'Connection': 'keep-alive'
        }
        
        url_list = self.get_scrap_urls(site_constant=Product.SITE_DIZOLAND, product=product)
        
        for url in url_list:
            try:
                logging.info(f"Scraping URL: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                tree = html.fromstring(response.content)
                
                price_nodes = tree.xpath(self.PRICE_XPATH)
                price = int(price_nodes[3].strip().replace(',', '')) if price_nodes else None
                
                description = ''
                description_nodes = tree.xpath(self.DESCRIPTION_XPATHS)
                if description_nodes:
                    description = ' '.join(text.strip() for text in description_nodes if text.strip())
                else:
                    logging.error(f"Error extracting description for {url}: {e}")

                warranty = None
                warranty_nodes = tree.xpath(self.WARRANTY_XPATH)
                warranty_options = [node.strip() for node in warranty_nodes if node.strip() and node.strip() != "یک گزینه را انتخاب کنید"]
                warranty = ', '.join(set(warranty_options)) if warranty_options else None
                
                try:
                    product = Product.objects.get(url=url)
                    product_name_for_save = product.product_name
                except Product.DoesNotExist:
                    logging.warning(f"No product record found for {url}")
                    continue
                
                # Save the scraped data in database
                try:
                    message = Product.save_product_data(
                        product_name=product_name_for_save,
                        description=description,
                        price=price,
                        warranty=warranty
                    )
                    logging.info(f"Product saved with message: {message}")
                except ProductNotFound as e:
                    logging.error(f"Failed to save {product_name_for_save}: {e.message} (Code: {e.code})")
        
            except requests.RequestException as e:
                logging.error(f"Network error for {url}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error for {url}: {e}")
        
        logging.info(f"Scraping completed with DIZOLAND")












