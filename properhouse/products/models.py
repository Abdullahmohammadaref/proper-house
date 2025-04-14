from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category} - {self.name}"

class SubCategoryProperty(models.Model):
    DATA_TYPES = [
        ('STRING', 'String'),
        ('INTEGER', 'Integer'),
        ('DECIMAL', 'Decimal'),
        ('MULTIPLE_STRINGS', 'multiple_strings'),
        ('MULTIPLE_INTEGERS', 'multiple_integers'),
        ('MULTIPLE_DECIMALS', 'multiple_decimals'),
    ]

    category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    name = models.CharField(max_length=50)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES, default='STRING')
    ranged = models.BooleanField(default=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        default='products/default.png'
    )
    pdf = models.FileField(
        upload_to='pdfs/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text='Upload product specification PDF'
    )

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.brand} - {self.category} - {self.name} "


class ProductModel(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='models'
    )
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.brand.name} {self.name}"

"""
class BaseProperty(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

class PropertyString(BaseProperty):
    value = models.CharField(max_length=255)

class PropertyInteger(BaseProperty):
    value = models.IntegerField()

class PropertyDecimal(BaseProperty):
    value = models.DecimalField(max_digits=10, decimal_places=2)

class PropertyMultipleStrings(BaseProperty):
    values = models.JSONField(default=list)

class PropertyMultipleIntegers(BaseProperty):
    values = models.JSONField(default=list)

class PropertyMultipleDecimals(BaseProperty):
    values = models.JSONField(default=list)

class PropertyRangeInteger(BaseProperty):
    min_value = models.IntegerField()
    max_value = models.IntegerField()

class PropertyRangeDecimal(BaseProperty):
    min_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_value = models.DecimalField(max_digits=10, decimal_places=2)




value_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    value_object_id = models.PositiveIntegerField()
    value = GenericForeignKey('value_content_type', 'value_object_id')
    
    
    
    
    
    expected_type = self.property.data_type
        actual_type = self.value_content_type.model_class().__name__.lower()
        if not actual_type.startswith(expected_type.split('_')[0].lower()):
            raise ValueError(f"Expected {expected_type} but got {actual_type}")
"""



class ModelProperty(models.Model):
    model = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    property = models.ForeignKey(
        SubCategoryProperty,
        on_delete=models.CASCADE
    )

    value = model.CharField(max_length=255, default='')


    class Meta:
        unique_together = ('model', 'property')

    def __str__(self):
        return f"{self.model} - {self.property.name}"

    def clean(self):
        super().clean()
        if self.property.category != self.model.product.category:
            raise ValueError("Category must be equal to product.category")

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforces validation
        super().save(*args, **kwargs)






