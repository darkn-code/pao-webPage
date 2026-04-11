from django.urls import path
from .views import get_products_grouped

urlpatterns = [
    path('products-grouped/', get_products_grouped),
]