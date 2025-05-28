from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name
    