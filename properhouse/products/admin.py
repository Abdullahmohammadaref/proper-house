from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CategoryPropertyInline(admin.TabularInline):
    model = SubCategoryProperty
    extra = 1  # Number of empty forms to display

@admin.register(SubCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    inlines = [CategoryPropertyInline]  # Allows editing CategoryProperties inline

@admin.register(SubCategoryProperty)
class CategoryPropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'data_type')
    list_filter = ('category', 'data_type')
    search_fields = ('name', 'category__name')

class ProductModelInline(admin.TabularInline):
    model = ProductModel
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'image', 'pdf')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'category__name', 'brand__name')
    inlines = [ProductModelInline]  # Allows managing ProductModels inline
    # In ProductAdmin
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "-"

    image_preview.short_description = 'Preview'

class ModelPropertyInline(admin.TabularInline):
    model = ModelProperty
    extra = 1

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')
    search_fields = ('name', 'product__name')
    inlines = [ModelPropertyInline]  # Allows managing ModelProperties inline

admin.site.register(ModelProperty)
"""
class BasePropertyInline(GenericTabularInline):
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 0


class PropertyStringInline(BasePropertyInline):
    model = PropertyString


class PropertyIntegerInline(BasePropertyInline):
    model = PropertyInteger


class PropertyDecimalInline(BasePropertyInline):
    model = PropertyDecimal


class PropertyMultipleStringsInline(BasePropertyInline):
    model = PropertyMultipleStrings


class PropertyMultipleIntegersInline(BasePropertyInline):
    model = PropertyMultipleIntegers


class PropertyMultipleDecimalsInline(BasePropertyInline):
    model = PropertyMultipleDecimals


class PropertyRangeIntegerInline(BasePropertyInline):
    model = PropertyRangeInteger


class PropertyRangeDecimalInline(BasePropertyInline):
    model = PropertyRangeDecimal


class ModelPropertyAdmin(admin.ModelAdmin):
    list_display = ('model', 'property', 'value_type', 'value_preview')
    list_filter = ('property__data_type',)
    inlines = [
        PropertyStringInline,
        PropertyIntegerInline,
        PropertyDecimalInline,
        PropertyMultipleStringsInline,
        PropertyMultipleIntegersInline,
        PropertyMultipleDecimalsInline,
        PropertyRangeIntegerInline,
        PropertyRangeDecimalInline,
    ]

    def value_type(self, obj):
        return obj.property.get_data_type_display()

    def value_preview(self, obj):
        if obj.value:
            return str(obj.value)
        return "-"

    value_preview.short_description = "Value"

    def get_inline_instances(self, request, obj=None):
        
        if not obj:
            return []

        data_type = obj.property.data_type.lower()
        inlines = {
            'string': [PropertyStringInline],
            'integer': [PropertyIntegerInline],
            'decimal': [PropertyDecimalInline],
            'multiple_strings': [PropertyMultipleStringsInline],
            'multiple_integers': [PropertyMultipleIntegersInline],
            'multiple_decimals': [PropertyMultipleDecimalsInline],
            'range_integer': [PropertyRangeIntegerInline],
            'range_decimal': [PropertyRangeDecimalInline],
        }
        return [inline(self.model, self.admin_site) for inline in inlines.get(data_type, [])]


admin.site.register(ModelProperty, ModelPropertyAdmin)


# Add JavaScript to hide/show appropriate inlines
class Media:
    js = (
        'admin/js/jquery.init.js',
        'admin/js/modelproperty_inlines.js',
    )

"""