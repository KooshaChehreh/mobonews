from django.core.management.base import BaseCommand, CommandError
from scraper.scrapers.ilandino import ScrapIlandino
from scraper.scrapers.dizoland import ScrapDiznoland
from scraper.scrapers.greenlion import ScrapGreenlion
from scraper.scrapers.iranpowerology import ScrapIranpower
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from scraper.exceptions import ProductNotFound


from django.core.management.base import BaseCommand
from scraper.tasks import scrap_ilandino, scrap_dizoland, scrap_greenlion, scrap_iranpower

class Command(BaseCommand):
    help = 'Scrape product data from ilandino.com, dizoland, greenlion, and iranpower'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--name',
            type=str,
            help='Optional product name to scrape (e.g., "Samsung Galaxy S24 FE")'
        )

    def handle(self, *args, **kwargs):
        product_name = kwargs['name']
        self.stdout.write(self.style.SUCCESS('Starting scraping tasks...'))

        # Run Celery tasks asynchronously
        ilandino_task = scrap_ilandino.delay(product_name)
        dizoland_task = scrap_dizoland.delay(product_name)
        greenlion_task = scrap_greenlion.delay(product_name)
        iranpower_task = scrap_iranpower.delay(product_name)

        results = [
            ilandino_task.get(),
            dizoland_task.get(),
            greenlion_task.get(),
            iranpower_task.get()
        ]

        for result in results:
            logging.info(result)