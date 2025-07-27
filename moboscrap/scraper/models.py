from django.db import models
from django.core.exceptions import ValidationError
import logging

# Log Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    PRODUCT_TYPE_PHONE = 'PHONE'
    PRODUCT_TYPE_OTHER = 'OTHER'
    PRODUCT_TYPE_CHOICES = [
        (PRODUCT_TYPE_PHONE, "تلفن همراه"),
        (PRODUCT_TYPE_OTHER, "غیره"),
    ]
    product_name = models.CharField(max_length=255, verbose_name="نام محصول")
    color_prices = models.JSONField(default=dict, null=True, blank=True, )
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default=PRODUCT_TYPE_OTHER)
    color_prices = models.JSONField(default=dict, blank=True, verbose_name="قیمت گوشی بر اساس رنگ")
    price = models.IntegerField(null=True, blank=True, verbose_name="قیمت محصول")  
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
    def save_product_data(product_name, price=None, color_price_data=None, description=None, warranty=None, stock=None):
        """
        Save or update a product record with color-price JSON, description, warranty and stock.
        
        Args:
            product_name (str): Name of the product (e.g., "Samsung Galaxy S24 FE")
            color_price_data (dict): JSON data like {"black-phantom": 135000000, ...}
            description (str): Product description text
            warranty (str): Warranty name if it is available on site
            stock (int): The invetory of the product
        """
        try:
            try:
                target_product = Product.objects.get(product_name=product_name)
            except Product.DoesNotExist:
                logging.error(f"No record found for {product_name}") 
            if target_product.product_type == Product.PRODUCT_TYPE_PHONE:
                if color_price_data is not None:
                    target_product.color_prices = color_price_data
                    target_product.description = description
                    target_product.warranty = warranty
                    target_product.stock = stock
                    target_product.price = None
                    target_product.save()

                    return f"Updated {product_name}"
                else:
                    logging.error(f"color price field could not be empty for {product_name}")
            else:
                if price is not None:
                    target_product.price = price  # For non-phones
                    target_product.color_prices = {}  # Clear color_prices
                    target_product.description = description
                    target_product.warranty = warranty
                    target_product.stock = stock
                    target_product.save()

                    return f"Updated {product_name}"
                else:
                    logging.error(f"price field could not be empty for {product_name}")
        except Exception as e:
            return f"Error updating {product_name}: {e}"