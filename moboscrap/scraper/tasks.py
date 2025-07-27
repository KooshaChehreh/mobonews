from celery import shared_task
from scraper.scrapers.ilandino import ScrapIlandino
from scraper.scrapers.dizoland import ScrapDiznoland
from scraper.scrapers.greenlion import ScrapGreenlion
from scraper.scrapers.iranpowerology import ScrapIranpower

@shared_task(bind=True, max_retries=3, retry_backoff=True)
def scrap_ilandino(self, product=None):
    try:
        scraper = ScrapIlandino()
        scraper.scrap(product=product)
    except Exception as e:
        self.retry(countdown=60)
    return f"Completed scraping ilandino for {product or 'all products'}"

@shared_task(bind=True, max_retries=3, retry_backoff=True)
def scrap_dizoland(self, product=None):
    try:
        scraper = ScrapDiznoland()
        scraper.scrap(product=product)
    except Exception as e:
        self.retry(countdown=60)
    return f"Completed scraping dizoland for {product or 'all products'}"

@shared_task(bind=True, max_retries=3, retry_backoff=True)
def scrap_greenlion(self, product=None):
    try:
        scraper = ScrapGreenlion()
        scraper.scrap(product=product)
    except Exception as e:
        self.retry(countdown=60)
    return f"Completed scraping greenlion for {product or 'all products'}"

@shared_task(bind=True, max_retries=3, retry_backoff=True)
def scrap_iranpower(self, product=None):
    try:
        scraper = ScrapIranpower()
        scraper.scrap(product=product)
    except Exception as e:
        self.retry(countdown=60)
    return f"Completed scraping iranpower for {product or 'all products'}"