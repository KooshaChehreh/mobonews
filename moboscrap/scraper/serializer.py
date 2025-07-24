from rest_framework import serializers
from scraper.models import Product

class ReferralSerialzer(serializers.ModelSerializer):
    class Meta:
        models = Product
        fields = [
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
        ]
        read_only_fields = ["id", "updated_at", "created_at"]