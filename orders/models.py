from django.db import models

from products.models import Product
from django.conf import settings


class Cart(models.Model):
    total_price = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_order = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.pk} {self.user}"


class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} x{self.quantity}"

    def save(self, *args, **kwargs):
        self.price = (
                self.quantity * self.product.price
        )
        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f"{self.id} {self.user}"