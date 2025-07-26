from django.db import models

class Product(models.Model):
    SITE_ILANDINO = "IL"
    SITE_DIZOLAND = "DZ"
    SITE_IRANPOWER = "IP"
    SITE_GREENLION = "GL"
    SITE_CHOICES = [
        (SITE_ILANDINO, "آیلندینو"),
        (SITE_DIZOLAND, "دیزولند"),
        (SITE_IRANPOWER, "ایران پاور"),
        (SITE_GREENLION, "گرین لاین"),
    ]
    phone_model = models.CharField(max_length=255, verbose_name="مدل گوشی")
    color_prices = models.JSONField(default=dict, null=True, blank=True, verbose_name="قیمت بر اساس رنگ")
    warranty = models.CharField(max_length=100, null=True, blank=True, verbose_name="گارانتی")
    stock = models.CharField(max_length=50, null=True, blank=True, verbose_name="موجودی")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات محصول")
    source_site = models.CharField(max_length=2, choices=SITE_CHOICES, verbose_name="منبع سایت")
    url = models.CharField(max_length=255, verbose_name="آدرس محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        unique_together = ('source_site', 'url')
    
    @staticmethod
    def save_product_data(phone_model, color_price_data, description=None, warranty=None, stock=None):
        """
        Save or update a product record with color-price JSON, description, warranty and stock.
        
        Args:
            phone_model (str): Name of the product (e.g., "Samsung Galaxy S24 FE")
            color_price_data (dict): JSON data like {"black-phantom": 135000000, ...}
            description (str): Product description text
            warranty (str): Warranty name if it is available on site
            stock (int): The invetory of the product
        """
        try:
            if not Product.objects.filter(phone_model=phone_model).exists():
                return f"No record found for {phone_model}"
            
            Product.objects.filter(phone_model=phone_model).update(
                color_prices=color_price_data or {},
                description=description,
                warranty=warranty,
                stock=stock
            )
            return f"Updated {phone_model}"
        except Exception as e:
            return f"Error updating {phone_model}: {e}"