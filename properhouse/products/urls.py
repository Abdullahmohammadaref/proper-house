from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("products/", views.products, name="products"),
    path("products/<str:category_name>/", views.category, name="category"),
    path("products/<str:category_name>/<str:subcategory_name>/", views.subcategory, name="subcategory"),
    path("products/<str:category_name>/<str:subcategory_name>/<str:product_id>/", views.product, name="product"),
    path("locations/", views.locations, name="locations"),
    path("contact/", views.contact, name="contact"),
]
