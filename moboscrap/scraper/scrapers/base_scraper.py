from abc import ABC, abstractmethod

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