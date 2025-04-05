from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("products", views.products, name="products"),
    path("locations", views.locations, name="locations"),
    path("contact", views.contact, name="contact"),

]