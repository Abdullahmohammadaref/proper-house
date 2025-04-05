from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    color = models.CharField(max_length=100)
    category = models.CharField(max_length=100)