from django.db import models

from django.conf import settings


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)


class Product(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    pictures = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    is_watched = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now_add=False)
    day = models.DateTimeField(auto_now_add=False)
    category = models.ForeignKey(
        ProductCategory,
        related_name="category",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name

