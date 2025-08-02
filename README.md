🌟 Mobonews Web Scraper
Mobonews is a Django-based web scraping project that extracts product data (price, description, color-price variations) from four e-commerce sites: ilandino.com, dizoland.com, greenlion.net, and iranpower.ir. Built with Django and Celery for asynchronous task processing, it uses SQLite for testing and includes a custom run_scraper command to trigger scraping tasks.
📋 Project Overview
My Contributions

Developed four scraper classes (ScrapIlandino, ScrapDiznoland, ScrapGreenlion, ScrapIranpower) using lxml and requests, inheriting from an abstract Scraper base class.
Designed a Product model to store data in the scraper_product table.
Integrated Celery for asynchronous scraping with retry logic for reliability.
Created the run_scraper command to scrape all or specific products.
Wrote mocked unit tests to prevent database errors (e.g., no such table: scraper_product).

Key Features

🚀 Asynchronous scraping with Celery for efficient task processing.
🎯 Supports scraping all products or a single product across four sites.
✅ Sample unit tests provided (to be completed for full coverage).

🛠️ Setup Instructions

Clone the Repository:
git clone <repository-url>
cd mobonews


Build and Run with Docker Compose:
docker-compose build
docker-compose up

This starts the Django app, Celery workers, Redis, and applies migrations automatically.


🚀 Running the Project
The project runs via docker-compose up and is accessible at http://localhost:8000.
🧪 Running Tests
Tests are sample implementations and should be completed for full coverage. To run them outside the container environment, in the directory containing manage.py:
python manage.py test

🔐 Django Admin
Manage products via the Django admin interface at http://localhost:8000/admin. Required fields: product_name, url, product_type, and source_site.

Access the app container:docker exec -it mobonews bash
cd moboscrap/


Create a superuser:python manage.py createsuperuser


Log in at http://localhost:8000/admin and add products.

🕸️ Running the Scraping Command
The run_scraper command triggers scraping for all four sites.
In the Terminal

Access the app container:docker exec -it mobonews bash
cd moboscrap/


Run the command:
Update All Products:python manage.py run_scraper


Update a Specific Product:python manage.py run_scraper -n "Roborock Saros 10R"


How It Works
The run_scraper command triggers Celery tasks to scrape and update product data (price, color prices, description) for each site where the product exists in the Product model.
