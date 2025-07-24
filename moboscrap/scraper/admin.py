from django.contrib import admin
from scraper.models import Product

@admin.register(Product)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_model",
        "price",
        "warranty",
        "availability",
        "description",
        "source_site",
        "path",
        "created_at",
        "updated_at",
    )
