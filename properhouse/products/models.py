from django.db import models

# Create your models here.



class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    model = models.CharField(max_length=50)
    power = models.IntegerField()
    min_lumen = models.IntegerField()
    max_lumen = models.IntegerField()
    min_voltage= models.IntegerField()
    max_voltage= models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    size = models.IntegerField()
    cct = models.IntegerField()  ### make this a list somehow
    pcs_cnt = models.IntegerField()
    price = models.FloatField()
    color = models.CharField(max_length=50)  ## make a tuples inside list, because some lamps can change colors while other have fixed colored but the cutomer can buy difrent colors
    material = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
