from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Min, Max
# Create your views here.

def home(request):
    return render(request, 'products/home.html')

def about(request):
    return render(request, 'products/about.html')


def products(request):
    return render(request, 'products/products.html',{
        "categories": Category.objects.all(),
        "subcategories": Subcategory.objects.all(),
    })

def locations(request):
    return render(request, 'products/locations.html')

def contact(request):
    return render(request, 'products/contact.html')

def product(request, product_id, category_name, subcategory_name):
    product = Product.objects.get(pk=product_id)
    return render(request, 'products/product.html',{
        'product': product,
    })

def category(request, category_name):
    category = Category.objects.get(name=category_name)
    return render(request, 'products/category.html',{
        'category': category
    })

def subcategory(request, subcategory_name, category_name):
    category = Category.objects.get(name=category_name)
    subcategory = Subcategory.objects.get(name=subcategory_name, category=category)
    products = Product.objects.filter(category=subcategory)


    if request.method == "GET":
        submitted_data = {
            key: value
            for key, value in request.GET.items()
            if key != 'csrfmiddlewaretoken'  # Exclude CSRF token
        }

        for key, value in submitted_data.items():
            if key == "brand":
                for product in products:
                    if product.brand.id != value:
                        products = products.exclude(id=product.id)
                    else:
                        continue

    return render(request, 'products/subcategory.html', {
        'subcategory': subcategory,
        'category': category,
        'products': products,
        'brands': Brand.objects.all(),
    })


