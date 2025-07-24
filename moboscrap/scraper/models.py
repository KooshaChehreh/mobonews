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
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    warranty = models.CharField(max_length=100, null=True, blank=True, verbose_name="گارانتی")
    availability = models.CharField(max_length=50, null=True, blank=True, verbose_name="موجود است؟")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات محصول")
    source_site = models.CharField(max_length=2, choices=SITE_CHOICES, verbose_name="منبع سایت")
    path = models.CharField(max_length=255, verbose_name="آدرس محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        unique_together = ('source_site', 'path')