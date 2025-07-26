from django.core.management.base import BaseCommand, CommandError
from scraper.scrapers.ilandino import scrape_ilandino_site
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
        try:
            results = scrape_ilandino_site(product_name=product_name)
            for result in results:
                if "Updated" in result:
                    self.stdout.write(self.style.SUCCESS(result))
                else:
                    self.stdout.write(self.style.ERROR(result))
        except ProductNotFound as e:
            self.stdout.write(self.style.ERROR(f"Failed: {e.message} (Code: {e.code})"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))
