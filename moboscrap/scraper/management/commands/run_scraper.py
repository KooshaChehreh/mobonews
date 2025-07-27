from django.core.management.base import BaseCommand, CommandError
from scraper.scrapers.ilandino import ScrapIlandino
from scraper.scrapers.dizoland import ScrapDiznoland
from scraper.scrapers.greenlion import ScrapGreenlion
from scraper.scrapers.iranpowerology import ScrapIranpower


from scraper.exceptions import ProductNotFound


class Command(BaseCommand):
    help = 'Scrape product data from ilandino.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--name',
            type=str,
            help='Optional product name to scrape (e.g., "Samsung Galaxy S24 FE")'
        )

    def handle(self, *args, **kwargs):
        product_name = kwargs['name']
        # try:
        ilandino_scraper = ScrapIlandino()
        ilandino_results = ilandino_scraper.scrap(product=product_name)

        dizoland_scraper = ScrapDiznoland()
        dizoland_results = dizoland_scraper.scrap(product=product_name)

        greenlion_scraper = ScrapGreenlion()
        greenlion_results = greenlion_scraper.scrap(product=product_name)

        iranpower_scraper = ScrapIranpower()
        iranpower_results = iranpower_scraper.scrap(product=product_name)

