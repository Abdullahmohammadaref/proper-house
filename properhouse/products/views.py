from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
# Create your views here.

def home(request):
    return render(request, 'products/home.html')

def about(request):
    return render(request, 'products/about.html')

def products(request):
    return render(request, 'products/products.html')

def locations(request):
    return render(request, 'products/locations.html')

def contact(request):
    return render(request, 'products/contact.html')
