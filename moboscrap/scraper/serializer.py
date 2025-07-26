from rest_framework import serializers
from scraper.models import Product

class ReferralSerialzer(serializers.ModelSerializer):
    class Meta:
        models = Product
        fields = [
        "id",
        "phone_model",
        "color_prices",
        "warranty",
        "stock",
        "description",
        "source_site",
        "url",
        "created_at",
        "updated_at",
        ]
        read_only_fields = ["id", "updated_at", "created_at"]