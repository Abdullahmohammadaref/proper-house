import nested_admin
from pdb import post_mortem

from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django import forms


class MediaInline(admin.TabularInline):
    model = Media
    can_delete = False  # Prevent deleting Media if Brand is saved
    max_num = 1         # Allow only 1 Media per Brand (OneToOne)
    fields = ('image', 'name')  # Exclude 'brand' field (auto-linked)

class ModelMediaInline(nested_admin.NestedTabularInline):
    model = ModelMedia
    extra = 1

class SubcategoryAttributeModelStringInline(nested_admin.NestedStackedInline):
    model = SubcategoryAttributeModelString
    extra = 1

class SubcategoryAttributeModelIntegerInline(nested_admin.NestedStackedInline):
    model = SubcategoryAttributeModelInteger
    extra = 1

class SubcategoryAttributeModelDecimalInline(nested_admin.NestedStackedInline):
    model = SubcategoryAttributeModelDecimal
    extra = 1

class SubcategoryAttributeModelRangedIntegerInline(nested_admin.NestedStackedInline):
    model = SubcategoryAttributeModelRangedInteger
    extra = 1

class SubcategoryAttributeModelRangedDecimalInline(nested_admin.NestedStackedInline):
    model = SubcategoryAttributeModelRangedDecimal
    extra = 1

class AttributeInline(admin.TabularInline):
    model = SubcategoryAttribute

class ModelInline(nested_admin.NestedStackedInline):
    model = Model
    inlines = [
        ModelMediaInline,
        SubcategoryAttributeModelStringInline,
        SubcategoryAttributeModelIntegerInline,
        SubcategoryAttributeModelDecimalInline,
        SubcategoryAttributeModelRangedIntegerInline,
        SubcategoryAttributeModelRangedDecimalInline,
    ]
    extra = 1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [MediaInline]  # Add the inline
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [MediaInline]  # Add the inline
    list_display = ('name',)

@admin.register(Subcategory)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [MediaInline, AttributeInline]  # Add the inline
    list_display = ('name', 'category')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    # Optional: Hide 'brand' in standalone Media admin
    exclude = ('brand', 'category', 'subcategory')
    list_display = ('image', 'pdf')

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ModelInline]

@admin.register(Integer)
class IntegerAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(Decimal)
class DecimalAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(String)
class StringAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(RangedDecimal)
class RangedDecimalAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(RangedInteger)
class RangedIntegerAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


'''
problems and tasks:
1- task: make autonaming for media with the help of __str__ for the model
2- problem: one model can have a attributes(like wat, volt, etc) from another subcategory (it should only be able to have access to the attributes of its own subcategory)
3- order the models in admin terminal in this order: Brand, Category, Subcategory, Products
4- fix the venv
'''

