Mobonews Web Scraper
Mobonews is a Django-based web scraping project that extracts product data (price, description, color-price variations) from four e-commerce sites: ilandino.com, dizoland.com, greenlion.net, and iranpower.ir. It uses Django, Celery for asynchronous tasks, and SQLite for testing. The run_scraper command triggers scraping tasks.
Project Overview
What I’ve Done

Built four scraper classes (ScrapIlandino, ScrapDiznoland, ScrapGreenlion, ScrapIranpower) using lxml and requests, inheriting from an abstract Scraper base class.
Designed a Product model for storing product data in the scraper_product table.
Integrated Celery for asynchronous scraping with retry logic.
Created the run_scraper command to scrape all or specific products.
Wrote mocked unit tests to avoid database errors like no such table: scraper_product.

Key Features

Asynchronous scraping with Celery.
Supports single-product or all-products scraping.


Setup Instructions

Clone the Repository:
git clone <repository-url>
cd mobonews


Build and Run with Docker Compose:
docker-compose build
docker-compose up

This starts the Django app, Celery workers, Redis, and applies migrations automatically.


Running the Project

The project runs via docker-compose up at http://localhost:8000.

Running Tests
tests could be ran out of the container environment. in the directory of manage.py just run:
python manage.py test

**mention that tests are sample and they should be completed.

Django admin
is available on http://localhost:8000/admin
create a super user and loging and add products. product_name, url, product_type and source_site are constraints.
1. docker exec -it mobonews bash
2. cd moboscrap/
3. python manage.py createsuperuser

Running the Scraping Command
The run_scraper command triggers scraping for all four sites.
In the Terminal open the app container:
1. docker exec -it mobonews bash
2. cd moboscrap/
then run:
Update All Products:python manage.py run_scraper


Update a Specific Product:python manage.py run_scraper -n "Roborock Saros 10R"


How It Works: The command triggers Celery tasks to scrape and update the product’s data (price, color prices, description) for each site where it exists.

Project Structure
mobonews/
├── moboscrap/
│   ├── scraper/
│   │   ├── management/
│   │   │   ├── commands/
│   │   │   ├── run_scraper.py
│   │   ├── migrations/
│   │   ├── scrapers/
│   │   │   ├── base_scraper.py
│   │   │   ├── ilandino.py
│   │   │   ├── dizoland.py
│   │   │   ├── greenlion.py
│   │   │   ├── iranpower.py
│   │   ├── tests/
│   │   │   ├── test_ilandino.py
│   │   ├── models.py
│   │   ├── tasks.py
│   ├───mobonews/
│   │   ├── __init__.py
│   │   ├── celery.py
│   │   ├── settings.py
│   ├───manage.py
├── requirements.txt
├── docker-compose.yml
