from django.urls import path

from .views import (
    MothersDayProductListCreateAPIView,
    MothersDayProductRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('products/', MothersDayProductListCreateAPIView.as_view(), name='mothers-day-product-list-create'),
    path('products/<int:pk>/', MothersDayProductRetrieveUpdateDestroyAPIView.as_view(), name='mothers-day-product-detail'),
    path('products/<int:pk>/edit/', MothersDayProductRetrieveUpdateDestroyAPIView.as_view(), name='mothers-day-product-edit'),
    path('products/<int:pk>/delete/', MothersDayProductRetrieveUpdateDestroyAPIView.as_view(), name='mothers-day-product-delete'),
]
