from abc import ABC, abstractmethod
from scraper.models import Product
import logging

# Log Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Scraper(ABC):
    @abstractmethod
    def scrap(self, product: str):
        """
        Scrape product data for the given product model.
        
        Args:
            product (str): Product model name (e.g., "Samsung Galaxy S24 FE")
        
        Returns:
            List: List of result messages (e.g., ["Updated Samsung Galaxy S24 FE"])
        
        Raises:
            ProductNotFound: If no product record exists
        """
        pass

    def get_scrap_urls(self, site_constant, product=None):
        """
        Retrieve URLs for a single product or all products for a specific site.
        
        Args:
            product (str, optional): Product name to scrape a single product.
            site_constant (str): Site identifier (e.g., Product.SITE_ILANDINO).
        
        Returns:
            list: List of URLs to scrape.
        """
        url_list = []
        try:
            if product:
                try:
                    product_obj = Product.objects.get(product_name=product)
                    url_list.append(product_obj.url)
                    logging.info(f"Processing single product: {product}")
                except Product.DoesNotExist:
                    logging.error(f"Product not found: {product}")
                    return [f"Skipped {product}: Product not found"]
            else:
                products = Product.objects.filter(source_site=site_constant).values('url')
                url_list = [product['url'] for product in products]
                logging.info(f"Processing {len(url_list)} products from site {site_constant}")
        except Exception as e:
            logging.error(f"Error retrieving product URLs: {e}")
            return [f"Failed to retrieve URLs: {e}"]
        return url_list