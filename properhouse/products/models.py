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
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def values_range(self):
        values_range = (self.min_value, self.max_value)
        return values_range

    class Meta:
        unique_together = ('min_value', 'max_value')

    def __str__(self):
        return f"{self.min_value}-{self.max_value}"


class RangedInteger(models.Model):
    min_value = models.IntegerField(blank=False, null=False)
    max_value = models.IntegerField(blank=False, null=False)

    def values_range(self):
        values_range = (self.min_value, self.max_value)
        return values_range

    class Meta:
        unique_together = ('min_value', 'max_value')

    def __str__(self):
        return f"{self.min_value} - {self.max_value}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"

class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

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

    class Meta:
        unique_together = ('category', 'name')


    def __str__(self):
        return f"{self.name}"

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
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        unique_together = [
            ('image', 'pdf', 'name'),
            ('image', 'pdf'),
        ]                                        ### check if this is good

    def __str__(self):
        return f"{self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"


class SubcategoryAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'subcategory')

    def __str__(self):
        return f"{self.subcategory} - {self.attribute}"


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        unique_together = [
            ('brand', 'subcategory', 'name'),
            ('brand', 'subcategory'),
        ]

    def __str__(self):
        return f"{self.brand} - {self.subcategory} - {self.name}"


class Model(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    model_letter = models.CharField(max_length=10, blank=True, null=False)
    model_number = models.IntegerField(blank=False, null=False)
    media = models.ManyToManyField(Media, through="ModelMedia")

    string_values = models.ManyToManyField(String, through="SubcategoryAttributeModelString")
    integer_values = models.ManyToManyField(Integer, through="SubcategoryAttributeModelInteger")
    decimal_values = models.ManyToManyField(Decimal, through="SubcategoryAttributeModelDecimal")
    ranged_integer_value = models.ManyToManyField(RangedInteger, through="SubcategoryAttributeModelRangedInteger")
    ranged_decimal_value = models.ManyToManyField(RangedDecimal, through="SubcategoryAttributeModelRangedDecimal")

    def value(self):
        values = 0
        attribute_value = None
        value_attributes = [self.string_values, self.integer_values, self.decimal_values, self.ranged_integer_value,
                            self.ranged_decimal_value]
        for value in value_attributes:
            if value is not None:
                values += values
                attribute_value = value
        if values != 1:
            raise ValueError("A subcategory attribute cannot have less than or more than 1 value")
        else:
            return attribute_value

    value = value

    unique_together = [
        ('model_number', 'model_letter', 'product', 'value'),
        ('model_number', 'model_letter', 'product'),
        ('model_number', 'model_letter'),
    ]

    def __str__(self):
        return f"{self.product} - {self.model_letter}{self.model_number}"  # i removed  - {self.value} here becaue i got eror, find solution

class ModelMedia(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('media', 'model')

class SubcategoryAttributeModelString(models.Model):
    subcategory_attribute = models.ForeignKey(SubcategoryAttribute, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    string = models.ForeignKey(String, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('subcategory_attribute','string'),
            ('model', 'string'),
            ('model', 'subcategory_attribute'),
            ('subcategory_attribute', 'string', 'model')
        ]

    def __str__(self):
        return f"{self.subcategory_attribute} - {self.model} - {self.string}"


class SubcategoryAttributeModelInteger(models.Model):
    subcategory_attribute = models.ForeignKey(SubcategoryAttribute, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    integer = models.ForeignKey(Integer, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('subcategory_attribute','integer'),
            ('model', 'integer'),
            ('model', 'subcategory_attribute'),
            ('subcategory_attribute', 'integer', 'model')
        ]

    def __str__(self):
        return f"{self.subcategory_attribute} - {self.model} - {self.integer}"


class SubcategoryAttributeModelDecimal(models.Model):
    subcategory_attribute = models.ForeignKey(SubcategoryAttribute, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    decimal = models.ForeignKey(Decimal, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('subcategory_attribute','decimal'),
            ('subcategory_attribute', 'decimal', 'model')
        ]

    def __str__(self):
        return f"{self.subcategory_attribute} - {self.model} - {self.decimal}"

class SubcategoryAttributeModelRangedInteger(models.Model):
    subcategory_attribute = models.ForeignKey(SubcategoryAttribute, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    ranged_integer = models.ForeignKey(RangedInteger, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('subcategory_attribute','ranged_integer'),
            ('model', 'ranged_integer'),
            ('model', 'subcategory_attribute'),
            ('subcategory_attribute', 'ranged_integer', 'model')
        ]

    def __str__(self):
        return f"{self.subcategory_attribute} - {self.model} - {self.ranged_integer}"

class SubcategoryAttributeModelRangedDecimal(models.Model):
    subcategory_attribute = models.ForeignKey(SubcategoryAttribute, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    ranged_decimal = models.ForeignKey(RangedDecimal, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('subcategory_attribute','ranged_decimal'),
            ('model', 'ranged_decimal'),
            ('model', 'subcategory_attribute'),
            ('subcategory_attribute', 'ranged_decimal', 'model')
        ]

    def __str__(self):
        return f"{self.subcategory_attribute} - {self.model} - {self.ranged_decimal}"





