from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MothersDayProductViewSet

router = DefaultRouter()
router.register('products', MothersDayProductViewSet, basename='mothers-day-products')

urlpatterns = [
    path('', include(router.urls)),
]
