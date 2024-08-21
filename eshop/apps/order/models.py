from django.db import models
from django.contrib.auth.models import User
from apps.product.models import Product


class Order(models.Model):
    code = models.CharField(
        max_length=100, 
        unique=True
    )
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=2
    )
    purchase_date = models.DateField(
        null=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="orders"
    )
    products = models.ManyToManyField(
        Product, 
        related_name="orders"
    )

    def __str__(self):
        return self.code
