from django.urls import path
from .views import get_products_grouped
from .views import sync_products, get_products_db

urlpatterns = [
    path('products-grouped/', get_products_grouped),
    path('sync/', sync_products),
    path('products/', get_products_db),
]