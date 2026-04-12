from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.TextField()
    price = models.FloatField()
    image = models.URLField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)

    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name