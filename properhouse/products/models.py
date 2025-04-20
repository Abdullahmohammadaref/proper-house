from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class String(models.Model):
    value = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.value}"


class Integer(models.Model):
    value = models.IntegerField(unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.value}"


class Decimal(models.Model):
    value = models.DecimalField(unique=True, blank=False, null=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.value}"


class RangedDecimal(models.Model):
    min_value = models.DecimalField(max_digits=10, decimal_places=2, unique=True, blank=False, null=False)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, unique=True, blank=False, null=False)

    def values_range(self):
        values_range = (self.min_value, self.max_value)
        return values_range

    def __str__(self):
        return f"{self.min_value} - {self.max_value}"


class RangedInteger(models.Model):
    min_value = models.IntegerField(unique=True, blank=False, null=False)
    max_value = models.IntegerField(unique=True, blank=False, null=False)

    def values_range(self):
        values_range = (self.min_value, self.max_value)
        return values_range

    def __str__(self):
        return f"{self.min_value} - {self.max_value}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"

class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    value = models.ManyToManyField()
    def __str__(self):
        return f"{self.name}"

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    attribute = models.ManyToManyField(
        Attribute,
        through='SubcategoryAttribute',
        related_name='subcategory'
    )

    def __str__(self):
        return f"{self.name}"




class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value =

    class Meta:
        unique_together = ('attribute',)

    def __str__(self):
        return f"{self.attribute}:{self.value}"
    """


    class AttributeValueString(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    string = models.ForeignKey(String, on_delete=models.CASCADE)

class AttributeValueInteger(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    integer = models.ForeignKey(Integer, on_delete=models.CASCADE)

class AttributeValueDecimal(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    decimal = models.ForeignKey(Decimal, on_delete=models.CASCADE)

class AttributeValueRangedDecimal(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    ranged_decimal = models.ForeignKey(RangedDecimal, on_delete=models.CASCADE)

class AttributeValueRangedInteger(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    ranged_integer = models.ForeignKey(RangedInteger, on_delete=models.CASCADE)
    """


"""
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    string_values = models.JSONField(default=list, null=True, blank=True)
    integer_values = ...
    decimal_values = ...
    ranged_integer_value = ..
    ranged_decimal_value = ...

    def value(self):
        values = 0
        attribute_value = None
        value_attributes = [self.string_values, self.integer_values, self.decimal_values, self.ranged_integer_value, self.ranged_decimal_value]
        for value in value_attributes:
            if value is not None:
                values += values
                attribute_value = value
        if values != 1:
            raise ValueError
        else:
            return attribute_value

    value = value

    class Meta:
        unique_together = ('name', 'value')

    def __str__(self):

         f"{self.attribute}:{self.value}"   ## there is a missing return here 
"""


class Media(models.Model):
    brand = models.OneToOneField(
        'Brand',
        on_delete=models.SET_NULL,
        null=True,  # Allow Media without a Brand
        blank=True,  # Allow empty in forms/admin
        related_name='media'  # Access Media from Brand via `brand.media`
    )
    category = models.OneToOneField(
        'Category',
        on_delete=models.SET_NULL,
        null=True,  # Allow Media without a Brand
        blank=True,  # Allow empty in forms/admin
        related_name='media'  # Access Media from Brand via `brand.media`
    )
    subcategory = models.OneToOneField(
        'Subcategory',
        on_delete=models.SET_NULL,
        null=True,  # Allow Media without a Brand
        blank=True,  # Allow empty in forms/admin
        related_name='media'  # Access Media from Brand via `brand.media`
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        default='products/default.png'
    )
    pdf = models.FileField(
        upload_to='pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text='Upload product specification PDF'
    )

    class Meta:
        unique_together = ('image', 'pdf')


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"


class SubcategoryAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'subcategory')


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        unique_together = ('brand', 'subcategory', 'name')

    def __str__(self):
        return f"{self.name}"


class Model(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    model_letter = models.CharField(max_length=10, blank=True, null=False)
    model_number = models.IntegerField(blank=False, null=False)
    media = models.ManyToManyField(Media, through="ModelMedia")
    attribute_values = models.ManyToManyField(AttributeValue, through="ModelAttribute")

    class Meta:
        unique_together = ('product', 'model_letter', 'model_number')

    def __str__(self):
        return f"{self.model_letter}{self.model_number}"


class ModelAttribute(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute_value', 'model')


class ModelMedia(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('media', 'model')















