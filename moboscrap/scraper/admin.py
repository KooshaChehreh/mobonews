from django.contrib import admin
from scraper.models import Product

@admin.register(Product)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "color_prices",
        "warranty",
        "stock",
        "description",
        "source_site",
        "url",
        "created_at",
        "updated_at",
    )
