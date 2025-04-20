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
    fields = ('image', 'pdf')  # Exclude 'brand' field (auto-linked)

class ModelMediaInline(nested_admin.NestedTabularInline):
    model = ModelMedia
    extra = 1

class StringInline(nested_admin.NestedTabularInline):
    model = String
    max_num = 1

class IntegerInline(nested_admin.NestedTabularInline):
    model = Integer
    max_num = 1

class DecimalInline(nested_admin.NestedTabularInline):
    model = Decimal
    max_num = 1

class RangedIntegerInline(nested_admin.NestedTabularInline):
    model = RangedInteger
    max_num = 1

class RangedDecimalInline(nested_admin.NestedTabularInline):
    model = RangedDecimal
    max_num = 1

class AttributeValueInline(nested_admin.NestedGenericStackedInline):
    model = AttributeValue
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1

    inlines = [
        StringInline,
        IntegerInline,
        DecimalInline,
        RangedIntegerInline,
        RangedDecimalInline
    ]

class ModelAttributeInline(nested_admin.NestedStackedInline):
    model = ModelAttribute
    extra = 1


class AttributeInline(admin.TabularInline):
    model = SubcategoryAttribute
    autocomplete_fields = ['attribute']

class SubcategoryInline(admin.TabularInline):
    model = SubcategoryAttribute
    autocomplete_fields = ['subcategory']




class ModelInline(nested_admin.NestedStackedInline):
    model = Model
    inlines = [ModelMediaInline, ModelAttributeInline]
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
    search_fields = ['name']

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    # Optional: Hide 'brand' in standalone Media admin
    exclude = ('brand', 'category', 'subcategory')
    list_display = ('image', 'pdf')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ModelInline]

"""
class CategoryForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)
        self.fields['name'].help_text = 'test help text'
    class Meta:
        model = Category
        exclude = ("",)

@admin.register(Category)
class CategoryFormAdmin(admin.ModelAdmin):
    form = CategoryForm

# admin.py
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from .models import *


# ================ VALUE TYPE ADMINS ================
@admin.register(String)
class StringAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(Integer)
class IntegerAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(Decimal)
class DecimalAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(RangedDecimal)
class RangedDecimalAdmin(admin.ModelAdmin):
    search_fields = ['min_value', 'max_value']


@admin.register(RangedInteger)
class RangedIntegerAdmin(admin.ModelAdmin):
    search_fields = ['min_value', 'max_value']


# ================ ATTRIBUTE SYSTEM ================
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ['attribute__name', 'value__value']
    list_filter = ['attribute']


class AttributeValueInline(GenericTabularInline):
    model = AttributeValue
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 1
    autocomplete_fields = ['attribute']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


# ================ MEDIA ADMIN ================
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['preview_image', 'pdf_link']
    search_fields = ['image', 'pdf']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

    def pdf_link(self, obj):
        if obj.pdf:
            return format_html('<a href="{}">📄 PDF</a>', obj.pdf.url)
        return "-"


# ================ PRODUCT HIERARCHY ================
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'media_preview']

    def media_preview(self, obj):
        if obj.media and obj.media.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.media.image.url)
        return "-"


# ================ PRODUCTS & MODELS ================
class ModelMediaInline(admin.TabularInline):
    model = ModelMedia
    extra = 1
    autocomplete_fields = ['media']


class ModelAttributeInline(admin.TabularInline):
    model = ModelAttribute
    extra = 1
    autocomplete_fields = ['attribute_value']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    search_fields = ['model_letter', 'model_number']
    list_display = ['model_display', 'product']  # Changed from full_model_code
    autocomplete_fields = ['product']
    inlines = [ModelMediaInline, ModelAttributeInline]

    def model_display(self, obj):
        return f"{obj.product.brand} {obj.product} {obj.model_letter}{obj.model_number}"
    model_display.short_description = "Full Model Code"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'brand', 'subcategory']
    autocomplete_fields = ['brand', 'subcategory']


# ================ ADMIN CUSTOMIZATION ================
admin.site.site_header = "Product Database Admin"
admin.site.site_title = "Product Admin Portal"
admin.site.index_title = "Welcome to Product Management"
"""
"""
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Model)
admin.site.register(Media)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(String)
admin.site.register(Integer)
admin.site.register(Decimal)
admin.site.register(RangedDecimal)
admin.site.register(RangedInteger)
"""
"""
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